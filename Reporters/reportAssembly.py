#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from reportMonograph import reduceMonograph

from reportVistAData import VISTA_RED_LOCN_TEMPL, muRPCInterfaceDefinition

"""
fill in data sources + other stuff below (sources must move to /data and definitions

NOTE: big focus is suggestion of "DELETION/REMOVAL" of RPCs and CODE ... get those routines (total too) WHICH are exclusive to inactive RPCs, mixed and otherwise.
"""
def reportAssembly():
    
    rpcInterfaceDefinition = json.load(open("../Definitions/rpcInterfaceDefinition.bjsn"), object_pairs_hook=OrderedDict)
    
    mu = """## VA VistA RPC Interface Definition 
    
"""

    mu += muRPCInterfaceDefinition(rpcInterfaceDefinition)
    
    # Add in information on Sources
    cntSSOs = Counter()
    cntFromSSO = Counter()
    for defn in rpcInterfaceDefinition:
        for sso in defn["inVistAs"]:
            cntSSOs[sso] += 1
        cntFromSSO[defn["fromVistA"]] += 1
    mu += """### Source Information for Integrated Definition
    
The integrated interface definition combines RPC definitions from multiple real VistA and FOIA. Overall __{}__ RPCs are not in FOIA.

""".format(reportAbsAndPercent(len(rpcInterfaceDefinition) - cntSSOs["999"], len(rpcInterfaceDefinition)))
    tbl = MarkdownTable(["Station", "RPCs", "Definition Contribution"])
    for sso in sorted(cntSSOs):
        tbl.addRow([sso, cntSSOs[sso], cntFromSSO[sso]])
    mu += tbl.md() + "\n\n"
    
    print mu
    
    open("../Reports/rpcInterfaceDefinition.md", "w").write(mu) 

"""

definition of:

FOIA + COTS-stuff redacted + "uniques added by each VistA"

but now it has to be

 "common subset of real VistAs" + "uniques added by each VistA"
 
... DEFINING BASE VistA (goes into README)
 
REDO as WANT per VistA app/package etc (see grouping) and reflect first distrib and first installed 

------------------------------------
        
DSIC VA CERTIFIED COMPONENTS - DSSI ... common elements for others
DSIR RELEASE OF INFORMATION - DSSI
DSIF FEE BASIS CLAIMS SYSTEM
DSIT DSIT TELECARE RECORD MANAGER | YEP!
DSIV INSURANCE CAPTURE BUFFER <------------ don't see RPCs but let's see
DSIU MENTAL HEALTH SUITE, DSS INC. | YEP!
DSIH DATA BRIDGE <------------- DSIHH in Mono?
DSIQ DSIQ - VCM ie/ VistA Chemotherapy Manager | Yep!
DSII DSII - RX-FRAMEWORK
DSIG DSIG <------------ second unmatched in Mono
DSIY DSIY APAR | YEP!
DSIB DSIB Caribou CLC Suite <------- wow!! Caribou ... supposed to be DSIHH in mono!

No DSIP: Encoder Product Suite/EPS
No APAT / DSIVA

> The DSIG namespace and number-space resides within the VEJD namespace and
number-space assigned by the VA DBA.
                and
> V1.0 Initial build containing Routines and RPCs converted from the VEJD
namespace to the DSIG namespace.

Priority TODO for release README:
- RPCs with NO options => unavailable OR disabled?
- build info/install info for RPCs along with PKG (vista app) identity
  ie/ to put in context.
  ie/ to organize
- how many have unusual availability?

Others to report:
- emulated in VAM 1 (fixed defn) ... rem move to breath first
- reference param use #'s 
ie/ broad metrics for planning 

... TODO: move to separate reporter as a manifest / progress report
... will go along with RPC i/f improved docs

These RPCs are NOT in FOIA but are in VistAs available from VA

Key is DSS + others and aligning DSS's with their apps. Not all are in Monograph
but from TRM (ex/ Data Bridge) can see it too
"""
def oldReportNonFOIARPCs():

    definitionsByRPC = json.load(open("../Definitions/rpcInterfaceDefinition.bjsn"), object_pairs_hook=OrderedDict)
    
    rpcsByPrefix = defaultdict(list)
    for rpc in definitionsByRPC:
        prefix = rpc.split(" ")[0]
        rpcsByPrefix[prefix].append(rpc)
        
    foiaPrefixes = set(rpc.split(" ")[0] for rpc in definitionsByRPC if "999" in definitionsByRPC[rpc]["_vistas"])
    foiaOnlyPrefixes = set(rpc.split(" ")[0] for rpc in definitionsByRPC if "999" in definitionsByRPC[rpc]["_vistas"] and len(definitionsByRPC[rpc]["_vistas"]) == 1)    
    _640Prefixes = set(rpc.split(" ")[0] for rpc in definitionsByRPC if "640" in definitionsByRPC[rpc]["_vistas"])
    _640OnlyPrefixes = set(rpc.split(" ")[0] for rpc in definitionsByRPC if "640" in definitionsByRPC[rpc]["_vistas"] and len(definitionsByRPC[rpc]["_vistas"]) == 1)
    _442Prefixes = set(rpc.split(" ")[0] for rpc in definitionsByRPC if "442" in definitionsByRPC[rpc]["_vistas"])
    _442OnlyPrefixes = set(rpc.split(" ")[0] for rpc in definitionsByRPC if "442" in definitionsByRPC[rpc]["_vistas"] and len(definitionsByRPC[rpc]["_vistas"]) == 1)
    _442And640OnlyPrefixes = (_640Prefixes.intersection(_442Prefixes) - foiaPrefixes)

    
    mu = """
"""

    # TODO: may merge prefixes if in same options
    
    """
    Note: DSS/COTS RPCs
    
    Options are VEJD... and DSIHH DATABRIDGE and DSIU MENTAL HEALTH SUITE
    
    --- no match
    - APGK
    - AXVVA
    - CW
    - DSIB
    - DSIG
    ------
    - DSIHH ... DATABRIDGE
    - 
    
    A lot is DSS and VEJD
    
    """
    
    monRed = reduceMonograph()
    monAllNSs = monRed["allNamespaces"]    
    prefixByNamespace = defaultdict(list)
    for prefix in _442And640OnlyPrefixes:
        matched = ""
        for ns in sorted(monAllNSs, key=lambda x: len(x), reverse=True):
            if re.match(ns, prefix):
                matched = ns
                break
        if matched != "":
            prefixByNamespace[matched].append(prefix)
        else:
            prefixByNamespace[prefix].append(prefix)
    monRPCs = []
    VEJDRPCs = []
    extraDSIRPCs = []
    otherPrefixes = set()
    
    mu += "## Not in FOIA, in BOTH 442 and 640\n\n"
    totalRPCs = sum(len(rpcsByPrefix[prefix]) for prefix in _442And640OnlyPrefixes)
    mu += "{:,} prefixes are not in FOIA but in both 640 and 442 covering {:,} RPCs\n".format(len(_442And640OnlyPrefixes), totalRPCs)
    mu += "Reduces to {:,} if go on namespaces in monograph\n\n".format(len(prefixByNamespace))
    for i, namespace in enumerate(sorted(prefixByNamespace), 1):
        officialMMU = " - OFFICIAL MONO __{}__".format(", ".join(monRed["dssByNamespace"][namespace])) if namespace in monAllNSs else ""
        mu += "{} with {:,} prefixes{}\n\n".format(namespace, len(prefixByNamespace[namespace]), officialMMU)
        tbl = MarkdownTable(["RPC"])
        for prefix in sorted(prefixByNamespace[namespace]):
            for rpc in sorted(rpcsByPrefix[prefix]):
                onlyMU = ""
                if len(definitionsByRPC[rpc]["_vistas"]) == 1:
                    onlyMU = "Only {}".format(definitionsByRPC[rpc]["_vistas"][0])
                if "options" in definitionsByRPC[rpc]:
                    optionsMU = ", ".join(sorted(definitionsByRPC[rpc]["options"]))
                else:
                    optionsMU = ""
                tbl.addRow([rpc, onlyMU, optionsMU])
                if namespace in monAllNSs:
                    monRPCs.append(rpc)
                elif re.match(r'DSI', rpc):
                    extraDSIRPCs.append(rpc)
                elif re.match(r'VEJD', rpc):
                    VEJDRPCs.append(rpc)
                else:
                    otherPrefixes.add(prefix)
        mu += tbl.md() + "\n\n"     
    
    print mu
        
    print
    
    """
    1. a/c for other DSSs
        ... don't see but VEJD is DSS in general ... it seems to have being used across DSS prods until split up
        ... two extras beyond mono and TRM to work out!!! ... see Packages
        
        > The DSIG namespace and number-space resides within the VEJD namespace and
number-space assigned by the VA DBA.
                and
        > V1.0 Initial build containing Routines and RPCs converted from the VEJD
namespace to the DSIG namespace.

    in DSS package ie/ moved on
        
    2. a/c for other apps (see below ... seem special cls III? see in pkgs)
    
    Get from Packages next in 640/442!
    
    Only this from OSEHRA PKG:
        Try this artifact: https://code.osehra.org/dox/Packages_Namespace_Mapping.html
        Vendor - Document Storage Systems | VEJD
        ... link two for it. Integrated Billing (IB) and Prosthetics (RMPR, RMPO, RMPS)
    
    Mon RPC total 919 vs 1256
        VEJD + DSI Extra RPCs 93 ie 1101 leaving only 155
        
    Other Prefixes: ... want other apps for these
    
    - APGK, APGKCLC0: APGK ALL RPCS etc (some of these only in 442 but most common)
    APG is PHOENIX VAMC in OSEHRA
    
    - AXVVA: AXVVA VISUAL AID CLIN APPS ... is it? 
    https://www.va.gov/vdl/application.asp?appid=106
    VISN 20 in osehra pkg has AXV
    
    - CW: CW MAIL is it https://www.va.gov/vdl/application.asp?appid=85
      ... OSEHRA 
      ... has CW GUIMAIL CWMA
      
    - NVSS: NVSS SYSTEM MONITOR option - https://www.cdc.gov/nchs/nvss/index.htm?
       ... NATIONAL VISTA SUPPORT has NVS
       
    - R1ENING: R1ENING GUI CONTEXT
    - R1ENINU1: R1ENINU1 GUI CONTEXT
    - R1OREPI: R1OREPI GUI CONTEXT
    - R1SDCIP: R1SDCI
    - R1SRL: R1SRL OR SCHEDULE VIEWER
    - R1XUM: R1XUM MENUS
    
    ADD TO RPCs: SUBSCRIPTION availability ie/ all fields now
    
    DSIG could be: https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=6756 (grade of membership)
    """
    print "Mon RPC total", len(monRPCs), "vs", totalRPCs
    print "\tVEJD + DSI Extra RPCs", len(VEJDRPCs), "ie", len(monRPCs) + len(VEJDRPCs) + len(extraDSIRPCs), "leaving only", totalRPCs - (len(monRPCs) + len(VEJDRPCs) + len(extraDSIRPCs))
    print "\tOther RPCs have {} prefixes".format(len(otherPrefixes)), "--", sorted(list(otherPrefixes))
    
    """
    DSS
    
    DSIG, DSIB not monograph but should be?
    
    VEJDARM with 1 prefixes

\# | RPC
--- | ---
1 | VEJDARM CLAIM SCRUB USAGE RPT | &nbsp; | VEJD AUDIT REPORT MANAGER
2 | VEJDARM PING | &nbsp; | VEJD AUDIT REPORT MANAGER
3 | VEJDARM START | &nbsp; | VEJD AUDIT REPORT MANAGER
4 | VEJDARM STOP | &nbsp; | VEJD AUDIT REPORT MANAGER
5 | VEJDARM UPDATE | &nbsp; | VEJD AUDIT REPORT MANAGER


VEJDDM with 1 prefixes

\# | RPC
--- | ---
1 | VEJDDM ADD/DELETE QUEUE | &nbsp; | &nbsp;
2 | VEJDDM GET STATUS | &nbsp; | &nbsp;


VEJDDPT with 1 prefixes

\# | RPC
--- | ---
1 | VEJDDPT GET DEMO | &nbsp; | DSIF FEEBASIS, VEJD VG FOR QM MEDREC


VEJDENM with 1 prefixes

\# | RPC
--- | ---
1 | VEJDENM ALL REASONS | &nbsp; | VEJD AUDIT REPORT MANAGER
2 | VEJDENM GET ORIGINALS | &nbsp; | VEJD AUDIT REPORT MANAGER, VEJD PCE RECORD MANAGER
3 | VEJDENM GET REASONS | &nbsp; | VEJD AUDIT REPORT MANAGER, VEJD PCE RECORD MANAGER
4 | VEJDENM INACTIVE TOGGLE | &nbsp; | VEJD AUDIT REPORT MANAGER
5 | VEJDENM REPORT | &nbsp; | VEJD AUDIT REPORT MANAGER, VEJD PCE RECORD MANAGER

VEJDG with 1 prefixes

\# | RPC
--- | ---
1 | VEJDG TIU DOCUMENTS BY CONTEXT | &nbsp; | VEJDSAT TELECARE GIU, VEJDWPB CORE RPCS
    """
    
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))

    reportAssembly()

if __name__ == "__main__":
    main()