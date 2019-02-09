#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

VISTA_RPCD_LOCN_TEMPL = "/data/vista/{}/RPCDefinitions/"

SNOS = ["442", "640", "999"] # SHOULD PUT DATE ON THESE

"""
First just keep first copy of RPC and tag others have it. 

TODO: validate consistency
"""
def assemble(): 
    
    definitionsByRPC = OrderedDict()
    
    for sno in SNOS:
        
        _8994Reductions = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_8994Reduction.json"), object_pairs_hook=OrderedDict)
        
        for red in _8994Reductions:
            
            if red["label"] in definitionsByRPC:
                definition = definitionsByRPC[red["label"]]
                definition["_vistas"].append(sno)
                continue
                
            red["_vistas"] = [sno]
            rpc = red["label"]
            del red["label"]
            definitionsByRPC[rpc] = red
        
    """
    \# | Metric | Count
    --- | --- | ---
    1 | Total RPCs | 5,475
    2 | In all 3 | 3,669
    3 | In all 442/640 but not FOIA | 1,481
    4 | Exclusive 442 | 87
    5 | Exclusive 640 | 231
    6 | Exclusive 999 | 5
    """
    tbl = MarkdownTable(["Metric", "Count"])
    tbl.addRow(["Total RPCs", len(definitionsByRPC)])
    tbl.addRow(["In all 3", sum(1 for rpc in definitionsByRPC if len(definitionsByRPC[rpc]["_vistas"]) == 3)])
    tbl.addRow(["In all 442/640 but not FOIA", sum(1 for rpc in definitionsByRPC if set(definitionsByRPC[rpc]["_vistas"]) == set(["442", "640"]))])
    for sno in SNOS:
        tbl.addRow(["Exclusive {}".format(sno), sum(1 for rpc in definitionsByRPC if len(definitionsByRPC[rpc]["_vistas"]) == 1 and sno in definitionsByRPC[rpc]["_vistas"])])
    print tbl.md()
        
    json.dump(definitionsByRPC, open("../Definitions/rpcInterfaceDefinition.json", "w"), indent=4)

# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    assemble()

if __name__ == "__main__":
    main()
