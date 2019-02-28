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
- fix up so NO matching for package or any custom reduction here i/e ONLY
do pull in's of pre reds
"""
def reportBuildsNInstalls(stationNo):

    buildsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
    
    # For report
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = [red["label"] for red in _8994Reduction]
    
    """
    NOTE: will probably move into reduce step when embed packages in builds
    
    TODO MORE
        https://github.com/OSEHRA/VistA/blob/master/Packages.csv
        https://www.oit.va.gov/Services/TRM/ReportVACategoryMapping.aspx
        
    TODO: gotta replace use of newer label with older one
    """
    class PackageMatcher: # see how monograph can come in handy
        
        def __init__(self, stationNo):
            _9_4Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_4PlusReduction.json"))
            self.__pkgByPrefix = defaultdict(list)
            self.__prefixByPkg = defaultdict(list)
            self.__unmatched = []
            for entry in _9_4Reduction:
                if "prefix" in entry and entry["prefix"] in ["NTSI", "ASTR", "HIVO", "PSOC"]:
                    print entry
                if "prefix" not in entry:
                    print x
                self.__pkgByPrefix[entry["prefix"]].append(entry["label"])
                self.__prefixByPkg[entry["label"]].append(entry["prefix"])
            print "Loaded {:,} packages".format(len(_9_4Reduction))
            print "{:,} prefixes".format(len(self.__pkgByPrefix))
            print "{:,} package labels".format(len(self.__prefixByPkg))
            for prefix in self.__pkgByPrefix:
                if len(self.__pkgByPrefix[prefix]) == 1:
                    continue
                print prefix, self.__pkgByPrefix[prefix]
                
        # Searching on Builds with no matches and see matches in Monograph or online
        # ... Note: if R1 starts build name, probably means Region 1 and it is local
        # and prone to reuse across versions 
        BEYOND_PACKAGE_MATCHES = {
            "AXVVA": "Visual Aid for Clinic Appointments (VISN 20)",
            "DSIP": "Encoder Product Suite (EPS)", # monograph
            "DSIVA": "Advanced Prosthetics Acquisition Tool (APAT)", # monograph
            "VANOD": "VA Nursing Outcomes Database (Project)" # based in Puget Sound
        }
        
        """
        # Expects 'buildMN' to be have added to buildInfo!
        
        If package link exists, take that
        If type name is prefix of a package then take that
        if type name is package name then use it
        See manual matches of type name
        OR no match (usually R1 etc)
        
        TODO: figure out why the list of [] package to avoid problem below
        TODO BIGGER: probably move BACK to reduction along with buildMN
        """
        def match(self, buildInfo):
        
            # the check of __prefixByPkg ensures package ref is valid ... invalid in FOIA
            if "package" in buildInfo and re.sub(r'\_', '/', buildInfo["package"]) not in self.__prefixByPkg:
                return [buildInfo["package"]]
                
            if buildInfo["buildMN"] in self.__pkgByPrefix:
                return self.__pkgByPrefix[buildInfo["buildMN"]]
                
            if buildInfo["buildMN"] in self.__prefixByPkg:
                return [buildInfo["buildMN"]]
                
            if buildInfo["buildMN"] in PackageMatcher.BEYOND_PACKAGE_MATCHES:
                return [PackageMatcher.BEYOND_PACKAGE_MATCHES[buildInfo["buildMN"]]]
                
            self.__unmatched.append(buildInfo["label"])
            
            return None
            
        def unmatched(self):
            return self.__unmatched         
        
    buildsByRPC = {}
    countRPCsOfBuilds = Counter()
    countBuildsWithRPCs = 0
    rpcsByBuildMN = defaultdict(set)
    dateDistributeds = []
    dateInstalleds = []
    countBuildsByYr = Counter()
    countNewRPCBuildsByYr = Counter()
    packagesCount = Counter()
    for buildInfo in buildsReduction:
        if "rpcs" not in buildInfo:
            continue
        countBuildsWithRPCs += 1
        """
        if package:
            buildInfo["package"] = package
            for pkg in package:
                packagesCount[pkg] += 1 # some use one build for > 1 pkg
        """
        for actionType in buildInfo["rpcs"]:
            for rpc in buildInfo["rpcs"][actionType]:
                info = {"build": buildInfo["label"], "action": actionType}
                if "buildMN" in buildInfo:
                    info["buildMN"] = buildInfo["buildMN"]
                    info["version"] = buildInfo["buildMNVersion"]
                """
                if package:
                    info["package"] = package
                """
                countRPCsOfBuilds[buildInfo["label"]] += 1
                if "dateDistributed" in buildInfo:
                    info["distributed"] = buildInfo["dateDistributed"]
                    if not re.search(r'FMQL', info["build"]):
                        dateDistributeds.append(buildInfo["dateDistributed"])
                        countBuildsByYr[buildInfo["dateDistributed"].split("-")[0]] += 1
                        if rpc not in buildsByRPC: # ie/ new
                            countNewRPCBuildsByYr[
                            buildInfo["dateDistributed"].split("-")[0]] += 1
                if rpc not in buildsByRPC:
                    buildsByRPC[rpc] = []
                if "dateInstalledFirst" in buildInfo:
                    info["installed"] = buildInfo["dateInstalledFirst"]
                    if not re.search(r'FMQL', info["build"]):
                        dateInstalleds.append(buildInfo["dateInstalledFirst"])
                buildsByRPC[rpc].append(info)
                if "buildMN" in info:
                    rpcsByBuildMN[info["buildMN"]].add(rpc)
    dateDistributeds = sorted(dateDistributeds)
    rpcWithMost = sorted(buildsByRPC, key=lambda x: len(buildsByRPC[x]), reverse=True)[0]
    buildMNWithMost = sorted(rpcsByBuildMN, key=lambda x: len(rpcsByBuildMN[x]), reverse=True)[0]
    deletedRPCs = set(rpc for rpc in buildsByRPC if buildsByRPC[rpc][-1]["action"] == "DELETE AT SITE") # this will include those never even installed!
    deletedRPCsIn8994 = [rpc for rpc in deletedRPCs if rpc in _8994Labels]
    activeRPCs = set(buildsByRPC) - deletedRPCs
    greaterThanOneTypeActiveRPCs = [rpc for rpc in activeRPCs if len(set(bi["buildMN"] for bi in buildsByRPC[rpc])) > 1]
    extraRPCs = set(_8994Labels) - activeRPCs # beyond active/still there
    missingRPCs = activeRPCs - set(_8994Labels) # should be there but not
    medianRPCCountOfBuilds = numpy.percentile(countRPCsOfBuilds.values(), 50)
          
    mu = """## RPC Builds of {}
    
There are {:,} builds defining {:,} RPCs starting in {} and going to {}. There are {:,} types, the most popular of which is __{}__ with {:,} RPCs. RPCs are in {:,} packages. The RPC __{}__ appears in the most builds, {:,}. The median number of RPCs per RPC Build is {:,}.

Builds can delete as well as add RPCs - {:,} of the RPCs were deleted by the final Build they appeared in, leaving {:,} RPCs active and installed.
    
""".format(
        stationNo, 
        
        countBuildsWithRPCs, 
        len(buildsByRPC),
        dateDistributeds[0], 
        dateDistributeds[-1],
        len(rpcsByBuildMN), 
        buildMNWithMost,
        len(rpcsByBuildMN[buildMNWithMost]),
        len(packagesCount), 
        rpcWithMost, 
        medianRPCCountOfBuilds,
        
        len(buildsByRPC[rpcWithMost]),
        len(deletedRPCs),
        len(activeRPCs)
    )
    
    """
    Packages used 
    
    TODO: move RPCs to latest package ie/ isolate latest package => can move off
    unused.
    """
    tbl = MarkdownTable(["Package", "Build Count"])
    for pkg in sorted(packagesCount, key=lambda x: packagesCount[x], reverse=True):
        tbl.addRow([pkg, packagesCount[pkg]])
    mu += "Packages used ...\n\n"
    mu += tbl.md() + "\n\n"
        
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
                    
    tbl = MarkdownTable(["RPC", "Builds", "Type(s)", "Package(s)", "Distributed", "[First] Install Gap", "Version(s)"])
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
        
        buildMNs = list(set(bi["buildMN"] for bi in buildsByRPC[rpc]))
        if len(buildMNs) > 1:
            versionMU = ", ".join("{} ({})".format(bi["buildMN"], bi["version"]) for bi in buildsByRPC[rpc])
        else:
            versionMU = ", ".join(bi["version"] for bi in buildsByRPC[rpc])
        buildMNMU = ", ".join(sorted(buildMNs)) if len(buildMNs) > 1 else buildMNs[0]
        
        # may // buildMNs or merge if moved the prefix along
        packages = set()
        for bi in buildsByRPC[rpc]:
            if "package" not in bi:
                continue
            for package in bi["package"]:
                packages.add(package)
        packageMU = ", ".join(sorted(list(packages))) if len(packages) else ""
                                
        tbl.addRow(["__{}__".format(rpc), len(buildsByRPC[rpc]), buildMNMU, packageMU, distribMU, installGapMU, versionMU])
                
    mu += "__{:,}__ Active/Installed RPCs. The maximum gap in days between distribution and install is {:,}, the median is {:,}, {:,} have no gap at all. The gap isn't available if necessary dates are missing ({:,}) or the first install date comes BEFORE the build distribution date (__{:,}__). Note that an install before a distribution probably reflects the re-release of a build and that greater than 1 type for {:,} RPCs probably reflects a change in the type's name over the years ...\n\n".format(len(activeRPCs), max(gaps), numpy.percentile(gaps, 50), sum(1 for g in gaps if g == 0), len(noGapRPCs), len(badGapRPCs), len(greaterThanOneTypeActiveRPCs))
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
    mu += "__Rogue RPCs__ are [1] in 8994 but are not active according to Builds (\"EXTRA\" {:,}) or active by builds but not in 8994 (\"MISSING\" {:,}) or deleted by builds but in 8994 (\"SHOULD BE DELETED\" {:,}) ...\n\n".format(len(extraRPCs), len(missingRPCs), len(deletedRPCsIn8994), len(rogueRPCs))
    mu += tbl.md() + "\n\n"
    
    if stationNo == "999":
        mu += "__Note__: FOIA (999) has MANY _Rogues_. It seems that redaction is partial for non Open Source RPCs. It seems that the code is removed but the RPC remains.\n\n"
    
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcBuilds.md", "w").write(mu)
        
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
        dateDistributeds = sorted([bi["dateDistributed"].split("-")[0] for bi in buildsByPackage[pkg] if "dateDistributed" in bi])
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
    
    reportPackagesNBuilds(stationNo)
    
    reportBuildsNInstalls(stationNo)

if __name__ == "__main__":
    main()