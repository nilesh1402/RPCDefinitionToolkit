#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime

from fmqlutils.cacher.cacherUtils import FilteredResultIterator
from fmqlutils.reporter.reportUtils import MarkdownTable
from fmqlutils.schema.reduceReportTypes import DATA_LOCN_TEMPL

VISTA_RED_LOCN_TEMPL = "/data/vista/{}/RPCDefinitions/"

"""
Each VistA has information about its RPC interface in FileMan files. Here we reduce
all available data per VistA before assembling into a basic, cross-VistA, data-based RPC Interface definition.
  * 8994
  * references to 8994
  * build/install data about RPCs, Options, ...

TODO: 
- finish 9_4 (for vista app id with monograph), 9_7 for install dates per vista
and report red file ... before doing assembly
- finish others
- split out to module with reduce8994 etc with one main caller
- EXPECT on raw data in /data => force full cache

From 442 Follow on: in builds but not 8994
> 	set([u'ORQTL EXISTING TEAM AUTOLINKS', u'MAG GET SOP CLASS METHOD', u'WWW WEBTOP', u'ORQTL USER TEAMS', u'PSA UPLOAD', u'ORQTL TEAM LIST INFO', u'ORQTL TEAM LIST PATIENTS', u'ORQTL ALL USER TEAMS PATIENTS', u'ORQQPX OTHERS REMINDERS', u'ORQQVI2 VITALS STORE', u'ORQTL TEAM LIST USERS'])
"""

def reduceVistAData(stationNo):

    # Phase 1
    try:
        redResults = json.load(open("redResults.json"))
    except:
        redResults = {}
        
    reduce8994(stationNo, redResults)
    
    reduce19(stationNo, redResults)
    
    reduce101_24(stationNo, redResults)
    
    reduce9_4Plus(stationNo, redResults)
    
    reduce9_7(stationNo, redResults)
    
    reduce9_6(stationNo, redResults)
    
    reduce3_081(stationNo, redResults)
    
    reduce200(stationNo, redResults)
            
    json.dump(redResults, open("redResults.json", "w"), indent=4)
    
    print "\n# VistA Reductions (so far)\n"
    tbl = MarkdownTable(["Type", "Station No (Total/Reduction)"])
    for typeId in sorted(redResults, key=lambda x: float(re.sub(r'\_', '.', x))):
        typeInfo = redResults[typeId]
        mu = ", ".join(["{} ({})".format(sNo if sNo != "999" else "FOIA", "{:,} / {:,}".format(typeInfo[sNo]["total"], typeInfo[sNo]["reduced"]) if typeInfo[sNo]["total"] > typeInfo[sNo]["reduced"] else typeInfo[sNo]["reduced"]) for sNo in sorted(typeInfo)])
        cstoppedMU = ", ".join(typeInfo["cstopped"]) if "cstopped" in typeInfo else ""
        tbl.addRow([typeId, mu])
    print tbl.md() + "\n"
    print
    
    # RPC centric reduction (builds on cleanups above)
    reduceRPCBPIs(stationNo)
    
# ################ Clean Sources to enable RPC-centric Reduction ########
    
"""
Common package ref reduction to:
- remove bad refs (label == IEN)
- make match 9_4 reduction where upper case variations take over and which uses
/ and not _
"""
def reducePackageRef(value):
    if value["id"].split("-")[1] == value["label"]: # bad ref
        return ""
    return re.sub(r'\_', '/', value["label"]).upper()

"""
REMOTE PROCEDURE (8994)

Note missing 'is' properties for "session setup" (SIGNON SETUP etc) or basic
comms (IM HERE) ie/ the "Broker RPCs" ie/ not particular to a package

TODO check MUMPS:
- 'inactive': isLocalInactive, isRemoteInactive, isInactive and effect
- app_proxy_allowed
- suppress_rdv_user_setup

TODO CHECK consistency
- 30% with no input parameters - do they have availability of RESTRICTED? OR
  - XWB EGCHO MEMO retricted and comment says takes parameter but none spec'ed
"""
def reduce8994(stationNo, redResults):
    
    resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "8994")
    
    class Reducer(object):
    
        def __init__(self):
            self.__noReduced = 0
            self.__cstopped = []
    
        def reduce(self, resource):
            self.__reduction = OrderedDict()
            for prop in resource:
                if prop == "fmqlHasStops":
                    self.__cstopped.append(resource["_id"].split("-")[1])
                    continue
                if prop in ["label", "type"]:
                    continue
                if not hasattr(self, prop):
                    raise Exception("Unexpected 8994 property {}".format(prop))
                getattr(self, prop)(resource[prop])
            self.__noReduced += 1
            return self.__reduction
            
        def totalReduced(self):
            return self.__noReduced
            
        def cstopped(self):
            return self.__cstopped

        # ################## Mandatory or Close to It ###############
      
        # not doing id for now (ie/ IEN not needed)
        def _id(self, value):
            return
        
        # name - LITERAL - 5,239 (100%)                  
        def name(self, value): # ... name only would be interesting!
            self.__reduction["label"] = value
            
        # return_value_type - LITERAL - 5,235 (100%)
        def return_value_type(self, value):
            self.__reduction["returnType"] = value
            
        # routine - LITERAL - 5,235 (100%)
        def routine(self, value):
            self.__reduction["routine"] = value
        
        # tag - LITERAL - 5,235 (100%)
        def tag(self, value):
            self.__reduction["tag"] = value
            
        # description - LITERAL - 4,311 (82%)
        def description(self, value):
            self.__reduction["description"] = value
            
        # ################## 40 --> % ##########################
        
        # input_parameter - LIST - 3,658 (70%)
        def input_parameter(self, values):
            self.__reduction["parameters"] = []
            lastIEN = -1
            # IMPORTANT: leaving sequence_number in ... not 
            # consistently used and must see why (may drop or
            # see if inconsistency has merit?)
            for value in values:
                ien = int(value["ien"])
                if ien <= lastIEN:
                    raise Exception("Parameters out of order")
                lastIEN = ien
                del value["ien"]
                value["label"] = value["input_parameter"]
                del value["input_parameter"]
                if "required" in value:
                    if value["required"] == True:
                        value["isRequired"] = True
                    del value["required"]
                self.__reduction["parameters"].append(value)
            
        # return_parameter_description - LITERAL - 3,344 (64%)
        def return_parameter_description(self, value):
            self.__reduction["returnDescription"] = value
        
        """
        # availability - LITERAL - 2,954 (56%)
        # ... TODO: default is "P:PUBLIC"? See behaviors in code
        
        > Entry of the input and return parameter information is at the 
        > option of the developing package for RESTRICTED
        """
        def availability(self, value):
            self.__reduction["availability"] = value
        
        # word_wrap_on - LITERAL - 2,233 (43%)
        # ... Affects GLOBAL ARRAY and WORD PROCESSING return value types only
        def word_wrap_on(self, value):
            if value == "1:TRUE":
                self.__reduction["isWordWrap"] = True
    
        # ################## Rare - may drop but keeping to see if distinguishing        
        
        """
        # inactive - LITERAL - 830 (16%)
        
        TODO: important interplay with application context - will REDO. Check code.
        """
        def inactive(self, value):
            if value == "0:ACTIVE": # ie/ default to ACTIVE!
                return
            if value == "1:INACTIVE":
                self.__reduction["isInactive"] = True
                return
            if value == "2:LOCAL INACTIVE (ACTIVE REMOTELY)":
                self.__reduction["isLocalInactive"] = True
                return
            if value == "3:REMOTE INACTIVE (ACTIVE LOCALLY)":
                self.__reduction["isRemoteInactive"] = True
                return
            raise Exception("Unexpected value for 'inactive': {}".format(value))
            
        # version - LITERAL - 638 (12%)
        def version(self, value): # keeping for now, see if can use cross VistAs
            self.__reduction["version"] = value
                        
        # app_proxy_allowed - BOOLEAN - 392 (7%)
        def app_proxy_allowed(self, value):
            if value != True:
                return
            self.__reduction["isApplicationProxyAllowed"] = True
            
        """
        suppress_rdv_user_setup - BOOLEAN - 57 (1%)
        
        Logic that remote client prevented from setting up new 200 entry
        and fall back on POST MASTER
        """
        def suppress_rdv_user_setup(self, value):
            if value == True:
                self.__reduction["isPreventRemoteUserSetup"] = True 
            
        # client_manager - BOOLEAN - 4 (0%)
        def client_manager(self, value):
            if value != True:
                return
            self.__reduction["isClientManager"] = True
                
    reducer = Reducer()
    reductions = []
    print "Reducing 8994 for {}".format(stationNo)
    for i, resource in enumerate(resourceIter, 1):
        if (i % 1000) == 0:
            print "\tprocessing another 1000 8994's"
        reduction = reducer.reduce(resource)
        reductions.append(reduction)
    print "\t... done after {:,}".format(reducer.totalReduced())
        
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json", "w"), indent=4)
        
    if "8994" not in redResults:
        redResults["8994"] = {}
    redResult = {"total": reducer.totalReduced(), "reduced": reducer.totalReduced()}
    cstopped = reducer.cstopped()
    if len(cstopped):
        redResult["cstopped"] = cstopped
    redResults["8994"][stationNo] = redResult
    
"""
{'qprop': 'rpc:rpc', 'fileName': u'RPC', 'topFileName': u'OPTION', 'topFileId': u'19', 'prop': u'rpc', 'fileId': u'19.05'}

Just for RPC options ie/ type_4 == B:Broker (Client/Server)

Note: may be missing rpcs none the less ie if deleted?

TODO: may extend to
- A:action
- X:extended action <------- here's the extended actions that trigger protocols
"""
def reduce19(stationNo, redResults):

    resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "19")
    
    class Reducer(object):
    
        def __init__(self):
            self.__noSeen = 0
            self.__noReduced = 0
            self.__cstopped = []
    
        def reduce(self, resource):
            self.__noSeen += 1
            if not ("type_4" in resource and resource["type_4"] == "B:Broker (Client/Server)"):
                return None
            self.__reduction = OrderedDict()
            SUPPRESS_PROPS = ["menu_text", "timestamp_of_primary_menu", "timestamp", "display_option", "delegable", "short_menu_text", "entry_action", "e_action_present", "xquit_message", "keep_from_deleting"]
            for prop in resource:
                if prop == "fmqlHasStops":
                    self.__cstopped.append(resource["_id"].split("-")[1])
                    continue
                if prop in SUPPRESS_PROPS:
                    continue
                if prop in ["label", "type"]:
                    continue
                # if not hasattr(self, prop):
                #    raise Exception("Unexpected 19 property {}".format(prop))
                if not hasattr(self, prop):
                    continue
                getattr(self, prop)(resource[prop])
            self.__noReduced += 1
            return self.__reduction
            
        def totalSeen(self):
            return self.__noSeen
            
        def totalReduced(self):
            return self.__noReduced
            
        def cstopped(self):
            return self.__cstopped

        # ################## Mandatory or Close to It ###############
      
        # not doing id for now (ie/ IEN not needed)
        def _id(self, value):
            return
            
        # type_4 - LITERAL - 151 (100%)
        # ... used for filter so fixed
        def type_4(self, value):
            return
        
        """
        > The formal name of an option, prefaced with the package name. Each option must 
        > be preceded by its package prefix (a 2-4 character) code specified in the 
        > PACKAGE file, or the letter "Z" or "A".
        """
        # name - LITERAL - 151 (100%)              
        def name(self, value): 
            self.__reduction["label"] = value
                        
        # uppercase_menu_text - LITERAL - 151 (100%)
        # ... instead of 'menu_text'
        def uppercase_menu_text(self, value):
            self.__reduction["menuText"] = value
            
        # rpc - LIST - 143 (95%) (or 1% of full list)
        def rpc(self, values):
            try:
                self.__ensureRPCLabelUnique
            except:
                self.__ensureRPCLabelUnique = defaultdict(set)
            rpcLabels = set()
            for rpcInfo in resource["rpc"]:
                self.__ensureRPCLabelUnique[
                rpcInfo["rpc"]["label"]].add(rpcInfo["rpc"]["id"])
                rpcLabels.add(re.sub(r'\_', '/', rpcInfo["rpc"]["label"]))
                # for now just note: may include properly later
                if "rules" in rpcInfo:
                    self.__reduction["isRPCsRuled"] = True
                if "rpckey" in rpcInfo:
                    self.__reduction["isRPCsKeyed"] = True
            if sum(1 for rpcLabel in self.__ensureRPCLabelUnique if len(self.__ensureRPCLabelUnique[rpcLabel]) > 1):
                raise Exception("Assumption that RPC label is unique for an RPC is false")
            self.__reduction["rpcs"] = sorted(list(rpcLabels))
                        
        # description - LITERAL - 109 (72%)
        def description(self, value):
            self.__reduction["description"] = value

        """
        package - POINTER - 65 (43%) - 9_4
        """ 
        def package(self, value):
            rvalue = reducePackageRef(value)
            if rvalue:
                self.__reduction["package"] = rvalue
                        
        # routine - LITERAL - 8 (5%)
        def routine(self, value):
            self.__reduction["routine"] = value
            
        # lock - LITERAL - 3 (2%)
        def lock(self, value):
            self.__reduction["keyRequired"] = value
            
        # out_of_order_message - LITERAL - 3 (2%)
        def out_of_order_message(self, value):
            self.__reduction["removedReason"] = value
            self.__reduction["isRemoved"] = True
            
        # menu - LIST - 2 (1%)
        def menu(self, values):
            subOptions = sorted(list(set(val["item"]["label"] for val in values)))
            self.__reduction["subOptions"] = subOptions
            
    reducer = Reducer()
    reductions = []
    print "Reducing 19 for {}".format(stationNo)
    for i, resource in enumerate(resourceIter, 1):
        if (i % 1000) == 0:
            print "\tprocessing another 1000 19's"
        reduction = reducer.reduce(resource)
        if reduction:
            reductions.append(reduction)
    print "\t... done after {:,}, {:,} reduced".format(reducer.totalSeen(), reducer.totalReduced())
    cstopped = reducer.cstopped()
    if len(cstopped):
        print "\t** Warning: {} were CSTOPPED".format(cstopped)
        
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_19Reduction.json", "w"), indent=4)
        
    if "19" not in redResults:
        redResults["19"] = {}
    redResult = {"total": reducer.totalSeen(), "reduced": reducer.totalReduced()}
    cstopped = reducer.cstopped()
    if len(cstopped):
        redResult["cstopped"] = cstopped
    redResults["19"][stationNo] = redResult
    
"""
Goal: "Build-Backed" Package List 

Specifically 9_4 not a definitive package list as [1] builds or some other mechanism with bad package names (named for individual builds, dup existing package with case variants ...) introduce duplicate or invalid entries and [2] some builds, particularly COTS or Class III lack package references. 

This means __9_4 IS A STARTING POINT__ and that __9_6 ITSELF ALONG WITH OUTSIDE LISTS__ must deliver the definitive package list. Getting to A DEFINITIVE PACKAGE LIST WILL BE AN ITERATIVE, CROSS VISTA PROCESS.

Hence plus in _reduce9_4Plus_ ... for one thing new packages are added from an "in code"
definition.

Note: the 9_4 DD does NOT enforce unique labels OR unique prefixes though that's
what is intended. A reduction in instances happens because [1] the same label 
is used > once or [2] the same prefix is used > once.

442: 310 ...

    name - LITERAL - 310 (100%)
    prefix - LITERAL - 310 (100%)
    -----------------------------
    version - LIST - 274 (88%)
    current_version - LITERAL - 269 (87%)
    ------------------------------
    developer_person_site - LITERAL - 199 (64%)
    class - LITERAL - 197 (64%) <----------- NOT USABLE
        I:National - 147 (74.6%)
        III:Local - 49 (24.9%) <---------- some Locals are really National!
        II:Inactive - 1 (0.5%)
    ------------------------------
    file - LIST - 176 (57%)
    ------------------------------
    lowest_file_number - LITERAL - 89 (29%)
    highest_file_number - LITERAL - 88 (28%)
    ------------------------------
    excluded_name_space - LIST - 61 (20%)
    ------------------------------
    additional_prefixes - LIST - 32 (10%)
    synonym - LIST - 1 (0%)
    
and note that 94% of Build (9_6's) have package_file link as does install (9_7).

label uniqueness: 
    442 has two of VOLUNTARY TIMEKEEPING but both have the same primary prefix.
The later one has a higher version. The other lower versions.

and 640: 343 ...

    name - LITERAL - 343 (100%)
    prefix - LITERAL - 342 (100%) <------- one missing
    -------------------------------
    version - LIST - 296 (86%)
    current_version - LITERAL - 278 (81%)
    -------------------------------
    developer_person_site - LITERAL - 199 (58%)
    file - LIST - 181 (53%)
    class - LITERAL - 156 (45%) <----------- NOT USABLE
        I:National - 112 (71.8%)
        III:Local - 43 (27.6%) <---------- some Locals are really National!
        II:Inactive - 1 (0.6%)
    --------------------------------
    lowest_file_number - LITERAL - 99 (29%)
    highest_file_number - LITERAL - 98 (29%)
    ---------------------------------
    additional_prefixes - LIST - 32 (9%)
    synonym - LIST - 1 (0%)
    
and 90% Build (9_6's) have package file links as does install (9_7)
"""
# Fixed VistA Stuff and off OSEHRA packages as not covered in 9_4 
# ... this will expand as we refine to a definitive, "Build-backed" Package list
#
# - https://github.com/OSEHRA/VistA/blob/master/Packages.csv
# - https://www.oit.va.gov/Services/TRM/ReportVACategoryMapping.aspx
# - Monograph (in git)
#        
BEYOND_9_4_PACKAGE_INDEX = {
    "AXVVA": "VISUAL AID FOR CLINIC APPOINTMENTS (VISN 20)",
    "DSIP": "ENCODER PRODUCT SUITE (EPS)", # monograph
    "DSIVA": "ADVANCED PROSTHETICS ACQUISITION TOOL (APAT)", # monograph
    "VANOD": "VA NURSING OUTCOMES DATABASE PROJECT", # based in Puget Sound
    "NVS": "NATIONAL VISTA SUPPORT", # OSEHRA Packages.csv
    "APG": "PHOENIX VAMC", # OSEHRA Packages.csv
    "ANU": "ANU HS DOWNLOAD", # Shawn Hardenbrook Nashville VA Medical Center - downloading health summaries
    "R1ENINL": "R5 VBA IMPORT TOOL", # GUI application which validates the data against the AEMS/MERS database
    "R1SRL": "R1 SURGERY SCHEDULE VIEWER" # Surgery App viewer (http://robertdurkin.com/projects/R1SRLORScheduleViewer/index.html)
}

def reduce9_4Plus(stationNo, redResults):

    resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "9_4")

    print "Reducing 9_4 for {}".format(stationNo)

    """
    Dealing with duplicates:
    - same label, same prefix or different prefix
    - different label, same prefix
    ... issue of two entries earlier matching (ie/ same name and separately same prefix)
    ... would need to merge them before continuing with override. Not doing as doesn't
    ... seem to arise.
    
    Note: upper cases name to match reducePackageRef
    """
    reductions = []
    # assuming BOTH label and prefix are reserved for individual packages ie/ identifying
    redOfLabel = defaultdict(list)
    redOfPrefix = defaultdict(list)
    cstopped = []
    for i, resource in enumerate(resourceIter, 1):
        if (i % 200) == 0:
            print "\tprocessing another 200 9_4's"
        # let's force dup names cause of case diffs to be merged
        # ... fit's with reducePackageRef
        uname = resource["name"].upper()
        if uname != resource["name"]:
            print "\tuppercasing name {} before matching".format(resource["name"])
        # same label, new or same prefix
        if uname in redOfLabel:
            info = redOfLabel[uname]
            # is this an additional prefix
            if "prefix" in resource and resource["prefix"] not in info["prefixes"]:
                if resource["prefix"] in redOfPrefix and redOfPrefix[resource["prefix"]]["label"] != uname:
                    # This would require some break. Assume doesn't happen
                    raise Exception("Clash of name/prefix - diff name earlier also has that prefix. Which previous entry to take? By same name or by same prefix")
                redOfPrefix[resource["prefix"]] = info
                info["prefixes"].append(resource["prefix"])
            print "\toverride w/new definition of same name {} - prefixes now {}".format(uname, ",".join(info["prefixes"]))
        # else new label and existing prefix
        elif "prefix" in resource and resource["prefix"] in redOfPrefix:
            info = redOfPrefix[resource["prefix"]]
            print "\toverride w/new definition of same prefix {} and different name {} from {}".format(resource["prefix"], uname, info["label"])
            if "oldLabels" not in info:
                info["oldLabels"] = []
            info["oldLabels"].append(info["label"])
            info["label"] = uname
            redOfLabel[info["label"]] = info
        else: # new label, new prefix
            if uname in BEYOND_9_4_PACKAGE_INDEX.values():
                print json.dumps(resource, indent=4)
                raise Exception("Didn't Expect 'BEYOND_9_4_PACKAGE_INDEX' name to have a built in 9_4 entry for any VistA - {}".format(uname))
            info = {"label": uname, "prefixes": []}
            redOfLabel[info["label"]] = info
            reductions.append(info)
            if "prefix" in resource:
                if resource["prefix"] in BEYOND_9_4_PACKAGE_INDEX:
                    raise Exception("Didn't Expect 'BEYOND_9_4_PACKAGE_INDEX' prefix to have a built in 9_4 entry for any VistA - {}/{}".format(uname, resource["prefix"]))
                info["prefixes"].append(resource["prefix"])
                redOfPrefix[resource["prefix"]] = info
        for prop, nprop in {"class": "class", "current_version": "currentVersion", "lowest_file_number": "lowestFileNumber", "highest_file_number": "highestFileNumber"}.items():
            if prop not in resource:
                continue
            info[nprop] = resource[prop]
        if "additional_prefixes" in info:
            info["additionalPrefixes"] = [ap["additional_prefixes"] for ap in resource["additional_prefixes"]] 
        if "fmqlHasStops" in resource:
            cstopped.append(resource["_id"])
    # clean up empty prefixes
    for reduction in reductions:
        if len(reduction["prefixes"]) == 0:
            del reduction["prefixes"]
            
    print "\t... done after {:,} producing {:,} distinct definitions with {:,} prefixes".format(i, len(reductions), len(redOfPrefix))
        
    if "9_4" not in redResults:
        redResults["9_4"] = {}
    redResult = {"total": i, "reduced": len(reductions)}
    if len(cstopped):
        redResult["cstopped"] = cstopped
    redResults["9_4"][stationNo] = redResult
    
    # Add manual enhancement of Packages (note: checked above that not in 9_4)
    for prefix in BEYOND_9_4_PACKAGE_INDEX:
        info = {"label": BEYOND_9_4_PACKAGE_INDEX[prefix], "prefixes": [prefix]}
        reductions.append(info)
    print "\t... added {:,} packages manually to the 9_4 list bringing total to {:,}".format(len(BEYOND_9_4_PACKAGE_INDEX), len(reductions))
    
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_4PlusReduction.json", "w"), indent=4)
            
    return reductions
    
"""
9_7 install is reduced for its install times/completeness
"""
def reduce9_7(stationNo, redResults):
    resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "9_7")
    reductions = []
    cstopped = []
    print "Reducing 9_7 for {}".format(stationNo)
    for i, resource in enumerate(resourceIter, 1):
        if (i % 1000) == 0:
            print "\tprocessing another 1000 9_7's"
        red = {
            "name": resource["name"],
        }
        # status - LITERAL - 13,616 (100%) 640 isn't quite mandatory
        if "status" in resource:
            red["status"] = resource["status"]
        for prop in ["install_start_time", "install_complete_time"]:
            if prop in resource:
                red[prop] = resource[prop]["value"]
        if "starting_package" in resource and resource["starting_package"]["id"] != resource["_id"]:
            red["isPartOf"] = True
        # Ala others, to match 9_4 red, go upper case and ensure / for _
        if "package_file_link" in resource:
            rvalue = reducePackageRef(resource["package_file_link"])
            if rvalue:
                red["package"] = rvalue
        if "fmqlHasStops" in resource:
            cstopped.append(resource["_id"])
        reductions.append(red)
    if "9_7" not in redResults:
        redResults["9_7"] = {}
    redResult = {"total": i, "reduced": i}
    print "\t... done after {:,}".format(i)
    if len(cstopped):
        print "\t** Warning: {} were CSTOPPED".format(cstopped)
        redResult["cstopped"] = cstopped
    redResults["9_7"][stationNo] = redResult
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_7Reduction.json", "w"), indent=4)
    return reductions
               
"""
Initially only doing if REMOTE PROCEDURE BUILD COMPONENT there but will expand ...
- Build Component REMOTE PROCEDURE and OPTION (focus on RPC Option) and ROUTINE (focus
  on entry routines for RPCs)
- files (for later)

Has HL7, Protocols etc etc too but of less interest for now

Note: gives date of distribution. 9_7 gives install or not and when.

Note: "track_package_nationally": false seems to be always the case

TODO: 
- 100100_003 ... VDL link ... see if this file is in file list of builds
""" 
def reduce9_6(stationNo, redResults):

    resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "9_6")
    
    class Reducer(object):
    
        BUILD_COMPONENTS_TO_REDUCE = {"REMOTE PROCEDURE": "rpcs", "OPTION": "options", "ROUTINE": "routines"}
    
        def __init__(self, packageByPrefix, installInfoByName):
            self.__packageByPrefix = packageByPrefix
            self.__installInfoByName = installInfoByName
            self.__noSeen = 0
            self.__noReduced = 0
            self.__cstopped = []
            self.__trackMNPackageLink = Counter()
    
        def reduce(self, resource):
            self.__noSeen += 1
            self.__currentResource = resource # for checks below
            """
            DO ALL ...
            # only want if options, routines and remote procedures added
            if not ("build_components" in resource and sum(1 for entry in resource["build_components"] if entry["build_component"]["label"] in Reducer.BUILD_COMPONENTS_TO_REDUCE and "entries" in entry)):
                return None
            """
            self.__reduction = OrderedDict()
            SUPPRESS_PROPS = ["alpha_beta_testing", "transport_build_number", "postinstall_routine", "delete_postinit_routine", "xpz1", "xpi1", "environment_check_routine", "xpo1", "preinstall_routine", "delete_env_routine", "delete_preinit_routine", "installation_message", "pretransportation_routine", "install_questions", "test", "global"] 
            for prop in resource:
                if prop == "fmqlHasStops":
                    self.__cstopped.append(resource["_id"].split("-")[1])
                    continue
                if prop in SUPPRESS_PROPS:
                    continue
                if prop in ["label", "type"]:
                    continue
                # if not hasattr(self, prop):
                #    raise Exception("Unexpected 19 property {}".format(prop))
                if not hasattr(self, prop):
                    continue
                getattr(self, prop)(resource[prop])
            self.__noReduced += 1
            return self.__reduction
            
        def totalSeen(self):
            return self.__noSeen
            
        def totalReduced(self):
            return self.__noReduced
            
        def cstopped(self):
            return self.__cstopped
            
        def mnPackageLinked(self):
            return self.__trackMNPackageLink

        # ################## Mandatory or Close to It ###############
      
        # not doing id for now (ie/ IEN not needed)
        def _id(self, value):
            return
            
        # name - LITERAL - 10,774 (100%)        
        def name(self, value): 
            try:    
                self.__namesSeen
            except:
                self.__namesSeen = set()
            if value in self.__namesSeen:
                raise Exception("Expected builds to be unique by name")
            self.__namesSeen.add(value)
            self.__reduction["label"] = value
            self.__processNameForMN(value)
            self.__processInstallInfo(value)
            
        """
        Split name into buildMNVersion and buildMN. Want to use this to match
        to prefix in Package.
        
        Note: may see combo and label reused for different versions but would
        only know from installs AS build label is unique in 9_6. Reuse (and no
        rename) only lazily occurs for Class III's.
        
        KEY: using buildMN to link package if can when not otherwise available.
        REM that package == packageLabel.
        """
        def __processNameForMN(self, value):
            mnMatch = re.match(r'([^\*^ ^\_]+)', value)
            if not mnMatch:
                print "\tNo MN match for Build Name \"{}\"".format(value)
                return # ex/ '442 Cheyenne ICD 10.0'
            buildMN = re.sub(r' +$', '', mnMatch.group(1)) # trailing out
            if re.match(r'VEJD', buildMN):
                buildMN = "VEJD"
            if len(buildMN) < 2 or re.match(r'\d+$', buildMN):
                print "\tToo small or all number MN match for Build Name \"{}\"".format(value)
                return
            self.__reduction["buildMN"] = buildMN
            versionMatch = re.search(r'(\d.+)$', value)
            if not versionMatch:
                raise Exception("Expect to find version in Build Name: {}".format(value))
            self.__reduction["buildMNVersion"] = versionMatch.group(1)
            # Extra - if NO package ref, then use mn to link
            if "package_file_link" not in self.__currentResource:
                if buildMN in self.__packageByPrefix:
                    self.__reduction["package"] = self.__packageByPrefix[buildMN]
                    self.__trackMNPackageLink[self.__reduction["package"]] += 1
            
        """
        Add 9_7 install info inside 9_6
        - looking for 3:Install Completed and an install_complete_time
                and
        - no subsequent 4:De-Installed
        """
        def __processInstallInfo(self, name):
                    
            if name not in self.__installInfoByName:
                self.__reduction["isInstalled"] = False
                self.__reduction["countInstalls"] = 0
                return
                
            installInfos = self.__installInfoByName[name]
            
            self.__reduction["installs"] = installInfos
            deInstallIndexes = [i for i, iinfo in enumerate(installInfos) if "status" in iinfo and iinfo["status"] == "4:De-Installed"]
            frmIndex = 0
            if len(deInstallIndexes):
                if deInstallIndexes[-1] == len(installInfos) - 1:
                    self.__reduction["isInstalled"] = False
                    return
                frmIndex = deInstallIndexes[-1]+1
            installInfos = [ii for ii in installInfos[frmIndex:] if "status" in ii and ii["status"] == "3:Install Completed" and "install_complete_time" in ii]
            if len(installInfos) == 0:
                self.__reduction["isInstalled"] = False
                return
            self.__reduction["isInstalled"] = True
            # post the last de install
            self.__reduction["dateInstalledFirst"] = installInfos[0]["install_complete_time"]
            self.__reduction["dateInstalledLast"] = installInfos[-1]["install_complete_time"]
            
        # type_2 - LITERAL - 10,772 (100%)
        # ... 0:SINGLE PACKAGE - 10,681 (99.2%)
        # ... only 1 GLOBAL PACKAGE (from imaging) with no date, few fields
        # ... 90 MULTI-PACKAGE all with multiple_build and few with package links
        def type_2(self, value):
            if value == '0:SINGLE PACKAGE':
                return
            if value == "1:MULTI-PACKAGE":
                self.__reduction["isMultiPackage"] = True
                return
            elif value == "2:GLOBAL PACKAGE":
                self.__reduction["isGlobalPackage"] = True
                return
            raise Exception("Invalid value {} for type_2".format(value))
            
        # track_package_nationally - BOOLEAN - 10,769 (100%)
        # ... False - 10,769 (100.0%)
        def track_package_nationally(self, value):
            if value != False:
                raise Exception("Expected track_package_nationally to always be False")
                
        # build_components - LIST - 10,698 (99%)
        # ... many entries are empty, ignoring those and ignoring checksum for others
        def build_components(self, values):
            componentsByTypeByAction = defaultdict(lambda: defaultdict(list))
            for bcInfo in values:
                if "entries" not in bcInfo: # empty
                    continue
                # As there are EMPTY components in multi-builds, this check
                # only applies when we find filled in components
                if "type_2" in self.__currentResource: 
                    if self.__currentResource["type_2"] != "0:SINGLE PACKAGE":
                        raise Exception("Expect components ONLY in SINGLE PACKAGEs")
                # ignoring 'file': REMOTE PROCEDURE, file = {"id": "1-8994" etc
                # ... sometimes there for REMOTE PROCEDURE etc but sometimes not
                componentType = bcInfo["build_component"]["label"]
                if componentType not in Reducer.BUILD_COMPONENTS_TO_REDUCE:
                    continue
                prop = Reducer.BUILD_COMPONENTS_TO_REDUCE[componentType]
                if prop in self.__reduction:
                    raise Exception("Only expect one Build Component with a type in a particular build")
                self.__reduction[prop] = defaultdict(list)
                for entry in bcInfo["entries"]:
                    if "action" not in entry:
                        actionType = "**UNSET**" # defaulting : TODO - check
                    else:
                        actionType = entry["action"].split(":")[1]
                    self.__reduction[prop][actionType].append(entry["entries"])
            
        # date_distributed - DATE - 10,159 (94%)
        def date_distributed(self, value):
            self.__reduction["dateDistributed"] = value["value"]
            
        """
        package_file_link - POINTER - 10,152 (94%) - 9_4
        
        Note: when missing, will try to match using buildMN above.
        """ 
        def package_file_link(self, value):
            rvalue = reducePackageRef(value) # takes care of the invalid
            if rvalue:
                self.__reduction["package"] = rvalue
                        
        # description_of_enhancements - LITERAL - 9,224 (86%)
        def description_of_enhancements(self, value):
            self.__reduction["description"] = value
            
        # required_build - LIST - 7,560 (70%)
        def required_build(self, values):
            return
            
        # seq - LITERAL - 3,245 (30%)
        def seq(self, value):
            return
            
        # file - LIST - 3,188 (30%)
        # ... TODO: revisit and do more than just list files
        def file(self, values):
            fls = []
            if len(values) and "type_2" in self.__currentResource:
                if self.__currentResource["type_2"] != "0:SINGLE PACKAGE":
                    raise Exception("Expect Files only in SINGLE PACKAGE BUILDs")
            for fInfo in values:
                fls.append(fInfo["file"]["id"].split("-")[1])
            self.__reduction["files"] = fls
            
        # address_for_usage_reporting - LITERAL - 279 (3%)
        # ... may feed in later
        # ... mainly G.IMAGING DEVELOPMENT TEAM@FORUM.VA.GOV - 108 (38.7%)
        def address_for_usage_reporting(self, value):
            self.__reduction["email_to_track_use"] = value
            
        # package_namespace_or_prefix - LIST - 138 (1%)
        def package_namespace_or_prefix(self, values):
            return
            
        # multiple_build - LIST - 92 (1%)
        # - 100% is type_2 is MULTI-PACKAGE: multiple_build - LIST - 90 (100%)
        def multiple_build(self, values):
            return

    print "Reducing 9_6 for {}".format(stationNo)
    
    # Rely 9_4 done for adding links to packages where missing
    try:
        _9_4Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_4PlusReduction.json"))
    except:
        raise Exception("9_6 reduction requires 9_4 reduction first")
    packageByPrefix = {}
    for packageInfo in _9_4Reductions:
        if "prefixes" not in packageInfo:
            continue
        for prefix in packageInfo["prefixes"]:
            packageByPrefix[prefix] = packageInfo["label"]
        
    # Rely 9_7 done first ie/ putting install inside builds 
    try:
        _9_7Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_7Reduction.json"))
    except:
        raise Exception("9_6 reduction requires 9_7 reduction first")
    installInfoByName = defaultdict(list)
    for installInfo in _9_7Reductions:
        installInfoByName[installInfo["name"]].append(installInfo)
        
    reducer = Reducer(packageByPrefix, installInfoByName)
    reductions = []
    for i, resource in enumerate(resourceIter, 1):
        if (i % 1000) == 0:
            print "\tprocessing another 1000 9_6's"
        reduction = reducer.reduce(resource)
        if reduction:
            reductions.append(reduction)
    print "\t... done after {:,}, {:,} reduced".format(reducer.totalSeen(), reducer.totalReduced())
    mnPackageLinked = reducer.mnPackageLinked()
    if len(mnPackageLinked):
        print "\t\t{:,} packages linked to {:,} builds using MN linking".format(len(mnPackageLinked), sum(mnPackageLinked[pkg] for pkg in mnPackageLinked))
        
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json", "w"), indent=4)
        
    if "9_6" not in redResults:
        redResults["9_6"] = {}
    redResult = {"total": reducer.totalSeen(), "reduced": reducer.totalReduced()}
    cstopped = reducer.cstopped()
    if len(cstopped):
        print "\t** Warning: {} were CSTOPPED".format(cstopped)
        redResult["cstopped"] = cstopped
    redResults["9_6"][stationNo] = redResult
    
    return reductions    
    
"""
9_8 Routine
"""
def reduce9_8(stationNo, redResults):
    pass

"""
{'fileName': u'OE/RR REPORT', 'fileId': u'101.24', 'prop': u'rpc'}
... only have for 442 now (catch exception)
"""
def reduce101_24(stationNo, redResults):
    pass
    
"""
{'fileName': u'ARHCWEB1 EVENT LOG', 'fileId': u'662931', 'prop': u'rpc'}
                        
640 only BUT empty - placeholder for now.
"""
def reduce662931(stationNo, redResults):
    pass
    
"""
TEXT NAME (not 8994 proper)

19685.6 detail_rpc, remote_procedure | definitely take ie/ add in reduction

Only have type for 442 and need data (236)
"""
def reduce19685_6(stationNo, redResults):
    pass
    
"""
> File to maintain link between package file 9.4 and VA's VDL [VistA Document Library] URL specific to this package.

... not in FOIA but there are some RPCs that return the link!
... given as file in R1XUM*1.0*1 (no pkg obvious). See what other builds update this file!

http://localhost:9050/schema#100100_003
"""
def reduce100100_003(stationNo, redResults):
    pass
    
"""
Sign on - for signon period users - will be used to reduce users
... more a user information reduction ie/ count signons per user
"""
def reduce3_081(stationNo, redResults, forceRedo=False):

    if not forceRedo: # as big
        try:
            json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_3_081UserReduction.json"))
        except:
            pass
        else:
            return # as done already

    print "Reducing 3_081 to pick out Active Users"
    _3_081ResourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "3_081")
    userSignOnCount = Counter()
    for i, _3_081Resource in enumerate(_3_081ResourceIter, 1):    
        if (i % 10000) == 0:
            print "\tprocessed another {} sign ons, now {} users seen".format(i, len(userSignOnCount))
        userSignOnCount[_3_081Resource["user"]["id"]] += 1
    print "... {} users signed on".format(len(userSignOnCount))
    reductions = [{"userId": userId, "signOnCount": userSignOnCount[userId]} for userId in userSignOnCount]
    
    if "3_081" not in redResults:
        redResults["3_081"] = {}
    redResult = {"total": i, "reduced": len(reductions)}
    redResults["3_081"][stationNo] = redResult
    
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_3_081UserReduction.json", "w"), indent=4)
    
    return reductions
    
"""
User - for secondary_menu_options, primary_menu_option and keys
"""
def reduce200(stationNo, redResults, forceRedo=False):

    if not forceRedo: # as big
        try:
            json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_200Reduction.json"))
        except:
            pass
        else:
            return # as done already
    
    try:
        _3_081Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_3_081UserReduction.json"))
    except:
        raise Exception("200 reduction requires 3_081 reduction first")
    signedOnUserIds = set(red["userId"] for red in _3_081Reductions)

    print "Reducing Users to bags of Options and whether has signon or not ..."
    _200ResourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "200")
    reductions = []
    for i, _200Resource in enumerate(_200ResourceIter, 1):
        user = {"userId": _200Resource["_id"]}
        if (i % 1000) == 0:
            print "\tprocessed another {} users"
        if _200Resource["_id"] in signedOnUserIds:
            user["hasSignOn"] = True
        if "primary_menu_option" in _200Resource:
            user["primaryMenuOption"] = _200Resource["primary_menu_option"]["label"]
        if "secondary_menu_options" in _200Resource:
            smoLabels = set()
            for entry in _200Resource["secondary_menu_options"]:
                smoLabel = entry["secondary_menu_options"]["label"]
                smoLabels.add(smoLabels)
            user["secondaryMenuOptions"] = sorted(list(smoLabels))
        if "primaryMenuOption" in user or "secondaryMenuOptions" in user:
            reductions.append(user)
    print "Processed {:,} users, reduced to {:,}".format(i, len(reductions))
    
    if "200" not in redResults:
        redResults["200"] = {}
    redResult = {"total": i, "reduced": len(reductions)}
    redResults["200"][stationNo] = redResult
    
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_200Reduction.json", "w"), indent=4)
    
    return reductions
    
# ######################### Specific RPC or RPC centric views ####
#
# Overall: by RPC, 8994, Builds, Options ... an RPC must be [a] in 8994
# and [b] be active according to the Builds (proxy for is code there)
# and [c] be in an active (used recently) option (may also note if in
# any option too)
# 

"""
RPC "BPIs", Build-Package-Installs ie/ builds with install and package info
"""
def reduceRPCBPIs(stationNo):

    buildsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json"))
    buildsRPCReduction = [bi for bi in buildsReduction if "rpcs" in bi]
    
    _200Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_200Reduction.json"))

    """
    Flips from Builds to view from RPC side: only considers Builds that are installed and 
    if the first build seen for an RPC, it must be a SEND TO SITE (create) build.
    """
    rpcBPIByRPC = {}  
    nixBuildAsNotInstalled = 0
    nixBuildForRPCAsFirstButNotSend = 0
    for buildInfo in buildsRPCReduction:
        if buildInfo["isInstalled"] == False: # let's not count it!
            nixBuildAsNotInstalled += 1
            continue
        for actionType in buildInfo["rpcs"]:
            for rpc in buildInfo["rpcs"][actionType]:
                if rpc not in rpcBPIByRPC:
                    if actionType != "SEND TO SITE": # let's not count until get a SEND
                        nixBuildForRPCAsFirstButNotSend += 1
                        continue 
                    rpcBPIByRPC[rpc] = {"label": rpc, "installed": buildInfo["dateInstalledFirst"], "builds": []}   
                    if "dateDistributed" in buildInfo:
                        rpcBPIByRPC[rpc]["distributed"] = buildInfo["dateDistributed"]
                bir = {"label": buildInfo["label"], "action": actionType, "installed": buildInfo["dateInstalledFirst"]}
                rpcBPIByRPC[rpc]["builds"].append(bir) 
                if "package" in buildInfo:
                    bir["package"] = buildInfo["package"]
                if "dateDistributed" in buildInfo:
                    bir["distributed"] = buildInfo["dateDistributed"]
    for rpc in rpcBPIByRPC:
        bpi = rpcBPIByRPC[rpc]       
        if bpi["builds"][-1]["action"] == "DELETE AT SITE":
            bpi["isDeleted"] = True
            bpi["deleteInstalled"] = bpi["builds"][-1]["installed"]
            if "distributed" in bpi["builds"][-1]:
                bpi["deleteDistributed"] = bpi["builds"][-1]["distributed"]
        packages = [bi["package"] for bi in bpi["builds"] if "package" in bi]
        if len(set(packages)) == 1:
            bpi["package"] = packages[0]
        elif len(packages): # can be none! 
            packages.reverse()
            # ex override: [u'ORDER ENTRY/RESULTS REPORTING', u'GEN. MED. REC. - VITALS']
            bpi["package"] = [pkg for pkg in packages if pkg != "ORDER ENTRY/RESULTS REPORTING"][0] # last which isn't the overused OE
    rpcBPIs = sorted(rpcBPIByRPC.values(), key=lambda x: x)
    json.dump(rpcBPIs, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json", "w"), indent=4)
    
    print "Phase 2 {}: flushed BPIs of {:,} RPCs".format(stationNo, len(rpcBPIs))
    
"""
Add usage for RPC options using User (200) and Active User (user with signon).

Background: just having options isn't enough - are they used?

NOTE: may flip properly --- SEE REPORT ie/ per RPC, show its options and only 
have RPCs that have an option ie/ RPC centric ala BPI
"""
def reduceRPCOptionByUse(stationNo):
    
    print "Reducing RPC Options using all users and active users"
    rpcOptionsReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_19Reduction.json"))
    rpcOptions = set(red["label"] for red in rpcOptionsReduction)
    print "... start with {} RPC Options".format(len(rpcOptions))
    
    signedOnUsersReduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_3_081UserReduction.json"))
    signedOnUserIds = set(red["userId"] for red in signedOnUsersReduction)
    
    # See if user has a recent login (3.081)
    _3_081ResourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "3_081")
    userSignOnCount = Counter()
    for i, _3_081Resource in enumerate(_3_081ResourceIter, 1):    
        if (i % 10000) == 0:
            print "\tprocessed another {} sign ons, now {} users seen".format(i, len(userSignOnCount))
        userSignOnCount[_3_081Resource["user"]["id"]] += 1
    print "... {} users signed on".format(len(userSignOnCount))
    
    primariesCount = Counter()
    primariesActiveCount = Counter()
    secondariesCount = Counter()
    secondariesActiveCount = Counter()
    print "Walking all Users looking for Options ..."
    _200ResourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "200")
    for i, _200Resource in enumerate(_200ResourceIter, 1):
        if (i % 1000) == 0:
            print "\tprocessed another {} users, now {} secondaries seen".format(i, len(secondariesCount))
        if "primary_menu_option" in _200Resource:
            pmoLabel = _200Resource["primary_menu_option"]["label"]
            if pmoLabel in rpcOptions:
                primariesCount[pmoLabel] += 1
                if _200Resource["_id"] in userSignOnCount:
                    primariesActiveCount[pmoLabel] += 1
        if "secondary_menu_options" in _200Resource:
            for entry in _200Resource["secondary_menu_options"]:
                smoLabel = entry["secondary_menu_options"]["label"]
                if smoLabel in rpcOptions:
                    secondariesCount[smoLabel] += 1
                    if _200Resource["_id"] in userSignOnCount:
                        secondariesActiveCount[smoLabel] += 1
    print "Saw {} primaries, {} active".format(len(primariesCount.keys()), len(primariesActiveCount))
    print "Saw {} secondaries, {} active".format(len(secondariesCount.keys()), len(secondariesActiveCount))
    
    # Add in information
    optionsUsed = set()
    optionsUsedRecently = set()
    for red in rpcOptionsReduction:
        if red["label"] in primariesCount:
            red["isPrimaryOfUser"] = True
            optionsUsed.add(red["label"])
        if red["label"] in primariesActiveCount:
            red["isPrimaryOfActiveUser"] = True
            optionsUsedRecently.add(red["label"])
        if red["label"] in secondariesCount:
            red["isSecondaryOfUser"] = True
            optionsUsed.add(red["label"])
        if red["label"] in secondariesActiveCount:
            red["isSecondaryOfActiveUser"] = True
            optionsUsedRecently.add(red["label"])
    
    print "Flushing Option Reduction with usage - out of {}, {} are marked as used and {} are marked as used recently (\"Active\")".format(len(optionsUsed), len(optionsUsedRecently))
    json.dump(rpcOptionsReduction, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_rpcOptionsWithUsage.json", "w"), indent=4)
    
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    """
    redResults = {}
    reduce3_081(stationNo, redResults)
    reduce200(stationNo, redResults)
    print redResults
    # reduceRPCOptionByUse(stationNo)
    return
    """
    
    reduceVistAData(stationNo)

if __name__ == "__main__":
    main()
