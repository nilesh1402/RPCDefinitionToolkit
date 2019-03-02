#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

VISTA_RPCD_LOCN_TEMPL = "/data/vista/{}/RPCDefinitions/"

"""
Assembled 5,592 RPCs using Build/Package/Install across 2 VistAs plus FOIA.
Done merging to get 5,592 complete definitions - had to force delete 3 from builds as though NOT deleted, still no 8994 etc
5,439 (97.26%) are active, 153 (2.74%) deleted, 1,024 in 1, 4,568 in 2, 5 only in FOIA
Flushing 5,231 actives of 442
Flushing 3,208 actives of 999
Flushing 5,350 actives of 640
"""

SNOS = ["442", "640", "999"] # SHOULD PUT DATE ON THESE in config

def assembleBase():

    mbpiByRPCs = assembleMBPIs()
    restByRPCs = assembleRest()
    
    defns = []
    forcingDeleteAsSyncIssue = []
    for rpc in mbpiByRPCs:
        defn = mbpiByRPCs[rpc]
        if rpc not in restByRPCs:
            if "isDeleted" not in defn:
                forcingDeleteAsSyncIssue.append(defn["label"])
                defn["isDeleted"] = True
                defn["isDeletedAsNo8994"] = True # to mark off
        else:
            rest = restByRPCs[rpc]
            for prop in rest:
                if prop == "_vistas":
                    continue # let build determine
                defn[prop] = rest[prop]
        defns.append(defn)
    
    print "Done merging to get {:,} complete definitions - had to force delete {:,} from builds as though NOT deleted, still no 8994 etc".format(len(defns), len(forcingDeleteAsSyncIssue))
    
    print "{} are active, {} deleted, {:,} in 1, {:,} in 2, {:,} only in FOIA".format(
        reportAbsAndPercent(sum(1 for defn in defns if "isDeleted" not in defn), len(defns)),
        reportAbsAndPercent(sum(1 for defn in defns if "isDeleted" in defn), len(defns)),
        sum(1 for defn in defns if defn["sourceCount"] == 1),
        sum(1 for defn in defns if defn["sourceCount"] == 2),
        sum(1 for defn in defns if "isSourceFOIA" in defn)
    ) 
    
    defns = sorted(defns, key=lambda x: x["label"])
        
    json.dump(defns, open("../Definitions/rpcInterfaceDefinition.bjsn", "w"), indent=4)

    activesBySNO = assembleActiveRPCsPerStationNumber()
    for sno in activesBySNO:
        print "Flushing {:,} actives of {}".format(len(activesBySNO[sno]), sno)
        # preparing to add overrides beyond 'label'
        json.dump(activesBySNO[sno], open("../Definitions/rpcInterfaceDefinition{}.bjsn".format(sno), "w"), indent=4)   

"""
Using builds across VistAs and NOT 8994 to defined RPCs
"""
def assembleMBPIs():

    # Load all BPIs and assemble RPC interface from that
    bpiByRPCBySNO = defaultdict(dict)
    for stationNo in SNOS:
        bpiBySNo = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json"))
        for bpi in bpiBySNo:
            bpiByRPCBySNO[bpi["label"]][stationNo] = bpi
    
    mbpiByRPC = {}
    
    def defineMBPI(rpc, snosToUse):
        sno = snosToUse[0]
        mbpi = bpiByRPCBySNO[rpc][sno]
        mbpi["build"] = mbpi["builds"][0]["label"]
        del mbpi["builds"]
        del mbpi["installed"]
        if len(snosToUse) > 1:
            mbpi["sourceCount"] = len(snosToUse)
        else:
            mbpi["sourceCount"] = 1
            mbpi["sourceStationNumber"] = sno
        if sno == "999":
            mbpi["isSourceFOIA"] = True # Unusual and not important
        mbpiByRPC[rpc] = mbpi
        
    for rpc in bpiByRPCBySNO:
    
        snos = [sno for sno in bpiByRPCBySNO[rpc].keys() if sno != "999"]
        if len(snos) == 0:
            snos = ["999"]
            
        # Only one non 999 source or 999  
        if len(snos) == 1:
            defineMBPI(rpc, snos) # just take from one
            continue  
            
        distributeds = sorted([bpiByRPCBySNO[rpc][sno]["distributed"] for sno in snos if "distributed" in bpiByRPCBySNO[rpc][sno]])
        deletedSNOs = [sno for sno in snos if "isDeleted" in bpiByRPCBySNO[rpc][sno]]
        
        # Note: DELETED - not allowing UNDELETE. Pick first distrib if available
        if len(deletedSNOs): 
            snosToUse = deletedSNOs
            distributedsDeleted = sorted([bpiByRPCBySNO[rpc][sno]["distributed"] for sno in deletedSNOs if "distributed" in bpiByRPCBySNO[rpc][sno]])
            if len(distributedsDeleted): # use sno with deleted/distrib
                snosToUse = [sno for sno in deletedSNOs if bpiByRPCBySNO[rpc][sno]["distributed"] == distributedsDeleted[0]]
            defineMBPI(rpc, snosToUse)
            continue
        
        # If any distributed - pick first one (Crude as ignoring first build
        # lacking distributed - return to this with build list work later TODO)
        if len(distributeds):
            snosToUse = [sno for sno in snos if "distributed" in bpiByRPCBySNO[rpc][sno] and bpiByRPCBySNO[rpc][sno]["distributed"] == distributeds[0]]
            defineMBPI(rpc, snosToUse)
            continue          
            
        # No distrib/not deleted - take any 
        defineMBPI(rpc, snos) 
        continue  
        
    if len(mbpiByRPC) != len(bpiByRPCBySNO):
        raise Exception("No all RPCs known from VistA's accounted for in merge")       
        
    print "Assembled {:,} RPCs using Build/Package/Install across {:,} VistAs plus FOIA.".format(
        len(mbpiByRPC),
        len(SNOS) - 1
    )
    
    return mbpiByRPC

"""
From 8994 and 19
"""
def assembleRest():
    
    definitionsByRPC = OrderedDict()
    
    for sno in SNOS:
        
        _8994Reductions = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_8994Reduction.json"), object_pairs_hook=OrderedDict)
        for red in _8994Reductions:
            if red["label"] in definitionsByRPC:
                definition = definitionsByRPC[red["label"]]
                definition["_vistas"].append(sno)
                continue
            red["_vistas"] = [sno]
            rpc = red["label"]
            del red["label"]
            definitionsByRPC[rpc] = red
           
        # For now, just unifying options listed
        try:
            _19Reductions = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_19Reduction.json"), object_pairs_hook=OrderedDict)
        except:
            pass
        else:
            optionsOfRPCs = defaultdict(set)
            for _19Red in _19Reductions:
                if "rpcs" not in _19Red:
                    continue
                for rpc in _19Red["rpcs"]:
                    optionsOfRPCs[rpc].add(_19Red["label"])    
            for rpc in optionsOfRPCs:
                if rpc not in definitionsByRPC:
                    continue # may be rogue or bad entry?
                definitionsByRPC[rpc]["options"] = sorted(list(optionsOfRPCs[rpc]))
                
    return definitionsByRPC
    
"""
By SNO - what is active
"""
def assembleActiveRPCsPerStationNumber():
    bySNO = {}
    for stationNo in SNOS:
        activeRPCs = []
        bpiBySNo = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json"))    
        for bpi in bpiBySNo:
            if "isDeleted" not in bpi:
                activeRPCs.append({"label": bpi["label"], "installed": bpi["installed"]})
        bySNO[stationNo] = sorted(activeRPCs, key=lambda x: x["label"])
    return bySNO
        
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    assembleBase()

if __name__ == "__main__":
    main()
