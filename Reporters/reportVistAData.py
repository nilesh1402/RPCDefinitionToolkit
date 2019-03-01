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
RPC i/f according to builds and installs - still installed? (active) or 
never installed? or deleted? ie/ what if there was no 8994? And correct it too

Note: must migrate some heuristics from here and into RED step.
1. __ORDER ENTRY/RESULTS REPORTING__ too well liked. Removed as package if
another available ... play with that ie/ PRIMARY PACKAGE ASSERTION in REDUCTION
2. MAY do buildsByRPC as a reduction ie/ a second level reduction BEFORE doing
this report OR doing assembly
"""
def reportBuildsNInstalls(stationNo):

    buildsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
    buildsRPCReduction = [bi for bi in buildsReduction if "rpcs" in bi]
    
    # For report - will OVERRIDE based on ACTIVE from Builds or Not (soon options too)
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = set(red["label"] for red in _8994Reduction)

    buildsWNewRPCReduction = [] 
    buildsByRPC = defaultdict(list)
    buildsByPackage = defaultdict(list)
    packagesByRPC = defaultdict(lambda: Counter()) # want latest to come out
    dateDistributeds = []
    countBuildsByYr = Counter()
    countNewRPCBuildsByYr = Counter()

    # Builds per RPC form an "audit" trail of RPC introduction, change and deletion
    rpcsSeen = set()
    for buildInfo in buildsRPCReduction:
        newRPCSeen = False
        if "package" in buildInfo:
            buildsByPackage[buildInfo["package"]].append(buildInfo)
        if "dateInstalledFirst" in buildInfo:
            installed = buildInfo["dateInstalledFirst"]
        for actionType in buildInfo["rpcs"]:
            for rpc in buildInfo["rpcs"][actionType]:
                info = {"build": buildInfo["label"], "action": actionType}
                if "package" in buildInfo:
                    packagesByRPC[rpc][buildInfo["package"]] += 1
                    if "packages" not in info:
                        info["packages"] = []
                    if buildInfo["package"] not in info["packages"]:
                        info["packages"].append(buildInfo["package"])
                if "dateDistributed" in buildInfo:
                    info["distributed"] = buildInfo["dateDistributed"]
                    if rpc not in rpcsSeen: 
                        newRPCSeen = True
                        rpcsSeen.add(rpc) 
                if "dateInstalledFirst" in buildInfo:
                    info["installed"] = installed
                buildsByRPC[rpc].append(info)
        if newRPCSeen:
            buildsWNewRPCReduction.append(buildInfo)
        if "dateDistributed" in buildInfo:
            distributed = buildInfo["dateDistributed"]
            if not re.search(r'FMQL', buildInfo["label"]):
                dateDistributeds.append(distributed)
                countBuildsByYr[distributed.split("-")[0]] += 1
                if newRPCSeen:
                    countNewRPCBuildsByYr[distributed.split("-")[0]] += 1
                    
    # PICK ANYTHING BUT 'ORDER ENTRY/RESULTS REPORTING' if another there
    rpcsByPackage = defaultdict(list)
    for rpc in packagesByRPC:
        if len(packagesByRPC[rpc]) > 1 and "ORDER ENTRY/RESULTS REPORTING" in packagesByRPC[rpc]:
            del packagesByRPC[rpc]["ORDER ENTRY/RESULTS REPORTING"]
        for pkg in packagesByRPC[rpc]:
            rpcsByPackage[pkg].append(rpc)

    dateDistributeds = sorted(dateDistributeds)
    rpcWithMostBuilds = sorted(buildsByRPC, key=lambda x: len(buildsByRPC[x]), reverse=True)[0]
    packageWithTheMostRPCs = sorted(rpcsByPackage, key=lambda x: len(rpcsByPackage[x]), reverse=True)[0]

    deletedRPCs = set(rpc for rpc in buildsByRPC if buildsByRPC[rpc][-1]["action"] == "DELETE AT SITE") # this will include those never even installed!
    activeRPCs = set(buildsByRPC) - deletedRPCs

    _8994MissingActiveRPCs = activeRPCs - _8994Labels # should be there but not   
    _8994DeletedRPCs = _8994Labels.intersection(deletedRPCs)
    _8994NoBuildRPCs = _8994Labels - activeRPCs # beyond active/still there
          
    mu = """## RPCs According to Builds and Installs of {}
    
There are {} builds defining {:,} RPCs distributed from {} to {}, {} of which introduce new RPCs. RPC __{}__ appears in the most builds, {:,}. The median number of RPCs per Build is {:,}. 

RPCs are spread across {:,} packages. Package _{}_ has the most RPCs, {:,}. {:,} RPCs have more than one Package usually because of re-organization and splitting of Packages over the years. {:,} RPCs have no package because their builds weren't assigned a package (yet).

Builds can delete as well as add RPCs - {:,} of the RPCs were deleted by the final Build they appeared in, leaving {:,} RPCs active and installed.

File _8994_ is suppossed to define the active RPCs in a VistA. However the 8994 of this system has {:,} deleted RPCs, is missing {:,} active RPCs and has {:,} extra RPCs that never appear in a Build.
    
""".format(

        stationNo, 
        
        reportAbsAndPercent(len(buildsRPCReduction), len(buildsReduction)), 
        len(buildsByRPC),
        dateDistributeds[0], 
        dateDistributeds[-1],
        reportAbsAndPercent(len(buildsWNewRPCReduction), len(buildsRPCReduction)),
        rpcWithMostBuilds, 
        len(buildsByRPC[rpcWithMostBuilds]),
        numpy.percentile([len(buildsByRPC[rpc]) for rpc in buildsByRPC], 50),
        
        len(buildsByPackage), 
        packageWithTheMostRPCs,
        len(rpcsByPackage[packageWithTheMostRPCs]),
        sum(1 for rpc in packagesByRPC if len(packagesByRPC[rpc]) > 1),
        sum(1 for rpc in buildsByRPC if rpc not in packagesByRPC),
        
        len(deletedRPCs),
        len(activeRPCs),
        
        len(_8994DeletedRPCs),
        len(_8994MissingActiveRPCs),
        len(_8994NoBuildRPCs)
    
    )
        
    """        
    Builds by Year - may be restated subsequently so distinguish builds introducing
    fresh RPCs from those just restating. Note that the total of "new RPCs" is roughly
    the total of RPCs (some builds lack a date which accounts for the discrepency)
    """
    tbl = MarkdownTable(["Year", "All RPC Builds", "New RPC Builds"])
    for yr in sorted(countBuildsByYr, key=lambda x: int(x), reverse=True):
        tbl.addRow([yr, reportAbsAndPercent(countBuildsByYr[yr], len(buildsRPCReduction)), reportAbsAndPercent(countNewRPCBuildsByYr[yr], len(buildsWNewRPCReduction))])
    mu += """RPC Builds by distribution year. Note that as builds often restate pre-existing RPCs, the following distinguishes all builds with RPCs from those that introduce new RPCs ...
     
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
                    
    tbl = MarkdownTable(["RPC", "Builds", "(Latest) Package", "Distributed", "[First] Install Gap"])
    lastBuildMNMU = ""
    gaps = []
    noGapRPCs = []
    badGapRPCs = []
    for i, rpc in enumerate(sorted(activeRPCs, key=lambda x: x), 1):
            
        firstD, lastD = muDate(buildsByRPC[rpc], "distributed")
        distribMU = lastD
        if firstD != lastD:
            distribMU = "{} - {}".format(firstD, distribMU)    

        firstI, lastI = muDate(buildsByRPC[rpc], "installed")  
        if firstI == "" or firstD == "":
            installGapMU = "__N/A__"
            noGapRPCs.append(rpc)
        elif firstI > firstD:
            installGapMU = str(datetime.strptime(firstI, "%Y-%m-%d") - datetime.strptime(firstD, "%Y-%m-%d")).split(",")[0]
            gaps.append(int(re.match(r'(\d+)', installGapMU).group(1)))
        elif firstI == firstD:
            installGapMU = ""
            gaps.append(0)
        else:
            installGapMU = "__RERELEASE: D > I__: {} > {}".format(firstD, firstI)
            badGapRPCs.append(rpc)
            
        # Alt: move out of 'ORDER ENTRY/RESULTS REPORTING' if another as more precise too
        packageMU = sorted(packagesByRPC[rpc], key=lambda x: packagesByRPC[rpc][x], reverse=True)[0] if rpc in packagesByRPC else ""
                                        
        tbl.addRow(["__{}__".format(rpc), len(buildsByRPC[rpc]), packageMU, distribMU, installGapMU])
                
    mu += "__{:,}__ Active/Installed RPCs. The maximum gap in days between distribution and install is {:,}, the median is {:,}, {:,} have no gap at all. The gap isn't available if necessary dates are missing ({:,}) or the first install date comes BEFORE the build distribution date (__{:,}__) ...\n\n".format(len(activeRPCs), max(gaps), numpy.percentile(gaps, 50), sum(1 for g in gaps if g == 0), len(noGapRPCs), len(badGapRPCs))
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
        # a/cs for when no install info
        whenMU = "{} / {}".format(lastDelBuildInfo["distributed"], lastDelBuildInfo["installed"].split("T")[0] if "installed" in lastDelBuildInfo else "-")
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
    rogueRPCs = (_8994MissingActiveRPCs.union(_8994NoBuildRPCs)).union(_8994DeletedRPCs)
    tbl = MarkdownTable(["RPC", "Problem"])
    for rpc in sorted(list(rogueRPCs)):
        problem = "EXTRA"
        if rpc in _8994MissingActiveRPCs:
            problem = "MISSING"
        elif rpc in _8994DeletedRPCs:
            problem = "SHOULD BE DELETED"
        problem = "MISSING" if rpc in _8994MissingActiveRPCs else "EXTRA"
        tbl.addRow([rpc, problem])
    mu += "__8994 Rogue RPCs__ are [1] in 8994 but are not active according to Builds (\"EXTRA\" {:,}) or active by builds but not in 8994 (\"MISSING\" {:,}) or deleted by builds but in 8994 (\"SHOULD BE DELETED\" {:,}) ...\n\n".format(len(_8994NoBuildRPCs), len(_8994MissingActiveRPCs), len(_8994DeletedRPCs), len(rogueRPCs))
    mu += tbl.md() + "\n\n"
    
    if stationNo == "999":
        mu += "__Note__: FOIA (999) has MANY _Rogues_. It seems that redaction is partial for non Open Source RPCs. It seems that the code is removed but the RPC remains.\n\n"
        
    # ADD TABLE PER PACKAGE and then end
    tbl = MarkdownTable(["Package", "\# RPCs", "Example RPC"])
    for pkg in sorted(rpcsByPackage, key=lambda x: len(rpcsByPackage[x]), reverse=True):
        tbl.addRow(["__{}__".format(pkg), len(rpcsByPackage[pkg]), sorted(list(rpcsByPackage[pkg]))[0]])
    mu += "{:,} Packages have RPCs ...\n\n".format(len(rpcsByPackage))
    mu += tbl.md() + "\n\n"
    
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcsByBuildsNInstalls.md", "w").write(mu)
        
"""
Want to gather builds by packages and focus in particular on packages
with RPC builds
"""
def reportPackagesNBuilds(stationNo):

    _9_6Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
    
    buildsByPackage = defaultdict(list)
    noPackageBuilds = []
    allDatesDistributeds = set()
    for buildInfo in _9_6Reduction:
        if "dateDistributed" in buildInfo and not re.search(r'FMQL', buildInfo["label"]):
            allDatesDistributeds.add(buildInfo["dateDistributed"])
        if "package" in buildInfo:
            buildsByPackage[buildInfo["package"]].append(buildInfo)
            continue
        noPackageBuilds.append(buildInfo)
    packagesWith2013OnBuilds = [pkg for pkg in buildsByPackage if sum(1 for bi in buildsByPackage[pkg] if "dateDistributed" in bi and int(bi["dateDistributed"].split("-")[0]) >= 2013)]
    allDatesDistributeds = sorted(list(allDatesDistributeds))
    firstDateDistributed = allDatesDistributeds[0]
    lastDateDistributed = allDatesDistributeds[-1]
    countBuildsPerPackage = dict((pkg, len(buildsByPackage[pkg])) for pkg in buildsByPackage)
    medianBuildsPerPackage = numpy.percentile(countBuildsPerPackage.values(), 50)
    maxBuildsPerPackage = max(countBuildsPerPackage.values())
    pkgsOrdered = [pkg for pkg in sorted(countBuildsPerPackage, key=lambda x: countBuildsPerPackage[x], reverse=True)]
    pkgWithMostBuilds = pkgsOrdered[0]
    
    mu = """## Packages and Builds
    
There are {:,} builds, distributed between {} and {}. {:,} packages cover {} of the builds, median number of builds per package is {:,}, maximum is {:,} in __{}__. Only {} packages have builds distributed from 2013 on (_should the balance be retired?_). {} builds have no package and only {} builds have RPCs.
    
""".format(
        len(_9_6Reduction), 
        firstDateDistributed,
        lastDateDistributed,
        
        len(buildsByPackage),
        reportAbsAndPercent(len([bi for pkg in buildsByPackage for bi in buildsByPackage[pkg]]), len(_9_6Reduction)),
        medianBuildsPerPackage,
        maxBuildsPerPackage,
        pkgWithMostBuilds,
        
        reportAbsAndPercent(len(packagesWith2013OnBuilds), len(buildsByPackage)),
        
        reportAbsAndPercent(len(noPackageBuilds), len(_9_6Reduction)),
        reportAbsAndPercent(sum(1 for bi in _9_6Reduction if "rpcs" in bi), len(_9_6Reduction))
    )
    
    mu += "{:,} Packages and their builds, highlight for the {:,} packages with at least one RPC build ...\n\n".format(len(buildsByPackage), sum(1 for pkg in buildsByPackage if sum(1 for bi in buildsByPackage[pkg] if "rpcs" in bi)))
    tbl = MarkdownTable(["Package", "Build \#", "Build Dates", "Build w/RPC \#", "Build w/RPC Delete \#"])
    for pkg in sorted(buildsByPackage):
        pkgMU = "__{}__".format(pkg) if sum(1 for bi in buildsByPackage[pkg] if "rpcs" in bi) else pkg
        dateDistributeds = sorted(list(set(bi["dateDistributed"].split("-")[0] for bi in buildsByPackage[pkg] if "dateDistributed" in bi)))
        if len(dateDistributeds) == 0:
            ddMU = ""
        elif len(dateDistributeds) > 1:
            ddMU = "{} - {}".format(dateDistributeds[0], dateDistributeds[-1])
        else:
            ddMU = dateDistributeds[0]
        rpcBuildInfos = [bi for bi in buildsByPackage[pkg] if "rpcs" in bi]
        rpcBuildInfosDelete = [bi for bi in rpcBuildInfos if "DELETE AT SITE" in bi["rpcs"]]
        tbl.addRow([pkgMU, len(buildsByPackage[pkg]), ddMU, len(rpcBuildInfos) if len(rpcBuildInfos) > 0 else "", len(rpcBuildInfosDelete) if len(rpcBuildInfosDelete) > 0 else ""])
        
    mu += tbl.md() + "\n\n"
    
    noPackageBuildsWRPCs = [bi for bi in noPackageBuilds if "rpcs" in bi]
    mu += "{:,} Builds without a Package but with RPCs ...\n\n".format(len(noPackageBuildsWRPCs))
    tbl = MarkdownTable(["Build", "RPC \#s"])
    for bi in sorted(noPackageBuildsWRPCs, key=lambda x: x["label"]):
        tbl.addRow([bi["label"], sum(len(bi["rpcs"][x]) for x in bi["rpcs"])])
    mu += tbl.md() + "\n\n"
    
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "packagesAndBuilds.md", "w").write(mu)
        
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    # reportPackagesNBuilds(stationNo)
    
    reportBuildsNInstalls(stationNo)

if __name__ == "__main__":
    main()