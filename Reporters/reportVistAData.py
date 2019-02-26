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
- do 

Unmatched 442 Note: shows R1 etc ... need to do more
=====================================================
    
    ANU HS DOWNLOAD*2.0*0: Developed by Shawn Hardenbrook Nashville VA Medical Center, 
    for downloading health summaries (should be uninstalled - installed twice but
    both after distrib date)
    
    APGKCLC0*3.0*1: No match but also a file in 644 range (local?) 
    APGKNU 2.0: No Match but has files with comments about GUIs
            
    AXVVA*1.0*6: VISN-20's "Visual Aid for Clinic Appointments"
            
    NVS[S]: maybe National Vital Statistics System (NVSS) but RPCs don't match this
    intent.
    
    DSIP...: Monograph has Encoder Product Suite (EPS) ie/ TODO is link in Monograph
    DSIVA 1.6: Monograph has DSIVA as Advanced Prosthetics Acquisition Tool (APAT). ie/ TODO is link in Monograph
    
    R1ENING 2.0: No Match but context and RPCs about bed changes
    
    R1ENINL 1.0: Region 5 VBA import tool ... GUI application which validates the data against the AEMS/MERS database (and has its own option) ... Note: why not Region 5? ie/ R5
    
    R1ENINU*1.0*1: Can't Match (Note: another one with its own context)
    R1OREPI 1.0: Can't Match (Note: another one with its own context)
    R1SDCI*1.0*[23]: Can't Match
    
    [R1]SRLOR
        R1SRL OR SCHEDULE VIEWER 1.0
        R1SRL OR SCHEDULE VIEWER 2.0
    Surgery App viewer (http://robertdurkin.com/projects/R1SRLORScheduleViewer/index.html)
    
    R1UTTFU 1.0: Can't Match
    R1XUM*1.0*1: Can't Match (but does update VDL file)
    
    VANOD: VA Nursing Outcomes Database (Project)
    ... based in Puget Sound
    https://www.hsrd.research.va.gov/research/abstracts.cfm?Project_ID=2141692554 
    ... from 2005 and crude as responsible for many of the "RERELEASE" RPCs ... seems
    to release a new update with new RPCs!
    
    <---- double check if responsible for install order issue too
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
    """
    class PackageMatcher: # see how monograph can come in handy
        
        def __init__(self, stationNo):
            _9_4Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_4Reduction.json"))
            self.__pkgByPrefix = defaultdict(list)
            self.__prefixByPkg = defaultdict(list)
            self.__unmatched = []
            for entry in _9_4Reduction:
                self.__pkgByPrefix[entry["prefix"]].append(entry["label"])
                self.__prefixByPkg[entry["label"]].append(entry["prefix"])
                
        # Searching on Builds with no matches and see matches in Monograph or online
        # ... Note: if R1 starts build name, probably means Region 1 and it is local
        # and prone to reuse across versions 
        BEYOND_PACKAGE_MATCHES = {
            "AXVVA": "Visual Aid for Clinic Appointments (VISN 20)",
            "DSIP": "Encoder Product Suite (EPS)", # monograph
            "DSIVA": "Advanced Prosthetics Acquisition Tool (APAT)", # monograph
            "VANOD": "VA Nursing Outcomes Database (Project)"
        }
        
        """
        # Expects 'typeName' to be have added to buildInfo!
        
        If package link exists, take that
        If type name is prefix of a package then take that
        if type name is package name then use it
        See manual matches of type name
        OR no match (usually R1 etc)
        
        TODO: figure out why the list of [] package to avoid problem below
        TODO BIGGER: probably move BACK to reduction along with typeName
        """
        def match(self, buildInfo):
        
            # the check of __prefixByPkg ensures package ref is valid ... invalid in FOIA
            if "package" in buildInfo and re.sub(r'\_', '/', buildInfo["package"]) not in self.__prefixByPkg:
                return [buildInfo["package"]]
                
            if buildInfo["typeName"] in self.__pkgByPrefix:
                return self.__pkgByPrefix[buildInfo["typeName"]]
                
            if buildInfo["typeName"] in self.__prefixByPkg:
                return [buildInfo["typeName"]]
                
            if buildInfo["typeName"] in PackageMatcher.BEYOND_PACKAGE_MATCHES:
                return [PackageMatcher.BEYOND_PACKAGE_MATCHES[buildInfo["typeName"]]]
                
            self.__unmatched.append(buildInfo["label"])
            
            return None
            
        def unmatched(self):
            return self.__unmatched         
        
    buildsByRPC = {}
    countRPCsOfBuilds = Counter()
    countBuildsWithRPCs = 0
    rpcsByTypeName = defaultdict(set)
    dateDistributeds = []
    dateInstalleds = []
    countBuildsByYr = Counter()
    countNewRPCBuildsByYr = Counter()
    packagesCount = Counter()
    packageMatcher = PackageMatcher(stationNo)
    for buildInfo in buildsReduction:
        if "rpcs" not in buildInfo:
            continue
        countBuildsWithRPCs += 1
        versionMatch = re.search(r'(\d.+)$', buildInfo["label"])
        if versionMatch:
            version = versionMatch.group(1)
            # TODO: issue with R1SDCI1.02 etc exception but no a/cing
            typeName = re.sub(r' +$', '', re.match(r'([^\*^\d]+)', buildInfo["label"]).group(1)) # trailing out
        else:
            raise Exception("Expect to find version in Build Name: {}".format(buildInfo["label"]))
        buildInfo["typeName"] = typeName
        package = packageMatcher.match(buildInfo) # list now but fix this
        if package:
            buildInfo["package"] = package
            for pkg in package:
                packagesCount[pkg] += 1 # some use one build for > 1 pkg
        for actionType in buildInfo["rpcs"]:
            for rpc in buildInfo["rpcs"][actionType]:
                info = {"build": buildInfo["label"], "typeName": typeName, "version": version, "action": actionType}
                if package:
                    info["package"] = package
                countRPCsOfBuilds[buildInfo["label"]] += 1
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
                buildsByRPC[rpc].append(info)
                rpcsByTypeName[typeName].add(rpc)
    dateDistributeds = sorted(dateDistributeds)
    rpcWithMost = sorted(buildsByRPC, key=lambda x: len(buildsByRPC[x]), reverse=True)[0]
    typeNameWithMost = sorted(rpcsByTypeName, key=lambda x: len(rpcsByTypeName[x]), reverse=True)[0]
    deletedRPCs = set(rpc for rpc in buildsByRPC if buildsByRPC[rpc][-1]["action"] == "DELETE AT SITE") # this will include those never even installed!
    deletedRPCsIn8994 = [rpc for rpc in deletedRPCs if rpc in _8994Labels]
    activeRPCs = set(buildsByRPC) - deletedRPCs
    greaterThanOneTypeActiveRPCs = [rpc for rpc in activeRPCs if len(set(bi["typeName"] for bi in buildsByRPC[rpc])) > 1]
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
        len(rpcsByTypeName), 
        typeNameWithMost,
        len(rpcsByTypeName[typeNameWithMost]),
        len(packagesCount), 
        rpcWithMost, 
        medianRPCCountOfBuilds,
        
        len(buildsByRPC[rpcWithMost]),
        len(deletedRPCs),
        len(activeRPCs)
    )
    
    """
    Packages used
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
    lastTypeNameMU = ""
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
        
        typeNames = list(set(bi["typeName"] for bi in buildsByRPC[rpc]))
        if len(typeNames) > 1:
            versionMU = ", ".join("{} ({})".format(bi["typeName"], bi["version"]) for bi in buildsByRPC[rpc])
        else:
            versionMU = ", ".join(bi["version"] for bi in buildsByRPC[rpc])
        typeNameMU = ", ".join(sorted(typeNames)) if len(typeNames) > 1 else typeNames[0]
        
        # may // typeNames or merge if moved the prefix along
        packages = set()
        for bi in buildsByRPC[rpc]:
            if "package" not in bi:
                continue
            for package in bi["package"]:
                packages.add(package)
        packageMU = ", ".join(sorted(list(packages))) if len(packages) else ""
                                
        tbl.addRow(["__{}__".format(rpc), len(buildsByRPC[rpc]), typeNameMU, packageMU, distribMU, installGapMU, versionMU])
                
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