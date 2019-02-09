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

SNOS = ["442", "640", "999"]

def assemble(): # first just compare contents
    pass

# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    reduceFMData(stationNo)

if __name__ == "__main__":
    main()
