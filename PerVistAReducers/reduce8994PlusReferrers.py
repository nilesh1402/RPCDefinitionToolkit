#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict
from datetime import datetime

from fmqlutils.cacher.cacherUtils import FilteredResultIterator
from fmqlutils.reporter.reportUtils import MarkdownTable, reportAbsAndPercent
from fmqlutils.schema.reduceReportTypes import DATA_LOCN_TEMPL

VISTA_RPCD_LOCN_TEMPL = "/data/vista/{}/RPCDefinitions/"

"""
Each VistA has information about its RPC interface, mainly in FileMan files. One key
subset is VistA's own RPC i/f defn file 8994 and all files that refer to it.
"""

def reduce8994PlusReferrers(stationNo):

    redResults = json.load(open("redResults.json"))

    reduce8994(stationNo, redResults)
    
    reduce19(stationNo, redResults)
    
    reduce101_24(stationNo, redResults)
    
    json.dump(redResults, open("redResults.json", "w"), indent=4)
    
    print "# VistA Reductions (so far)\n"
    tbl = MarkdownTable(["Type", "Station No (Total/Reduction)"])
    for typeId in sorted(redResults):
        typeInfo = redResults[typeId]
        mu = ", ".join(["{} ({:,}/{:,})".format(sNo if sNo != "999" else "FOIA", typeInfo[sNo]["total"], typeInfo[sNo]["reduced"]) for sNo in sorted(typeInfo)])
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
        
    json.dump(reductions, open(VISTA_RPCD_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json", "w"), indent=4)
        
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
        
    json.dump(reductions, open(VISTA_RPCD_LOCN_TEMPL.format(stationNo) + "_19Reduction.json", "w"), indent=4)
        
    if "19" not in redResults:
        redResults["19"] = {}
    redResults["19"][stationNo] = {"total": reducer.totalSeen(), "reduced": reducer.totalReduced()}
    
"""
{'fileName': u'OE/RR REPORT', 'fileId': u'101.24', 'prop': u'rpc'}
"""
def reduce101_24(stationNo, redResults):
    pass
    
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    reduce8994PlusReferrers(stationNo)

if __name__ == "__main__":
    main()
