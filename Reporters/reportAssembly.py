#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

SNOS = ["442", "640", "999"] # SHOULD PUT DATE ON THESE

"""
Others to report:
- emulated in VAM 1 (fixed defn) ... rem move to breath first
- reference param use #'s 
ie/ broad metrics for planning 

... TODO: move to separate reporter as a manifest / progress report
... will go along with RPC i/f improved docs
"""
def reportAssembly():

    definitionsByRPC = json.load(open("../Definitions/rpcInterfaceDefinition.bjsn"), object_pairs_hook=OrderedDict)
        
    """
    \# | Metric | Count
    --- | --- | ---
    1 | Total RPCs | 5,475
    2 | In all 3 | 3,669
    3 | In both 442/640 but not FOIA | 1,481
    4 | Exclusive 442 | 87
    5 | Exclusive 640 | 231
    6 | Exclusive 999 | 5
    """
    tbl = MarkdownTable(["Metric", "Count"])
    tbl.addRow(["__Total RPCs__", "__{:,}__".format(len(definitionsByRPC))])
    tbl.addRow(["In all 3", sum(1 for rpc in definitionsByRPC if len(definitionsByRPC[rpc]["_vistas"]) == 3)])
    tbl.addRow(["In both 442/640 but not FOIA", sum(1 for rpc in definitionsByRPC if set(definitionsByRPC[rpc]["_vistas"]) == set(["442", "640"]))])
    for sno in SNOS:
        tbl.addRow(["Exclusive {}".format(sno), sum(1 for rpc in definitionsByRPC if len(definitionsByRPC[rpc]["_vistas"]) == 1 and sno in definitionsByRPC[rpc]["_vistas"])])
    print tbl.md()
    print
    
    """
    Break this down ...
    """
    byOptionCount = defaultdict(set)
    rpcsByOption = defaultdict(set)
    for rpc in definitionsByRPC:
        if "options" not in definitionsByRPC[rpc]:
            byOptionCount[0].add(rpc)
            continue
        byOptionCount[len(definitionsByRPC[rpc]["options"])].add(rpc)
        if len(definitionsByRPC[rpc]["options"]) > 10:
            continue
        for opt in definitionsByRPC[rpc]["options"]:
            rpcsByOption[opt].add(rpc)
    print "## Menu options\n" 
    print "{} RPCs don't appear in any option, {} have only one option, {} have 2, {} 3, {} between 4 and 9, {} more. The biggest number for any RPC is {}, the RPC {}.".format(
        reportAbsAndPercent(len(byOptionCount[0]), len(definitionsByRPC)), 
        reportAbsAndPercent(len(byOptionCount[1]), len(definitionsByRPC)),
        reportAbsAndPercent(len(byOptionCount[2]), len(definitionsByRPC)),
        reportAbsAndPercent(len(byOptionCount[3]), len(definitionsByRPC)),
        reportAbsAndPercent(sum(len(byOptionCount[x]) for x in byOptionCount if x > 3 and x < 10), len(definitionsByRPC)),
        reportAbsAndPercent(sum(len(byOptionCount[x]) for x in byOptionCount if x >= 10), len(definitionsByRPC)),
        max(byOptionCount.keys()),
        list(byOptionCount[max(byOptionCount.keys())])[0]
    )
    print
    print "Top Options - number of RPCs:"
    for i, opt in enumerate(sorted(rpcsByOption, key=lambda x: len(rpcsByOption[x]), reverse=True), 1):
        if i > 15:
            break
        print "\t{}. {} - {}".format(i, opt, len(rpcsByOption[opt]))
        
    print 
    
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    reportAssembly()

if __name__ == "__main__":
    main()