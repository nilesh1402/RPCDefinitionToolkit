"""
Produces - rpcMethodInfos

Problem: original was deleted (stupid!). The following rebuilds it as needed. Right
now only covers cacheing files and parsing the first comment in methods by method name
(as needed a fix)

TODO: expand to cover complete methodInfo build.
"""
import urllib
import re
import json

def parseLeadingComment(methodLines):
    if len(methodLines) < 2:
        return
    lcLines = []
    for i, line in enumerate(methodLines, 1):
        if i == 1:
            continue
        if re.match(r' ;', line):   
            lcLines.append(line[2:]) # nix  ;
            continue
        break
    return lcLines
    
"""
"GMV USER": [" RPC: [GMV USER]", "", " Input parameters", "  1. RESULTS [Reference/Required] RPC Return array", "  2. OPTION [Literal/Required] RPC Option to execute", "  3. DATA [Literal/Required] Other data as required for call", ""]

NOTE: older pass of this on Cheyenne led to /data/cheyenne2011/JSONOLD, /data/cheyenne/JSONLDOLD - new caching is in JSON and is only NEW JSON (config set in cheyenne2011)
"""
        
def parseOutMethodLines(src):
    methodsByName = {}
    thismethod = ""
    for line in src.splitlines():
        if re.match(r'[A-Z]', line): # may be a method
            thismethod = line
            name = re.match(r'([A-Z\d]+)', line).group(1)
            methodsByName[name] = [thismethod]
            continue
        if not thismethod:
            raise Exception("Should always be in method (or header of file) by now")
        methodsByName[name].append(line)
    return methodsByName

OSEHRA_LOCATION_TEMPLATE = "http://code.osehra.org/dox/Routine_%s_source.html"
def parseSourceFromOSEHRAHTML(fileName):

    url = OSEHRA_LOCATION_TEMPLATE % fileName
    urlContent = urllib.urlopen(url).read()
    xmp = re.split("\<xmp [^\>]+\>", urlContent)[1].split("</xmp>")[0]
    
    return xmp

def main():
    lclsByRPCName = {}
    methodInfosByName = json.load(open("json/rpcMethodInfos.bjsn"))
    fileMethods = {}
    for rpcName in methodInfosByName:
        methodInfo = methodInfosByName[rpcName]
        if "leadingCommentLines" not in methodInfo:
            continue
        if methodInfo["file"] not in fileMethods:
            src = parseSourceFromOSEHRAHTML(methodInfo["file"])
            fileMethods[methodInfo["file"]] = parseOutMethodLines(src)
        methodLines = fileMethods[methodInfo["file"]][methodInfo["tag"]]
        lcls = parseLeadingComment(methodLines)
        if not len(lcls):
            raise Exception("Old one had lcls but this doesn't " + rpcName)
        lclsByRPCName[rpcName] = lcls
        methodInfosByName[rpcName]["leadingCommentLines"] = lcls
    print "Got lcls for ", len(lclsByRPCName)
    json.dump(methodInfosByName, open("rpcMethodInfos.bjsn", "w"), indent=4)
        
if __name__ == "__main__":
    main()
