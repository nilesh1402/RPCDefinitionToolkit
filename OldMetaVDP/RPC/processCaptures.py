"""
Process/analyze capture.txt from rpcServer/log

Focus on RPCs up to Patient Select and then from Patient Select to BEFORE
choose a domain specific tab like Orders etc. Those specifics for allergies,
orders etc should be in own captures.

Starting point: complete captures from TCPConnect hopefully up to #BYE#
Slice using known cut off RPCs.

TODO: 
- contract volume of RPCs for Order to other domains (Allergy etc)
- move to .md for phases
"""

import os
import sys
import re
import json
from collections import defaultdict
from collections import OrderedDict

from markdownCategorizedRPCs import reportPercent

CAPTURE_LOCN = "captures/"
RPCS_CATEGORIZED_JSON = "json/rpcsCategorized.json"
    
#
# Phase 1 over to 2:
#   before TOP checking Patient and excludes LIST and sorts that follow. End in 
#   'ORQPT DEFAULT LIST SOURCE' which gives team etc of User (but isn't patient specific 
#   per se)
#

def reportCapture(captureFile, phase="", jsonListRPCs=False):

    if not phase:
        phase = re.match(r'capture\-p(\d)', captureFile).group(1)

    rpcInfoList = json.load(open(CAPTURE_LOCN + captureFile))

    rpcsCategorizedByName = json.load(open(RPCS_CATEGORIZED_JSON))
        
    rpcInfosByName = defaultdict(list)
    rpcInfosByDivision = defaultdict(list)
    total = 0
    for rpcInfo in rpcInfoList:
        name = rpcInfo["name"]
        division = "AUTHENTICATION" if name in ["TCPConnect", "#BYE#"] else rpcsCategorizedByName[rpcInfo["name"]]["division"]
        rpcInfosByDivision[division].append(rpcInfo)
        if division == "OUT OF SCOPE":
            continue
        total += 1
        rpcInfosByName[name].append(rpcInfo)
        
    print
    print "-----------------------------------------------------"
    print
    print "Phase", phase, "capture file", "<" + captureFile + ">"
    print
    print "Total RPCs invoked:", "\t", total, "\t", len(rpcInfosByName), "[UNIQUE]"
    print "\tFirst:", "\t", rpcInfoList[0]["name"] # TCPConnect if complete
    print "\tLast:", "\t", rpcInfoList[-1]["name"] # "#BYE#" if complete
    print
    print "By Name:"
    for i, name in enumerate(sorted(rpcInfosByName.keys()), 1):
        print "\t", i, name, "\t", len(rpcInfosByName[name])
    print
    print "By Division (unlike By Name, includes OUT OF SCOPE):"
    urpcNamesByDivision = {}
    for i, division in enumerate(sorted(rpcInfosByDivision.keys()), 1):
        uRPCNames = sorted(list(set([rpcInfo["name"] for rpcInfo in rpcInfosByDivision[division]])))
        urpcNamesByDivision[division] = uRPCNames
        print "\t", i, division, "\t", reportPercent(len(rpcInfosByDivision[division]), total), "\t", reportPercent(len(uRPCNames), len(rpcInfosByName.keys())), "[UNIQUE]"
    print
    
    # If division < one fifth then print them
    for division in sorted(rpcInfosByDivision.keys()):
        print
        if (float(len(rpcInfosByDivision[division])) / float(total)) < 0.2:
            print "All", division + ":"
            for i, rpcName in enumerate(urpcNamesByDivision[division], 1):
                print "\t", i, rpcName
            print

    if not jsonListRPCs:
        return
    print
    print "List", json.dumps(sorted(rpcInfosByName.keys()))
    print
            
"""
Ex/
pruneCaptureFile("capture-order-createsigndetail.txt", "capture-p2orderpsel.txt", fromRPC=P2_MARKER_RPC, uptoRPC=P3_ORDERSTART_MARKER_RPC, prunePOLLs=True)
"""
P2_MARKER_RPC = "ORWPT TOP" 
P3_ORDERSTART_MARKER_RPC = "ORWDX WRLST" # doesn't support break discontinue from create inside orders as based on second LOCK

def pruneCaptureFile(captureFile, newCaptureFile, fromRPC="", uptoRPC="", prunePOLLs=True):
    add = False
    rpcInfoList = json.load(open(CAPTURE_LOCN + captureFile))
    nRPCInfoList = []
    for rpcInfo in rpcInfoList:
        if uptoRPC and rpcInfo["name"] == uptoRPC:
            break
        if fromRPC and rpcInfo["name"] == fromRPC:
            add = True
        if not add:
            continue
        if prunePOLLs and rpcInfo["name"] == "ORWCV POLL":
            continue
        nRPCInfoList.append(rpcInfo) 
    json.dump(nRPCInfoList, open(CAPTURE_LOCN + newCaptureFile, "w"), indent=2)
    
def rpcNames(rpcInfoList):
    return sorted([rpcInfo["name"] for rpcInfo in rpcInfoList])
        
# ##################### DRIVER ################
        
def main():

    reportCapture("capture-p1bpsel.txt", phase=1)
    return

    reportCapture("capture-p3PCE.txt", jsonListRPCs=True)
    return

    reportCapture("capture-p3medopcrsers.txt", jsonListRPCs=True)
    return

    reportCapture("capture-p3allergies.txt", jsonListRPCs=True)

    reportCapture("capture-p3problems.txt", jsonListRPCs=True)

    reportCapture("capture-p3vitals.txt", jsonListRPCs=True)

    reportCapture("capture-p3mednvacrsrdrs.txt", jsonListRPCs=True) 
 
    return
            
    reportCapture("capture-p1bpsel.txt", phase=1)
            
    reportCapture("capture-p2psel.txt", phase=2)  
        
if __name__ == "__main__":
    main()
    
