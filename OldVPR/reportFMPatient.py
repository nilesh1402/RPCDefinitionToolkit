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
TODO: see final 2 wk list including:
... focus on Reduction/Report pattern split and stick to honing report
as much as can BEFORE doing new reduce. REM: VPR is a Bonus off this. Must stand alone.

<----- add in to reduce from prodclone ... [PTER] ... keep range is < certain amount

... will move Reduction to general typer; reporter off to be standard type report (in Reporters)

NOTE: off reframed patient and not just Data (v2) patient
"""

# Follows REDUCE/REPORT split pattern
FMREDUCTIONTEMPL = "/data/vista/{}/DataReductions/"
LAST_EIGHTEEN_MONTHS_START = datetime(2017, 1, 1, 0, 0, 0) # start 2017

# TODO: MOVE TO TYPE DEFN
class RecordPropertyTyper:

    def __init__(self):
        self.__propDefns = {}

    def propDefns(self):
    
        def __cleanPropDefns():
            pass
    
        return self.__propDefns

    """
    Add properties of a record to definitions. 
    
    Supports many defns per property:
    - classic cases of ENUM style value
    occuring a few times in what is a string or a date-time being sometimes
    a date and sometimes a date-time
    - if > 1 type, will resolve at end ie/ not an enum if totals don't add up
    """
    def addRecordProperties(self, record):
    
        def lookupPropDefnByType(prop, typ):
            if prop not in self.__propDefns:
                self.__propDefns[prop] = []
            else:
                for onePropDefn in self.__propDefns[prop]:
                    if onePropDefn["type"] == typ:
                        return onePropDefn
            onePropDefn = {"type": typ, "details": defaultdict(int)} if typ not in ["STRING", "NUMERIC", "RECORD"] else {"type": typ, "count": 0}
            self.__propDefns[prop].append(onePropDefn) 
            return onePropDefn
    
        PTERKEYS = set(["id", "label"])
        DTKEYS = set(["value", "type"])
        for prop in record:
            if prop in ["_id", "id", "type", "label"]:
                continue
            if isinstance(record[prop], list):
                onePropDefn = lookupPropDefnByType(prop, "MULTIPLE")
                onePropDefn["details"][len(record[prop])] += 1
                continue
            if isinstance(record[prop], dict):
                if set(record[prop].keys()) == PTERKEYS:
                    onePropDefn = lookupPropDefnByType(prop, "POINTER")
                    onePropDefn["details"][record[prop]["id"].split("-")[0]] += 1
                elif set(record[prop].keys()) == DTKEYS:
                    onePropDefn = lookupPropDefnByType(prop, "DATE-TIME")
                    if record[prop]["value"].split("T")[0] == record[prop]:
                        onePropDefn["details"]["DATE"] += 1
                    else:
                        onePropDefn["details"]["DATE-TIME"] += 1
                else:
                    onePropDefn = lookupPropDefnByType(prop, "RECORD")
                    onePropDefn["count"] += 1
                continue
            if isinstance(record[prop], bool):
                onePropDefn = lookupPropDefnByType(prop, "BOOLEAN")
                onePropDefn["details"][record[prop]] += 1
                continue
            if isinstance(record[prop], basestring) and re.match(r'[A-Z\d]+:[A-Z\d\- ]+', record[prop]):
                onePropDefn = lookupPropDefnByType(prop, "ENUM")
                onePropDefn["details"][record[prop]] += 1
                continue                
            if isinstance(record[prop], int):
                onePropDefn = lookupPropDefnByType(prop, "NUMERIC")
                onePropDefn["count"] += 1
                continue
            onePropDefn = lookupPropDefnByType(prop, "STRING")
            onePropDefn["count"] += 1
    
"""
Report that goes with Patient (type) reduction

TODO: make for all types ie/ refine to be generic (some specials will still work like break by pter based type-391 once TYPE reducer supports that ala ProdClones)
"""
def reportPatient2(stationNo, replyTempl, title):
       
    def reducePatient(patientReductionFile): 
        _20PatientIENS = set(pinfo[1] for pinfo in PATIENTS)
        fmqlReplyStore = FMQLReplyStore(replyTempl.format(stationNo))
        iter = fmqlReplyStore.iterator() # onlyTypes=["2"]
        print replyTempl.format(stationNo)
        countPatient = 0
        topProps = RecordPropertyTyper()
        last18MonthTopProps = RecordPropertyTyper()
        _20TopProps = RecordPropertyTyper()
        now = datetime.now()
        for reply in iter.next():
            if isinstance(reply, list):
                results = reply
            else:
                results = reply["results"]  
            for result in results:
                countPatient += 1
                if (countPatient % 10000) == 0:
                    print "Examined 10K more {}'s".format(2)
                    sys.stdout.flush()
                topProps.addRecordProperties(result)
                if result["_id"].split("-")[1] in _20PatientIENS:
                    _20TopProps.addRecordProperties(result)
                if "date_entered_into_file" in result:
                    # allow for bad date time
                    try:
                        createdTime = datetime.strptime(result["date_entered_into_file"]["value"], "%Y-%m-%d")
                    except: # template for bad date in general and date typing
                        pass
                    else:
                        if createdTime > LAST_EIGHTEEN_MONTHS_START: 
                            last18MonthTopProps.addRecordProperties(result)
        print "Total patient seen {}".format(countPatient)
        reduction = {"all": topProps.propDefns(), "_20": _20TopProps.propDefns(), "last18Count": last18MonthTopProps.propDefns()}
        json.dump(reduction, open(patientReductionFile, "w"))
        return reduction
                
    fmReductionDir = FMREDUCTIONTEMPL.format(stationNo)
    if not os.path.isdir(fmReductionDir):
        os.mkdir(fmReductionDir)
    patientReductionFile = fmReductionDir + "patient2Prop{}.json".format(title)
    if not os.path.isfile(patientReductionFile):
        reduction = reducePatient(patientReductionFile)
    else:
        reduction = json.load(open(patientReductionFile))    
        
    def muReport(title, propDefns):
        
        mu = "## {}\n\n".format(title)
        
        if len(propDefns) == 0:
            mu += "----- No Definitions ----\n\n"
            return mu
        
        def countProp(onePropDefns):
            cnt = 0
            for onePropDefn in onePropDefns:
                if "details" in onePropDefn:
                    cnt += sum(b for a, b in onePropDefn["details"].iteritems())
                    continue
                cnt += onePropDefn["count"]
            return cnt
        propCounts = dict((prop, countProp(propDefns[prop])) for prop in propDefns)
        
        # Mandatory == max count for a prop ie/ assume record have at least one
        totalCount = max(propCounts[prop] for prop in propCounts)
        multiples = {}
        records = {}
        
        mu += "Total: {}\n\n".format(totalCount)    

        mu += "\# | Property | Count | Type(s) | Details\n"
        mu += "--- | --- | --- | --- | ---\n"
        thress = [[False, 100.0, False], [False, 95.0, False], [False, 90.0, False], [False, 80.0, False], [False, 50.0, False], [False, 10.0, False], [False, 1.0, False]]
        for i, prop in enumerate(sorted(propCounts.keys(), key=lambda x: propCounts[x], reverse=True), 1):
            perc = float(propCounts[prop])/float(totalCount) * 100
            # grab Multiples
            if propDefns[prop][0]["type"] == "MULTIPLE":
                multiples[prop] = perc
            elif propDefns[prop][0]["type"] == "RECORD":
                records[prop] = perc
            for thresDefn in thress:
                if not thresDefn[2]:
                    if perc < thresDefn[1]:
                        thresDefn[2] = True
                        # % markup
                        mu += "*** | *** | __{}%__ | *** | ***\n".format(str(thresDefn[1]).split(".")[0])
                        break
            propTypeMU = propDefns[prop][0]["type"] if len(propDefns[prop]) == 1 else ", ".join([opd["type"] for opd in propDefns[prop]])
            detailsMUs = []
            for opd in propDefns[prop]:
                if "details" not in opd:
                    continue
                bs = []
                for a, b in opd["details"].iteritems():
                    detailsMUs.append("{} ({})".format(a, b))
                    bs.append(b)
                maxb = max(bs)
                minb = min(bs)
            if len(detailsMUs) == 0:
                detailsMU = "&nbsp;"
            elif len(detailsMUs) < 10:
                detailsMU = ", ".join(detailsMUs)
            else:
                detailsMU = "MANY DETAILS - {} ({} to {})".format(len(detailsMUs), minb, maxb) 
            # Bold the Mandatories 
            propMU = "__{}__".format(prop) if propCounts[prop] == totalCount else prop   
            mu += "{} | {} | {} ({:.2f}%) | {} | {}\n".format(i, propMU, propCounts[prop], perc, propTypeMU, detailsMU)
        mu += "\n"
        
        for multitype in [("Multiples", multiples), ("Records", records)]:
            mu += "### {} (Isolated)\n\n".format(multitype[0])
            mu += "\# | Property | Counts\n--- | --- | ---\n"
            for i, prop in enumerate(sorted(multitype[1], key=lambda p: multitype[1][p], reverse=True), 1):
                mu += "{} | {} | {:.2f}%\n".format(i, prop, multitype[1][prop])
            mu += "\n"
        
        return mu
    
    mu = "Summary Property #'s: All ({}), 20 ({}), Last 18 ({})\n\n".format(len(reduction["all"]), len(reduction["_20"]), len(reduction["last18Count"]))
    mu += "... TO ADD: show retirement of properties (all to 18) and move up or down in popularity of main ones\n\n"
    mu += muReport("Last 18 Months", reduction["last18Count"])
    mu += muReport("Total", reduction["all"])
    mu += muReport("20 Selection", reduction["_20"])
    print mu
    
    open("reportFM{}.md".format(title), "w").write(mu)
    
# ############################# Driver ####################################

def main():

    stationNumber = "442"
        
    # title = "Data"
    # REPLY_TEMPL = "/data/vista/{}/Data/"
    # reportPatient2(stationNumber, REPLY_TEMPL, "Data")
    
    title = "DataReframe"
    REPLY_TEMPL = "/data/vista/{}/DataReframe/"
    reportPatient2(stationNumber, REPLY_TEMPL, "DataReframe")
    
if __name__ == "__main__":
    main()
