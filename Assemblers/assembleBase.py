#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
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
           
        # For now, just unifying options listed
        try:
            _19Reductions = json.load(open(VISTA_RPCD_LOCN_TEMPL.format(sno) + "_19Reduction.json"), object_pairs_hook=OrderedDict)
        except:
            pass
        else:
            optionsOfRPCs = defaultdict(set)
            for _19Red in _19Reductions:
                if "rpcs" not in _19Red:
                    continue
                for rpc in _19Red["rpcs"]:
                    optionsOfRPCs[rpc].add(_19Red["label"])    
            for rpc in optionsOfRPCs:
                if rpc not in definitionsByRPC:
                    continue # may be rogue or bad entry?
                definitionsByRPC[rpc]["options"] = sorted(list(optionsOfRPCs[rpc]))
            
    json.dump(definitionsByRPC, open("../Definitions/rpcInterfaceDefinition.bjsn", "w"), indent=4)
        
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    assemble()

if __name__ == "__main__":
    main()
