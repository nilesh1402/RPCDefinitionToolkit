#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime
import numpy

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

VISTA_RED_LOCN_TEMPL = "/data/vista/{}/RPCDefinitions/"
VISTA_REP_LOCN_TEMPL = "../Reports/PerVistA/{}/"

"""
Options subset RPCs named in 8994 and/or Builds:
- you can't invoke all but built-in RPCs without an option (broker option with RPC list)
- options may not be defined for any user or more particularly any recent/sign on user
... expect 15% reduction of build-named, active RPCs using "active, used option" inclusion
as a criteria.

KEY for REDUCING RPC LIST TO 'EFFECTIVE NUMBER OF ACTIVE, USED RPCs'
"""
def reportRPCOptions(stationNo):

    mu = """## RPC Options of {} 
    
Using _Active, Used RPC Options_ to subset 8994 and Build named RPCs. Expect a __15% reduction__ if we add a requirement that an RPC needs to belong to [1] an active option [2] belonging to a recently signed on user.
    
""".format(stationNo)

    if stationNo == "999":
        mu += "__Exception: with its inconsisent builds and 8994 and its lack of user sign ons and types, FOIA (999) does not follow a regular VistA pattern so many observations below don't apply to it.__\n\n" 
    
    # Raw RPC Broker Options to give # that don't have "rpcs" (purely for reporting)
    _19Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_19Reduction.json"))
    """
    Form: {"label": rpc, "options": [{"label" "isRemoved", sUsersCount, usersCount}]
    ... note: not ALL broker options as some have no RPCs (must get from raw 19)
                    and will flip to
          byOption: {"label" (option), ... "rpcs": []} 
    ie/ so options under rpcs and rpcs under options
    
    and then two sets: activeNUsedOptions and the RPCs of those options
    """
    rpcOptionsWithUse = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "rpcOptionsWithUse.json")) 
    rpcOptionInfoByLabel = {} # includes RPCs of options    
    for roi in rpcOptionsWithUse:
        rpc = roi["label"]
        for oi in roi["options"]:
            if oi["label"] not in rpcOptionInfoByLabel:
                rpcOptionInfoByLabel[oi["label"]] = oi # flip
                oi["rpcs"] = []
            rpcOptionInfoByLabel[oi["label"]]["rpcs"].append(roi["label"])
    activeUsedOptions = set(option for option in rpcOptionInfoByLabel if "isRemoved" not in rpcOptionInfoByLabel[option] and "sUsersCount" in rpcOptionInfoByLabel[option])
    rpcsOfActiveUsedOptions = set(rpc for option in activeUsedOptions for rpc in rpcOptionInfoByLabel[option]["rpcs"])
                            
    mu += """There are {:,} RPC Broker options, {:,} of which name __{:,}__ RPCs. {:,} of these options are marked 'deleted', leaving __{:,}__ of such option-backed RPCs. A further {:,} options are not assigned to an active, recently signed on user - of these, {:,} had older, no longer active users. When those without signed-on users are removed, we're left with __{}__ RPCs backed by __{:,}__ active options with users who recently signed on.
    
__Note__: options _{}_ require keys and {:,} options have Proxy Users - both need testing and analysis.
    
""".format(
        len(_19Reductions),
        len(rpcOptionInfoByLabel),
        len(rpcOptionsWithUse),
        
        sum(1 for option in rpcOptionInfoByLabel if "isRemoved" in rpcOptionInfoByLabel[option]),
        len(set(rpc for option in rpcOptionInfoByLabel if "isRemoved" not in rpcOptionInfoByLabel[option] for rpc in rpcOptionInfoByLabel[option]["rpcs"])),
        
        sum(1 for option in rpcOptionInfoByLabel if not ("isRemoved" in rpcOptionInfoByLabel[option] or "sUsersCount" in rpcOptionInfoByLabel[option])), 
        sum(1 for option in rpcOptionInfoByLabel if "usersCount" in rpcOptionInfoByLabel[option] and "sUsersCount" not in rpcOptionInfoByLabel[option]),
        
        reportAbsAndPercent(
            len(rpcsOfActiveUsedOptions), 
            len(rpcOptionsWithUse)
        ),
        len(activeUsedOptions),
        
        ", ".join(sorted(["\"{}\"".format(option) for option in rpcOptionInfoByLabel if "keyRequired" in rpcOptionInfoByLabel[option] and "sUsersCount" in rpcOptionInfoByLabel[option]])),
        sum(1 for option in rpcOptionInfoByLabel if "proxyUsersCount" in rpcOptionInfoByLabel[option])
        
    ) 
    
    """
    Let's see how many of these option RPCs are 
    """
    bpis = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_rpcBPIs.json"))
    _buildActiveRPCs = set(re.sub(r'\_', '/', bpi["label"]) for bpi in bpis if "isDeleted" not in bpi)
    _inOptionsButNotInBuilds = set(rpc for rpc in rpcsOfActiveUsedOptions if rpc not in _buildActiveRPCs) # few
    _inBuildsButNotOptions = set(rpc for rpc in _buildActiveRPCs if rpc not in rpcsOfActiveUsedOptions)
    _8994Reduction = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994Reduction.json"))
    _8994Labels = set(re.sub(r'\_', '/', red["label"]) for red in _8994Reduction) 
    _allBuildActiveAnd8994RPCs = _buildActiveRPCs.union(_8994Labels)
    _inOptionsButNot8994 = set(rpc for rpc in rpcsOfActiveUsedOptions if rpc not in _8994Labels)
    _in8994ButNotOptions = set(rpc for rpc in _8994Labels if rpc not in rpcsOfActiveUsedOptions)
    
    mu += """When compared to _Build RPCs_ and _8994 RPCs_:
    
  * Installed Builds name __{}__ RPCs not in used options while those options name __{:,}__ RPCs not in these Builds ({}).
  * 8994 defines __{}__ RPCs not in user options while those options name __{:,}__ RPCs not in 8994.
  
__Conclusion:__ _Used Options_ reduce the __{:,}__ RPCs named by both Builds and 8994s to __{}__.

""".format(
        reportAbsAndPercent(len(_inBuildsButNotOptions), len(_buildActiveRPCs)),
        len(_inOptionsButNotInBuilds), 
        ", ".join(["\"{}\"".format(rpc) for rpc in _inOptionsButNotInBuilds]),
    
        reportAbsAndPercent(len(_in8994ButNotOptions), len(_8994Labels)),
        len(_inOptionsButNot8994),
        
        len(_allBuildActiveAnd8994RPCs),
        reportAbsAndPercent(len(rpcsOfActiveUsedOptions), len(_allBuildActiveAnd8994RPCs))
    )

    # Show Active RPC Option details
    cols = ["Option", "RPC \#", "Exclusive RPC \#"]
    if stationNo != "999":
        cols.append("\# User / SO / SO0 / Proxy")
    tbl = MarkdownTable(cols)
    for option in sorted(activeUsedOptions, key=lambda x: len(rpcOptionInfoByLabel[x]["rpcs"]) if stationNo == "999" else rpcOptionInfoByLabel[x]["sUsersCount"], reverse=True):
        rpcsOfOtherOptions = set(rpc for ooption in activeUsedOptions if ooption != option for rpc in rpcOptionInfoByLabel[ooption]["rpcs"]) # of other ACTIVE/SO options!
        exclusiveRPCCount = sum(1 for rpc in rpcOptionInfoByLabel[option]["rpcs"] if rpc not in rpcsOfOtherOptions)
        row = ["__{}__".format(option), len(rpcOptionInfoByLabel[option]["rpcs"]), exclusiveRPCCount] 
        if stationNo != "999":
            optionInfo = rpcOptionInfoByLabel[option]
            userCountMU = optionInfo["usersCount"]
            _0SUsersCountMU = "{:,}".format(optionInfo["_0SUsersCount"]) if "_0SUsersCount" in optionInfo else "-"
            proxyUserCountMU = "{:,}".format(rpcOptionInfoByLabel[option]["proxyUsersCount"]) if "proxyUsersCount" in rpcOptionInfoByLabel[option] else "-"
            userCountMU = "{:,} / {:,} / {} / {}".format(userCountMU, optionInfo["sUsersCount"], _0SUsersCountMU, proxyUserCountMU)
            row.append(userCountMU)
        tbl.addRow(row)
    mu += "{:,} Active, SO User Options ...\n\n".format(len(activeUsedOptions))
    mu += tbl.md() + "\n\n"
           
    # Excluded Options, their RPCs, exclusive or otherwise 
    excludedOptions = set(option for option in rpcOptionInfoByLabel if "isRemoved" in rpcOptionInfoByLabel[option] or "sUsersCount" not in rpcOptionInfoByLabel[option])
    rpcsOfExcludedOptions = set(rpc for option in excludedOptions for rpc in rpcOptionInfoByLabel[option]["rpcs"])
    rpcsExclusiveToExcludedOptions = rpcsOfExcludedOptions - rpcsOfActiveUsedOptions
    tbl = MarkdownTable(["Option", "RPC \#", "E+E RPC \#", "(No SO) User \#", "Is Deleted"]) 
    for option in sorted(excludedOptions, key=lambda x: len(rpcOptionInfoByLabel[x]["rpcs"]), reverse=True):
        oInfo = rpcOptionInfoByLabel[option]
        userCountMU = oInfo["usersCount"] if "usersCount" in oInfo else ""
        isRemovedMU = "__YES__" if "isRemoved" in oInfo else ""
        exclusiveExcludedRPCCount = sum(1 for rpc in oInfo["rpcs"] if rpc in rpcsExclusiveToExcludedOptions)
        exclusiveExcludedRPCCountMU = exclusiveExcludedRPCCount if exclusiveExcludedRPCCount > 0 else ""
        tbl.addRow([option, len(oInfo["rpcs"]), exclusiveExcludedRPCCountMU, userCountMU, isRemovedMU])
    mu += "{:,} Excluded (removed or no SO User) Options with {:,} RPCs, {:,} of which don't appear in active options. Note that only a small minority of these options are formally deleted ...\n\n".format(len(excludedOptions), len(rpcsOfExcludedOptions), len(rpcsExclusiveToExcludedOptions))
    mu += tbl.md() + "\n\n"    
    
    mu += """__TODO__:

  * Enhance: Add Build data for options using option info in builds => see first introduction etc
  * Besides the CPRS option, pay attention to Active/SO options with a high proproportion of 0 users: MAG WINDOWS, CAPRI, MAGJ VISTARAD WINDOWS, KPA VRAM GUI, VPR APPLICATION PROXY
  * Focus on options with many 'Exclusive RPCs' like CAPRI, MAG DICOM VISA, YS BROKER1, R1SDCI and others which also have a highish number of users - unlike the OVERLAPPING options, these introduce whole new sets of RPCs
  * SO0 is responsible for most of the logins for many of the most significant SO's (MAG, KPA etc)
  * PROXY users (see user class in user reduction): see the proxy users count. If close to all then very special option
  * Implication of DELETING Excluded Options and their exclusive RPCs - reducing VistA size
  
"""
        
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcOptions.md", "w").write(mu) 

"""
RPC Option Details

TODO MORE:
- see effective # of non zero and zero RPC options (ie/ not if any one of them have one but many 0.25? do)
"""
def reportRPCOptionDetails(stationNo):

    if stationNo == "999":
        raise Exception("Can't support FOIA 999 as not enough representative sign ons")
    
    # Four inputs: users (with sign ons inside), RPC options, Apps and Options
    userInfos = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_200Reduction.json"))
    _19Reductions = json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_19Reduction.json"))
    rpcsOfOptions = dict((_19Reduction["label"], _19Reduction["rpcs"]) for _19Reduction in _19Reductions if "rpcs" in _19Reduction)
    remoteAppsAndOptions = dict((_8994_5Reduction["label"], _8994_5Reduction["option"]) for _8994_5Reduction in json.load(open(VISTA_RED_LOCN_TEMPL.format(stationNo) + "_8994_5Reduction.json")))
        
    moUserCounts = Counter()
    mo0UserCount = Counter()
    moNon0UserCount = Counter()
    qualifierMOUserCountByMO = defaultdict(lambda: Counter())
    moAloneUserCounts = Counter()
    menuOptionCombinationCounts = defaultdict(lambda: Counter()) # ie/ # of combos expected
    jmoUserCounts = Counter()
    cntSOUsers = 0
    cntSOUsersRPCOptions = 0
    cntSOUsersNoRPCOptions = 0
    cntNon0SOUsersRPCOptions = 0
    for userInfo in userInfos:
        if "signOnCount" not in userInfo:
            continue
        cntSOUsers += 1
        if "menuOptions" not in userInfo:
            raise Exception("Expect ALL signed on users to have at least one menu option")
        # Leaving in "userClasses"/ proxies
        userHasRPCMenuOption = False
        jMenuOptions = "/".join([mo for mo in sorted(userInfo["menuOptions"]) if mo in rpcsOfOptions])
        if jMenuOptions != "":
            jmoUserCounts[jMenuOptions] += 1
        for menuOption in userInfo["menuOptions"]:
            if menuOption not in rpcsOfOptions:
                continue
            if menuOption == "CG FMQL QP USER":
                continue
            moUserCounts[menuOption] += 1
            if "isCreatedBy0" in userInfo:
                mo0UserCount[menuOption] += 1
            else:
                moNon0UserCount[menuOption] += 1
            userHasRPCMenuOption = True
            combined = False
            for cmenuOption in userInfo["menuOptions"]:
                if cmenuOption not in rpcsOfOptions:
                    continue
                if cmenuOption == menuOption:
                    continue
                if cmenuOption == "CG FMQL QP USER":
                    continue
                qualifierMOUserCountByMO[menuOption][cmenuOption] += 1
                combined = True
            if not combined:
                moAloneUserCounts[menuOption] += 1
            else:
                menuOptionCombinationCounts[menuOption][len(userInfo["menuOptions"]) - 1] += 1
        # There are SO users with no RPC menu options (important subset!)
        if userHasRPCMenuOption:
            cntSOUsersRPCOptions += 1
            if "isCreatedBy0" not in userInfo:
                cntNon0SOUsersRPCOptions += 1
        else:
            cntSOUsersNoRPCOptions += 1
    pureAlones = set(mo for mo in moAloneUserCounts if float(moAloneUserCounts[mo])/float(moUserCounts[mo]) > 0.15)
    pureQualifierOptions = set(mo for mo in moUserCounts if mo not in moAloneUserCounts)
    otherQualifierOptions = set(mo for mo in moUserCounts if mo in moAloneUserCounts and float(moAloneUserCounts[mo])/float(moUserCounts[mo]) <= 0.15)
    allQualifierOptions = pureQualifierOptions.union(otherQualifierOptions)

    mu = """## RPC Options of {} Classified
    
Based on active (SO) users use.
    
""".format(stationNo)

    tbl = MarkdownTable(["Type", "\#"])
    tbl.addRow(["Users", len(userInfos)])
    tbl.addRow(["SO Users", cntSOUsers])
    tbl.addRow(["SO Users with RPC Options", cntSOUsersRPCOptions])
    tbl.addRow(["SO Users with other than RPC Options", cntSOUsersNoRPCOptions])
    tbl.addRow(["Zero SO Users w/RPC Options", cntSOUsersRPCOptions - cntNon0SOUsersRPCOptions])
    tbl.addRow(["Non Zero SO Users w/RPC Options", cntNon0SOUsersRPCOptions])
    tbl.addRow(["RPC Options", len(rpcsOfOptions)]) 
    tbl.addRow(["Used RPC Options", len(moUserCounts)])
    tbl.addRow(["Zero SO Users RPC Options", len(mo0UserCount)])
    tbl.addRow(["Non Zero SO Users RPC Options", len(moNon0UserCount)])
    tbl.addRow(["Pure Alone Options", len(pureAlones)])
    tbl.addRow(["Singleton Alone Options (NEVER COMBINED)", sum(1 for mo in moUserCounts if mo not in qualifierMOUserCountByMO)])
    tbl.addRow(["Pure Qualifier Options - NEVER on their own", len(pureQualifierOptions)])
    tbl.addRow(["Other Qualifier Options - < 15% on their own (so not _Pure Alones_)", len(otherQualifierOptions)])
    mu += tbl.md() + "\n\n"

    optionsWithGT1PRCTUsers = set(option for option in moUserCounts if float(moUserCounts[option])/float(cntSOUsersRPCOptions) > 0.01)
    mu += """Despite there being __{:,}__ employed RPC Options, only __{:,}__ are used by more than 1% of sign on users, the vast majority of which are remote/0 users.
    
""".format(len(moUserCounts), len(optionsWithGT1PRCTUsers))
    tbl = MarkdownTable(["Option", "Total Users", "0 Users", "Non 0 Users", "RPCs"])
    for mo in sorted(list(optionsWithGT1PRCTUsers), key=lambda x: moUserCounts[x], reverse=True):
        tbl.addRow([
            mo, 
            moUserCounts[mo],
            reportAbsAndPercent(mo0UserCount[mo], moUserCounts[mo]) if mo in mo0UserCount else "",
            reportAbsAndPercent(moNon0UserCount[mo], moUserCounts[mo]) if mo in moNon0UserCount else "",
            len(rpcsOfOptions[mo])
        ])
    mu += tbl.md() + "\n\n"
    
    mu += "The {:,} active Non zero users need separate consideration. The top non Zero user options - > 10% non Zeros have it - are listed below. Note that other than the mainstream options, most are highlighted as they are mainly in Non Zero users\n\n".format(cntNon0SOUsersRPCOptions)
    optionsWithGT10PRCTUsers = set(option for option in moNon0UserCount if float(moNon0UserCount[option])/float(cntNon0SOUsersRPCOptions) > 0.1)
    tbl = MarkdownTable(["Option", "Non 0 Users", "Of Total", "RPCs"])
    for mo in sorted(list(optionsWithGT10PRCTUsers), key=lambda x: moNon0UserCount[x], reverse=True):
        level = round(float(moNon0UserCount[mo])/float(moUserCounts[mo]), 2)
        tbl.addRow([
            "__{}__".format(mo) if level > 0.75 else mo, 
            reportAbsAndPercent(moNon0UserCount[mo], cntNon0SOUsersRPCOptions),
            level,
            len(rpcsOfOptions[mo])
        ])
    mu += tbl.md() + "\n\n"
    
    mu += "\nThere are {:,} _Pure Alones_, options that can exist on their own (> 15% of users with them have only them)\n\n".format(len(pureAlones))
    tbl = MarkdownTable(["Option", "Total Users", "0 Users", "Alone Users", "CPRS Combos", "Other Combos", "Quals", "Alone Quals", "Top Quals", "RPCs"])
    for i, mo in enumerate(sorted(list(pureAlones), key=lambda x: moUserCounts[x], reverse=True), 1):
        cntNonCPRSQuals = sum(jmoUserCounts[jmo] for jmo in jmoUserCounts if not re.search(r'OR CPRS GUI CHART', jmo) and jmo != mo and re.search(mo, jmo))
        thres = .1 if moUserCounts[mo] > 100 else .9
        topQualsMU = ""
        if mo in qualifierMOUserCountByMO:
            topQuals = sorted([cmo for cmo in qualifierMOUserCountByMO[mo] if float(qualifierMOUserCountByMO[mo][cmo])/float(moUserCounts[mo]) > thres], key=lambda x: qualifierMOUserCountByMO[mo][x], reverse=True)
            if len(topQuals):
                topQualsMU = ", ".join(["{} ({:,})".format(cmo, qualifierMOUserCountByMO[mo][cmo]) for cmo in topQuals])
        _0Level = float(mo0UserCount[mo])/float(moUserCounts[mo])
        tbl.addRow([
            "__{}__".format(mo) if _0Level > 0.5 else mo, # only highlight if a lot of 0's
            moUserCounts[mo],
            reportAbsAndPercent(mo0UserCount[mo], moUserCounts[mo]) if mo in mo0UserCount else "",
            reportAbsAndPercent(moAloneUserCounts[mo], moUserCounts[mo]),
            reportAbsAndPercent(
                qualifierMOUserCountByMO[mo]["OR CPRS GUI CHART"],
                moUserCounts[mo]
            ) if mo in qualifierMOUserCountByMO and "OR CPRS GUI CHART" in qualifierMOUserCountByMO[mo] else "",
            reportAbsAndPercent(
                cntNonCPRSQuals,
                moUserCounts[mo]
            ) if cntNonCPRSQuals > 0 else "",
            len(qualifierMOUserCountByMO[mo].keys()),
            reportAbsAndPercent(
                sum(1 for cmo in qualifierMOUserCountByMO[mo] if cmo in pureAlones),
                len(qualifierMOUserCountByMO[mo].keys())
            ),
            topQualsMU,
            len(rpcsOfOptions[mo])
        ])
    mu += tbl.md() + "\n\n"
    
    mu += """__Note__:
    
  * _KPA VRAM GUI_ belongs to __VistA Remote Access Management (VRAM) Graphical User Interface (GUI)__ according to this [patch](https://github.com/OSEHRA/VistA/blob/master/Packages/Kernel/Patches/XU_8.0_629/XU-8_SEQ-502_PAT-629.TXT). It has a 8995 application entry and seems to sync credentials from the VBA 'VistA' to a local VistA - check out the RPCs it allows. Note that half its users are stand alone while the rest use CAPRI and very few use CPRS. Note too that this option DOES NOT HAVE MANY QUALIFIERS (unlike other 'alones')
  * _MAGJ VISTARAD WINDOWS_ is a __VistARad__ option according [to](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf). Additionally, note that the _Rad/Nuc Med Personnel menu_ defines further user permissions (where stored?) and there are a series of security keys guarding actions. Note that this option DOES NOT HAVE MANY QUALIFIERS (unlike other 'alones')
  * _MAG WINDOWS_ for __VistA Imaging and Capture Software__ according to [this](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf). Note that ala Rad, there are keys to further restrict options.
  * _DSIY ABOVE PAR_ belongs to __Above PAR (APAR)__ by the [TRM](https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=7725)
  * _RMPR PURCHASE ORDER GUI_ is part of __PROSTHETICS PURCHASE ORDER GUI__
  * _OOP GUI EMPLOYEE_ is from __ASISTS__ which is being decommissioned in Jan 2019.
  
"""
    mu += "The balance of the \"Qualifier\" Options are defined at the end of this report.\n\n"
        
    # 8994_5 and use
    mu += "### File 8994_5 Applications and their options\n\n"
    mu += """File 8994_5 defines 'Remote Applications'. Each is given a (default) option. There are {:,} applications using/sharing {:,} options. Note that {:,} of these options are NOT RPC options and {:,} are not assigned to any active user. Note that _JLV_ (for now) lacks an entry here or its own option (it uses CPRS, CAPRI and VPR options). The following shows the applications by option ...
    
""".format(
        len(remoteAppsAndOptions),
        len(set(remoteAppsAndOptions.values())),
        
        sum(1 for option in set(remoteAppsAndOptions.values()) if option not in rpcsOfOptions),
        sum(1 for option in set(remoteAppsAndOptions.values()) if option not in moUserCounts)
    )
    byOption = defaultdict(list)
    for label, option in remoteAppsAndOptions.iteritems():
        byOption[option].append(label)
    tbl = MarkdownTable(["Option", "RPCs", "Users", "Applications"])
    for option in sorted(byOption):
        optionMU = "__{}__".format(option) if option in moUserCounts else option
        tbl.addRow([optionMU, "NO" if option not in rpcsOfOptions else "", moUserCounts[option] if option in moUserCounts else "", ", ".join(sorted(byOption[option]))])
    mu += tbl.md() + "\n\n"
    
    stats = {}
    for userInfo in userInfos:
        if "signOnCount" not in userInfo:
            continue
        if "menuOptions" not in userInfo:
            raise Exception("Expect ALL signed on users to have at least one menu option")
        # Leaving in "userClasses" / proxies
        rpcMOs = [mo for mo in userInfo["menuOptions"] if mo in rpcsOfOptions]
        if not len(rpcMOs):
            continue
        if "remoteApps" in userInfo["signOnDetails"]:
            for rapp in userInfo["signOnDetails"]["remoteApps"]:
                if rapp not in remoteAppsAndOptions:
                    raise Exception("New Unexpected Remote App {}".format(rapp)) 
        # for lbl, app, mo in appMOPairs:
        for app, mo in remoteAppsAndOptions.iteritems():
            lbl = app
            if lbl not in stats:
                stats[lbl] = {"moLabel": mo, "appLabel": app, "mo": set(), "app": set(), "app0User": 0}
            if mo in rpcMOs:
                stats[lbl]["mo"].add(userInfo["userId"])
            if "remoteApps" in userInfo["signOnDetails"] and app in userInfo["signOnDetails"]["remoteApps"]:
                stats[lbl]["app"].add(userInfo["userId"])
                if "isCreatedBy0" in userInfo:
                    stats[lbl]["app0User"] += 1 # note if app use by 0 user  
    tblRowCount = 0                  
    tbl = MarkdownTable(["App", "Option", "App Users", "App 0 Users", "App+MO", "!App MO", "App !MO"]) 
    for lbl in sorted(stats, key=lambda x: len(stats[x]["app"]), reverse=True):
        stat = stats[lbl]
        # clean if all mo and no app
        if len(stat["app"]) == 0:
            continue
        if float(len(stats[lbl]["mo"].intersection(stats[lbl]["app"])))/float(len(stats[lbl]["app"])) < 0.9:
            moAndAppMU = "{:,} [UNDER MATCH]".format(len(stats[lbl]["mo"].intersection(stats[lbl]["app"])))
        else:
            moAndAppMU = reportAbsAndPercent(len(stats[lbl]["mo"].intersection(stats[lbl]["app"])), len(stats[lbl]["app"]))
        moNoApp = len(stats[lbl]["mo"] - stats[lbl]["app"])
        moNoAppMU = "{:,} [APP-OPTION MATCH]".format(moNoApp) if float(moNoApp)/float(len(stat["app"])) < 0.1 else moNoApp
        row = [
            stat["appLabel"],
            stat["moLabel"],
            len(stat["app"]),
            reportAbsAndPercent(stat["app0User"], len(stat["app"])),
            moAndAppMU,
            moNoAppMU,
            len(stats[lbl]["app"] - stats[lbl]["mo"])
        ]
        tbl.addRow(row)
        tblRowCount += 1
    mu += """What 8994.5 applications are used? It's {:,} out of the {:,}. What option best matches an app - does the __presence of an option predict the use of a (8994.5) application?__ Note that even 8994.5 shows option sharing and such sharing is borne out in the table of signon and user information below.
    
The low counts in the _App !MO_ column shows that the apps are good indicators that an option is present but in general _!App MO_ shows many cases where an option is too broadly given (CPRS, MAG WINDOWS ...) to predict app use. _VRAM_ is the only clear exception though VISTARAD and its singular option is probably an exception too.

Note that _DVBA CAPRI GUI_ is the only _qualifier_ option here. It is actually a _stand alone_ but is always paired with _OR CPRS GUI CHART_ by the CAPRI-style setup code. It's high _!App MO_ count is because of this pairing which is used by JLV and other apps.
    
""".format(tblRowCount, len(remoteAppsAndOptions))
    mu += tbl.md() + "\n\n"
    
    # Back to Qualifier Details
    tblMU = MarkdownTable(["Option", "Total Users", "0 Users", "Others Quals", "Alone Quals", "Top Quals", "RPCs"]) 
    tblLU = MarkdownTable(["Option", "Total Users", "0 Users", "Others Quals", "Alone Quals", "Top Quals", "RPCs"]) 
    lessUsedThreshold = 30
    tblMUCount = 0
    tblLUCount = 0
    for i, mo in enumerate(sorted(list(allQualifierOptions), key=lambda x: moUserCounts[x], reverse=True), 1):
        row = [
            "__{}__".format(mo) if len(qualifierMOUserCountByMO[mo]) < moUserCounts[mo] else mo,
            moUserCounts[mo],
            reportAbsAndPercent(mo0UserCount[mo], moUserCounts[mo]) if mo in mo0UserCount else "",
            len(qualifierMOUserCountByMO[mo]),
            sum(1 for cmo in qualifierMOUserCountByMO[mo] if cmo in pureAlones)
        ]
        tcmus = []
        for cmo in sorted(qualifierMOUserCountByMO[mo], key=lambda x: qualifierMOUserCountByMO[mo][x], reverse=True): 
            level = round(float(qualifierMOUserCountByMO[mo][cmo]) / float(moUserCounts[mo]), 2)
            # want Alones or High Match
            if not (level > 0.25 or cmo in pureAlones):
                continue
            if level == 1:
                tcmu = "__{}__ (ALL)".format(cmo)
            elif cmo in moAloneUserCounts:
                tcmu = "__{}__ ({})".format(cmo, level)
            else:
                tcmu = "{} ({})".format(cmo, level)
            tcmus.append(tcmu)
        if len(tcmus) < len(qualifierMOUserCountByMO[mo]):
            tcmus.append("...")
        row.append(", ".join(tcmus))
        row.append(len(rpcsOfOptions[mo]))
        if moUserCounts[mo] < lessUsedThreshold:
            tblLU.addRow(row)
            tblLUCount += 1
            continue
        tblMU.addRow(row)
        tblMUCount += 1
    # Back to Qualifiers
    mu += "### {:,} Qualifier Option Details\n\n".format(tblMUCount + tblLUCount)
    mu += "There are {:,} more used (> {:,} users) qualifiers. Those with more users than other qualifiers are highlighted as are combinations with primary/alone options ...\n\n".format(tblMUCount, lessUsedThreshold)
    mu += tblMU.md() + "\n\n"
    mu += "There are {:,} less used (< {:,} users) qualifiers ...\n\n".format(tblLUCount, lessUsedThreshold)
    mu += tblLU.md() + "\n\n"
    
    byCombo = Counter()
    for userInfo in userInfos:
        if "signOnCount" not in userInfo:
            continue
        if "menuOptions" not in userInfo:
            continue
        # note: leaving in userClasses
        if sum(1 for mo in userInfo["menuOptions"] if mo in rpcsOfOptions) == 0:
            continue
        if "CG FMQL QP USER" in userInfo["menuOptions"]:
            continue
        if sum(1 for mo in userInfo["menuOptions"] if mo in moAloneUserCounts) == 0:
            combo = "/".join(sorted([mo for mo in userInfo["menuOptions"] if mo in moUserCounts]))
            byCombo[combo] += 1
        
    if len(byCombo):
        mu += """There are {:,} users w/o Alones - ie/ their 'apps' are option combos.
    
""".format(sum(byCombo[combo] for combo in byCombo))
        tbl = MarkdownTable(["Combination", "Users"])
        for combo in sorted(byCombo, key=lambda x: byCombo[x], reverse=True):
            tbl.addRow([combo, byCombo[combo]])
        mu += tbl.md() + "\n\n"
                    
    qualifiersWithoutAlones = [mo for mo in allQualifierOptions if sum(1 for cmo in qualifierMOUserCountByMO[mo] if cmo in moAloneUserCounts) == 0]
    if len(qualifiersWithoutAlones):
        mu += "__Note__: the following Qualifiers (ie/ not alones) are NOT combined with Alones: {}\n\n\n".format(", ".join(qualifiersWithoutAlones))
        
    open(VISTA_REP_LOCN_TEMPL.format(stationNo) + "rpcOptionDetails.md", "w").write(mu) 
    
    """
    # show combo overlaps
    
    for jmo in sorted(jmoUserCounts, key=lambda x: jmoUserCounts[x], reverse=True):
        shownJMO = False
        jmops = jmo.split("/")
        for ojmo in sorted(jmoUserCounts, key=lambda x: jmoUserCounts[x], reverse=True):
            if ojmo == jmo:
                continue
            ojmops = ojmo.split("/")
            jaccSim = jaccard_similarity(jmops, ojmops)
            if jaccSim > 0.7:
                if not shownJMO:
                    print
                    print jmo, jmoUserCounts[jmo]
                    shownJMO = True
                print "\t", ojmo, jaccSim, jmoUserCounts[ojmo]
    """
    
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2))) / float(len(s1.union(s2)))
            
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    reportRPCOptions(stationNo)
    reportRPCOptionDetails(stationNo)
        
if __name__ == "__main__":
    main()