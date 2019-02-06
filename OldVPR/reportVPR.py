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

from invokeVPR import VPR_TEMPLATE_DIR, TYPES, PATIENTS, STATION_NO

"""
TODO (full FM to/compare to VPR report):
- help fill in Map Template, type by type until ALL VPR covered
- cache extra P and M data as needed
- normalize both and location group FM if helps ie/ to get to "auto transform"
  ... group in **repo and others too
"""
class VPRModelFromData:

    def __init__(self):
        self.__cntRecordsByType = defaultdict(int)
        self.__classes = defaultdict(lambda: defaultdict(int))
        self.__typeProperties = defaultdict(lambda: defaultdict(int))
        self.__topPropsByType = defaultdict(lambda: defaultdict(int))

    def process(self, results):
        if len(results) == 0:
            return
        self.__type = results[0]["type"]
        for record in results:
            self.__cntRecordsByType[self.__type] += 1
            self.__processRecord(record)
        
    def __processRecord(self, record, parentProp=""):
    
        def typProp(qprop, value):
            return # problem - won't work for sctc which is longer #
            if not isinstance(value, basestring):
                return
            if re.match(r'[23]\d{6}\.?\d*$', value): # just day or day and time
                self.__typeProperties[self.__type + ":" + qprop]["DATE"] += 1
                if qprop == "provider/taxonomyCode":
                    print value
            elif self.__type + ":" + qprop in self.__typeProperties:
                print value
                print qprop
                print self.__typeProperties[self.__type + ":" + qprop]
                print x
    
        for prop in record:
            if not parentProp:
                self.__topPropsByType[self.__type][prop] += 1
            qprop = prop if not parentProp else parentProp + "/" + prop
            self.__classes[self.__type][qprop] += 1
            typProp(qprop, record[prop])
            if isinstance(record[prop], dict):
                self.__processRecord(record[prop], qprop)
                continue
            if isinstance(record[prop], list):
                for value in record[prop]:
                    if isinstance(value, dict):
                        self.__processRecord(value, qprop) # may add no later
                        
    def classes(self):
        return self.__classes
                        
    def report(self):
        mu = ""
        mu += "## Records seen (by type)\n\n"
        for i, typ in enumerate(sorted(self.__cntRecordsByType.keys()), 1):
            mu += "{}. {}: {}\n".format(i, typ, self.__cntRecordsByType[typ])
        mu += "\n"
        mu += "## Model\n\n"
        for i, typ in enumerate(sorted(self.__classes.keys()), 1):
            mu += "{}. {} ({})\n".format(i, typ, self.__cntRecordsByType[typ])
            cnt = 0
            for prop in ["id", "type", "patientIEN"]:
                if prop in self.__classes[typ]:
                    cnt += 1
                    mu += "\t{}. {}: {}\n".format(cnt, prop, self.__classes[typ][prop])                
            for prop in sorted([prop for prop in self.__classes[typ] if prop not in ["id", "type", "patientIEN"]]):
                cnt += 1
                if typ + ":" + prop in self.__typeProperties:
                    typeMU = " (" + json.dumps(self.__typeProperties[typ + ":" + prop]) + ")"
                else:
                    typeMU = ""
                mu += "\t{}. {}: {}{}\n".format(cnt, prop, self.__classes[typ][prop], typeMU)
            mu += "\n"
        mu += "\n"
        return mu
        
    def reportAllTopProperties(self): # for table fill in 
        mu = "# All properties - map table to fill in\n\n"
        for i, typ in enumerate(sorted(self.__topPropsByType.keys()), 1):
            mu += "## {}. {}\n\n".format(i, typ)
            mu += "\# | VPR | FM | Comment\n--- | --- | --- | ---\n"
            cnt = 0
            for topProp in sorted(self.__topPropsByType[typ]):
                if topProp in ["id", "type", "patientIEN"]:
                    continue
                cnt += 1
                if self.__cntRecordsByType[typ] == self.__topPropsByType[typ][topProp]:
                    mandMU = "*"
                else:
                    mandMU = ""
                mu += "{} | {}{} | - | -\n".format(cnt, topProp, mandMU)
            mu += "\n\n"
        return mu
            
"""
A series of reports on the VPR including:
- compare data to pre-built/code-based model

TODO:
- merge with VPR version (have a mode to handle Pointer/Date/_id)
- data points count ie/ total concrete assertions ie/ leaf asserts without 'type', 'id'
  - will do same with VPR when x: {code, name} <=> one data pt ie/ like a pointer ... group em everywhere (do in normalizer as read ...)
  - ALSO want # of date asserts, reference asserts (name/code | xIEN or Pointer)
  
... tweek individually and then move here
  
NOTE: will combine reports eventually ie/ 2 + Demographics ... side by side ...

NOTE: consider roll back into TypeIsolator of f***utils ie/ prelude to Schema ***
"""
class FMModelFromData:
 
    def __init__(self):
        self.__cntRecordsByType = defaultdict(int)
        self.__topPropsByType = defaultdict(lambda: defaultdict(int)) # expect to equal number per type!
        self.__classes = defaultdict(lambda: defaultdict(int))
        self.__typeProperties = defaultdict(lambda: defaultdict(int))
        self.__dates = set()
        self.__pointers = set()
        self.__assertsPerType = defaultdict(int) # leaves only

    def process(self, results):
        if len(results) == 0:
            return
        self.__type = results[0]["type"]
        for record in results:
            self.__cntRecordsByType[self.__type] += 1
            self.__processRecord(record)
        
    def __processRecord(self, record, parentProp=""):
    
        def isDateTimeAssert(qprop, rvalue):
            if isinstance(rvalue, dict) and set(rvalue.keys()) == set(["value", "type"]):
                self.__dates.add(self.__type + ":" + qprop)
                return True
            return False
            
        def isPointerAssert(qprop, rvalue):
            if isinstance(rvalue, dict) and set(rvalue.keys()) == set(["id", "label"]):
                self.__pointers.add(self.__type + ":" + qprop)
                return True
            return False
            
        # Boolean too? ... see TypeDefiner of f***utils
    
        for prop in record:
            if parentProp == "":
                self.__topPropsByType[self.__type][prop] += 1
            qprop = prop if not parentProp else parentProp + "/" + prop
            self.__classes[self.__type][qprop] += 1
            if isinstance(record[prop], dict) and not (isDateTimeAssert(qprop, record[prop]) or isPointerAssert(qprop, record[prop])):
                self.__processRecord(record[prop], qprop)
            elif isinstance(record[prop], list) and len(record[prop]) and (isinstance(record[prop][0], dict) and not (isDateTimeAssert(qprop, record[prop][0]) or isPointerAssert(qprop, record[prop][0]))):
                for value in record[prop]:
                    self.__processRecord(value, qprop) # may add no later
            else:
                self.__assertsPerType[self.__type] += 1
                        
    def classes(self):
        return self.__classes
               
    """
    REDO REPORT -- leaf props => split on / and show em ... see if totals agree
    """         
    def report(self):
        
        mu = ""
        mu += "## Records seen (by type)\n\n"
        for i, typ in enumerate(sorted(self.__cntRecordsByType.keys()), 1):
            mu += "{}. {}: {}\n".format(i, typ, self.__cntRecordsByType[typ])
        mu += "\n"
        mu += "## Model\n\n"
        for i, typ in enumerate(sorted(self.__classes.keys()), 1):
            mu += "{}. {} ({}) - {} assertions\n\n".format(i, typ, self.__cntRecordsByType[typ], self.__assertsPerType[typ])
            
            # Mandatory Properties per type => property with same # as records of type
            mandTopProps = sorted([prop for prop in self.__topPropsByType[typ] if self.__topPropsByType[typ][prop] == self.__cntRecordsByType[typ]]) 
            mu += "... mandatory properties: {}/{} - {}\n\n".format(len(mandTopProps), len(self.__topPropsByType[typ]), ", ".join(mandTopProps))
            mandTopProps = set(mandTopProps)
            
            cnt = 0
            for prop in ["id", "_id", "type", "label", "patient", "patient_name", "name"]:
                if prop in self.__classes[typ]:
                    cnt += 1
                    mu += "\t{}. {}: {}\n".format(cnt, prop, self.__classes[typ][prop])                
            for prop in sorted([prop for prop in self.__classes[typ] if prop not in ["id", "_id", "type", "patient", "patient_name", "name"]]):
                cnt += 1
                tprop = typ + ":" + prop
                if tprop in self.__dates:
                    typeMU = " (DATE)"
                elif tprop in self.__pointers:
                    typeMU = " (POINTER)"
                else:
                    typeMU = ""
                mandMU = " **M**" if prop in mandTopProps else ""
                mu += "\t{}. {}: {}{}{}\n".format(cnt, prop, self.__classes[typ][prop], typeMU, mandMU)
            mu += "\n"
        mu += "\n"
        return mu
        
def main():

    # Ensure Directory Exists
    fmDir = "/data/vista/{}/PatientSlices/FM/".format(STATION_NO)
    
    mfd = FMModelFromData()

    for i, patientIEN in enumerate(os.listdir(fmDir), 1):
    
        print "{}. Patient {}".format(i, patientIEN)
        
        patientDir = fmDir + patientIEN + "/"
                
        for patientDataFile in os.listdir(patientDir):
        
            typ = patientDataFile.split(".")[0]
            print "\tprocessing {}".format(typ)
            
            results = json.load(open(patientDir + patientDataFile))
            mfd.process(results)
            
    mu = mfd.report()
    print mu
    open("fmReport.md", "w").write(mu)
    
    # Ensure Directory Exists
    vprDir = VPR_TEMPLATE_DIR.format(STATION_NO)
    
    mfd = VPRModelFromData()

    for i, patientIEN in enumerate(os.listdir(vprDir), 1):
    
        print "{}. Patient {}".format(i, patientIEN)
        
        patientDir = vprDir + patientIEN + "/"
        patientDirJSON = patientDir + "JSON/"
                
        for patientDataFile in os.listdir(patientDirJSON):
        
            typ = patientDataFile.split(".")[0]
            print "\tprocessing {}".format(typ)
            
            results = json.load(open(patientDirJSON + patientDataFile))
            mfd.process(results)
            
    mu = mfd.report()
    print mu
    open("vprReport.md", "w").write(mu)
    mu = mfd.reportAllTopProperties()
    open("vprMapTemplate.md", "w").write(mu)
                                
if __name__ == "__main__":
    main()