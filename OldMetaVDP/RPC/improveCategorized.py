"""
Enhancing categorized RPCs from other data - merge with manually added data
ie/ don't overwrite PARAMETER or FILE lists but enhance them as some manual
entries will always be necessary.

TODO: 
- LOCKED: completed numbers ie/ record in categorized for markdown (or have as separate JSON?) ie/ CSV parse
  - in MARKDOWN will change top tables to reflect LOCKED %s
- all PARAMETERs without parameters listed ... add em (http://vistadataproject.info/artifacts/cprsRPCBreakdown/bdNon_Clinical)
- process out any nuance/meta from ed enhanced JSON and nix
- compare files list to KFILEs from PIKS ie/ want %'s (may do in report py). Also PIKS must feed into devdocs for VDM (ie/ to be a deliverable)
- tags like GUI and VERSION (version related stuff) and nix old KGRAF etc tags ie/ FORMALLY define meaning of all tags

BIGGIE: formalize version CPRS code/vista code comes from ie/ when parsed and from where.
"""

import os
import sys
import re
import json
from collections import defaultdict
from collections import OrderedDict

RPCS_METHODS = "json/rpcMethodInfos.bjsn"
RPCS_CATEGORIZED_JSON = "json/rpcsCategorized.json"

#
# from *** processCapture.py ***
#
P1BPSELSet = ["OREVNTX1 DLGIEN", "ORQPT DEFAULT LIST SOURCE", "ORQQPX NEW REMINDERS ACTIVE", "ORWCH LDFONT", "ORWCH LOADALL", "ORWCH LOADSIZ", "ORWDBA1 BASTATUS", "ORWDBA3 HINTS", "ORWDX DGNM", "ORWDXM FORMID", "ORWGRPC ALLVIEWS", "ORWGRPC GETPREF", "ORWGRPC TESTSPEC", "ORWGRPC TYPES", "ORWORDG IEN", "ORWPCE I10IMPDT", "ORWRP GET DEFAULT PRINTER", "ORWSR SHOW SURG TAB", "ORWU DT", "ORWU HASKEY", "ORWU NPHASKEY", "ORWU TOOLMENU", "ORWU USERINFO", "ORWU VERSRV", "TCPConnect", "TIU TEMPLATE GET DEFAULTS", "XUS AV CODE", "XUS DIVISION GET", "XUS GET USER INFO", "XUS INTRO MSG", "XUS PKI GET UPN", "XUS SIGNON SETUP", "XWB CREATE CONTEXT", "XWB GET BROKER INFO"]

P2PSELSet = ["DG CHK BS5 XREF ARRAY", "DG CHK PAT/DIV MEANS TEST", "DG SENSITIVE RECORD ACCESS", "OR GET COMBAT VET", "ORCNOTE GET TOTAL", "ORPRF CLEAR", "ORPRF HASFLG", "ORQQAL LIST", "ORQQPL LIST", "ORQQPP LIST", "ORQQVI VITALS", "ORVAA VAA", "ORWCH SAVEALL", "ORWCH SAVFONT", "ORWCIRN AUTORDV", "ORWCIRN FACLIST", "ORWCOM PTOBJ", "ORWCV START", "ORWCV STOP", "ORWCV VST", "ORWCV1 COVERSHEET LIST", "ORWDBA1 BASTATUS", "ORWMHV MHV", "ORWOR UNSIGN", "ORWORB FASTUSER", "ORWORB GETSORT", "ORWORB SETSORT", "ORWPS COVER", "ORWPT DIEDON", "ORWPT ENCTITL", "ORWPT ID INFO", "ORWPT LEGACY", "ORWPT LIST ALL", "ORWPT SELECT", "ORWPT SHARE", "ORWPT TOP", "ORWPT1 PRCARE", "ORWU NPHASKEY", "ORWU PATCH", "TIU TEMPLATE SET DEFAULTS", "XWB DEFERRED CLEARALL"]

P3VITALSSet = ["GMV ADD VM", "GMV CLOSEST READING", "GMV DLL VERSION", "GMV EXTRACT REC", "GMV GET CURRENT TIME", "GMV GET VITAL TYPE IEN", "GMV LATEST VM", "GMV MANAGER", "GMV MARK ERROR", "GMV PARAMETER", "GMV USER", "GMV V/M ALLDATA", "GMV VITALS/CAT/QUAL", "ORQQAL LIST", "ORQQPL LIST", "ORQQPP LIST", "ORQQVI VITALS", "ORWCV POLL", "ORWCV START", "ORWCV STOP", "ORWCV VST", "ORWCV1 COVERSHEET LIST", "ORWPCE GETSVC", "ORWPS COVER", "ORWPT ENCTITL", "ORWTPD1 GETEAFL", "ORWTPD1 GETEDATS", "ORWU DT", "ORWU NEWPERS", "ORWU1 NEWLOC", "TIU TEMPLATE ACCESS LEVEL", "TIU TEMPLATE GETROOTS", "XWB CREATE CONTEXT"]

P3PROBLEMSSet = ["ORIMO ISCLOC", "ORQQPL ADD SAVE", "ORQQPL CHECK DUP", "ORQQPL DELETE", "ORQQPL DETAIL", "ORQQPL EDIT LOAD", "ORQQPL EDIT SAVE", "ORQQPL INIT PT", "ORQQPL INIT USER", "ORQQPL LIST", "ORQQPL PROB COMMENTS", "ORQQPL PROBLEM LIST", "ORQQPL REPLACE", "ORQQPL UPDATE", "ORQQPL USER PROB CATS", "ORQQPL4 LEX", "ORWCV POLL", "ORWCV VST", "ORWLEX GETFREQ", "ORWPCE ACTIVE CODE", "ORWPCE GETSVC", "ORWPT ENCTITL", "ORWTPD1 GETEAFL", "ORWTPD1 GETEDATS", "ORWU CLINLOC", "ORWU DT", "ORWU NEWPERS", "ORWU NPHASKEY", "ORWU1 NEWLOC", "TIU TEMPLATE ACCESS LEVEL", "TIU TEMPLATE GETROOTS"]

P3ALLERGIESSet = ["ORDEA DEATEXT", "ORDEA SIGINFO", "ORPRF CLEAR", "ORQQAL DETAIL", "ORQQAL LIST", "ORQQPP LIST", "ORWCH SAVEALL", "ORWCH SAVFONT", "ORWDAL32 ALLERGY MATCH", "ORWDAL32 CLINUSER", "ORWDAL32 DEF", "ORWDAL32 LOAD FOR EDIT", "ORWDAL32 SAVE ALLERGY", "ORWDAL32 SITE PARAMS", "ORWDAL32 SYMPTOMS", "ORWDBA1 BASTATUS", "ORWDX LOCK", "ORWDX UNLOCK", "ORWOR UNSIGN", "ORWPCE SCDIS", "ORWPS ACTIVE", "ORWPT CWAD", "ORWU DT", "ORWU NEWPERS", "ORWU VALDT", "TIU GET REQUEST", "TIU TEMPLATE SET DEFAULTS", "TIU UNLOCK RECORD"]

P3NVAORDERSet = ["ORCDLR2 CHECK ALL LC TO WC", "ORDEA DEATEXT", "ORDEA SIGINFO", "OREVNTX PAT", "OREVNTX1 GETSTS", "OREVNTX1 GTEVT", "OREVNTX1 ODPTEVID", "ORIMO IMOLOC", "ORIMO ISIVQO", "ORPRF CLEAR", "ORQOR DETAIL", "ORQQAL LIST", "ORQQPP LIST", "ORWCH LOADSIZ", "ORWCH SAVEALL", "ORWCH SAVFONT", "ORWCOM ORDEROBJ", "ORWCV STOP", "ORWCV VST", "ORWDBA1 BASTATUS", "ORWDBA1 SCLST", "ORWDPS1 SCHALL", "ORWDPS2 CHKGRP", "ORWDPS2 OISLCT", "ORWDPS2 QOGRP", "ORWDPS4 CPINFO", "ORWDPS4 IPOD4OP", "ORWDX AGAIN", "ORWDX DGNM", "ORWDX DLGDEF", "ORWDX LOCK", "ORWDX LOCK ORDER", "ORWDX SAVE", "ORWDX SEND", "ORWDX UNLOCK", "ORWDX UNLOCK ORDER", "ORWDX WRLST", "ORWDX1 DCREN", "ORWDX2 DCREASON", "ORWDXA DC", "ORWDXA ISACTOI", "ORWDXA OFCPLX", "ORWDXA VALID", "ORWDXC ON", "ORWDXC SESSION", "ORWDXM1 BLDQRSP", "ORWDXM2 CLRRCL", "ORWDXM3 ISUDQO", "ORWDXR ISCPLX", "ORWOR PKISITE", "ORWOR UNSIGN", "ORWOR VWGET", "ORWORB KILL EXPIR MED ALERT", "ORWORB KILL UNSIG ORDERS ALERT", "ORWORB KILL UNVER MEDS ALERT", "ORWORB KILL UNVER ORDERS ALERT", "ORWORDG IEN", "ORWORDG MAPSEQ", "ORWORR AGET", "ORWORR GET4LST", "ORWPCE GETSVC", "ORWPCE SCDIS", "ORWPS ACTIVE", "ORWPS REASON", "ORWPT CWAD", "ORWPT ENCTITL", "ORWPT INPLOC", "ORWPT SELECT", "ORWPT1 PRCARE", "ORWTPD1 GETEAFL", "ORWTPD1 GETEDATS", "ORWU DT", "ORWU NPHASKEY", "ORWU1 NEWLOC", "ORWUL FV4DG", "ORWUL FVSUB", "ORWUL QV4DG", "TIU TEMPLATE ACCESS LEVEL", "TIU TEMPLATE GETROOTS", "TIU TEMPLATE SET DEFAULTS"]

P3MEDOPORDERSetDISC = ["ORALWORD ALLWORD", "ORCDLR2 CHECK ALL LC TO WC", "ORDEA CSVALUE", "ORDEA DEATEXT", "ORDEA SIGINFO", "OREVNTX PAT", "OREVNTX1 GETSTS", "OREVNTX1 GTEVT", "OREVNTX1 ODPTEVID", "ORIMO IMOLOC", "ORIMO ISIVQO", "ORPRF CLEAR", "ORQQAL LIST", "ORQQPP LIST", "ORWCH LOADSIZ", "ORWCOM ORDEROBJ", "ORWDBA1 BASTATUS", "ORWDBA1 SCLST", "ORWDPS1 FAILDEA", "ORWDPS1 ODSLCT", "ORWDPS1 SCHALL", "ORWDPS2 CHKGRP", "ORWDPS2 MAXREF", "ORWDPS2 OISLCT", "ORWDPS2 QOGRP", "ORWDPS32 AUTH", "ORWDPS32 VALQTY", "ORWDPS32 VALROUTE", "ORWDPS32 VALSCH", "ORWDPS4 CPINFO", "ORWDPS4 IPOD4OP", "ORWDRA32 LOCTYPE", "ORWDX AGAIN", "ORWDX DGNM", "ORWDX DLGDEF", "ORWDX LOCK", "ORWDX LOCK ORDER", "ORWDX SAVE", "ORWDX SEND", "ORWDX UNLOCK", "ORWDX UNLOCK ORDER", "ORWDX WRLST", "ORWDX1 DCREN", "ORWDX1 PATWARD", "ORWDX2 DCREASON", "ORWDXA DC", "ORWDXA ISACTOI", "ORWDXA OFCPLX", "ORWDXA VALID", "ORWDXC ON", "ORWDXC SESSION", "ORWDXM1 BLDQRSP", "ORWDXM2 CLRRCL", "ORWDXM3 ISUDQO", "ORWDXR ISCPLX", "ORWDXR01 ISSPLY", "ORWOR PKISITE", "ORWOR UNSIGN", "ORWOR VWGET", "ORWORB KILL EXPIR MED ALERT", "ORWORB KILL UNSIG ORDERS ALERT", "ORWORB KILL UNVER MEDS ALERT", "ORWORB KILL UNVER ORDERS ALERT", "ORWORDG IEN", "ORWORDG MAPSEQ", "ORWORR AGET", "ORWORR GET4LST", "ORWORR GETBYIFN", "ORWPCE SCDIS", "ORWPS ACTIVE", "ORWPS DETAIL", "ORWPS MEDHIST", "ORWPT CWAD", "ORWPT INPLOC", "ORWPT SELECT", "ORWPT1 PRCARE", "ORWU DT", "ORWU NPHASKEY", "ORWU VALIDSIG", "ORWUL FV4DG", "ORWUL FVSUB", "ORWUL QV4DG"]

P3MEDOPORDERSetEDIT = ["OR GET COMBAT VET", "ORALWORD ALLWORD", "ORCDLR2 CHECK ALL LC TO WC", "ORDEA CSVALUE", "ORDEA DEATEXT", "ORDEA SIGINFO", "OREVNTX PAT", "OREVNTX1 GETSTS", "OREVNTX1 GTEVT", "OREVNTX1 ODPTEVID", "ORIMO IMOLOC", "ORIMO IMOOD", "ORIMO ISIVQO", "ORPRF CLEAR", "ORQQAL LIST", "ORQQCN SVC W/SYNONYMS", "ORQQPL INIT PT", "ORQQPL INIT USER", "ORQQPL PROB COMMENTS", "ORQQPL PROBLEM LIST", "ORQQPL USER PROB CATS", "ORQQPP LIST", "ORWCH LOADSIZ", "ORWCOM ORDEROBJ", "ORWDBA1 BASTATUS", "ORWDBA1 SCLST", "ORWDCN32 DEF", "ORWDPS1 FAILDEA", "ORWDPS1 ODSLCT", "ORWDPS1 SCHALL", "ORWDPS2 CHKGRP", "ORWDPS2 CHKPI", "ORWDPS2 DAY2QTY", "ORWDPS2 MAXREF", "ORWDPS2 OISLCT", "ORWDPS2 QOGRP", "ORWDPS32 AUTH", "ORWDPS32 VALQTY", "ORWDPS32 VALROUTE", "ORWDPS32 VALSCH", "ORWDPS4 CPINFO", "ORWDPS4 IPOD4OP", "ORWDPS5 LESGRP", "ORWDRA32 LOCTYPE", "ORWDX AGAIN", "ORWDX DGNM", "ORWDX DLGDEF", "ORWDX LOADRSP", "ORWDX LOCK", "ORWDX LOCK ORDER", "ORWDX SAVE", "ORWDX SEND", "ORWDX UNLOCK", "ORWDX UNLOCK ORDER", "ORWDX WRLST", "ORWDX1 PATWARD", "ORWDX1 STCHANGE", "ORWDXA ISACTOI", "ORWDXA OFCPLX", "ORWDXA VALID", "ORWDXC ON", "ORWDXC SESSION", "ORWDXM1 BLDQRSP", "ORWDXM2 CLRRCL", "ORWDXM3 ISUDQO", "ORWDXR GETPKG", "ORWDXR ISREL", "ORWDXR RNWFLDS", "ORWDXR01 CANCHG", "ORWDXR01 ISSPLY", "ORWOR PKISITE", "ORWOR UNSIGN", "ORWOR VWGET", "ORWORB KILL EXPIR MED ALERT", "ORWORB KILL UNSIG ORDERS ALERT", "ORWORB KILL UNVER MEDS ALERT", "ORWORB KILL UNVER ORDERS ALERT", "ORWORDG IEN", "ORWORDG MAPSEQ", "ORWORR AGET", "ORWORR GET4LST", "ORWORR GETBYIFN", "ORWPCE SCDIS", "ORWPS ACTIVE", "ORWPS DETAIL", "ORWPS MEDHIST", "ORWPT CWAD", "ORWPT INPLOC", "ORWPT SELECT", "ORWPT1 PRCARE", "ORWU DT", "ORWU NEWPERS", "ORWU NPHASKEY", "ORWU VALIDSIG", "ORWUL FV4DG", "ORWUL FVSUB", "ORWUL QV4DG"]

P3PCDSet = ["GMV ADD VM", "GMV DLL VERSION", "GMV GET CURRENT TIME", "GMV GET VITAL TYPE IEN", "GMV LATEST VM", "GMV MANAGER", "GMV PARAMETER", "GMV USER", "GMV VITALS/CAT/QUAL", "ORQQCN UNRESOLVED", "ORQQPL INIT USER", "ORQQPXRM REMINDER CATEGORIES", "ORQQPXRM REMINDERS UNEVALUATED", "ORQQVI NOTEVIT", "ORQQVI VITALS", "ORWCH LOADSIZ", "ORWCV VST", "ORWLEX GETFREQ", "ORWLEX GETI10DX", "ORWPCE ACTIVE PROV", "ORWPCE ACTPROB", "ORWPCE ALWAYS CHECKOUT", "ORWPCE ANYTIME", "ORWPCE ASKPCE", "ORWPCE AUTO VISIT TYPE SELECT", "ORWPCE CXNOSHOW", "ORWPCE DIAG", "ORWPCE GET DX TEXT", "ORWPCE GET EDUCATION TOPICS", "ORWPCE GET EXAM TYPE", "ORWPCE GET EXCLUDED", "ORWPCE GET HEALTH FACTORS TY", "ORWPCE GET IMMUNIZATION TYPE", "ORWPCE GET SET OF CODES", "ORWPCE GET SKIN TEST TYPE", "ORWPCE GETSVC", "ORWPCE HASCPT", "ORWPCE HASVISIT", "ORWPCE HF", "ORWPCE IMM", "ORWPCE MHCLINIC", "ORWPCE NOTEVSTR", "ORWPCE PCE4NOTE", "ORWPCE PED", "ORWPCE PROC", "ORWPCE SAVE", "ORWPCE SCDIS", "ORWPCE SCSEL", "ORWPCE SK", "ORWPCE VISIT", "ORWPCE XAM", "ORWPCE1 NONCOUNT", "ORWPT ENCTITL", "ORWTIU CHKTXT", "ORWTIU GET TIU CONTEXT", "ORWTPD1 GETEAFL", "ORWTPD1 GETEDATS", "ORWU DT", "ORWU EXTNAME", "ORWU NEWPERS", "ORWU PARAM", "ORWU PATCH", "ORWU VALIDSIG", "ORWU1 NEWLOC", "TIU AUTHORIZATION", "TIU CREATE RECORD", "TIU DOCUMENTS BY CONTEXT", "TIU GET DEFAULT PROVIDER", "TIU GET DOCUMENT PARAMETERS", "TIU GET PERSONAL PREFERENCES", "TIU GET PRINT NAME", "TIU GET RECORD TEXT", "TIU GET REQUEST", "TIU HAS AUTHOR SIGNED?", "TIU ID CAN ATTACH", "TIU ID CAN RECEIVE", "TIU IS THIS A CONSULT?", "TIU IS USER A PROVIDER?", "TIU ISPRF", "TIU LOAD BOILERPLATE TEXT", "TIU LOCK RECORD", "TIU LONG LIST OF TITLES", "TIU ONE VISIT NOTE?", "TIU PERSONAL TITLE LIST", "TIU REQUIRES COSIGNATURE", "TIU SET DOCUMENT TEXT", "TIU SIGN RECORD", "TIU TEMPLATE ACCESS LEVEL", "TIU TEMPLATE GETLINK", "TIU TEMPLATE GETROOTS", "TIU UNLOCK RECORD", "TIU UPDATE RECORD", "TIU WAS THIS SAVED?", "TIU WHICH SIGNATURE ACTION"]

# fixed from R1.3 (Oct/Nov 2015)
eHMPSet = ["GMV ADD VM", "GMV CLOSEST READING", "GMV MARK ERROR", "GMV V/M ALLDATA", "GMV VITALS/CAT/QUAL", "HMPCRPC RPC", "ORQOR DETAIL", "ORQQPL ADD SAVE", "ORQQPL DELETE", "ORQQPL EDIT SAVE", "ORQQPL4 LEX", "ORQQPX REMINDER DETAIL", "ORQQPX REMINDERS LIST", "ORWDAL32 ALLERGY MATCH", "ORWDAL32 CLINUSER", "ORWDAL32 SAVE ALLERGY", "ORWDAL32 SYMPTOMS", "ORWDPS1 DFLTSPLY", "ORWDPS2 DAY2QTY", "ORWDPS2 OISLCT", "ORWDX DLGDEF", "ORWDX LOADRSP", "ORWDX LOCK ORDER", "ORWDX SAVE", "ORWDX SEND", "ORWDX UNLOCK ORDER", "ORWDX2 DCREASON", "ORWDXA DC", "ORWDXA VALID", "ORWPCE GETSVC", "ORWPT CWAD", "ORWRP REPORT LISTS", "ORWRP REPORT TEXT", "ORWU NPHASKEY", "ORWU VALIDSIG", "ORWUL FV4DG", "ORWUL FVIDX", "ORWUL FVSUB", "TIU AUTHORIZATION", "TIU CREATE RECORD", "TIU LOCK RECORD", "TIU SIGN RECORD", "TIU UNLOCK RECORD", "TIU UPDATE RECORD", "TIU WHICH SIGNATURE ACTION"]

# Besides VPR - see issue: https://github.com/vistadataproject/nodeVISTA/issues/26
JLVSet = ["ORWPT ADMITLST", "ORWRP REPORT TEXT", "ORQQAL DETAIL", "ORQQPX REMINDER DETAIL", "ORWPT SELECT", "XWB GET VARIABLE VALUE", "ORWPT1 PRCARE", "ORWPT PTINQ", "ORWLRR INTERIM", "ORWPS DETAIL", "ORQQCN DETAIL", "ORQOR DETAIL", "ORQQPL DETAIL", "ORQQPL PROB COMMENTS"]


# SEE THE DUZ / SEE THE PARAMETER from methods ie/ see if there (may nix out of here?)
def enhanceAndFix():
    
    byName = json.load(open(RPCS_CATEGORIZED_JSON), object_pairs_hook=OrderedDict)
    methodByName = json.load(open(RPCS_METHODS))
        
    noSimple = 0
    
    ALLOFEM = set()
    
    changedIds = []
        
    for name in byName:
    
        # if tags change, so may division
        oldDivision = byName[name]["division"]
        reassignDivision(byName[name])
        newDivision = byName[name]["division"]
        if oldDivision != newDivision:
            oldId, newId = updateIdForDivisionChange(name, byName)
            changedIds.append((name, oldId, newId))
        
        if name not in methodByName:
            continue
            
        methodInfo = methodByName[name]
        
        # FIRST: parameters   
        if "lines" in methodInfo:       
            xparInfos = parseXPARsFromLines(methodInfo["lines"])
        else:
            xparInfos = None
            
        if xparInfos:
                        
            xparParameters = set((xparInfo["parameter"] if "parameter" in xparInfo else "*VARIABLE*") for xparInfo in xparInfos)

            # Want to allow for manual addition
            if "parameters" not in byName[name]:
                byName[name]["parameters"] = sorted(list(xparParameters))
            else:
                byName[name]["parameters"] = sorted(list(set(byName[name]["parameters"]) | xparParameters))   
                
            # Finally for non clinical (no DUZ) RPC: 
            # if "DUZ" not in tags and VA(200 in a PARAMETER then add DUZ 
            if (byName[name]["division"] == "NON CLINICAL") and "DUZ" not in byName[name]["tags"] and sum(1 for xparInfo in xparInfos if "VA200" in xparInfo):
                if "K/META" in byName[name]["tags"]:
                    byName[name]["tags"].remove("K/META") # can't have both
                byName[name]["tags"].append("DUZ")
                
        # Resync tag and parameters
        if "parameters" in byName[name]:
            # Ensure Tag
            if "tags" not in byName[name]:
                byName[name]["tags"] = ["PARAMETER"]
            elif "PARAMETER" not in byName[name]["tags"]:
                byName[name]["tags"].append("PARAMETER")
                
        # NEXT: files (not automatically adding 200 because DUZ as may just be for PARAMETER lookup
        if "lines" in methodInfo:       
            fileIds = parseFileIdsFromLines(methodInfo["lines"])
            #
            # Note: 200 problem - ^VA(200 for PARAMETERs with DUZ. Don't count as 
            # file work.
            #
            if fileIds and "parameters" in byName[name] and "200" in fileIds:
                fileIds.remove("200")
                if len(fileIds) == 0:
                    fileIds = None
        else: 
            fileIds = None

        if fileIds:
                    
            ALLOFEM |= set(fileIds)
                
            # Ensure Tag
            if "tags" not in byName[name]:
                byName[name]["tags"] = ["FILE"]
            elif "FILE" not in byName[name]["tags"]:
                byName[name]["tags"].append("FILE")
                
            if "files" not in byName[name]:
                byName[name]["files"] = sorted(fileIds)
            else:
                byName[name]["files"] = sorted(list(set(byName[name]["files"]) | set(fileIds)))         
                
        # resync files and FILE (may have "files" from before fileIds - hence separate)
        if "files" in byName[name]:
            # Ensure Tag
            if "tags" not in byName[name]:
                byName[name]["tags"] = ["FILE"]
            elif "FILE" not in byName[name]["tags"]:
                byName[name]["tags"].append("FILE")  
                
        for tag, lst in [("P1BPSEL", P1BPSELSet), ("P2PSEL", P2PSELSet), ("JLV", JLVSet), ("eHMP", eHMPSet), ("P3ALLERGIES", P3ALLERGIESSet), ("P3PROBLEMS", P3PROBLEMSSet), ("P3VITALS", P3VITALSSet), ("P3NVAORDERS", P3NVAORDERSet), ("P3MEDOPORDERS", P3MEDOPORDERSetDISC), ("P3MEDOPORDERS", P3MEDOPORDERSetEDIT), ("P3PCE", P3PCDSet)]:
            if name in lst:
                if "tags" not in byName[name]:
                    byName[name]["tags"] = []
                if tag not in byName[name]["tags"]:
                    byName[name]["tags"].append(tag)
                                            
        # simple categorizer
        tf = simpleCategorizer(methodInfo) 
        if tf:
            byName[name]["simple"] = True
            noSimple += 1
    
    json.dump(byName, open(RPCS_CATEGORIZED_JSON, "w"), indent=4)
    
    print "Changed Ids:"
    for ci in changedIds:
        print "\t", ci[0], ci[1], ci[2]
    print 
    
"""
To stop id's all getting moved up or down as an RPC is re-categorized, we fix the ids
and assign an RPC to a new category using a fresh id of that category.
"""
def updateIdForDivisionChange(name, byName):

    oldId = byName[name]["id"]
    newDivision = byName[name]["division"]
    
    if newDivision == "NON CLINICAL":
        if "FILE" in byName[name]["tags"] and "PARAMETER" in byName[name]["tags"]:
            idMN = "PF"
        elif "FILE" not in byName[name]["tags"] and "PARAMETER" in byName[name]["tags"]:
            idMN = "P"
        elif "FILE" in byName[name]["tags"] and "PARAMETER" not in byName[name]["tags"]:
            idMN = "F"
        else:
            idMN = "O"
    elif newDivision == "CLINICAL":
        idMN = "C"
    elif newDivision == "AUTHENTICATION":
        idMN = "A"
    else:
        idMN = "OS"
        
    nextIntId = sorted([int(re.sub(r'^[A-Z]+', "", byName[iname]["id"])) for iname in byName if re.match(idMN, byName[iname]["id"])])[-1] + 1
    nextId = idMN + str(nextIntId)
    oldId = byName[name]["id"] 
    byName[name]["id"] = nextId
    return oldId, nextId
        
"""
Basic division of C | NC | A | OUT OF SCOPE

KEY: moving away from K/META (ie/ removing it)
"""
def reassignDivision(rpcInfo):
    if "OUT OF SCOPE" in rpcInfo["tags"]:
        rpcInfo["division"] = "OUT OF SCOPE"
        return
    # If not OUT OF SCOPE and catag AUTHENTICATION
    if rpcInfo["catag"] == "AUTHENTICATION":
        rpcInfo["division"] = "AUTHENTICATION"
        return
    if "DFN" in rpcInfo["tags"] or "LOCK" in rpcInfo["tags"]:
        rpcInfo["division"] = "CLINICAL"
        if len(set(["DUZ", "K/META"]) & set(rpcInfo["tags"])):
            raise Exception("Corrupt tags - Clinical RPC " + rpcName + " has DUZ or K/META tag")
        return
    rpcInfo["division"] = "NON CLINICAL"
    if len(set(["DUZ", "K/META"]) & set(rpcInfo["tags"])) == 2:
        raise Exception("Can't have DUZ AND K/META together - one or other only " + rpcName)
                        
"""
MUST REDO as PARs no longer in METHODINFO ... 

TODO: add <VARIABLE> in parameters then not simple. If not parameters defined then indirection => not simple etc
ie/ get simple in there otherwise ie/ tag it ie/ do as tag

... and do report in dump on simples in prelude to redoing "K/GRAF" vs.
"""
def simpleCategorizer(methodInfo):
        if "args" in methodInfo and len(methodInfo["args"]) != 1:
            return False
        if not ("lines" in methodInfo and len(methodInfo["lines"]) < 5):
            return False
        if not ("XPARs" in methodInfo and len(methodInfo["XPARs"]) == 1):
            return False
        return True
        
"""
PARAMETER parsing

(bonus of VA(200)

A/C for:
- > 1 XPAR in a line
- expressions (with ('s) inside arguments
- no PARAMETER named explicitly (in variable)
- notes if VA(200 ie/ DUZ of some sort, is involved

Note: as methodInfo lines don't include comments then commented out XPARS
won't (correct!) be included.
"""
def parseXPARsFromLines(lines):
    txparInfos = []
    for line in lines:
        xparInfos = parseXPARsFromLine(line)
        if xparInfos:
            if txparInfos:
                yep = True
            txparInfos.extend(xparInfos)
    return txparInfos   

def parseXPARsFromLine(line):

    if not re.search(r'\^XPAR\(', line):
        return None
    
    # Pass 1: take out one or more XPARs and following string up to next XPAR if any
    xparPieces = re.split(r'([A-Z]+\^XPAR)', line)
    xparInfo = None
    xparInfos = []
    # Optional leading text before XPAR, then set of pairs of XPAR|ARGS
    for xparPiece in xparPieces:
        if not xparInfo and re.search(r'\^XPAR', xparPiece):
            xparInfo = {"type": xparPiece.split("^")[0]}
            continue
        if xparInfo:
            xparInfo["argsString"] = xparPiece
            xparInfos.append(xparInfo)
            xparInfo = None
        
    # Pass 2: parse arguments out of argsString    
    for i, xparInfo in enumerate(xparInfos, 1):
    
        # Take the args
        args = re.match(r'\(((?<=\().*(?=\)))\)', xparInfo["argsString"]).group(1).split(",")
        # Can go on too far - assume last arg always simple so split on first )
        if re.search(r'\)', args[-1]):
            larg = args.pop()
            args.append(larg.split(")")[0])
        xparInfo["args"] = args
        del xparInfo["argsString"]
        
        # Take out the PARAMETER
        candidateParameters = [arg[1:-1] for arg in args[1:] if re.match(r'"[A-Z\d\/\-]+ [A-Z\d\/\-]+[A-Z\d \/\-]*"$', arg)]
        if len(candidateParameters) > 1:
            raise Exception("Just one parameter should be in args " + json.dumps(args) + "--" + json.dumps(candidateParameters))
        # Can be a variable like PARAM or an expression like ("ORQQLR DATE RANGE "_RNG)
        # ... most are concrete.
        if len(candidateParameters) == 1:
            xparInfo["parameter"] = candidateParameters[0]
            
        # Note if VA(200 in there (vptr so may be DUZ_";VA(200" or another var name. VA(200 enough
        if re.search(r'VA\(200', args[0]):
            xparInfo["VA200"] = True
        
    return xparInfos
    
"""
File ids appear in direct global references in $O/$G/$D

Out of scope for now: new FileMan API calls
"""

# some file globals not offset but its # (seen so far!)
# ... will exception for globals not disallowed (TMP) or in this list
NONFILEID_GLOBALS = {
    "DIC": "1",
    "DPT": "2",
    "HOLIDAY": "40.5",
    "SC": "44",
    "DGPM": "405",
    "AUPNVSIT": "9000010",
    "AUPNPROB": "9000011",
    "AUTTLOC": "9999999.06",
    "AUTTEDT": "9999999.09",
    "AUTTIMM": "9999999.14",
    "AUTTEXAM": "9999999.15",
    "AUTTTRT": "9999999.17",
    "AUTNPOV": "9999999.27",
    "AUTTSK": "9999999.28",
    "AUTTHF": "9999999.64"
}

def parseFileIdsFromLines(lines):
    fileIds = set()
    for line in lines:
        fileIds |= parseFileIdsFromLine(line)
    if not len(fileIds):
        return None
    return list(fileIds)    

def parseFileIdsFromLine(line):
    fileIds = set()
    # Assume $[O|G|D]
    for s in re.findall("\$[ODG]\(\^([A-Z\d]+\([\d\.]*)", line):
        if re.search(r'(TMP|UTILITY)', s.split("(")[0]):
            continue
        if s.split("(")[1] == "":
            gl = s.split("(")[0]
            if gl in NONFILEID_GLOBALS:
                fileIds.add(NONFILEID_GLOBALS[gl])
            # often lookup XUSEC index - DISV is not in top of nodeVISTA
            # XMB seems to be index too?
            elif gl not in ["XUSEC", "DISV", "XMB"]: 
                raise Exception("Parsed a pure GLOBAL name not accounted for: " + gl)
        else:
            fileIds.add(s.split("(")[1])
    return fileIds
            
# ############################## Driver #######################
                    
def main():
        
    enhanceAndFix()
    
if __name__ == "__main__":
    main()
