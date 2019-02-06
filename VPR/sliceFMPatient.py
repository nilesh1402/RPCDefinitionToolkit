#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import re 
import json
from datetime import datetime
from collections import defaultdict, OrderedDict
from fmqlutils.cacher.cacherUtils import FMQLReplyStore

from invokeVPR import PATIENTS, STATION_NO

"""
Slide out (into Zips) the complete record of a Patient

Focus on ones known (will cache further - for gaps when get to them)

Note: WILL do [a] basic grouper transform AND [b] add in sameAs support too. For sameAs, 
replacing locals with nationals/standard urns => can also quantify intrinsically
local ids.
"""

FMPATIENTDIRTEMPL = "/data/vista/{}/PatientSlices/FM/"

def slicePatient2(fmqlReplyStore, stationNo, patientIENs):
    print "Slicing PATIENT (2) for {} patients".format(len(patientIENs))
    fmPatientDir = FMPATIENTDIRTEMPL.format(stationNo)
    if not os.path.isdir(fmPatientDir):
        os.mkdir(fmPatientDir)
    iter = fmqlReplyStore.iterator(onlyTypes=["2"])
    cnt = 0
    patientCnt = 0
    for reply in iter.next():
        for result in reply["results"]:
            cnt += 1
            if (cnt % 10000) == 0:
                print "Examined 10K more {}'s".format(2)
                sys.stdout.flush()
            patientIEN = result["_id"].split("-")[1]
            if patientIEN in patientIENs:
                print "Taking record of {}".format(patientIEN)
                sys.stdout.flush()
                patientDir = fmPatientDir + patientIEN + "/" 
                if not os.path.isdir(patientDir):
                    os.mkdir(patientDir)
                patientCnt += 1
                json.dump([result], open(patientDir + "2.json", "w"), indent=4) # will keep order as OrderDict is form
        if patientCnt == len(patientIENs):
            break # have em all
    print "... Patient (2) slice complete - {} from {} seen out of {} wanted".format(patientCnt, cnt, len(patientIENs)) 
    sys.stdout.flush()
    
def sliceVAMData(fmqlReplyStore, stationNo, patientIENs):
    fmPatientDir = FMPATIENTDIRTEMPL.format(stationNo)
    # Note: leaving Problem List Audit (125_8) as doesn't ref patient/refs problem!
    for typId, patientProp in [("120_8", "patient"), ("120_85", "patient"), ("120_86", "name"), ("9000011", "patient_name"), ("120_5", "patient")]:
        print "Processing for type {}".format(typId)
        perPatientResults = defaultdict(list)
        iter = fmqlReplyStore.iterator(onlyTypes=[typId])
        cnt = 0
        for reply in iter.next():
            for result in reply["results"]:
                cnt += 1
                if (cnt % 1000) == 0:
                    print "\tExamined 1K more {}'s".format(typId)
                    sys.stdout.flush()
                if patientProp not in result:
                    continue
                patientIEN = result[patientProp]["id"].split("-")[1]
                if patientIEN in patientIENs:
                    print "\tTaking record of {}".format(patientIEN)
                    sys.stdout.flush()
                    perPatientResults[patientIEN].append(result)
        for patientIEN in perPatientResults:
            patientDir = fmPatientDir + patientIEN + "/" 
            json.dump(perPatientResults[patientIEN], open(patientDir + "{}.json".format(typId), "w"), indent=4) # will keep order as OrderDict is form
        print "\t... Type {} slice complete - {} processed, {} taken for {} patients".format(typId, cnt, sum(len(perPatientResults[ien]) for ien in perPatientResults), len(perPatientResults)) 
        sys.stdout.flush()
    print "... all types complete"
    
# ############################# Driver ####################################

def main():
 
    stationNumber = "442"

    replyLocation = "/data/vista/{}/Data/".format(stationNumber)
    fmqlReplyStore = FMQLReplyStore(replyLocation)
    patientIENs = set([patientIEN for patientName, patientIEN in PATIENTS])
    
    # Type by type
    # slicePatient2(fmqlReplyStore, stationNumber, patientIENs)
    sliceVAMData(fmqlReplyStore, stationNumber, patientIENs)
    
if __name__ == "__main__":
    main()