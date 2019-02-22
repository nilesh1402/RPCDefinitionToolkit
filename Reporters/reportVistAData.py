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

TODO: may combine with Installs (and even packages) - reportBuildInstallPackage
- order of install and if install vs distribution
- want to see if multi-build install is issue
- tie to pkgs not types ie/ conical app 
- more per year: NEW RPCs per year vs builds with RPCs (can be redundant)
"""
def reportBuilds(stationNo):

    buildsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
        
    buildsByRPC = {}
    countBuildsWithRPCs = 0
    rpcsByTypeName = defaultdict(set)
    dateDistributeds = []
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
                if "package" in buildInfo:
                    info["package"] = buildInfo["package"]
                buildsByRPC[rpc].append(info)
                rpcsByTypeName[typeName].add(rpc)
    dateDistributeds = sorted(dateDistributeds)
    rpcWithMost = sorted(buildsByRPC, key=lambda x: len(buildsByRPC[x]), reverse=True)[0]
    typeNameWithMost = sorted(rpcsByTypeName, key=lambda x: len(rpcsByTypeName[x]), reverse=True)[0]
    deletedRPCs = set(rpc for rpc in buildsByRPC if buildsByRPC[rpc][-1]["action"] == "DELETE AT SITE")
          
    mu = """## RPC Builds of {}
    
There are {:,} builds defining {:,} RPCs starting in {} and going to {}. There are {:,} types, the most popular of which is __{}__ with {:,} RPCs. The RPC __{}__ appears in the most builds, {:,}. Note that Builds can delete as well as add RPCs - {:,} of the RPCs were deleted by the final Build they appeared in. 
    
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
        len(deletedRPCs)
    )
            
    tbl = MarkdownTable(["Year", "Builds"])
    total = sum(countBuildsByYr[yr] for yr in countBuildsByYr)
    for yr in sorted(countBuildsByYr, key=lambda x: int(x), reverse=True):
        tbl.addRow([yr, reportAbsAndPercent(countBuildsByYr[yr], total)])
    mu += """RPC Builds by year ...
     
"""
    mu += tbl.md() + "\n\n"

                    
    def calcDistrib(buildInfos, first=False):
        distrib = ""
        for buildInfo in buildInfos:
            if "distributed" in buildInfo:
                distrib = buildInfo["distributed"]
                if first:
                    break
        return distrib
    tbl = MarkdownTable(["RPC", "Builds", "Type(s)", "[First Distributed]/Last Distributed", "Version(s)"])
    lastTypeNameMU = ""
    for i, rpc in enumerate(sorted(buildsByRPC, key=lambda x: x), 1):

        lastDistrib = calcDistrib(buildsByRPC[rpc], False)
        distribMU = lastDistrib
        firstDistrib = calcDistrib(buildsByRPC[rpc], True)
        if firstDistrib != lastDistrib:
            distribMU = "{} - {}".format(firstDistrib, distribMU)

        typeNames = list(set(bi["typeName"] for bi in buildsByRPC[rpc]))
        if len(typeNames) > 1:
            versionMU = ", ".join("{} ({})".format(bi["typeName"], bi["version"]) for bi in buildsByRPC[rpc])
        else:
            versionMU = ", ".join(bi["version"] for bi in buildsByRPC[rpc])
        typeNameMU = ", ".join(sorted(typeNames)) if len(typeNames) > 1 else typeNames[0]
        
        isLastActionDelete = True if buildsByRPC[rpc][-1]["action"] == "DELETE AT SITE" else False
        
        rpcMU = "{} (__DELETED__)".format(rpc) if isLastActionDelete else rpc
                
        tbl.addRow([rpcMU, len(buildsByRPC[rpc]), typeNameMU, distribMU, versionMU])
        
    mu += tbl.md() + "\n\n"
    
    mu += """__Notes:__
    
  * the list here (active and deleted) need to be compared to the 8994 list of the same system (preliminary check shows few 8994 for deleted or non build-defined RPCs and nearly all deleted RPCs don't appear in 8994)
  * the Install (9.7) SHOULD (?) fix any lack of correlation between the builds and 8994. A build may not have been installed or installed in a different order from distribution order. A combined report will be needed.
  * greater than 1 type for an RPC (based on builds they appear in) seems to reflect mistakes or a change in a package/build designation name ('TEXT INTEGRATION UTILITIES' became 'TIU')
  * the "type" needs to be aligned with Package (9_4) prefixes to tie RPCs to VistA 'applications'. 
  * NEW RPCs per year vs just new build with RPCs per year
   
"""
    
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
    
    reportBuilds(stationNo)

if __name__ == "__main__":
    main()