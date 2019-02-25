#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime
import numpy

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

VISTA_RED_LOCN_TEMPL = "/data/vista/{}/RPCDefinitions/"
VISTA_REP_LOCN_TEMPL = "../Reports/PerVistA/{}/"

"""
Reports for Per VistA Reductions, the initial sources of an integrated
RPC Interface Definition.

TODO: 
- may combine with package: reportBuildInstallPackages ie/ of RPCs
  ... will take similar approach from reduction to assembly
- tie to pkgs not types ie/ conical app 
"""
def reportBuildsNInstalls(stationNo):

    buildsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
    
    # For report
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = [red["label"] for red in _8994Reduction]
        
    buildsByRPC = {}
    countBuildsWithRPCs = 0
    rpcsByTypeName = defaultdict(set)
    dateDistributeds = []
    dateInstalleds = []
    countBuildsByYr = Counter()
    countNewRPCBuildsByYr = Counter()
    for buildInfo in buildsReduction:
        if "rpcs" not in buildInfo:
            continue
        countBuildsWithRPCs += 1
        versionMatch = re.search(r'(\d.+)$', buildInfo["label"])
        if versionMatch:
            version = versionMatch.group(1)
            typeName = re.sub(r' +$', '', re.match(r'([^\*^\d]+)', buildInfo["label"]).group(1)) # trailing out
        else:
            raise Exception("Expect to find version in Build Name: {}".format(buildInfo["label"]))
        for actionType in buildInfo["rpcs"]:
            for rpc in buildInfo["rpcs"][actionType]:
                info = {"build": buildInfo["label"], "typeName": typeName, "version": version, "action": actionType}
                if "dateDistributed" in buildInfo:
                    info["distributed"] = buildInfo["dateDistributed"]
                    if not re.search(r'FMQL', typeName):
                        dateDistributeds.append(buildInfo["dateDistributed"])
                        countBuildsByYr[buildInfo["dateDistributed"].split("-")[0]] += 1
                        if rpc not in buildsByRPC: # ie/ new
                            countNewRPCBuildsByYr[
                            buildInfo["dateDistributed"].split("-")[0]] += 1
                if rpc not in buildsByRPC:
                    buildsByRPC[rpc] = []
                if "dateInstalledFirst" in buildInfo:
                    info["installed"] = buildInfo["dateInstalledFirst"]
                    if not re.search(r'FMQL', typeName):
                        dateInstalleds.append(buildInfo["dateInstalledFirst"])
                if "package" in buildInfo:
                    info["package"] = buildInfo["package"]
                buildsByRPC[rpc].append(info)
                rpcsByTypeName[typeName].add(rpc)
    dateDistributeds = sorted(dateDistributeds)
    rpcWithMost = sorted(buildsByRPC, key=lambda x: len(buildsByRPC[x]), reverse=True)[0]
    typeNameWithMost = sorted(rpcsByTypeName, key=lambda x: len(rpcsByTypeName[x]), reverse=True)[0]
    deletedRPCs = set(rpc for rpc in buildsByRPC if buildsByRPC[rpc][-1]["action"] == "DELETE AT SITE")
    deletedRPCsIn8994 = [rpc for rpc in deletedRPCs if rpc in _8994Labels]
    activeRPCs = set(buildsByRPC) - deletedRPCs
    greaterThanOneTypeActiveRPCs = [rpc for rpc in activeRPCs if len(set(bi["typeName"] for bi in buildsByRPC[rpc])) > 1]
    extraRPCs = set(_8994Labels) - activeRPCs # beyond active/still there
    missingRPCs = activeRPCs - set(_8994Labels) # should be there but not
          
    mu = """## RPC Builds of {}
    
There are {:,} builds defining {:,} RPCs starting in {} and going to {}. There are {:,} types, the most popular of which is __{}__ with {:,} RPCs. The RPC __{}__ appears in the most builds, {:,}. Builds can delete as well as add RPCs - {:,} of the RPCs were deleted by the final Build they appeared in, leaving {:,} RPCs active and installed ...
    
""".format(
        stationNo, 
        countBuildsWithRPCs, 
        len(buildsByRPC),
        dateDistributeds[0], 
        dateDistributeds[-1],
        len(rpcsByTypeName), 
        typeNameWithMost, 
        len(rpcsByTypeName[typeNameWithMost]),
        rpcWithMost, 
        len(buildsByRPC[rpcWithMost]),
        len(deletedRPCs),
        len(activeRPCs)
    )
    
    """        
    Builds by Year - may be restated subsequently so distinguish builds introducing
    fresh RPCs from those just restating. Note that the total of "new RPCs" is roughly
    the total of RPCs (some builds lack a date which accounts for the discrepency)
    """
    tbl = MarkdownTable(["Year", "All RPC Builds", "New RPC Builds"])
    total = sum(countBuildsByYr[yr] for yr in countBuildsByYr)
    for yr in sorted(countBuildsByYr, key=lambda x: int(x), reverse=True):
        tbl.addRow([yr, reportAbsAndPercent(countBuildsByYr[yr], total), reportAbsAndPercent(countNewRPCBuildsByYr[yr], total)])
    mu += """RPC Builds by year. Note that as builds often restate pre-existing RPCs, the following distinguishes all builds with RPCs from those that introduce new RPCs ...
     
"""
    mu += tbl.md() + "\n\n"
                   
    # distributed | installed 
    def muDate(buildInfos, dtProp):
        def calcDate(buildInfos, dtProp, first=False):
            dt = ""
            for buildInfo in buildInfos:
                if dtProp in buildInfo:
                    dt = buildInfo[dtProp] 
                    if re.search(r'T', dt): # only day
                        dt = dt.split("T")[0]
                    if first:
                        break
            return dt
        last = calcDate(buildsByRPC[rpc], dtProp, False)
        first = calcDate(buildsByRPC[rpc], dtProp, True)
        return first, last    
                    
    tbl = MarkdownTable(["RPC", "Builds", "Type(s)", "Distributed", "[First] Install Gap", "Version(s)"])
    lastTypeNameMU = ""
    gaps = []
    noGapRPCs = []
    for i, rpc in enumerate(sorted(activeRPCs, key=lambda x: x), 1):
            
        firstD, lastD = muDate(buildsByRPC[rpc], "distributed")
        distribMU = lastD
        if firstD != lastD:
            distribMU = "{} - {}".format(firstD, distribMU)    

        firstI, lastI = muDate(buildsByRPC[rpc], "installed")  
        if firstI == "" or firstD == "":
            installGapMU = "__N/A__"
        elif firstI > firstD:
            installGapMU = str(datetime.strptime(firstI, "%Y-%m-%d") - datetime.strptime(firstD, "%Y-%m-%d")).split(",")[0]
            gaps.append(int(re.match(r'(\d+)', installGapMU).group(1)))
        elif firstI == firstD:
            installGapMU = ""
            gaps.append(0)
        else:
            installGapMU = "__BAD: D > I__: {} > {}".format(firstD, firstI)
            noGapRPCs.append(rpc)
        
        typeNames = list(set(bi["typeName"] for bi in buildsByRPC[rpc]))
        if len(typeNames) > 1:
            versionMU = ", ".join("{} ({})".format(bi["typeName"], bi["version"]) for bi in buildsByRPC[rpc])
        else:
            versionMU = ", ".join(bi["version"] for bi in buildsByRPC[rpc])
        typeNameMU = ", ".join(sorted(typeNames)) if len(typeNames) > 1 else typeNames[0]
                                
        tbl.addRow(["__{}__".format(rpc), len(buildsByRPC[rpc]), typeNameMU, distribMU, installGapMU, versionMU])
                
    mu += "{:,} Active/Installed RPCs. The maximum gap in days between distribution and install is {:,}, the median is {:,}, {:,} have no gap at all and the gap for {:,} isn't available because necessary dates are missing. Note that greater than 1 type for {:,} RPCs probably reflects a change in the type's name over the years ...\n\n".format(len(activeRPCs), max(gaps), numpy.percentile(gaps, 50), sum(1 for g in gaps if g == 0), len(noGapRPCs), len(greaterThanOneTypeActiveRPCs))
    mu += tbl.md() + "\n\n"

    """
    Deleted RPCs - note that there are probably more? or should be more (retired 
    packages). Note that only 'SHOULD BE DELETED' RPCs (see below) need concern
    the integrated RPC Interface definition.
    
    TODO: work out retirement better to enforce more retireds
    """
    tbl = MarkdownTable(["RPC", "(Last) Deleting Build", "When (Dist/Install)"])
    for i, rpc in enumerate(sorted(deletedRPCs), 1):
        lastDelBuildInfo = buildsByRPC[rpc][-1]
        whenMU = "{} / {}".format(lastDelBuildInfo["distributed"], lastDelBuildInfo["installed"].split("T")[0])
        tbl.addRow([rpc, lastDelBuildInfo["build"], whenMU])
    mu += "{:,} Deleted/Uninstalled RPCs ...\n\n".format(len(deletedRPCs))
    mu += tbl.md() + "\n\n"
        
    """
    8994 tie: Rogue RPCs 
    
    those [1] builds says SHOULD be there but aren't ("MISSING") and [2] builds don't 
    account for them or should be deleted ("EXTRA") and [3] builds delete but are 
    still in 8994 ("SHOULD BE DELETED")
    
    Note: possible build logic wrong OR builds badly built (remote of RPC not done but
    code removed?) etc
    """
    rogueRPCs = (missingRPCs.union(extraRPCs)).union(deletedRPCsIn8994)
    tbl = MarkdownTable(["RPC", "Problem"])
    for rpc in sorted(list(rogueRPCs)):
        problem = "EXTRA"
        if rpc in missingRPCs:
            problem = "MISSING"
        elif rpc in deletedRPCsIn8994:
            problem = "SHOULD BE DELETED"
        problem = "MISSING" if rpc in missingRPCs else "EXTRA"
        tbl.addRow([rpc, problem])
    mu += "__Rogue RPCs__ are [1] in 8994 but are not active according to Builds (\"EXTRA\" {:,}) or active by builds but not in 8994 (\"MISSING\" {:,}) or deleted by builds but in 8994 (\"SHOULD BE DELETED\" {:,}). These {:,} \"Rogue RPCs\" should be isolated and tested. For instance, do _EXTRAs_ even have code implementing them or is 8994 wrong? ...\n\n".format(len(extraRPCs), len(missingRPCs), len(deletedRPCsIn8994), len(rogueRPCs))
    mu += tbl.md() + "\n\n"
    
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcBuilds.md", "w").write(mu)
    
"""
Packages

COMPARE: 
https://github.com/OSEHRA/VistA/blob/master/Packages.csv
... add to sources

Also tie to TRM for any packages. List is https://www.oit.va.gov/Services/TRM/ReportVACategoryMapping.aspx
"""

    
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    reportBuildsNInstalls(stationNo)

if __name__ == "__main__":
    main()