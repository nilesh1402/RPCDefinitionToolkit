"""
Create Markdown Document that breaks downs CPRS RPCs for work in Year 2.

TODO:
- in Clinical: JLV and eHMP as percentages (push VDP coverage)
- add a %locked to summary table (will take off csv based JSON) and put % on top of
each category's list ... and in TOC ... can give to Rafael ... LOCKED | PARTIAL LOCKED | NOT
- "GUI" tag for pure GUI ... want to highlight/isolate these from pure functionality
- MARKDOWN: link PARAMETER names out to nodeVISTA for parameter
"""

import os
import sys
import re
import json
from collections import defaultdict
from datetime import date

RPCS_METHODS = "json/rpcMethodInfos.bjsn"
RPCS_CATEGORIZED_JSON = "json/rpcsCategorized.json"
RPCS_EMULATED_SO_FAR = "json/rpcsEmulatedSoFar.json" # REGEN using reportEmulatedSoFar == js that requires models from MVDM

def buildMD():    

    rpcDetailsById = json.load(open(RPCS_CATEGORIZED_JSON))
    rpcEmulatedSoFarByDivision = json.load(open(RPCS_EMULATED_SO_FAR))
    rpcMethodsById = json.load(open(RPCS_METHODS))

    mu = """---
layout: default
title: VDP Year 2 - CPRS RPC Interface Breakdown TOC
---

"""
         
    mu += "# CPRS RPC Interface Breakdown\n\n"
    mu += "%d RPCs, %s locked, which divide into four groups ...\n\n" % (len(rpcDetailsById), reportAbsAndPercent(sum(1 for rpcName in rpcDetailsById if "RPCEMULATOR" in rpcDetailsById[rpcName]["tags"]), len(rpcDetailsById)))
    
    sliceMUTemplate = """---
layout: default
title: VDP Year 2 - CPRS RPC Interface, %s Slice Breakdown
---

"""
        
    tmu = "Name | Number\n--- | ---\n"
    # Basic breakdown + make slices
    for sliceName, sliceRPCs, sliceEmulated, sliceReporter in [
        ("Clinical", set(rpcName for rpcName in rpcDetailsById if rpcDetailsById[rpcName]["division"] == "CLINICAL"), rpcEmulatedSoFarByDivision["CLINICAL"], sectionClinicalSlice), 
        ("Non Clinical", set(rpcName for rpcName in rpcDetailsById if rpcDetailsById[rpcName]["division"] == "NON CLINICAL"), rpcEmulatedSoFarByDivision["NON CLINICAL"], sectionNonClinicalSlice), 
        ("Authentication", set(rpcName for rpcName in rpcDetailsById if rpcDetailsById[rpcName]["division"] == "AUTHENTICATION"), None, sectionAuthenticationSlice), 
        ("Out of Scope", set(rpcName for rpcName in rpcDetailsById if rpcDetailsById[rpcName]["division"] == "OUT OF SCOPE"), rpcEmulatedSoFarByDivision["OUT OF SCOPE"], sectionOutOfScopeSlice)
    ]:
        # For rel link: Name Name 2 (#) --> name-name2-#
        sliceReportName = "bd" + re.sub(r' ', '_', sliceName)
        tmu += "[%s](%s) | %s\n" % (sliceName, sliceReportName, reportAbsAndPercent(len(sliceRPCs), len(rpcDetailsById)))
        sliceRPCsOrdered = sorted(list(sliceRPCs))
        sliceMU = sliceMUTemplate % sliceName
        sliceRPCsEmulated = set() if sliceEmulated == None else set(sliceEmulated.keys())
        sliceMU += sliceReporter(sliceRPCsOrdered, sliceRPCsEmulated, rpcDetailsById, rpcMethodsById)
        open("markdowns/" + sliceReportName + ".md", "w").write(sliceMU)    
    tmu += "\n"
    
    # Table with Clinical etc breakdown
    mu += tmu 
            
    mu += "Most - %s - of the interface's RPCs _READ_ data.\n\n" % reportAbsAndPercent(sum(1 for rpcName in rpcDetailsById if rpcDetailsById[rpcName]["catag"] == "READ"), len(rpcDetailsById))
    
    mu += "\n\n\n\n" 

    mu += "<small>Generated on %s</small>" % date.today()
        
    open("markdowns/bdStart.md", "w").write(mu)
    
"""
Next for Clinical Breakdown:
0. ** SPLIT BETWEEN CPOE and NON CPOE ** (and note in Orders Issue)
1. MNs - correspond to Domains in some way ... mnToDomainMap ... domain COLUMN (must link to .md in prototypes section)
2. Extent of VPR covered here ie/ what's NOT here vs ...
3. Fill out files and parameters

"""
def sectionClinicalSlice(sliceRPCsOrdered, sliceRPCsEmulated, rpcDetailsById, rpcMethodsById):

    mu = "\n# [All](%s) &#8594; %s (%d)\n" % ("bdStart", "Clinical", len(sliceRPCsOrdered))

    # P tags => from capture and so in demo
    noWithPTags = sum(1 for rpcName in sliceRPCsOrdered if sum(1 for tag in rpcDetailsById[rpcName]["tags"] if re.match(r'P\d', tag)))
    noEmulated = sum(1 for rpcName in sliceRPCsOrdered if rpcName in sliceRPCsEmulated)
    mu += "\nIn Demo: __%s__" % reportAbsAndPercent(noWithPTags, len(sliceRPCsOrdered))
    mu += "\nEmulated so far: __%s__\n\n\n" % reportAbsAndPercent(noEmulated, noWithPTags) 
        
    mu += tableCategoryTotals(sliceRPCsOrdered, rpcDetailsById)
    
    mu += "\n\n"
    
    mu += muParameterFileCount(sliceRPCsOrdered, rpcDetailsById)
    
    mu += tableRPCs(sliceRPCsOrdered, rpcDetailsById, rpcMethodsById, ["DFN"])  
    mu += "\n\n\n\n"
    
    mu += "<small>Generated on %s</small>" % date.today()
    
    return mu
    
def muParameterFileCount(sliceRPCsOrdered, rpcDetailsById):

    mu = ""
    noParameters = len(set(parameter for rpcName in sliceRPCsOrdered if "parameters" in rpcDetailsById[rpcName] for parameter in rpcDetailsById[rpcName]["parameters"]))
    noFiles = len(set(file for rpcName in sliceRPCsOrdered if "files" in rpcDetailsById[rpcName] for file in rpcDetailsById[rpcName]["files"]))
    if noParameters or noFiles:
        mu = "These RPCs access at least %d parameters and %d files.\n\n" % (noParameters, noFiles) 
    return mu
        
"""
Next for NC Breakdown: complexity so LOW stand out
"""
def sectionNonClinicalSlice(sliceRPCsOrdered, sliceRPCsEmulated, rpcDetailsById, rpcMethodsById, title="Non Clinical"):
    mu = "\n# [All](%s) &#8594; %s (%d)\n\n" % ("bdStart", title, len(sliceRPCsOrdered))
                
    mu += "\n\n"
        
    mu += "Non Clinical RPCs (NC RPCs) don't affect a patient's medical record. In a phrase, they mainly 'get file data and parameter settings' and as they don't access patient data, their use needn't be monitored as closely as the Clinical RPCs - they don't involve HIPAA sensitive information.\n\n"
  
    mu += muParameterFileCount(sliceRPCsOrdered, rpcDetailsById)
    
    mu += "VDP will emulate NC RPCs exercised in the _VDP Demo_.\n"

    # P tags => from capture and so in demo
    noWithPTags = sum(1 for rpcName in sliceRPCsOrdered if sum(1 for tag in rpcDetailsById[rpcName]["tags"] if re.match(r'P\d', tag)))
    noEmulated = sum(1 for rpcName in sliceRPCsOrdered if rpcName in sliceRPCsEmulated)
    mu += "In Demo: __%s__" % reportAbsAndPercent(noWithPTags, len(sliceRPCsOrdered))
    mu += "\nEmulated so far: __%s__\n\n" % reportAbsAndPercent(noEmulated, noWithPTags)
            
    tmu = "\nName | Number | Seen in Demo | Emulated\n--- | --- | --- | ---\n"
    smu = ""
    for sliceName, sliceMN, sliceKeys, sliceDescr in [
        ("Parameter Only", "P", ["PARAMETER", "K/META"], "RPCs that ONLY access parameters and not files. A tag of DUZ means that they access per User data."), 
        ("File Only", "F", ["FILE", "K/META"], "RPCs that only access files and not parameters"), 
        ("Parameter and File", "PF", ["FILE", "PARAMETER", "K/META"], "RPCs that access parameters and files"),
        ("Other", "O", ["K/META"], "All other RPCs - don't access parameters or files. __Careful__ - in many cases these RPCs do use PARAMETERS/FILES but their definitions don't note that and so they end up (for now) in this table")
    ]:
        # take out by ID form
        sliceRPCs = [rpcName for rpcName in sliceRPCsOrdered if re.match(sliceMN + '\d+$', rpcDetailsById[rpcName]["id"])]
        
        # P tags => from capture and so in demo
        noWithPTags = sum(1 for rpcName in sliceRPCs if sum(1 for tag in rpcDetailsById[rpcName]["tags"] if re.match(r'P\d', tag)))
        
        # No emulated - of all emulated for slice 
        noEmulated = sum(1 for rpcName in sliceRPCs if rpcName in sliceRPCsEmulated) 
    
        #
        # Distinguish Demo Scope, Emulated
        # 
        # For rel link: Name Name 2 (#) --> name-name2-#
        sliceNameForRelLink = re.sub(r' ', '-', sliceName.lower()) + "-" + str(len(sliceRPCs))
        tmu += "[%s](#%s) | %s | __%s__ | __%s__\n" % (sliceName, sliceNameForRelLink, reportAbsAndPercent(len(sliceRPCs), len(sliceRPCsOrdered)), reportAbsAndPercent(noWithPTags, len(sliceRPCs)), reportAbsAndPercent(noEmulated, noWithPTags))
        
        # This section
        smu += "### %s (%d)\n\n" % (sliceName, len(sliceRPCs))
        smu += sliceDescr + ".\n\n"
        smu += tableCategoryTotals(sliceRPCs, rpcDetailsById)
        smu += "\n\n"
        smu += tableRPCs(sliceRPCs, rpcDetailsById, rpcMethodsById, sliceKeys, True)
        smu += "\n\n"
        
    tmu += "\n\n\n\n"
    mu += tmu
    mu += smu
    
    mu += "\n\n\n\n"
    
    mu += "<small>Generated on %s</small>" % date.today()
        
    return mu
    
def sectionAuthenticationSlice(sliceRPCsOrdered, sliceRPCsEmulated, rpcDetailsById, rpcMethodsById):
    mu = "\n# [All](%s) &#8594; %s (%d)\n\n" % ("bdStart", "Authentication", len(sliceRPCsOrdered))

    mu += "Authentication RPCs aren't locked over MVDM directly - they are implemented in rpcServer and rpcRunner.\n\n"

    mu += "\# | Name\n--- | ---\n"
    for i, rpcName in enumerate(sliceRPCsOrdered, 1):
        mu += "%s | %s\n" % (rpcDetailsById[rpcName]["id"], muRPCName(rpcName, rpcDetailsById))
    mu += "\n\n\n\n"
    
    mu += "<small>Generated on %s</small>" % date.today()
    
    return mu

"""
Formally OUT OF SCOPE
- PRINT
- REMOTE (CALLING) including MPI
- PATCH (CHECKING)
- REDACTED
"""    
def sectionOutOfScopeSlice(sliceRPCsOrdered, sliceRPCsEmulated, rpcDetailsById, rpcMethodsById):
    mu = "\n# [All](%s) &#8594; %s (%d)\n\n" % ("bdStart", "Out of Scope", len(sliceRPCsOrdered))

    mu += "We won't consider Print services and other system administration issues in VDP and so RPCs that deal with such concepts are out of scope. However, __we will formally isolate these RPCs in the _rpcServer_ before the end of year 2__.\n\n"

    mu += "\# | Name | Category | Tags\n--- | --- | --- | ---\n"
    for i, rpcName in enumerate(sliceRPCsOrdered, 1):
        tagsMU = ", ".join(sorted([tag for tag in rpcDetailsById[rpcName]["tags"] if tag != "OUT OF SCOPE"]))
        if tagsMU == "":
            tagsMU = "-"
        mu += "%s | %s | %s | %s\n" % (rpcDetailsById[rpcName]["id"], muRPCName(rpcName, rpcDetailsById), rpcDetailsById[rpcName]["catag"], tagsMU)
    mu += "\n\n\n\n"
    
    mu += "<small>Generated on %s</small>" % date.today()    

    return mu
    
def tableCategoryTotals(rpcs, rpcDetailsById, highlights=[]):
    byCategory = defaultdict(list)
    for rpcName in rpcs:
        byCategory[rpcDetailsById[rpcName]["catag"]].append(rpcName)
    mu = "Category | Number | Seen in Demo\n--- | --- | ---\n"
    for catag in sorted(byCategory):
        noInDemo = sum(1 for rpcName in byCategory[catag] if sum(1 for tag in rpcDetailsById[rpcName]["tags"] if re.match(r'P\d', tag)))
        mu += "%s | %s | __%s__\n" % ("__" + catag + "__" if catag in highlights else catag, reportAbsAndPercent(len(byCategory[catag]), len(rpcs)), reportAbsAndPercent(noInDemo, len(byCategory[catag])))
    mu += "\n\n\n"
    return mu
    
def tableRPCs(rpcs, rpcDetailsById, rpcMethodsById, excludeTags, highlightChange=False):

    NODEVISTAFILELINKTEMPL = "http://localhost:9000/schema/%s"
    def muFiles(rpcName, rpcDetailsById):
        if "files" not in rpcDetailsById[rpcName]:
            return ""
        filesMU = ""
        for i, file in enumerate(rpcDetailsById[rpcName]["files"]):
            fileLinkMU = "[" + file + "](" + (NODEVISTAFILELINKTEMPL % re.sub(r'\.', '_', file)) + ")"
            if i > 0:
                filesMU += ", "
            filesMU += fileLinkMU
        return filesMU

    def muParameters(rpcName, rpcDetailsById):
        return ", ".join(rpcDetailsById[rpcName]["parameters"]) if "parameters" in rpcDetailsById[rpcName] else ""

    mu = "" 

    mu += "\# | Name | Category | Args | Lines | Tags | Files | Parameters\n--- | --- | --- | --- | --- | --- | --- | ---\n"
    mn = ""
    # Force table to order by id and not name (note: will be the same in most cases)
    rpcs = sorted(rpcs, key=lambda x: int(re.sub(r'[A-Z]+', '', rpcDetailsById[x]["id"])))
    for i, rpcName in enumerate(rpcs, 1):
        tmn = rpcName.split(" ")[0]
        if not ((mn == "") or (mn == tmn)):
            mu += "&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;\n"
        mn = tmn
        catagMU = "__" + rpcDetailsById[rpcName]["catag"] + "__" if rpcDetailsById[rpcName]["catag"] == "CHANGE" and highlightChange else rpcDetailsById[rpcName]["catag"]
        mumpsLinkMU = "&nbsp;"
        mumpsArgsMU = "&nbsp;"
        mumpsNoLinesMU = "&nbsp;"
        if rpcName in rpcMethodsById:
            methodInfo = rpcMethodsById[rpcName]
            if "args" in methodInfo:
                mumpsArgsMU = ", ".join(methodInfo["args"])
            if "lines" in methodInfo:
                mumpsNoLinesMU = str(len(methodInfo["lines"]))
        # NOTE: parameters in rpcInfo come from parse in "improve" of methodInfos
        mu += "%s | %s | %s | %s | %s | %s | %s | %s\n" % (rpcDetailsById[rpcName]["id"], muRPCName(rpcName, rpcDetailsById), catagMU, mumpsArgsMU, mumpsNoLinesMU, tagsMU(rpcName, rpcDetailsById, excludeTags), muFiles(rpcName, rpcDetailsById), muParameters(rpcName, rpcDetailsById))
    return mu
    
def tagsMU(rpcName, rpcDetailsById, excluded):
    mu = ", ".join(sorted([tag for tag in rpcDetailsById[rpcName]["tags"] if tag not in excluded]))
    if mu == "":
        mu = "-"
    return mu
    
def checkDisallowedTags(rpcNames, rpcDetailsById, disallowedTags):
    disallowed = []
    for rpcName in rpcNames:
        for tag in disallowedTags:
            if tag in rpcDetailsById[rpcName]["tags"]:
                disallowed.append(rpcName)
    return disallowed
    
def percentageWithTag(rpcNames, rpcDetailsById, tag):
    return reportAbsAndPercent(sum(1 for rpcName in rpcNames if tag in rpcDetailsById[rpcName]["tags"]), len(rpcNames))

NATIVEDOCURLTEMPL = "http://vistadataproject.info/artifacts/devdocs/VISTARPC/%s"
def muRPCName(rpcName, rpcDetailsById):
    # link to native (8994 mainly) docs
    nameInURL = re.sub(r'\?', '%3F', rpcName)
    nameInURL = re.sub('[/|\s]', '_', nameInURL)

    muNameLink = "[" + rpcName + "](" + (NATIVEDOCURLTEMPL % nameInURL) + ")"
    # bold if locked or should be locked (ie/ if in demo)
    if sum(1 for tag in rpcDetailsById[rpcName]["tags"] if re.match(r'P\d', tag)):
        muNameLink = "__" + muNameLink + "__"
    return muNameLink

def reportAbsAndPercent(abs, total):
    return str(abs) + " (" + reportPercent(abs, total) + ")"

def reportPercent(piece, total):
    if not total: # can't divide by 0
        return "0%"
    return str(makePercent(piece, total)) + "%"

def makePercent(piece, total):
    fvalue = round((float(piece) * 100)/float(total), 1)
    return ('%f' % fvalue).rstrip('0').rstrip('.')

def main():
    buildMD()

if __name__ == "__main__":
    main()

