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

    redResults = json.load(open("redResults.json"))

    reduce8994(stationNo, redResults)
    
    reduce19(stationNo, redResults)
    
    reduce101_24(stationNo, redResults)
    
    reduce9_6(stationNo, redResults)
    
    reduce9_4(stationNo, redResults)
    
    json.dump(redResults, open("redResults.json", "w"), indent=4)
    
    print "\n# VistA Reductions (so far)\n"
    tbl = MarkdownTable(["Type", "Station No (Total/Reduction)"])
    for typeId in sorted(redResults):
        typeInfo = redResults[typeId]
        mu = ", ".join(["{} ({})".format(sNo if sNo != "999" else "FOIA", "{:,} / {:,}".format(typeInfo[sNo]["total"], typeInfo[sNo]["reduced"]) if typeInfo[sNo]["total"] > typeInfo[sNo]["reduced"] else typeInfo[sNo]["reduced"]) for sNo in sorted(typeInfo)])
        tbl.addRow([typeId, mu])
    print tbl.md() + "\n"

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
    
        def reduce(self, resource):
            self.__reduction = OrderedDict()
            for prop in resource:
                if prop in ["label", "type"]:
                    continue
                if not hasattr(self, prop):
                    raise Exception("Unexpected 8994 property {}".format(prop))
                getattr(self, prop)(resource[prop])
            self.__noReduced += 1
            return self.__reduction
            
        def totalReduced(self):
            return self.__noReduced

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
    redResults["8994"][stationNo] = {"total": reducer.totalReduced(), "reduced": reducer.totalReduced()}
    
"""
{'qprop': 'rpc:rpc', 'fileName': u'RPC', 'topFileName': u'OPTION', 'topFileId': u'19', 'prop': u'rpc', 'fileId': u'19.05'}

Just for RPC options ie/ type_4 == B:Broker (Client/Server)

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
    
        def reduce(self, resource):
            self.__noSeen += 1
            if not ("type_4" in resource and resource["type_4"] == "B:Broker (Client/Server)"):
                return None
            self.__reduction = OrderedDict()
            SUPPRESS_PROPS = ["menu_text", "timestamp_of_primary_menu", "timestamp", "display_option", "delegable", "short_menu_text", "entry_action", "e_action_present", "xquit_message", "keep_from_deleting"]
            for prop in resource:
                if prop == "fmqlHasStops":
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

        # package - POINTER - 65 (43%) - 9_4
        # ... note: may get from name itself (compare)
        def package(self, value):
            self.__reduction["package"] = resource["package"]["label"]
                        
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
        
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_19Reduction.json", "w"), indent=4)
        
    if "19" not in redResults:
        redResults["19"] = {}
    redResults["19"][stationNo] = {"total": reducer.totalSeen(), "reduced": reducer.totalReduced()}
               
"""
Initially only doing if REMOTE PROCEDURE BUILD COMPONENT there but will expand ...
- Build Component REMOTE PROCEDURE and OPTION (focus on RPC Option) and ROUTINE (focus
  on entry routines for RPCs)
- files (for later)

Has HL7, Protocols etc etc too but of less interest for now

Note gives date of distribution. 9_7 gives installed or not and when.
""" 
def reduce9_6(stationNo, redResults):

    resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "9_6")
    
    class Reducer(object):
    
        BUILD_COMPONENTS_TO_REDUCE = {"REMOTE PROCEDURE": "rpcs", "OPTION": "options", "ROUTINE": "routines"}
    
        def __init__(self, installInfoByName):
            self.__installInfoByName = installInfoByName
            self.__noSeen = 0
            self.__noReduced = 0
    
        def reduce(self, resource):
            self.__noSeen += 1
            # only want if options, routines and remote procedures added
            if not ("build_components" in resource and sum(1 for entry in resource["build_components"] if entry["build_component"]["label"] in Reducer.BUILD_COMPONENTS_TO_REDUCE and "entries" in entry)):
                return None
            self.__reduction = OrderedDict()
            SUPPRESS_PROPS = ["alpha_beta_testing", "transport_build_number", "postinstall_routine", "delete_postinit_routine", "xpz1", "xpi1", "environment_check_routine", "xpo1", "preinstall_routine", "delete_env_routine", "delete_preinit_routine", "installation_message", "pretransportation_routine", "install_questions", "test", "global"] 
            for prop in resource:
                if prop == "fmqlHasStops":
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
            self.__processInstallInfo(value)
            
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
            deInstallIndexes = [i for i, iinfo in enumerate(installInfos) if iinfo["status"] == "4:De-Installed"]
            frmIndex = 0
            if len(deInstallIndexes):
                if deInstallIndexes[-1] == len(installInfos) - 1:
                    self.__reduction["isInstalled"] = False
                    return
                frmIndex = deInstallIndexes[-1]+1
            installInfos = [ii for ii in installInfos[frmIndex:] if ii["status"] == "3:Install Completed" and "install_complete_time" in ii]
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
            elif value == "2:GLOBAL PACKAGE":
                self.__reduction["isGlobalPackage"] = True
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
            
        # package_file_link - POINTER - 10,152 (94%) - 9_4
        def package_file_link(self, value):
            self.__reduction["package"] = value["label"]
                        
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
            
    """
    9_7 install is reduced for its install times/completeness
    """
    def reduce9_7(stationNo, redResults):
        resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "9_7")
        reductions = []
        redByName = defaultdict(list)
        print "Reducing 9_7 for {} - inside 9_6 reduction".format(stationNo)
        for i, resource in enumerate(resourceIter, 1):
            if (i % 1000) == 0:
                print "\tprocessing another 1000 9_7's"
            red = {
                "name": resource["name"],
                "status": resource["status"]
            }
            for prop in ["install_start_time", "install_complete_time"]:
                if prop in resource:
                    red[prop] = resource[prop]["value"]
            if "starting_package" in resource and resource["starting_package"]["id"] != resource["_id"]:
                red["isPartOf"] = True
            if "package_file_link" in resource:
                red["package"] = resource["package_file_link"]["label"]
            reductions.append(red)
        if "9_7" not in redResults:
            redResults["9_7"] = {}
        redResults["9_7"][stationNo] = {"total": i, "reduced": i}
        return reductions

    installInfoByName = defaultdict(list)
    for installInfo in reduce9_7(stationNo, redResults):
        installInfoByName[installInfo["name"]].append(installInfo)
    reducer = Reducer(installInfoByName)
    reductions = []
    print "Reducing 9_6 for {}".format(stationNo)
    for i, resource in enumerate(resourceIter, 1):
        if (i % 1000) == 0:
            print "\tprocessing another 1000 9_6's"
        reduction = reducer.reduce(resource)
        if reduction:
            reductions.append(reduction)
    print "\t... done after {:,}, {:,} reduced".format(reducer.totalSeen(), reducer.totalReduced())
        
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_6Reduction.json", "w"), indent=4)
        
    if "9_6" not in redResults:
        redResults["9_6"] = {}
    redResults["9_6"][stationNo] = {"total": reducer.totalSeen(), "reduced": reducer.totalReduced()}
    
    return reductions
    
"""
442: 310 ...

    prefix - LITERAL - 310 (100%)
    version - LIST - 274 (88%)
    current_version - LITERAL - 269 (87%)
    class - LITERAL - 197 (64%)
        I:National - 147 (74.6%)
        III:Local - 49 (24.9%)
        II:Inactive - 1 (0.5%)
    file - LIST - 176 (57%)

and 640: 343 ...

    prefix - LITERAL - 342 (100%)
    version - LIST - 296 (86%)
    current_version - LITERAL - 278 (81%)
    file - LIST - 181 (53%)
    class - LITERAL - 156 (45%)
        I:National - 112 (71.8%)
        III:Local - 43 (27.6%)
        II:Inactive - 1 (0.6%)
"""
def reduce9_4(stationNo, redResults):

    resourceIter = FilteredResultIterator(DATA_LOCN_TEMPL.format(stationNo), "9_4")

    # reducer = Reducer()
    reductions = []
    print "Reducing 9_4 for {}".format(stationNo)
    for i, resource in enumerate(resourceIter, 1):
        if (i % 1000) == 0:
            print "\tprocessing another 1000 9_4's"
        if "prefix" in resource:
            info = {"label": resource["name"], "prefix": resource["prefix"]}
        else:
            info = {"label": resource["name"]}
        reductions.append(info)
    
    json.dump(reductions, open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_9_4Reduction.json", "w"), indent=4)
        
    if "9_4" not in redResults:
        redResults["9_4"] = {}
    redResults["9_4"][stationNo] = {"total": i, "reduced": i}
    
    return reductions
    
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
   
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    reduceVistAData(stationNo)

if __name__ == "__main__":
    main()
