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
    
def reportRPCOptions(stationNo):

    # RPC Broker Options (checked in reduction that only they have RPCs)
    _19Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_19Reduction.json"))
    
    # Decision to use Build Definitions of RPCs ie/ active RPCs according to builds and not 8994    
    bpis = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json"))
    _buildActiveRPCs = set(re.sub(r'\_', '/', bpi["label"]) for bpi in bpis if "isDeleted" not in bpi)
    
    mu = """## RPC Options of {} 
    
Key is that nearly all RPCs need to be in Options or else they can't be invoked. But there's more - they need to have code behind them (from builds); they need to be in 8994; and a (recent) user must have an option they belong to. The following examines RPCs in terms of options and then the overlap of that set with the other ways an RPC can be active.

""".format(stationNo)

    removedBrokerOptions = []
    rpcLessBrokerOptions = []
    _19ReductionsWRPCs = []
    optionsOfRPCs = defaultdict(list)
    for _19Reduction in _19Reductions:
        if "isRemoved" in _19Reduction:
            removedBrokerOptions.append(_19Reduction)
            continue
        if "rpcs" not in _19Reduction:
            rpcLessBrokerOptions.append(_19Reduction)
            continue
        _19ReductionsWRPCs.append(_19Reduction)
        for rpc in _19Reduction["rpcs"]:
            optionsOfRPCs[rpc].append(_19Reduction["label"])
                    
    # REM: both active - possibility of further subset of ACTIVE RPCs
    _inOptionsButNotInBuilds = set(rpc for rpc in optionsOfRPCs if rpc not in _buildActiveRPCs) # few
    _inBuildsButNotOptions = set(rpc for rpc in _buildActiveRPCs if rpc not in optionsOfRPCs)
    
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = set(re.sub(r'\_', '/', red["label"]) for red in _8994Reduction) 
    _inOptionsButNot8994 = set(rpc for rpc in optionsOfRPCs if rpc not in _8994Labels)
    _in8994ButNotOptions = set(rpc for rpc in _8994Labels if rpc not in optionsOfRPCs)
    
    if stationNo != "999" and len(_inOptionsButNot8994):
        raise Exception("Expect all in Option to be in 8994 - not showing exceptions below")
    
    _in8994nBuildsButNotOptions = _inBuildsButNotOptions.intersection(_in8994ButNotOptions)
            
    mu += "Of {:,} RPC Broker Options, {:,} are removed and {:,} have no RPCs defined, leaving {:,} active covering {:,} RPCs. But {:,} of these are NOT in the list of Active RPCs according to the build system (see table below for where they appear). More importantly, the build system declares {:,} active RPCs which don't appear in any option - requiring an option would further subset the active RPC list. {:,} of the active RPCs are NOT in 8994 and {:,} of 8994 are not active RPCs. There are {:,} RPCs NOT in options but in both 8994 and Builds - broadly builds and 8994 agree but options exclude (this last statement applies to all but FOIA which has a messed up 8994).\n\n".format(
        len(_19Reductions),
        len(removedBrokerOptions),
        len(rpcLessBrokerOptions),
        len(_19ReductionsWRPCs),
        len(optionsOfRPCs),
        len(_inOptionsButNotInBuilds),
        len(_inBuildsButNotOptions),
        len(_inOptionsButNot8994),
        len(_in8994ButNotOptions),
        len(_in8994nBuildsButNotOptions)
        
    )      
    
    """
    Note: may subset options further - no active RPCs in Builds
    """
    tbl = MarkdownTable(["Option", "Count RPCs", "Exclusive RPCs", "Key Required", "RPCs not in Builds"])
    for _19Reduction in sorted(_19ReductionsWRPCs, key=lambda x: len(x["rpcs"]), reverse=True):
        label = _19Reduction["label"]
        exclusiveRPCs = [rpc for rpc in _19Reduction["rpcs"] if len(optionsOfRPCs[rpc]) == 1]
        keyRequiredMU = "__{}__".format(_19Reduction["keyRequired"]) if "keyRequired" in _19Reduction else ""
        rpcsInOptionButNotInBuildList = [rpc for rpc in _19Reduction["rpcs"] if rpc not in _buildActiveRPCs]
        rpcsInOptionButNotInBuildListMU = "" if len(rpcsInOptionButNotInBuildList) == 0 else len(rpcsInOptionButNotInBuildList)
        if len(rpcsInOptionButNotInBuildList) == len(_19Reduction["rpcs"]):
            label = "__{}__ [NOT ACTIVE]".format(label)
        tbl.addRow([label, len(_19Reduction["rpcs"]), len(exclusiveRPCs), keyRequiredMU, rpcsInOptionButNotInBuildListMU])
    mu += tbl.md() + "\n\n"
    mu += "__Note__: must examine Key's effect on options if present.\n\n"
    
    mu += "TODO: add if in User / UserSO"
    
    print mu
    
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcsByOptions.md", "w").write(mu)
        
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    reportRPCOptions(stationNo)
    return
    
    reportPackagesNBuilds(stationNo)
    reportBuildsNInstalls(stationNo)
    
if __name__ == "__main__":
    main()