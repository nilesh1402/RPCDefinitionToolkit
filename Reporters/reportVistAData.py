#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

# ########################### Monograph #######################
    
"""
For VistA-side app breakdown

Note: will go with Package (9_4) source from actual VistAs

Some Questions/Observations to use:
- if in Decommissioning, any still active? ie/ done or pending?
- some names in > 1 ns (many namespaces)
- COTS/DSS set
- some have no namespaces => NOT VISTA?
- groups sometimes mean shared NSs, sometimes not
"""
DECOMMISSION_GROUP = "Ongoing/Completed Application Decommissioning"
# Note: DSS has 35 products on TRM (https://www.oit.va.gov/Services/TRM/ReportToolVendor.aspx) but not all in Monograph
DSS_GROUP = "DSS Inc, Commercial-off-the-Shelf (COTS) VistA Integrations"

def reduceMonograph():

    monograph = json.load(open("../SourceArtifacts/monograph.bjsn"))
    
    bd = {"total": len(monograph["entries"]), "allNamespaces": set(), "decommissionedByNamespace": defaultdict(list), "noNamespace": [], "activeNotDSSByNamespace": defaultdict(list), "dssByNamespace": defaultdict(list), "haveManyNamespaces": {}, "byGroup": defaultdict(list)}
    
    for entry in monograph["entries"]:
        if not ("Namespace" in entry or "Namespaces" in entry):
            bd["noNamespace"].append(entry["Name"])
            continue
        nss = [entry["Namespace"]] if "Namespace" in entry else entry["Namespaces"]
        if "Namespaces" in entry:
            nss = entry["Namespaces"]
            bd["haveManyNamespaces"][entry["Name"]] = nss
        else:
            nss = [entry["Namespace"]]
        for ns in nss:
            bd["allNamespaces"].add(ns)
            if "Group" in entry: 
                if entry["Group"] == DECOMMISSION_GROUP:
                    bd["decommissionedByNamespace"][ns].append(entry["Name"])
                    continue
                if entry["Group"] == DSS_GROUP:
                    bd["dssByNamespace"][ns].append(entry["Name"])
                    continue
                if entry["Name"] not in bd["byGroup"][entry["Group"]]:
                    bd["byGroup"][entry["Group"]].append(entry["Name"])
            bd["activeNotDSSByNamespace"][ns].append(entry["Name"])    
    
    return bd

"""
Key to note missing:
- https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=8969 DSIHH, Databridge
- DSIG could be: https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=6756 (grade of membership)
"""
def reportMonograph():

    mred = reduceMonograph()
    
    mu = """
## Monograph
    
Category | Count (Details)
--- | ---
Total Apps | {:,}
No Namespace | {:,}
decommissioned | {:,} - {}
active NOT COTS | {:,}
COTS | {:,} - {}
Many Namespaces | {:,}
Groups | {:,}

""".format(
        mred["total"], 
        len(mred["noNamespace"]), 
        sum(len(mred["decommissionedByNamespace"][ns]) for ns in mred["decommissionedByNamespace"]), 
        ", ".join(sorted(mred["decommissionedByNamespace"].keys())), 
        sum(len(mred["activeNotDSSByNamespace"][ns]) for ns in mred["activeNotDSSByNamespace"]), 
        sum(len(mred["dssByNamespace"][ns]) for ns in mred["dssByNamespace"]),
        ", ".join(sorted(mred["dssByNamespace"].keys())),
        len(mred["haveManyNamespaces"]),
        len(mred["byGroup"])
    )

    mu += """
No Namespace ...

"""
    for i, entryName in enumerate(sorted(mred["noNamespace"]), 1):
        mu += "{}. {}\n".format(i, entryName)

    mu += """    
    
Active with 'X*' NS ...

"""
    i = 0
    for ns in sorted(mred["activeNotDSSByNamespace"]):
        if not re.match(r'X', ns):
            continue
        i += 1
        mu += "{}. {} - {}\n".format(i, ns, ", ".join(mred["activeNotDSSByNamespace"][ns]))
    
    mu += "\n\n"
    
    open("Reports/source_monograph.md", "w").write(mu)
    
"""
Packages

https://github.com/OSEHRA/VistA/blob/master/Packages.csv

Also tie to TRM for any packages. List is https://www.oit.va.gov/Services/TRM/ReportVACategoryMapping.aspx
"""

    
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    reportMonograph()

if __name__ == "__main__":
    main()