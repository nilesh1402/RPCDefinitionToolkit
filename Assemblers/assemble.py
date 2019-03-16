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
__3/8/2019__:

Integrated Definitions: __5,630__

  * 442: 103 (1.83%) / Last: 2018-03-01 / 5,376 (95.49%)
  * 640: 5,520 (98.05%) / Last: 2018-06-19 / 5,520 (98.05%)
  * FOIA (999): 7 (0.12%) / Last: 2018-02-22 / 3,750 (66.61%)

Active: __4,551 (80.83%)__

  * 442: 4,458 - not I 151
  * 640: 4,487 - not I 0
  * FOIA (999): 2,803 - not I 279
"""

SNOS = ["442", "640", "999"] # SHOULD PUT DATE ON THESE in config

def assemble(): # makes core and the per VistA qualifications
    assembleIntegrated()
    makePerVistAQualifiers()
    assembleApplications()

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
        installs = set(defn["installed"].split("T")[0] for defn in rpcInterfaceDefinitionBySNO[sno] if "installed" in defn and defn["label"] != "CG FMQL QP")
        lastInstallBySNO[sno] = sorted(list(installs))[-1]
                
    rpcDefinitionsById = {}
    for sno in sorted(SNOS, key=lambda x: lastInstallBySNO[x] if x != "999" else "1900-01-01", reverse=True):
        for rpcDefinition in rpcInterfaceDefinitionBySNO[sno]:
            rpc = rpcDefinition["label"]
            if rpc in rpcDefinitionsById:
                rpcDefinitionsById[rpc]["inVistAs"].append(sno)
                continue
            rpcDefinition["fromVistA"] = sno
            rpcDefinition["inVistAs"] = [sno]
            rpcDefinitionsById[rpc] = rpcDefinition
           
    integratedRPCInterfaceDefinition = sorted([rpcDefinitionsById[rpc] for rpc in rpcDefinitionsById], key=lambda x: x["label"]) 
    
    print "Integrated Definitions: __{:,}__\n".format(len(integratedRPCInterfaceDefinition))
    for sno in sorted(SNOS):
        print "  * {}: {} / Last: {} / {}".format(
            sno if sno != "999" else "FOIA (999)",
            reportAbsAndPercent(sum(1 for defn in integratedRPCInterfaceDefinition if defn["fromVistA"] == sno), len(integratedRPCInterfaceDefinition)),
            lastInstallBySNO[sno],
            reportAbsAndPercent(len(rpcInterfaceDefinitionBySNO[sno]), len(integratedRPCInterfaceDefinition)),            
        )
    # Could add appearances ie/ in 1, 2 or 3
    iActives = set(defn["label"] for defn in integratedRPCInterfaceDefinition if "isActive" in defn)
    print "\nActive: __{}__\n".format(
        reportAbsAndPercent(len(iActives), len(integratedRPCInterfaceDefinition))
    )
    for sno in sorted(SNOS):
        sActives = set(defn["label"] for defn in rpcInterfaceDefinitionBySNO[sno] if "isActive" in defn)
        print "  * {}: {:,} - not I {:,}".format(
            sno if sno != "999" else "FOIA (999)",
            len(sActives),
            len(sActives - iActives) # 0 if base!
        )
    print
    
    json.dump(integratedRPCInterfaceDefinition, open("../Definitions/rpcInterfaceDefinition.bjsn", "w"), indent=4)
    
"""
Manual and 8994_5 Used

REM: (remote) application use information from VistA is a small subset. Need
to expand with manual definitions. [1] most apps don't identify themselves and 
[2] option to app link is rough and needs searching and (manual) work
"""
def assembleApplications():

    # Start off with information from used remote app of VistAs"
    appsById = {}
    for sno in SNOS:
        if sno == "999":
            continue # no good as no user data
        rappsWithUse = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_rpcRemoteApplicationsWithUse.json"))
        for rappInfo in rappsWithUse:
            if "users" not in rappInfo:
                continue
            rappUse = sum(rappInfo["users"][userId] for userId in rappInfo["users"])
            if rappInfo["label"] in appsById:
                appInfo = appsById[rappInfo["label"]]
                appInfo["inVistAs"][sno] = rappUse
                continue
            appInfo = {"label": rappInfo["label"], "options": [rappInfo["option"]], "inVistAs": {sno: rappUse}, "isRemoteApplication": True}
            appsById[appInfo["label"]] = appInfo
    
    appInfos = appsById.values()
    mAppInfos = json.load(open("../SourceArtifacts/manualRPCApplications.json"))
    for mAppInfo in mAppInfos:
        if mAppInfo["label"] in appsById:
            appInfo = appsById[mAppInfo["label"]]
            if "note" in mAppInfo:
                appInfo["note"] = mAppInfo["note"]
            if "inMonograph" in mAppInfo:
                appInfo["inMonograph"] = True
            continue
        appInfos.append(mAppInfo)
    appInfos = sorted(appInfos, key=lambda x: x["label"])
    
    print "Assembled {:,} RPC App Definitions from {:,} in-use remote apps and {:,} manual definitions".format(len(appInfos), len(appsById), len(mAppInfos))
    json.dump(appInfos, open("../Definitions/rpcInterfaceApplications.bjsn", "w"), indent=4)
    
"""
By SNO - what is active and last install
"""
def makePerVistAQualifiers():
    print "Flushing 'active qualifiers' per station number:\n"
    for sno in SNOS:
        rpcInterfaceDefinition = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_rpcInterfaceDefinition.json"))
        quals = []
        for defn in rpcInterfaceDefinition:
            if "isActive" not in defn:
                continue
            qual = {"label": defn["label"], "installed": defn["installed"]}
            quals.append(qual)
        print "  * Flushing {} active 'qualifiers' for {}".format(len(quals), sno)
        json.dump(quals, open("../Definitions/rpcInterfaceDefinition{}.bjsn".format(sno), "w"), indent=4)
        
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    assembleApplications()
    return
    assemble()

if __name__ == "__main__":
    main()
