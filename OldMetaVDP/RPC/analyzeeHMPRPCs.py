import json
import os
import sys
import re

"""
HMP RPCs (Jan 2016)

Note: in CPRS package as processing in terms of CPRS covered/used RPCs

"ehmp does have its own set of RPCs. Many of these were introduced by the original hmp team in salt lake but have since been modified to support the enterprise effort. I think most of the ehmp RPCs have to do with syncing operational and patient meta data. These RPCS are part of the HMP SYNCHRONIZATION CONTEXT.  There have also been lots of KIDS packages introduced that support the vx-sync system as well (like write back triggers, etc)."

From: VACORE-eHMPRPCs-180316-1130-142.pdf

Pts:
  - On production sites, users must be configured to have access to the HMP contexts:
    - HMP SYNCHRONIZATION CONTEXT is added as a secondary menu option to the proxy user
    - HMP UI CONTEXT is added as a secondary menu option for any user which logs into eHMP.
  - The default RDK context is HMP UI CONTEXT.
  - ... In general the writeback resources use the current user in the default RDK context, whereas the pick-list resources use the RDK proxy user.

Complete Remote Procedure Call (RPC) List for HMP UI CONTEXT Option
List updated 7 January 2016.
Option NAME: HMP UI CONTEXT MENU TEXT: HMP UI CONTEXT version 20160107-01.US12124
"""
# NOTE MAY BE MORE - HMP PATIENT ACTIVITY ...
HMPRPCS = [
    "GMV ADD VM", 
    "GMV GET CURRENT TIME", 
    "GMV MARK ERROR", 
    "GMV VITALS/CAT/QUAL", 
    "HMP APPOINTMENTS", 
    "HMP CHKXTMP", 
    "HMP DATA VERSION", 
    "HMP DEFAULT PATIENT", 
    "HMP DELETE OBJECT", 
    "HMP DELETE ROSTER", 
    "HMP DELETE TIU NOTE", 
    "HMP GET OBJECT", 
    "HMP GET PATIENT DATA", 
    "HMP GET PATIENT DATA JSON", 
    "HMP GET ROSTER LIST", 
    "HMP GET SOURCE", 
    "HMP GLOBAL SIZE", 
    "HMP INPATIENTS", 
    "HMP LOCAL GETCORRESPONDINGIDS", 
    "HMP MED ORDER CHECKS", 
    "HMP PATIENT ADMIT SYNC", 
    "HMP PATIENT SCHED SYNC", 
    "HMP PATIENT SELECT", 
    "HMP PREVIEW ROSTER", 
    "HMP PUT DEMOGRAPHICS", 
    "HMP PUT OBJECT", 
    "HMP PUT OPERATION DATA", 
    "HMP PUT PATIENT DATA", 
    "HMP ROSTER PATIENTS", 
    "HMP ROSTERS", 
    "HMP SAVE NOTE STUB", 
    "HMP SUBSCRIBE", 
    "HMP TIU LONG LIST OF TITLES", 
    "HMP UPDATE ROSTER", 
    "HMP WRITEBACK ALLERGY", 
    "HMP WRITEBACK ALLERGY EIE", 
    "HMP WRITEBACK ENCOUNTERS", 
    "HMP WRITEBACK IMMUNIZATION", 
    "HMP WRITEBACK LAB ORDERS", 
    "HMP WRITEBACK MED SAVE ORDER", 
    "HMP WRITEBACK PROBLEM", 
    "HMP WRITEBACK SIGN ORDERS", 
    "HMP WRITEBACK SIGN TIU NOTE", 
    "HMP WRITEBACK TIU NOTE COMMIT", 
    "HMP WRITEBACK TIU NOTE SAVE", 
    "HMP WRITEBACK VITAL", 
    "HMP WRITEBACK VITAL EIE", 
    "HMPCORD RPC", 
    "HMPCPAT RPC", 
    "HMPCPRS RPC", 
    "HMPCRPC RPC", 
    "HMPCRPC RPCCHAIN", 
    "HMPFPTC CHKS", 
    "HMPFPTC LOG", 
    "ORCNOTE GET TOTAL", 
    "ORQOR DETAIL", 
    "ORQPT CLINIC PATIENTS", 
    "ORQPT DEFAULT PATIENT LIST", 
    "ORQPT PROVIDER PATIENTS", 
    "ORQPT SPECIALTIES", 
    "ORQPT SPECIALTY PATIENTS", 
    "ORQPT WARD PATIENTS", 
    "ORQPT WARDS", 
    "ORQQPL ADD SAVE", 
    "ORQQPL DELETE", 
    "ORQQPL EDIT SAVE", 
    "ORQQPL USER PROB LIST", 
    "ORQQPL4 LEX", 
    "ORQQPX REMINDER DETAIL", 
    "ORQQPX REMINDERS LIST", 
    "ORQQVI NOTEVIT", 
    "ORWCV VST", 
    "ORWDAL32 ALLERGY MATCH", 
    "ORWDAL32 CLINUSER", 
    "ORWDAL32 SAVE ALLERGY", 
    "ORWDAL32 SYMPTOMS", 
    "ORWLEX GETFREQ", 
    "ORWLEX GETI10DX", 
    "ORWLR CUMULATIVE REPORT", 
    "ORWLRR INTERIM", 
    "ORWPCE GETSVC", 
    "ORWPCE HASVISIT", 
    "ORWPCE LEX", 
    "ORWPCE NOTEVSTR", 
    "ORWPCE PCE4NOTE", 
    "ORWPCE SAVE", 
    "ORWPCE SCSEL", 
    "ORWPT ADMITLST", 
    "ORWPT APPTLST", 
    "ORWPT BYWARD", 
    "ORWPT LIST ALL", 
    "ORWRP COLUMN HEADERS", 
    "ORWRP REPORT LISTS", 
    "ORWRP REPORT TEXT", 
    "ORWRP3 EXPAND COLUMNS", 
    "ORWU CLINLOC", 
    "ORWU DT", 
    "ORWU EXTNAME", 
    "ORWU NEWPERS", 
    "ORWU USERINFO", 
    "ORWU VALIDSIG", 
    "PX SAVE DATA", 
    "PXVIMM ADMIN ROUTE", 
    "PXVIMM ADMIN SITE", 
    "PXVIMM IMM LOT", 
    "PXVIMM IMM MAN", 
    "PXVIMM IMMDATA", 
    "PXVIMM INFO SOURCE", 
    "PXVIMM VIS", 
    "TIU AUTHORIZATION", 
    "TIU CREATE ADDENDUM RECORD", 
    "TIU CREATE RECORD", 
    "TIU DELETE RECORD", 
    "TIU DOCUMENTS BY CONTEXT", 
    "TIU GET DOCUMENT TITLE", 
    "TIU GET RECORD TEXT", 
    "TIU GET REQUEST", 
    "TIU IS THIS A CONSULT?", # manually added ? 
    "TIU IS THIS A SURGERY?", # manually added ?
    "TIU ISPRF", 
    "TIU LOCK RECORD", 
    "TIU LONG LIST OF TITLES", 
    "TIU REQUIRES COSIGNATURE", 
    "TIU SET DOCUMENT TEXT", 
    "TIU SIGN RECORD", 
    "TIU UNLOCK RECORD", 
    "TIU UPDATE RECORD", 
    "VAFC LOCAL GETCORRESPONDINGIDS", 
    "XHD GET PARAMETER DEF LIST", 
    "YTQ ALLKEYS"
]

def checkAgainstNodeVISTA8994(defnsById):
    """
    # HMP RPCs 130
    # in 8994 of nodeVISTA 73
    # not in 8994, labeled HMP 50
    # not in 8994, not labeled HMP 7
	... note PXVIMM (Immunization) which we know we're missing and need (in clones?)
	1 PXVIMM ADMIN SITE
	2 PXVIMM INFO SOURCE
	3 PXVIMM IMMDATA
	4 PXVIMM VIS
	5 PXVIMM IMM MAN
	6 PXVIMM ADMIN ROUTE
	7 PXVIMM IMM LOT
    ie/ all extras are HMP specials besides the PXVIMM's

    HMP RPCs that are copies of others (VPR and one TIU) 5
    set(['DATA VERSION', 'TIU LONG LIST OF TITLES', 'GET PATIENT DATA JSON', 'GET PATIENT DATA', 'LOCAL GETCORRESPONDINGIDS'])
    """
    print
    
    print "# HMP RPCs", len(HMPRPCS)

    print "# in 8994 of nodeVISTA", sum(1 for rpc in HMPRPCS if rpc in defnsById)

    print "# not in 8994, labeled HMP", sum(1 for rpc in HMPRPCS if rpc not in defnsById and re.match(r'HMP', rpc))

    notHMPNot8994 = set(rpc for rpc in HMPRPCS if rpc not in defnsById and not re.match(r'HMP', rpc))
    print "# not in 8994, not labeled HMP", len(notHMPNot8994)
    if sum(1 for rpc in notHMPNot8994 if not re.match(r'PXV', rpc)):
        raise Exception("8994 missing PXVIMM - know that - and missing HMP but should have all others")
    print "\t", "... note PXVIMM (Immunization) which we know we're missing and need (in clones?)"
    for i, rpc in enumerate(notHMPNot8994, 1):
        print "\t", i, rpc
    print "ie/ all extras are HMP specials besides the PXVIMM's"

    print
    # HMP Copies!
    hmpRPCsLessHMP = set(re.sub(r'HMP ', '', rpc) for rpc in HMPRPCS if re.match(r'HMP', rpc))
    hmpCopyRPCs = hmpRPCsLessHMP & set(re.sub(r'^[A-Z\d]+ ', '', rpc) for rpc in defnsById)
    print "HMP RPCs that are copies of others (VPR and one TIU)", len(hmpCopyRPCs)
    print hmpCopyRPCs
    print
    
def main():

    d8994 = json.load(open("../nodeVISTA/8994.jsonld"))
    defnsById = dict((defn["name-8994"], defn) for defn in d8994["@graph"])
    checkAgainstNodeVISTA8994(defnsById)

if __name__ == "__main__":
    main()