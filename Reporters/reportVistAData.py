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

TODO first:
- date installed in report too (or just show time gap to most recent install)
  ... show range of gaps?
- highlight those NOT in 8994 but should: 3 ...
  - set([u'MAGQB PURNUL', u'ORQQPXRM MHDLLDMS', u'ROR LIST ICD-9'])
    ... note that 8994 has RPC ROR LIST ICD
    ... misbuilt build more than likely ... ie/ part of "Build loose ends"
- highlight the deleted (and shouldn't be in 8994) ... separate them
- highlight those in 8994 and no build ... ie/ to make build clear
<----- after this nail down package etc.
- ... first distrib of an RPC ie/ per year ie/ take out subsequent distribs
  <---- tighten when there
  ... then first_install (post last de-install) per year

TODO: 
- may combine with package: reportBuildInstallPackages ie/ of RPCs
  ... will take similar approach from reduction to assembly
- tie to pkgs not types ie/ conical app 
- report more per year: NEW RPCs per year vs builds with RPCs (can be redundant)
- report more on deletes
- report more on 8994 alignment
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
                if rpc not in buildsByRPC:
                    buildsByRPC[rpc] = []
                info = {"build": buildInfo["label"], "typeName": typeName, "version": version, "action": actionType}
                if "dateDistributed" in buildInfo:
                    info["distributed"] = buildInfo["dateDistributed"]
                    if not re.search(r'FMQL', typeName):
                        dateDistributeds.append(buildInfo["dateDistributed"])
                        countBuildsByYr[buildInfo["dateDistributed"].split("-")[0]] += 1
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
    activeRPCs = set(buildsByRPC) - deletedRPCs
    in8994RPCsNotActive = set(_8994Labels) - activeRPCs
          
    mu = """## RPC Builds of {}
    
There are {:,} builds defining {:,} RPCs starting in {} and going to {}. There are {:,} types, the most popular of which is __{}__ with {:,} RPCs. The RPC __{}__ appears in the most builds, {:,}. Note that Builds can delete as well as add RPCs - {:,} of the RPCs were deleted by the final Build they appeared in, leaving {:,} RPCs active and installed. 
    
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
            
    tbl = MarkdownTable(["Year", "Builds"])
    total = sum(countBuildsByYr[yr] for yr in countBuildsByYr)
    for yr in sorted(countBuildsByYr, key=lambda x: int(x), reverse=True):
        tbl.addRow([yr, reportAbsAndPercent(countBuildsByYr[yr], total)])
    mu += """RPC Builds by year ...
     
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
    in8994Count = 0
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
        
        typeNames = list(set(bi["typeName"] for bi in buildsByRPC[rpc]))
        if len(typeNames) > 1:
            versionMU = ", ".join("{} ({})".format(bi["typeName"], bi["version"]) for bi in buildsByRPC[rpc])
        else:
            versionMU = ", ".join(bi["version"] for bi in buildsByRPC[rpc])
        typeNameMU = ", ".join(sorted(typeNames)) if len(typeNames) > 1 else typeNames[0]
                                
        tbl.addRow(["__{}__".format(rpc), len(buildsByRPC[rpc]), typeNameMU, distribMU, installGapMU, versionMU])
        
        if rpc in _8994Labels:
            in8994Count += 1
                
    mu += "{:,} Active/Installed RPCs, {:,} in 8994 too, for whom the maximum gap in days between distribution and install is {:,}, the median is {:,}, while {:,} have no gap at all. Note {:,} are in 8994 and not active ...\n\n".format(len(activeRPCs), in8994Count, max(gaps), numpy.percentile(gaps, 50), sum(1 for g in gaps if g == 0), len(in8994RPCsNotActive))
    mu += tbl.md() + "\n\n"
    
    mu += """__Notes:__
    
  * the list here (active and deleted) need to be compared to the 8994 list of the same system (preliminary check shows few 8994 for deleted or non build-defined RPCs and nearly all deleted RPCs don't appear in 8994)
  * greater than 1 type for an RPC (based on builds they appear in) seems to reflect mistakes or a change in a package/build designation name ('TEXT INTEGRATION UTILITIES' became 'TIU')
  * the "type" needs to be aligned with Package (9_4) prefixes to tie RPCs to VistA 'applications'. 
  * NEW RPCs per year vs just new build with RPCs per year
   
"""

    in8994Count = 0
    tbl = MarkdownTable(["RPC", "(Last) Deleting Build", "When (Dist/Install)"])
    for i, rpc in enumerate(sorted(deletedRPCs), 1):
        lastDelBuildInfo = buildsByRPC[rpc][-1]
        whenMU = "{} / {}".format(lastDelBuildInfo["distributed"], lastDelBuildInfo["installed"].split("T")[0])
        tbl.addRow([rpc, lastDelBuildInfo["build"], whenMU])
        if rpc in _8994Labels:
            in8994Count += 1
    mu += "{:,} Deleted/Uninstalled RPCs, {:,} are in 8994 ...\n\n".format(len(deletedRPCs), in8994Count)
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