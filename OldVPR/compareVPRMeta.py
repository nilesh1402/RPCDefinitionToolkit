#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
from collections import defaultdict 
from fmqlutils.cacher.cacherUtils import FMQLReplyStore

FMDATADIR = "/data/vista/{}/Data/"
STATION_NOS = ["442", "640"]
TYPS = json.load(open("../Cacher/configs/chey0001VPRMetaExtra.json"))["included"]
EXPECT_SAME_OR_EXTRA = ["11", "10", "13", "21", "31", "408_32", "10_2"]

def checkIfSameOrExtra(s1, s2):
    iens1 = set(ien for ien in s1)
    iens2 = set(ien for ien in s2)
    if iens1 == iens2:
        result = "SAME"
        for ien in iens1:
            if s1[ien] != s2[ien]:
                print "\t{}: {} vs  {}".format(ien, s1[ien], s2[ien])
                result = "DIFFLABEL_SAMEIEN"
        return result
    for sA, sB in [(s1, s2), (s2, s1)]:
        if set(sA.keys()).issubset(set(sB.keys())):
            for ien in sA:
                if sA[ien] != sB[ien]:
                    return "DIFFLABEL_SUBSETIEN"
            return "SUBSET"
    return "DIFFERENT"

def compare():
    idsAndLabelsByTypBySSN = defaultdict(lambda: defaultdict(lambda: dict()))
    for typId in TYPS:
        for stationNo in STATION_NOS:
            fmDataDir = FMDATADIR.format(stationNo)
            fmqlReplyStore = FMQLReplyStore(fmDataDir)
            iter = fmqlReplyStore.iterator(onlyTypes=[typId])
            for reply in iter.next():
                for result in reply["results"]:
                    ien = result["_id"].split(":")[-1]
                    idsAndLabelsByTypBySSN[typId][stationNo][ien] = result["label"]

    for typId in idsAndLabelsByTypBySSN:
        print typId
        for ssn in idsAndLabelsByTypBySSN[typId]:
            print "\t", ssn, len(idsAndLabelsByTypBySSN[typId][ssn])
        print "... \tSame or Extra: {}".format(checkIfSameOrExtra(idsAndLabelsByTypBySSN[typId]["442"], idsAndLabelsByTypBySSN[typId]["640"])) 

compare()
