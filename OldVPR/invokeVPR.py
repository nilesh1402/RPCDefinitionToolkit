#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import re 
import sys
import json
import shutil
from datetime import datetime
from collections import OrderedDict, defaultdict
import logging
from logging.handlers import RotatingFileHandler
from logging import handlers

from fmqlutils.fmqlIF.brokerRPC import VistARPCConnection, RPCLogger
from fmqlutils.rpcRunner.vprUtils import VPRXMLToJSON

"""
NOTE: follows HOWTO from fmqlutils

Notes:
  * User (FMQL,USER being reused) must have access to "VPR APPLICATION PROXY" secondary menu option

From VPRD.m (https://code.osehra.org/vivian/files/dox/Routine_VPRD_source.html)

- ALL is set for TYPE is TYPE isn't specified. Can pass > 1 type, ";" separated.
  - note: of the 27 types, only 20 are in ALL list explicitly
- synonyms are allowed so "allerg" is mapped to "reactions" etc
- opening is always: "<results version='"_$$GET^XPAR("ALL","VPR VERSION")_"' timeZone='"_$$TZ^XLFDT_"' >"
- with type specific tag inside: <D ADD("<"_VPRTAG)
- other arguments like START/STOP/MAX/ID are passed into individual handlers

TO FILL IN:
- files
- any besides Reminder not from FM?
- panel vs lab? etc

\# | type | synonyms | not in ALL | Files | Comment
--- | --- | --- | --- 
1 | accessions | &nbsp; | NO 
2 | appointments | &nbsp; |
3 | clinicalProcedures | &nbsp; | NO
4 | consults | &nbsp; |
5 | demographics | patient | 
6 | documents | &nbsp; |
7 | educationTopics | &nbsp; |
8 | exams | &nbsp; |
9 | flags | &nbsp; |
10 | functionalMeasurements | function, fim | NO
11 | healthFactors | factor |
12 | immunizations | &nbsp; |
13 | insurancePolicies | insur, polic | 
14 | labs | &nbsp; |
15 | meds | med, pharm | 
16 | observations | &nbsp; |
17 | orders | &nbsp; | NO
18 | panels | &nbsp; | NO
19 | problems | &nbsp; |
20 | procedures | &nbsp; |
21 | radiologyExams | rad, xray | NO
22 | reactions | allerg | 
23 | reminders | &nbsp; | &nbsp; | - | NOT from FM
24 | skinTests | &nbsp; |
25 | surgeries | &nbsp; | NO
26 | visits | &nbsp; |
27 | vitals | &nbsp; |

Note: 
- code-parsing VPR Model/Report is missing 3 (clinicalProcedures), 7 (educationTopics), 8 (exams), 10 (functionalMeasurements). But there is "item" which embeds func, skin, exam, educa. (need to rerun)
- will be comparing this data against the model
"""

PATIENT_TEMPLATE_DIR = "/data/vista/{}/PatientSlices/"
VPR_TEMPLATE_DIR = PATIENT_TEMPLATE_DIR + "VPR/" # will store in per patient subdirectories

TYPES = ["accessions", "appointments", "clinicalProcedures", "consults", "demographics", "documents", "educationTopics", "exams", "flags", "functionalMeasurements", "healthFactors", "immunizations", "insurancePolicies", "labs", "meds", "observations", "orders", "panels", "problems", "procedures", "radiologyExams", "reactions", "reminders", "skinTests", "surgeries", "visits", "vitals"] # 27 in all

PATIENTS = [
    ("FOGG,PHIL LEE", "7218976"),
    ("SPAHN,WILEY LEE", "13596"),
    ("MEURER,NED SCOTT", "41207"),
    ("TABATT,VANCE HOWARD", "35385"),
    ("RYON,THURMAN BRUCE", "37791"),
    ("NAVARO,FORREST CHARLES", "17287"),
    ("HODEL,REUBEN JOE", "34518"),
    ("LEIGLAND,VANCE LEE", "26583"),
    ("WASP,QUENTIN LEE", "23841"),
    ("STERNBERG,DEWAYNE LYNN", "38599"),
    ("KIMPTON,VANCE EUGENE", "7181659"),
    ("KRISTENSEN,ASHLEY BRUCE", "7175228"),
    ("GOLDBLATT,VANCE PAUL", "41274"),
    ("OSMUNDSON,RIGOBERTO JAMES", "22650"),
    ("BADIE,LORENE KATHLEEN", "31694"),
    ("MCGRANT,COLIN RAYMOND", "33750"),
    ("PAV,ASHLEY CHARLES", "7181732"),
    ("BESCHORNER,HILLARY ANN", "33472"),
    ("TROUPE,BLAINE PAYSON", "14953"),
    ("DEAQUINO,STERLING DUANE", "28598")
]

"""
In most cases: 
    <results version='1.05' timezone='-0500'>
        <{DATATYPE} total='#'> 
        
even 'patient' (whose type is 'demographics') has ='1'. Vitals has measurements that group
measurement.
"""
def processReply(reply):
    pass

STATION_NO = "442"
HOSTDIRECT = "10.64.182.19"
PORTDIRECT = 9922 
ACCESS = "QLFM1234" # of FMQL USER
VERIFY = "QLFM1234!!"

def main():

    # Ensure Directory Exists
    patientDir = PATIENT_TEMPLATE_DIR.format(STATION_NO)
    if not os.path.isdir(patientDir):
        os.mkdir(patientDir)
    vprDir = VPR_TEMPLATE_DIR.format(STATION_NO)
    if not os.path.isdir(vprDir):
        os.mkdir(vprDir)

    print
    connection = VistARPCConnection(HOSTDIRECT, PORTDIRECT, ACCESS, VERIFY, "VPR APPLICATION PROXY", RPCLogger())
    print "connected ..."
    print
    
    for patientName, patientIEN in PATIENTS:
        print
        print "VPRing Patient: {} ({})".format(patientName, patientIEN)
        print
        patientDir = vprDir + patientIEN + "/"
        if not os.path.isdir(patientDir):
            os.mkdir(patientDir)
        patientXMLDir = patientDir + "XML/"
        if not os.path.isdir(patientXMLDir):
            os.mkdir(patientXMLDir)
        for dataType in TYPES:
            replyFile = patientXMLDir + dataType + ".xml"
            if os.path.isfile(replyFile):
                print "\tskipping {} as reply already cached".format(dataType)
                continue 
            print "\tretrieving {} ...".format(dataType)
            reply = connection.invokeRPC("VPR GET PATIENT DATA", [patientIEN, dataType])
            open(replyFile, "w").write(reply)
            print "\twrote {}".format(dataType)    
            # TODO ADD: VPRXMLToJSON ... jsnData = tj.transform(replyFile, patientIEN, dataType)
        print
    
if __name__ == "__main__":
    main()
