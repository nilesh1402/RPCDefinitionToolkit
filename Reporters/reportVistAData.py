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
From basic cleaned 9_* 

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
    for pkg in sorted(buildsByPackage, key=lambda x: len(buildsByPackage[x]), reverse=True):
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

    rpcBPIs = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json"))
    bpiByRPC = dict((bpi["label"], bpi) for bpi in rpcBPIs)
    rpcsByPackage = defaultdict(list)
    for bpi in rpcBPIs:
        if "package" not in bpi:
            continue
        rpcsByPackage[bpi["package"]].append(bpi["label"])
    # For report - will OVERRIDE based on ACTIVE from Builds or Not (soon options too)
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = set(red["label"] for red in _8994Reduction)

    """
    TODO: replace/fix up to get the info from rpcBPIs
    """
    buildsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
    buildsRPCReduction = [bi for bi in buildsReduction if "rpcs" in bi]
    buildsWNewRPCReduction = [] 
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
                if "package" in buildInfo:
                    packagesByRPC[rpc][buildInfo["package"]] += 1
                if "dateDistributed" in buildInfo:
                    if rpc not in rpcsSeen: 
                        newRPCSeen = True
                        rpcsSeen.add(rpc)
        if newRPCSeen:
            buildsWNewRPCReduction.append(buildInfo)
        if "dateDistributed" in buildInfo:
            distributed = buildInfo["dateDistributed"]
            if not re.search(r'FMQL', buildInfo["label"]):
                dateDistributeds.append(distributed)
                countBuildsByYr[distributed.split("-")[0]] += 1
                if newRPCSeen:
                    countNewRPCBuildsByYr[distributed.split("-")[0]] += 1

    rpcWithMostBuilds = sorted(rpcBPIs, key=lambda x: len(x["builds"]), reverse=True)[0]["label"]
    packageWithTheMostRPCs = sorted(rpcsByPackage, key=lambda x: len(rpcsByPackage[x]), reverse=True)[0]
    activeRPCs = set(bpi["label"] for bpi in rpcBPIs if "isDeleted" not in bpi)
    deletedRPCs = set(bpi["label"] for bpi in rpcBPIs if "isDeleted" in bpi)
    _8994DeletedRPCs = _8994Labels.intersection(deletedRPCs)
    _8994MissingActiveRPCs = activeRPCs - _8994Labels
    _8994NoBuildRPCs = _8994Labels - set(bpiByRPC.keys())
          
    mu = """## RPCs According to Builds and Installs of {}
    
There are __{}__ builds defining __{:,}__ RPCs distributed from _{}_ to _{}_, __{}__ of which introduce new RPCs. RPC _{}_ appears in the most builds, __{:,}__. The median number of RPCs per Build is __{:,}__. 

RPCs are spread across __{:,}__ packages. Package _{}_ has the most RPCs, __{:,}__. __{:,}__ RPCs have more than one Package usually because of re-organization and splitting of Packages over the years. __{:,}__ RPCs have no package because their builds weren't assigned a package (yet).

Builds can delete as well as add RPCs - __{:,}__ of the RPCs were deleted by the final Build they appeared in, leaving __{:,}__ RPCs active and installed.

File _8994_ is suppossed to define the active RPCs in a VistA. However the 8994 of this system has __{:,}__ deleted RPCs, is missing __{:,}__ active RPCs and has __{:,}__ extra RPCs that never appear in a Build.
    
""".format(

        stationNo, 
        
        reportAbsAndPercent(len(buildsRPCReduction), len(buildsReduction)), 
        len(rpcBPIs),
        dateDistributeds[0], 
        dateDistributeds[-1],
        reportAbsAndPercent(len(buildsWNewRPCReduction), len(buildsRPCReduction)),
        rpcWithMostBuilds, 
        len(bpiByRPC[rpcWithMostBuilds]["builds"]),
        numpy.percentile([len(bpi["builds"]) for bpi in rpcBPIs], 50),
        
        len(buildsByPackage), 
        packageWithTheMostRPCs,
        len(rpcsByPackage[packageWithTheMostRPCs]),
        sum(1 for bpi in rpcBPIs if len(set(bi["package"] for bi in bpi["builds"] if "package" in bi)) > 1),
        sum(1 for bpi in rpcBPIs if "package" not in bpi),
                
        len(deletedRPCs),
        len(activeRPCs),
        
        len(_8994DeletedRPCs),
        len(_8994MissingActiveRPCs),
        len(_8994NoBuildRPCs)
    
    )
    
    """
    Packages by RPC
    """
    tbl = MarkdownTable(["Package", "\# RPCs", "Example RPC"])
    for pkg in sorted(rpcsByPackage, key=lambda x: len(rpcsByPackage[x]), reverse=True):
        tbl.addRow(["__{}__".format(pkg), len(rpcsByPackage[pkg]), sorted(list(rpcsByPackage[pkg]))[0]])
    mu += "{:,} Packages have RPCs, while {:,} RPCs have no Package. Clearly the top Packages (ORDERS, IMAGES and some COTS packages) need to be examined first ...\n\n".format(len(rpcsByPackage), sum(1 for bpi in rpcBPIs if "package" not in bpi))
    mu += tbl.md() + "\n\n"
        
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
        last = calcDate(buildInfos, dtProp, False)
        first = calcDate(buildInfos, dtProp, True)
        return first, last    
                    
    tbl = MarkdownTable(["RPC", "Builds", "(Latest) Package", "Distributed", "[First] Install Gap"])
    lastBuildMNMU = ""
    gaps = []
    noGapRPCs = []
    badGapRPCs = []
    for i, rpc in enumerate(sorted(activeRPCs, key=lambda x: x), 1):
            
        firstD, lastD = muDate(bpiByRPC[rpc]["builds"], "distributed")
        distribMU = lastD
        if firstD != lastD:
            distribMU = "{} - {}".format(firstD, distribMU)    

        firstI, lastI = muDate(bpiByRPC[rpc]["builds"], "installed")  
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
                                        
        tbl.addRow(["__{}__".format(rpc), len(bpiByRPC[rpc]["builds"]), packageMU, distribMU, installGapMU])
                
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
        lastDelBuildInfo = bpiByRPC[rpc]["builds"][-1]
        # a/cs for when no install info
        whenMU = "{} / {}".format(lastDelBuildInfo["distributed"], lastDelBuildInfo["installed"].split("T")[0] if "installed" in lastDelBuildInfo else "-")
        tbl.addRow([rpc, lastDelBuildInfo["label"], whenMU])
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
    mu += "__8994 Rogue RPCs__ are [1] in 8994 but are not active according to Builds (\"EXTRA\" {:,}) or active by builds but not in 8994 (\"MISSING\" {:,}) or deleted by builds but in 8994 (\"SHOULD BE DELETED\" {:,}). __IMPORTANT__: must __test__ if the extra are still active (have code etc) and if so, why ...\n\n".format(len(_8994NoBuildRPCs), len(_8994MissingActiveRPCs), len(_8994DeletedRPCs), len(rogueRPCs))
    mu += tbl.md() + "\n\n"
    
    if stationNo == "999":
        mu += "__Note__: FOIA (999) has MANY _Rogues_. It seems that redaction is partial for non Open Source RPCs. It seems that the code is removed but the RPC remains.\n\n"
    
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcsByBuildsNInstalls.md", "w").write(mu)

"""
RPC i/f according to builds and installs - still installed? (active) or 
never installed? or deleted? ie/ what if there was no 8994? And correct it too

Note: must migrate some heuristics from here and into RED step.
1. __ORDER ENTRY/RESULTS REPORTING__ too well liked. Removed as package if
another available ... play with that ie/ PRIMARY PACKAGE ASSERTION in REDUCTION
2. MAY do buildsByRPC as a reduction ie/ a second level reduction BEFORE doing
this report OR doing assembly
"""
def reportBuildsNInstallsOld(stationNo):

    buildsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
    buildsRPCReduction = [bi for bi in buildsReduction if "rpcs" in bi]
    
    # For report - will OVERRIDE based on ACTIVE from Builds or Not (soon options too)
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = set(red["label"] for red in _8994Reduction)

    buildsByRPC = defaultdict(list)
    buildsWNewRPCReduction = [] 
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
                    info["package"] = buildInfo["package"]
                    packagesByRPC[rpc][buildInfo["package"]] += 1
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
                else:
                    print x
        
    """
    Flips from Builds to view from RPC side: only considers Builds that are installed and 
    if the first build seen for an RPC, it must be a SEND TO SITE (create) build.
    """
    rpcBPIByRPC = {}  
    nixBuildAsNotInstalled = 0
    nixBuildForRPCAsFirstButNotSend = 0
    for buildInfo in buildsRPCReduction:
        if buildInfo["isInstalled"] == False: # let's not count it!
            nixBuildAsNotInstalled += 1
            continue
        for actionType in buildInfo["rpcs"]:
            for rpc in buildInfo["rpcs"][actionType]:
                if rpc not in rpcBPIByRPC:
                    if actionType != "SEND TO SITE": # let's not count until get a SEND
                        nixBuildForRPCAsFirstButNotSend += 1
                        continue 
                    rpcBPIByRPC[rpc] = {"label": rpc, "installed": buildInfo["dateInstalledFirst"], "builds": []}   
                    if "dateDistributed" in buildInfo:
                        rpcBPIByRPC[rpc]["distributed"] = buildInfo["dateDistributed"]
                bir = {"label": buildInfo["label"], "action": actionType, "installed": buildInfo["dateInstalledFirst"]}
                rpcBPIByRPC[rpc]["builds"].append(bir) 
                if "package" in buildInfo:
                    bir["package"] = buildInfo["package"]
                if "dateDistributed" in buildInfo:
                    bir["distributed"] = buildInfo["dateDistributed"]
    for rpc in rpcBPIByRPC:
        bpi = rpcBPIByRPC[rpc]       
        if bpi["builds"][-1]["action"] == "DELETE AT SITE":
            bpi["isDeleted"] = True
            bpi["deleteInstalled"] = bpi["builds"][-1]["installed"]
            if "distributed" in bpi["builds"][-1]:
                bpi["deleteDistributed"] = bpi["builds"][-1]["distributed"]
        packages = [info["package"] for info in buildsByRPC[rpc] if "package" in info]
        if len(set(packages)) == 1:
            bpi["package"] = packages[0]
        elif len(packages): # can be none! 
            packages.reverse()
            # ex override: [u'ORDER ENTRY/RESULTS REPORTING', u'GEN. MED. REC. - VITALS']
            bpi["package"] = [pkg for pkg in packages if pkg != "ORDER ENTRY/RESULTS REPORTING"][0] # last which isn't the overused OE
    
    rpcBPIs = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json"), indent=4)
                                        
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
    
There are __{}__ builds defining __{:,}__ RPCs distributed from _{}_ to _{}_, __{}__ of which introduce new RPCs. RPC _{}_ appears in the most builds, __{:,}__. The median number of RPCs per Build is __{:,}__. 

RPCs are spread across __{:,}__ packages. Package _{}_ has the most RPCs, __{:,}__. __{:,}__ RPCs have more than one Package usually because of re-organization and splitting of Packages over the years. __{:,}__ RPCs have no package because their builds weren't assigned a package (yet).

Builds can delete as well as add RPCs - __{:,}__ of the RPCs were deleted by the final Build they appeared in, leaving __{:,}__ RPCs active and installed.

File _8994_ is suppossed to define the active RPCs in a VistA. However the 8994 of this system has __{:,}__ deleted RPCs, is missing __{:,}__ active RPCs and has __{:,}__ extra RPCs that never appear in a Build.
    
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
    Packages by RPC
    """
    tbl = MarkdownTable(["Package", "\# RPCs", "Example RPC"])
    for pkg in sorted(rpcsByPackage, key=lambda x: len(rpcsByPackage[x]), reverse=True):
        tbl.addRow(["__{}__".format(pkg), len(rpcsByPackage[pkg]), sorted(list(rpcsByPackage[pkg]))[0]])
    mu += "{:,} Packages have RPCs, while {:,} RPCs have no Package. Clearly the top Packages (ORDERS, IMAGES and some COTS packages) need to be examined first ...\n\n".format(len(rpcsByPackage), sum(1 for rpc in buildsByRPC if rpc not in packagesByRPC))
    mu += tbl.md() + "\n\n"
        
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
        tbl.addRow([rpc, re.sub(r'\*', '\\*', lastDelBuildInfo["build"]), whenMU])
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
    mu += "__8994 Rogue RPCs__ are [1] in 8994 but are not active according to Builds (\"EXTRA\" {:,}) or active by builds but not in 8994 (\"MISSING\" {:,}) or deleted by builds but in 8994 (\"SHOULD BE DELETED\" {:,}). __IMPORTANT__: must __test__ if the extra are still active (have code etc) and if so, why ...\n\n".format(len(_8994NoBuildRPCs), len(_8994MissingActiveRPCs), len(_8994DeletedRPCs), len(rogueRPCs))
    mu += tbl.md() + "\n\n"
    
    if stationNo == "999":
        mu += "__Note__: FOIA (999) has MANY _Rogues_. It seems that redaction is partial for non Open Source RPCs. It seems that the code is removed but the RPC remains.\n\n"
    
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcsByBuildsNInstalls.md", "w").write(mu)
    
"""
Options subset RPCs named in 8994 and/or Builds:
- you can't invoke all but built-in RPCs without an option (broker option with RPC list)
- options may not be defined for any user or more particularly any recent/sign on user
... expect 15% reduction of build-named, active RPCs using "active, used option" inclusion
as a criteria.

KEY for REDUCING RPC LIST TO 'EFFECTIVE NUMBER OF ACTIVE, USED RPCs'
"""
def reportRPCOptions(stationNo):

    mu = """## RPC Options of {} 
    
Using _Active, Used RPC Options_ to subset 8994 and Build named RPCs. Expect a __15% reduction__ if we add a requirement that an RPC needs to belong to [1] an active option [2] belonging to a recently signed on user.
    
""".format(stationNo)

    if stationNo == "999":
        mu += "__Exception: with its inconsisent builds and 8994 and its lack of user sign ons and types, FOIA (999) does not follow a regular VistA pattern so many observations below don't apply to it.__\n\n" 
    
    # Raw RPC Broker Options to give # that don't have "rpcs" (purely for reporting)
    _19Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_19Reduction.json"))
    """
    Form: {"label": rpc, "options": [{"label" "isRemoved", sUsersCount, usersCount}]
    ... note: not ALL broker options as some have no RPCs (must get from raw 19)
                    and will flip to
          byOption: {"label" (option), ... "rpcs": []} 
    ie/ so options under rpcs and rpcs under options
    
    and then two sets: activeNUsedOptions and the RPCs of those options
    """
    rpcOptionsWithUse = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "rpcOptionsWithUse.json")) 
    rpcOptionInfoByLabel = {} # includes RPCs of options    
    for roi in rpcOptionsWithUse:
        rpc = roi["label"]
        for oi in roi["options"]:
            if oi["label"] not in rpcOptionInfoByLabel:
                rpcOptionInfoByLabel[oi["label"]] = oi # flip
                oi["rpcs"] = []
            rpcOptionInfoByLabel[oi["label"]]["rpcs"].append(roi["label"])
    activeUsedOptions = set(option for option in rpcOptionInfoByLabel if "isRemoved" not in rpcOptionInfoByLabel[option] and "sUsersCount" in rpcOptionInfoByLabel[option])
    rpcsOfActiveUsedOptions = set(rpc for option in activeUsedOptions for rpc in rpcOptionInfoByLabel[option]["rpcs"])
                            
    mu += """There are {:,} RPC Broker options, {:,} of which name __{:,}__ RPCs. {:,} of these options are marked 'deleted', leaving __{:,}__ of such option-backed RPCs. A further {:,} options are not assigned to an active, recently signed on user - of these, {:,} had older, no longer active users. When those without signed-on users are removed, we're left with __{}__ RPCs backed by __{:,}__ active options with users who recently signed on.
    
__Note__: options _{}_ require keys and {:,} options have Proxy Users - both need testing and analysis.
    
""".format(
        len(_19Reductions),
        len(rpcOptionInfoByLabel),
        len(rpcOptionsWithUse),
        
        sum(1 for option in rpcOptionInfoByLabel if "isRemoved" in rpcOptionInfoByLabel[option]),
        len(set(rpc for option in rpcOptionInfoByLabel if "isRemoved" not in rpcOptionInfoByLabel[option] for rpc in rpcOptionInfoByLabel[option]["rpcs"])),
        
        sum(1 for option in rpcOptionInfoByLabel if not ("isRemoved" in rpcOptionInfoByLabel[option] or "sUsersCount" in rpcOptionInfoByLabel[option])), 
        sum(1 for option in rpcOptionInfoByLabel if "usersCount" in rpcOptionInfoByLabel[option] and "sUsersCount" not in rpcOptionInfoByLabel[option]),
        
        reportAbsAndPercent(
            len(rpcsOfActiveUsedOptions), 
            len(rpcOptionsWithUse)
        ),
        len(activeUsedOptions),
        
        ", ".join(sorted(["\"{}\"".format(option) for option in rpcOptionInfoByLabel if "keyRequired" in rpcOptionInfoByLabel[option] and "sUsersCount" in rpcOptionInfoByLabel[option]])),
        sum(1 for option in rpcOptionInfoByLabel if "proxyUsersCount" in rpcOptionInfoByLabel[option])
        
    ) 
    
    """
    Let's see how many of these option RPCs are 
    """
    bpis = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json"))
    _buildActiveRPCs = set(re.sub(r'\_', '/', bpi["label"]) for bpi in bpis if "isDeleted" not in bpi)
    _inOptionsButNotInBuilds = set(rpc for rpc in rpcsOfActiveUsedOptions if rpc not in _buildActiveRPCs) # few
    _inBuildsButNotOptions = set(rpc for rpc in _buildActiveRPCs if rpc not in rpcsOfActiveUsedOptions)
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = set(re.sub(r'\_', '/', red["label"]) for red in _8994Reduction) 
    _allBuildActiveAnd8994RPCs = _buildActiveRPCs.union(_8994Labels)
    _inOptionsButNot8994 = set(rpc for rpc in rpcsOfActiveUsedOptions if rpc not in _8994Labels)
    _in8994ButNotOptions = set(rpc for rpc in _8994Labels if rpc not in rpcsOfActiveUsedOptions)
    
    mu += """When compared to _Build RPCs_ and _8994 RPCs_:
    
  * Installed Builds name __{}__ RPCs not in used options while those options name __{:,}__ RPCs not in these Builds ({}).
  * 8994 defines __{}__ RPCs not in user options while those options name __{:,}__ RPCs not in 8994.
  
__Conclusion:__ _Used Options_ reduce the __{:,}__ RPCs named by both Builds and 8994s to __{}__.

""".format(
        reportAbsAndPercent(len(_inBuildsButNotOptions), len(_buildActiveRPCs)),
        len(_inOptionsButNotInBuilds), 
        ", ".join(["\"{}\"".format(rpc) for rpc in _inOptionsButNotInBuilds]),
    
        reportAbsAndPercent(len(_in8994ButNotOptions), len(_8994Labels)),
        len(_inOptionsButNot8994),
        
        len(_allBuildActiveAnd8994RPCs),
        reportAbsAndPercent(len(rpcsOfActiveUsedOptions), len(_allBuildActiveAnd8994RPCs))
    )

    # Show Active RPC Option details
    cols = ["Option", "RPC \#", "Exclusive RPC \#"]
    if stationNo != "999":
        cols.append("\# User / SO / SO0 / Proxy")
    tbl = MarkdownTable(cols)
    for option in sorted(activeUsedOptions, key=lambda x: len(rpcOptionInfoByLabel[x]["rpcs"]) if stationNo == "999" else rpcOptionInfoByLabel[x]["sUsersCount"], reverse=True):
        rpcsOfOtherOptions = set(rpc for ooption in activeUsedOptions if ooption != option for rpc in rpcOptionInfoByLabel[ooption]["rpcs"]) # of other ACTIVE/SO options!
        exclusiveRPCCount = sum(1 for rpc in rpcOptionInfoByLabel[option]["rpcs"] if rpc not in rpcsOfOtherOptions)
        row = ["__{}__".format(option), len(rpcOptionInfoByLabel[option]["rpcs"]), exclusiveRPCCount] 
        if stationNo != "999":
            optionInfo = rpcOptionInfoByLabel[option]
            userCountMU = optionInfo["usersCount"]
            _0SUsersCountMU = "{:,}".format(optionInfo["_0SUsersCount"]) if "_0SUsersCount" in optionInfo else "-"
            proxyUserCountMU = "{:,}".format(rpcOptionInfoByLabel[option]["proxyUsersCount"]) if "proxyUsersCount" in rpcOptionInfoByLabel[option] else "-"
            userCountMU = "{:,} / {:,} / {} / {}".format(userCountMU, optionInfo["sUsersCount"], _0SUsersCountMU, proxyUserCountMU)
            row.append(userCountMU)
        tbl.addRow(row)
    mu += "{:,} Active, SO User Options ...\n\n".format(len(activeUsedOptions))
    mu += tbl.md() + "\n\n"
           
    # Excluded Options, their RPCs, exclusive or otherwise 
    excludedOptions = set(option for option in rpcOptionInfoByLabel if "isRemoved" in rpcOptionInfoByLabel[option] or "sUsersCount" not in rpcOptionInfoByLabel[option])
    rpcsOfExcludedOptions = set(rpc for option in excludedOptions for rpc in rpcOptionInfoByLabel[option]["rpcs"])
    rpcsExclusiveToExcludedOptions = rpcsOfExcludedOptions - rpcsOfActiveUsedOptions
    tbl = MarkdownTable(["Option", "RPC \#", "E+E RPC \#", "(No SO) User \#", "Is Deleted"]) 
    for option in sorted(excludedOptions, key=lambda x: len(rpcOptionInfoByLabel[x]["rpcs"]), reverse=True):
        oInfo = rpcOptionInfoByLabel[option]
        userCountMU = oInfo["usersCount"] if "usersCount" in oInfo else ""
        isRemovedMU = "__YES__" if "isRemoved" in oInfo else ""
        exclusiveExcludedRPCCount = sum(1 for rpc in oInfo["rpcs"] if rpc in rpcsExclusiveToExcludedOptions)
        exclusiveExcludedRPCCountMU = exclusiveExcludedRPCCount if exclusiveExcludedRPCCount > 0 else ""
        tbl.addRow([option, len(oInfo["rpcs"]), exclusiveExcludedRPCCountMU, userCountMU, isRemovedMU])
    mu += "{:,} Excluded (removed or no SO User) Options with {:,} RPCs, {:,} of which don't appear in active options. Note that only a small minority of these options are formally deleted ...\n\n".format(len(excludedOptions), len(rpcsOfExcludedOptions), len(rpcsExclusiveToExcludedOptions))
    mu += tbl.md() + "\n\n"    
    
    mu += """__TODO__:

  * Enhance: Add Build data for options using option info in builds => see first introduction etc
  * Besides the CPRS option, pay attention to Active/SO options with a high proproportion of 0 users: MAG WINDOWS, CAPRI, MAGJ VISTARAD WINDOWS, KPA VRAM GUI, VPR APPLICATION PROXY
  * Focus on options with many 'Exclusive RPCs' like CAPRI, MAG DICOM VISA, YS BROKER1, R1SDCI and others which also have a highish number of users - unlike the OVERLAPPING options, these introduce whole new sets of RPCs
  * SO0 is responsible for most of the logins for many of the most significant SO's (MAG, KPA etc)
  * PROXY users (see user class in user reduction): see the proxy users count. If close to all then very special option
  * Implication of DELETING Excluded Options and their exclusive RPCs - reducing VistA size
  
"""
        
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcsByOptions.md", "w").write(mu)
    
"""
Use options of 200 to show option groups

1. Singles (highish #) ie/ those with high # of SO users and usable on their own
2. Exclusive of Singles
3. Used with Singles
4. Specials like KPA
"""
def reportUserTypes(stationNo):
    
    menuOptionCombosCount = Counter()
    _200Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_200Reduction.json"))
    for _200Info in _200Reductions:
        if not ("signOnCount" in _200Info and "menuOptions" in _200Info):
            continue
        mos = sorted(_200Info["menuOptions"])
        menuOptionCombosCount["/".join(mos)] += 1
        
    THRES = 5
    singles = set(moc for moc in menuOptionCombosCount if menuOptionCombosCount[moc] > THRES and len(moc.split("/")) == 1)
    print "Singles", singles
    mocsWithSinglesInside = set(moc for moc in menuOptionCombosCount if menuOptionCombosCount[moc] > THRES and re.search(r'\/', moc) and sum(1 for p in moc.split("/") if p in singles))
    for moc in mocsWithSinglesInside:
        print moc, menuOptionCombosCount[moc]
    return
    bigNonSingleCombos = set(moc for moc in menuOptionCombosCount if menuOptionCombosCount[moc] > THRES and "KPA VRAM GUI" in moc.split("/"))
    kpaCombos = set(moc for moc in menuOptionCombosCount if menuOptionCombosCount[moc] > THRES and "KPA VRAM GUI" in moc.split("/"))
    
    print bigNonSingleCombos
    return
        
    for moc in sorted(menuOptionCombosCount, key=lambda x: menuOptionCombosCount[x], reverse=True):
        if menuOptionCombosCount[moc] < 5:
            break
        if re.search(r'\/', moc):
            continue
        print moc, menuOptionCombosCount[moc]
            
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    reportUserTypes(stationNo)
    return
        
    reportPackagesNBuilds(stationNo)
    reportBuildsNInstalls(stationNo)
    reportRPCOptions(stationNo)
    
if __name__ == "__main__":
    main()