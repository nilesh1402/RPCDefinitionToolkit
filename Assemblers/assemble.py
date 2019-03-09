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
Integrated Definitions: 5,630
	From 442 - 103 (1.83%) (Last: 2018-03-01)
	From 640 - 5,520 (98.05%) (Last: 2018-06-19)
	From 999 - 7 (0.12%) (Last: -)
Active: 4,551 (80.83%)
442:
	Active in Local: 4,458
		Active in Local but not in I 151
		... if > 0 then not the base VistA and base overrides
640:
	Active in Local: 4,487
		Active in Local but not in I 0
		... if > 0 then not the base VistA and base overrides
999:
	Active in Local: 2,803
		Active in Local but not in I 279
		... if > 0 then not the base VistA and base overrides
"""

SNOS = ["442", "640", "999"] # SHOULD PUT DATE ON THESE in config

def assemble(): # makes core and the per VistA qualifications
    assembleIntegrated()
    makePerVistAQualifiers()

"""
Basic Assembly:
- order VistAs by "freshness" (FOIA always at end)
- pick first occurrence of an RPC defn and note source VistA id
... REM: no matter what, per VistA 'isActive' applies in the per VistA defns
        
TODO: More Advanced (reflect custom comparison reports):
- w/earliest BUILD (may only do if all active?) by distrib or that
first of other VistAs comes later ("MAG 3.0 ex which is first for some VistAs)
- if one has all removed options even if not freshest (ex/ HMP removed)
"""
def assembleIntegrated():
        
    rpcInterfaceDefinitionBySNO = {}
    lastInstallBySNO = {}
    for sno in SNOS:
        rpcInterfaceDefinitionBySNO[sno] = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_rpcInterfaceDefinition.json"))
        if sno == "999":
            lastInstallBySNO[sno] = "1900-01-01"
        else:
            installs = set(defn["installed"].split("T")[0] for defn in rpcInterfaceDefinitionBySNO[sno] if "installed" in defn and defn["label"] != "CG FMQL QP")
            lastInstallBySNO[sno] = sorted(list(installs))[-1]
                
    rpcDefinitionsById = {}
    for sno in sorted(SNOS, key=lambda x: lastInstallBySNO[x], reverse=True):
        for rpcDefinition in rpcInterfaceDefinitionBySNO[sno]:
            rpc = rpcDefinition["label"]
            if rpc in rpcDefinitionsById:
                continue
            rpcDefinition["fromStation"] = sno
            rpcDefinitionsById[rpc] = rpcDefinition
           
    integratedRPCInterfaceDefinition = sorted([rpcDefinitionsById[rpc] for rpc in rpcDefinitionsById], key=lambda x: x["label"]) 
    
    print "Integrated Definitions: {:,}".format(len(integratedRPCInterfaceDefinition))
    for sno in sorted(SNOS):
        print "\tFrom {} - {} (Last: {})".format(
            sno, 
            reportAbsAndPercent(sum(1 for defn in integratedRPCInterfaceDefinition if defn["fromStation"] == sno), len(integratedRPCInterfaceDefinition)),
            lastInstallBySNO[sno] if sno != "999" else "-"
        )
    iActives = set(defn["label"] for defn in integratedRPCInterfaceDefinition if "isActive" in defn)
    print "Active: {}".format(reportAbsAndPercent(len(iActives), len(integratedRPCInterfaceDefinition)))
    for sno in sorted(SNOS):
        print "{}:".format(sno)
        sActives = set(defn["label"] for defn in rpcInterfaceDefinitionBySNO[sno] if "isActive" in defn)
        print "\tActive in Local: {:,}".format(len(sActives))
        print "\t\tActive in Local but not in I {:,}".format(len(sActives - iActives))
        print "\t\t... if > 0 then not the base VistA and base overrides"
    print
    
    json.dump(integratedRPCInterfaceDefinition, open("../Definitions/rpcInterfaceDefinition.bjsn", "w"), indent=4)
    
"""
By SNO - what is active and last install
"""
def makePerVistAQualifiers():
    print "Flushing 'active qualifiers' per station number:"
    for sno in SNOS:
        rpcInterfaceDefinition = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_rpcInterfaceDefinition.json"))
        quals = []
        for defn in rpcInterfaceDefinition:
            if "isActive" not in defn:
                continue
            qual = {"label": defn["label"], "installed": defn["installed"]}
            quals.append(qual)
        print "\tFlushing {} active 'qualifiers' for {}".format(len(quals), sno)
        json.dump(quals, open("../Definitions/rpcInterfaceDefinition{}.bjsn".format(sno), "w"), indent=4)
        
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    assemble()

if __name__ == "__main__":
    main()
