#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from collections import defaultdict

"""
CRUDE DUMPS on rpcsCategorized.js BEFORE doing more formal .md reports
"""

def reportCategorized():
    rpcsCategorized = json.load(open("json/rpcsCategorized.json"))
    print
    print "Categorized RPC Total:", len(rpcsCategorized)
    byCatag = defaultdict(int)
    byTag = defaultdict(int)
    inDemoByDivision = defaultdict(set)
    for rpcName in rpcsCategorized:
        byCatag[rpcsCategorized[rpcName]["catag"]] += 1
        if "tags" not in rpcsCategorized[rpcName]:
            byTag["<NONE>"] += 1
            continue
        for tag in rpcsCategorized[rpcName]["tags"]:
            # in demo means has been P tagged
            if re.match(r'P\d', tag):
                inDemoByDivision[rpcsCategorized[rpcName]["division"]].add(rpcName)
            byTag[tag] += 1
    print
    print "Operation Type:"
    for i, catag in enumerate(byCatag, 1):
        j = 15 if i < 10 else 14
        k = 5
        print (str(i) + ".").ljust(k), catag.ljust(j), str(byCatag[catag]).ljust(k), str((byCatag[catag] * 100) / len(rpcsCategorized)) + "%"
    print
    print "Clinical/ NC/ Out of Scope:"
    for division in ["OUT OF SCOPE", "CLINICAL", "NON CLINICAL", "AUTHENTICATION"]:
        divsum = sum(1 for rpcName in rpcsCategorized if rpcsCategorized[rpcName]["division"] == division)
        print division, str((divsum * 100) / len(rpcsCategorized)) + "%" 
    print
    print "Tags (same RPC may be in many):"
    for i, tag in enumerate(byTag, 1):
        j = 15 if i < 10 else 14
        k = 5
        print (str(i) + ".").ljust(k), tag.ljust(j), str(byTag[tag]).ljust(k), str((byTag[tag] * 100) / len(rpcsCategorized)) + "%"
    print
    print "In demo by Division"
    for i, div in enumerate(inDemoByDivision, 1):
        print i, div, len(inDemoByDivision[div])
        print "\t", ",".join(sorted(list(inDemoByDivision[div])))
        print
    print
            
    
"""
Used for VDM slicing - VDM Non Clinical

... will keep growing as file definitions in NonClinicalRPCs expand
"""
def dumpNonClinicalFiles():
    files = set()
    rpcsCategorized = json.load(open("json/rpcsCategorized.json"))
    for rpcName in rpcsCategorized:
        rpcInfo = rpcsCategorized[rpcName]
        if rpcInfo["division"] != "NON CLINICAL":
            continue
        if "files" not in rpcInfo:
            continue
        files |= set(rpcInfo["files"])
    files = sorted(list(files))
    print "Non Clinical files", json.dumps(files)

"""
Used for meta data for CPOE/Order

... will keep growing as file definitions expand
... bonus: dumps parameters too if any

Note: put into Order Issue 
"""
def dumpOrderMetaFilesPlus():
    files = set()
    parameters = set()
    rpcsIfArgs = {}
    rpcsCategorized = json.load(open("json/rpcsCategorized.json"))
    rpcMethodInfos = json.load(open("json/rpcMethodInfos.bjsn"))
    for rpcName in rpcsCategorized:
        rpcInfo = rpcsCategorized[rpcName]
        if rpcInfo["division"] != "NON CLINICAL":
            continue
        if "files" not in rpcInfo:
            continue
        tfiles = [fl for fl in rpcInfo["files"] if float(fl) > 99 and float(fl) < 110]
        if not len(tfiles):
            continue
        if "parameters" in rpcInfo:
            parameters |= set(rpcInfo["parameters"])        
        files |= set(tfiles)
        rpcMethodInfo = rpcMethodInfos[rpcName]
        rpcsIfArgs[rpcName] = True if "args" in rpcMethodInfo else False 
    files = sorted(list(files), key=lambda x: float(x))
    print
    print "Order File and Parameter Info from Meta Data RPC Method Infos"
    print
    print "\tOrder Non Clinical files [100-><110] (%d): %s" % (len(files), json.dumps(files))
    print
    print "\tUse Parameters (%d): %s" % (len(parameters), json.dumps(sorted(list(parameters))))
    print
    print "\tIn RPCs (%d):" % len(rpcsIfArgs)
    woArgs = sorted([rpcName for rpcName in rpcsIfArgs if not rpcsIfArgs[rpcName]])
    print "\t\tWithout Args (%d): %s" % (len(woArgs), json.dumps(woArgs)) 
    wArgs = sorted([rpcName for rpcName in rpcsIfArgs if rpcsIfArgs[rpcName]])
    print "\t\tWith Args (%d): %s" % (len(wArgs), json.dumps(wArgs)) 
    print

"""
Generate Non Clinical Run in JS

REM: doesn't fill in arguments so those RPCs with arguments will probably (unless
optional) return errors. Other RPCs will return nothing. Both are tracked. 

Idea is to change this file manually until tests pass and to fill in meta so there
are no [] returns.

Let's you create sub test files based on tags and categories.
"""
def generateNonClinicalJSTestCode(catag="", needTags=None, excludeTags=None, testFileName="rpc_nc_generated_run"):

    rpcsCategorized = json.load(open("json/rpcsCategorized.json"))
    rpcMethodInfos = json.load(open("json/rpcMethodInfos.bjsn"))

    def comment(lines):
        cmu = "/*\n"
        for line in lines:
            cmu += " * " + line + "\n"
        return cmu + " */\n"

    def runner(i, rpcName, exArgs="", args=[], files=[], descr="", tags=[], parameters=[]):
        mu = "try {\n"
        mu += "    rpcName = \"" + rpcName + "\";\n" 
        mu += "    console.log(\"\\n\\n%d. %s\", " + str(i) + ", rpcName);\n"
        if args:
            mu += "    console.log(\"Arguments:\"" + ", \"" + ", ".join(args) + "\"" + ");\n"      
        if descr:
            mu += "    console.log(\"Description: \", \"" + re.sub(r'"', "'", descr) + "\");\n"
        if len(tags):
            mu += "    console.log(\"Tags:\"" + ", \"" + ", ".join(tags) + "\"" + ");\n"
        if len(files):
            mu += "    console.log(\"Files:\"" + ", \"" + ", ".join(files) + "\"" + ");\n"
        if len(parameters):
            mu += "    console.log(\"Parameters:\"" + ", \"" + ", ".join(parameters) + "\"" + ");\n"
        if len(exArgs):
            mu += "    console.log(\"Example argument(s): " + re.sub(r'"', "'", exArgs) + "\");\n"
            mu += "    exArgs = " + exArgs + ";\n"
            mu += "    res = rpcRunner.run(rpcName, exArgs);\n"
        else:
            mu += "    res = rpcRunner.run(rpcName);\n"
        mu += "    console.log(\"Reply: \");\n"
        mu += "    if (Array.isArray(res.result)) {\n"
        mu += "        if (res.result.length === 0) {\n"
        mu += "            emptyArrayResult += 1;\n"
        mu += "            console.dir(res, { depth: null, colors: false });\n"
        mu += "        }\n"
        mu += "        else if (res.result.length > 10) {\n"
        mu += "            console.dir(res.result.slice(0, 9), { depth: null, colors: false });\n"
        mu += "            console.log(\"... only first 10 shown\");\n"
        mu += "        }\n"
        mu += "        else\n"
        mu += "            console.dir(res, { depth: null, colors: false });\n"
        mu += "    }\n"
        mu += "    else if (res.result === \"\") {\n"
        mu += "        emptyStringResult += 1;\n"
        mu += "        console.dir(res, { depth: null, colors: false });\n"
        mu += "    }\n"
        mu += "    else {\n"
        mu += "        console.dir(res, { depth: null, colors: false });\n"
        mu += "    }\n"        
        mu += "}\ncatch(e) {\n"
        mu += "    console.log(\"Exception (bad arguments?): \", e);\n";
        mu += "    exceptionResult += 1;\n"
        mu += "}\n"
        mu += "console.log(\"\\n\\n\\n\");\n"
        mu += "\n\n\n"
        return mu

    def byMNDescr(rpcsCategorized):
        byMN = defaultdict(list)
        for rpcName in rpcsCategorized:
            byMN[rpcName.split(" ")[0]].append(rpcName)
        byMND = [] 
        for j, mn in enumerate(sorted(byMN.keys()), 1):
            byMND.append("\t" + str(j) + ". " + mn + " (" + str(len(byMN[mn])) + ")")
        return byMND 

    relevantRPCs = []
    for rpcName in sorted(rpcsCategorized.keys()):
        if "tags" not in rpcsCategorized[rpcName]:
            continue
        if rpcsCategorized[rpcName]["division"] != "NON CLINICAL":
            continue
        if catag and rpcsCategorized[rpcName]["catag"] != catag:
            continue
        if needTags and len(set(needTags) - set(rpcsCategorized[rpcName]["tags"])):
            continue
        if excludeTags and len(set(excludeTags) & set(rpcsCategorized[rpcName]["tags"])):
            continue
        relevantRPCs.append(rpcName)

    i = 0
    mu = "#!/usr/bin/env node\n\n"
    mu += comment(["Total: " + str(len(relevantRPCs)), "... by mneumonic ...", ""] + byMNDescr(relevantRPCs))  
    mu += """

var util = require('util');
var nodem = require('nodem');
// NB: ** MAY NEED TO CHANGE THIS PATH DEPENDING ON WHERE YOU RUN FILE **
var RPCRunner = require('../../VDM/prototypes/rpcRunner').RPCRunner;
var vdmUtils = require('../../VDM/prototypes/vdmUtils');

process.env.gtmroutines = process.env.gtmroutines + ' ' + vdmUtils.getVdmPath();

process.on('uncaughtException', function(err) {
    db.close();

    console.error('Uncaught Exception:\\n', err, err.stack);

    process.exit(1);
});

var db = new nodem.Gtm();
db.open();

var rpcRunner = new RPCRunner(db);
var DUZ = 61; // fix the user
rpcRunner.initializeUser(DUZ);

var res, rpcName, exArgs;
var exceptionResult = 0;
var emptyArrayResult = 0;
var emptyStringResult = 0;

"""
    for i, rpcName in enumerate(relevantRPCs, 1):
        mn = rpcName.split(" ")[0]
        descr = rpcsCategorized[rpcName]["descr"] if "descr" in rpcsCategorized[rpcName] else ""
        descr = descr.encode('ascii', 'replace').decode()
        mu += comment([str(i) + ". " + rpcName])
        tags = rpcsCategorized[rpcName]["tags"] if "tags" in rpcsCategorized[rpcName] else []
        parameters = rpcsCategorized[rpcName]["parameters"] if "parameters" in rpcsCategorized[rpcName] else []
        files = rpcsCategorized[rpcName]["files"] if "files" in rpcsCategorized[rpcName] else []
        methodInfo = rpcMethodInfos[rpcName]
        args = methodInfo["args"] if "args" in methodInfo else []
        mu += runner(i, rpcName, rpcsCategorized[rpcName]["exArgs"] if "exArgs" in rpcsCategorized[rpcName] else "", args, files, descr, tags, parameters)
    mu += "db.close();\n"
    mu += "\n\nconsole.log(\"Exceptioned (of %d)\", exceptionResult);\n" % i 
    mu += "\n\nconsole.log(\"Empty Array (of %d)\", emptyArrayResult);\n" % i 
    mu += "\n\nconsole.log(\"Empty String (of %d)\", emptyStringResult);\n\n" % i 

    open("rpcTestJS/" + testFileName + ".js", "w").write(mu)
    print
    print
    print "... generated test in rpcTestJS/" + testFileName + ".js"
    print
    print

def main():

    reportCategorized()
    return
    dumpNonClinicalFiles()
    dumpOrderMetaFilesPlus()

    # Tests: will try in nonClinicalRPCs (just to get that going fully)
    # Do READ PARAMETER tests
    generateNonClinicalJSTestCode("READ", ["PARAMETER"], ["FILE"], "rpc_nc_read_parameter_generated_run")
    # Do READ FILE tests
    generateNonClinicalJSTestCode("READ", ["FILE"], ["PARAMETER"], "rpc_nc_read_file_generated_run")
    # Do READ Both Tests
    generateNonClinicalJSTestCode("READ", ["FILE", "PARAMETER"], [], "rpc_nc_read_fileparameter_generated_run")

if __name__ == "__main__":
    main()
