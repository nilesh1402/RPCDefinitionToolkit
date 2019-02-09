"""
GOAL: parse CPRS source (and vital DLL as don't have src) to see what RPCs are used.

Bonus: 
- ties in JLV's and eHMP's coverage/overlap/use
- starts categorizing of RPCs into WRITE and READ

BG: CPRS use establishes a key measuring stick for VDM coverage.
"""

import os
import sys
import re
import json

"""
TODO: REDO eHMP RPC list (from eHMPRPCs.py) ... it's fuller and will bring pure HMP RPCs to the fore

Important: using knownRPCs from 8994 of OSEHRA VISTA to decide if really have an RPC or just have a piece of text.
Some vars are x := "..." ; others point to option names, not RPCs.

TODO: may bring RPC broker pascal in here (to go with Chart src). After all parsing vitals binary.  
https://github.com/OSEHRA/VistA/blob/1ce23e76b0d904d0a77912671ef60c581acde582/Packages/RPC%20Broker/BDK/Source/RpcSlogin.pas

"""
VITALSDLL = "GMV_VitalsViewEnter.dll"

CPRS_GUI_CHART_SOURCE = "./../../nodeVISTA/osehraVISTA/latestOSEHRA/Packages/Order Entry Results Reporting/CPRS/CPRS-Chart"

def parseEm(knownRPCs):
    rpcsPerFile = {}
    filesPerRPC = {}

    # Take RPCs from Pascal - var declarations and calls
    varsNotTaken = {} # var assignment looks to be to an RPC but isn't one. For trace
    callsNotTaken = {} # call assignment looks to be to an RPC but isn't. For trace
    pasFiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(CPRS_GUI_CHART_SOURCE) for f in fn if re.search(r'pas$', f)]
    for ff in pasFiles:
        contents = open(ff).read()
        rpcsInVars = set(rpc for rpc in re.findall(r'\:\= +\'([A-Z\d]{2,} [A-Z\d \?\(\)\-]+)\'', contents))
        # means options or basic assignments not to RPCs (or non OSEHRA RPC but assuming!) 
        if len(rpcsInVars - knownRPCs):
           varsNotTaken[ff] = rpcsInVars - knownRPCs
           rpcsInVars = rpcsInVars & knownRPCs
        # tCallV(Dest, 'ORWDAL32 LOAD FOR EDIT', [AllergyIEN])
        rpcsInTCalls = set(rpc for rpc in re.findall(r'tCall[vV]\([^,]+, *\'([^\']+)\'', contents))
        if len(rpcsInTCalls - knownRPCs):
           callsNotTaken[ff] = rpcsInTCalls - knownRPCs
           rpcsInTCalls = rpcsInTCalls & knownRPCs
        # note: not distinguishing SCallV from CallV ? ... CallV and Callv? tCallV etc - so dropping st etc
        rpcsInCalls = set(rpc for rpc in re.findall(r'Call[vV]\(\'([^\']+)\'', contents))
        if len(rpcsInCalls - knownRPCs):
           callsNotTaken[ff] = rpcsInCalls - knownRPCs
           rpcsInCalls = rpcsInCalls & knownRPCs
        rpcs = rpcsInVars | rpcsInCalls | rpcsInTCalls
        for rpcName in rpcs:
            if rpcName not in filesPerRPC:
                filesPerRPC[rpcName] = []
            ffs = re.sub(r'CPRS\-Chart\/', '', ff)
            if ffs not in filesPerRPC[rpcName]:
                filesPerRPC[rpcName].append(ffs)
    # print "Excluded Calls", callsNotTaken, "and vars", varsNotTaken

    # Don't have pascal for vitals so parsing the DLL taken from OSEHRA site (https://www.osehra.org/document/guis-used-automatic-functional-testing)
    rpcsPerFile[VITALSDLL] = []
    vitalsDLLContents = open(VITALSDLL).read();
    for gmvRPC in (set(re.findall(r'(GMV [A-Z\d\/ ]+)', vitalsDLLContents)) & knownRPCs):
        if gmvRPC not in filesPerRPC:
            filesPerRPC[gmvRPC] = []
        filesPerRPC[gmvRPC].append(VITALSDLL)

    print "Total PAS files + Vitals DLL", len(pasFiles) + 1, "Number RPCs", len(filesPerRPC), "in files", len(set(fl for rpc in filesPerRPC for fl in filesPerRPC[rpc]))

    return filesPerRPC

# fixed from R1.3 (Oct/Nov 2015)
eHMPSet = ["GMV ADD VM", "GMV CLOSEST READING", "GMV MARK ERROR", "GMV V/M ALLDATA", "GMV VITALS/CAT/QUAL", "HMPCRPC RPC", "ORQOR DETAIL", "ORQQPL ADD SAVE", "ORQQPL DELETE", "ORQQPL EDIT SAVE", "ORQQPL4 LEX", "ORQQPX REMINDER DETAIL", "ORQQPX REMINDERS LIST", "ORWDAL32 ALLERGY MATCH", "ORWDAL32 CLINUSER", "ORWDAL32 SAVE ALLERGY", "ORWDAL32 SYMPTOMS", "ORWDPS1 DFLTSPLY", "ORWDPS2 DAY2QTY", "ORWDPS2 OISLCT", "ORWDX DLGDEF", "ORWDX LOADRSP", "ORWDX LOCK ORDER", "ORWDX SAVE", "ORWDX SEND", "ORWDX UNLOCK ORDER", "ORWDX2 DCREASON", "ORWDXA DC", "ORWDXA VALID", "ORWPCE GETSVC", "ORWPT CWAD", "ORWRP REPORT LISTS", "ORWRP REPORT TEXT", "ORWU NPHASKEY", "ORWU VALIDSIG", "ORWUL FV4DG", "ORWUL FVIDX", "ORWUL FVSUB", "TIU AUTHORIZATION", "TIU CREATE RECORD", "TIU LOCK RECORD", "TIU SIGN RECORD", "TIU UNLOCK RECORD", "TIU UPDATE RECORD", "TIU WHICH SIGNATURE ACTION"]

# Besides VPR - see issue: https://github.com/vistadataproject/nodeVISTA/issues/26
JLVSet = ["ORWPT ADMITLST", "ORWRP REPORT TEXT", "ORQQAL DETAIL", "ORQQPX REMINDER DETAIL", "ORWPT SELECT", "XWB GET VARIABLE VALUE", "ORWPT1 PRCARE", "ORWPT PTINQ", "ORWLRR INTERIM", "ORWPS DETAIL", "ORQQCN DETAIL", "ORQOR DETAIL", "ORQQPL DETAIL", "ORQQPL PROB COMMENTS"]

CPRS_DELPHI_PASCAL_BASE = "https://github.com/OSEHRA/VistA/blob/master/Packages/Order%20Entry%20Results%20Reporting/CPRS/CPRS-Chart/"

def reportEm(filesPerRPC, defnsById):    

    if len(set(JLVSet) - set(defnsById)):
        raise Exception("Thought all JLV RPCs known to OSEHRA VISTA")

    mu = """---
layout: default
title: CPRS RPC Use
---

"""

    def isWrite(rpc):
        # ... There are others, particularly in ORDERs - expand later
        # Rough pass on "WRITE" designation - exclude if ? (IS THIS SAVED?), CAN ("CAN I?") or GET too
        if re.search(r' (SAVE|UPDATE|EDIT|ADD|MARK|DELETE)', rpc) and not re.search(r'(\?|GET|CAN)', rpc):
            return True
        return False

    mu += "# RPCs used by CPRS\n\n"
    rpcs = sorted(rpc for rpc in filesPerRPC)
    mu += "  1. (OSEHRA) CPRS uses __" + reportAbsAndPercent(len(rpcs), len(defnsById)) + " of the " + str(len(defnsById)) + " RPCs known__ to nodeVISTA (in its 8994 file).\n"
    hmpOnly = set(eHMPSet) - set(defnsById)
    mu += "  2. eHMP (r1.3 Oct 2015) uses " + reportAbsAndPercent(len(eHMPSet) - len(hmpOnly), len(rpcs)) + " of the CPRS-supported RPCs and extra custom RPC(s) (" + ", ".join(list(hmpOnly)) + ").\n"
    mu += "  3. JLV uses " + str(len(JLVSet)) + " (Get) RPCs in addition to its mainstay, the non CPRS-used VPR RPC\n" 
    filesWithRPCs = set(fl for rpc in filesPerRPC for fl in filesPerRPC[rpc])   
    mu += "  4. " + str(len(filesWithRPCs)) + " CPRS Pascal Files call RPCs\n"
    mu += "  5. PRELIM: number WRITE RPCs (not full list yet) - " + str(sum(1 for rpc in rpcs if isWrite(rpc))) + "\n"
    mu += "  6. Sources examined: [OSEHRA CPRS Chart Source](https://github.com/OSEHRA/VistA/tree/master/Packages/Order%20Entry%20Results%20Reporting/CPRS/CPRS-Chart), [Vitals DLL](https://www.osehra.org/document/guis-used-automatic-functional-testing), [eHMP r1.3](https://github.com/vistadataproject/nodeVISTA/tree/master/eHMP/Resources) and [JLV RPC Use](https://github.com/vistadataproject/nodeVISTA/issues/26).\n"
    mu += "Tracked in [issue](https://github.com/vistadataproject/VDM/issues/24)\n"
    mu += "\n\n\n"

    mu += "\# | RPC | MUMPS | CPRS File(s) | Description\n"
    mu += "--- | --- | --- | --- | ---\n"
    currentPrefix = ""
    metaForVDM = []
    for i, rpc in enumerate(rpcs, 1):
        rpcInfo = {"id": rpc, "files": list(filesPerRPC[rpc])} # for VDM: only stuff not already in other DEFNs
        rpcPrefix = re.match(r'([A-Z\d]+)', rpc).group(1)
        if not currentPrefix:
            currentPrefix = rpcPrefix
        elif rpcPrefix != currentPrefix: # skip a row
            mu += "&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;\n"
            currentPrefix = rpcPrefix
        qualifiers = [] 
        if rpc in eHMPSet:
            qualifiers.append("eHMP")
        if rpc in JLVSet:
            qualifiers.append("JLV")
        if isWrite(rpc):
            rpcInfo["write"] = True
            qualifiers.append("WRITE")
        if len(qualifiers):
            rpcMU = rpc + "<br>__" + "/ ".join(qualifiers) + "__"
            rpcInfo["qualifiers"] = qualifiers
        else:
            rpcMU = rpc
        impl = defnsById[rpc]["tag-8994"] + "^" + defnsById[rpc]["routine-8994"]
        if VITALSDLL in filesPerRPC[rpc]:
            if len(filesPerRPC[rpc]) != 1:
                raise Exception("Expected VITALSDLL - GMV_VitalsViewEnter.dll to be alone")
            filesMU = VITALSDLL
        else:
            filesMU = ", ".join("[" + fl + "](" + CPRS_DELPHI_PASCAL_BASE + fl + ")" for fl in filesPerRPC[rpc])
        mu += str(i) + " | " + rpcMU + " | " + impl + " | " + filesMU + " | " + (defnsById[rpc]["description-8994"] if "description-8994" in defnsById[rpc] else "")  + "\n"
        metaForVDM.append(rpcInfo)

    mu += "\n\n"

    open("cprsRPCs.md", "w").write(mu)
    json.dump(metaForVDM, open("../nodeVISTA/cprsRPCs.json", "w"))
    print "... report generated - JSON for VDM too"

def reportAbsAndPercent(abs, total):
    return str(abs) + " (" + reportPercent(abs, total) + ")"

def reportPercent(piece, total):
    if not total: # can't divide by 0
        return "0%"
    return str(makePercent(piece, total)) + "%"

def makePercent(piece, total):
    return round((float(piece) * 100)/float(total), 2)

def main():
    d8994 = json.load(open("../systems/ainaVISTA/8994.jsonld"))
    defnsById = dict((defn["name-8994"], defn) for defn in d8994["@graph"])
    filesPerRPC = parseEm(set(defnsById))
    json.dump(filesPerRPC, open("cprsCodeRPCs.json", "w"), indent=4)
    # reportEm(filesPerRPC, defnsById)

if __name__ == "__main__":
    main()

