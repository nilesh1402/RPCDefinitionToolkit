## RPC Interface Definition for 640
    
### Source Data Details

\# | File | Total | Count Processed
--- | --- | --- | ---
1 | 3.081 | 17,896,654 | 133,262
2 | 9.4 | 343 | 334
3 | 9.6 | 11,559 | 11,559
4 | 9.7 | 13,621 | 13,621
5 | 19 | 16,097 | 161
6 | 200 | 411,747 | 360,773
7 | 8994 | 5,381 | 5,381


### Basic Summary

There are __5,520__ RPCs, __4,487 (81.29%)__ of which are active. The first RPCs were distributed on _1996-04-14_, the last on _2018-05-22_. The last installation happened on _2018-06-19_.
    
RPCs are marked inactive in stages ...

\# | Stage | \# At/After
--- | --- | ---
1 | Total | 5,520
2 | 8994 Full Entry | 5,375
3 | Installed Build | 5,344
4 | Has currently used Active Option | 4,487


### RPC Distribution by Year
    
54 RPCs have no 'first distributed' date as their first builds lacked a date. Here is RPC distribution year by year, along with the small amount of deletion too. Note that only __135 (2.45%)__ RPCs are formally deleted though __1,033 (18.71%)__ should be.

\# | Year | Added \# | Deleted \# | Inactive \#
--- | --- | --- | --- | ---
1 | 2018 | 30 (0.55%) | &nbsp; | 3 (10.0%)
2 | 2017 | 177 (3.24%) | 1 | 7 (3.95%)
3 | 2016 | 869 (15.9%) | 13 | 136 (15.65%)
4 | 2015 | 185 (3.38%) | 5 | 51 (27.57%)
5 | 2014 | 78 (1.43%) | 3 | 4 (5.13%)
6 | 2013 | 268 (4.9%) | 3 | 30 (11.19%)
7 | 2012 | 138 (2.52%) | 1 | 56 (40.58%)
8 | 2011 | 182 (3.33%) | &nbsp; | 47 (25.82%)
9 | 2010 | 234 (4.28%) | &nbsp; | 83 (35.47%)
10 | 2009 | 289 (5.29%) | 1 | 19 (6.57%)
11 | 2008 | 162 (2.96%) | 4 | 14 (8.64%)
12 | 2007 | 131 (2.4%) | &nbsp; | 25 (19.08%)
13 | 2006 | 177 (3.24%) | 2 | 47 (26.55%)
14 | 2005 | 204 (3.73%) | 21 | 78 (38.24%)
15 | 2004 | 322 (5.89%) | 4 | 83 (25.78%)
16 | 2003 | 345 (6.31%) | 5 | 81 (23.48%)
17 | 2002 | 363 (6.64%) | 22 | 104 (28.65%)
18 | 2001 | 300 (5.49%) | 7 | 12 (4.0%)
19 | 2000 | 409 (7.48%) | 22 | 38 (9.29%)
20 | 1999 | 201 (3.68%) | 7 | 14 (6.97%)
21 | 1998 | 23 (0.42%) | 3 | 3 (13.04%)
22 | 1997 | 268 (4.9%) | &nbsp; | 36 (13.43%)
23 | 1996 | 111 (2.03%) | 11 | 27 (24.32%)


### MUMPS Routine Implementation
    
__5375__ RPCs are implemented in __1780__ separate MUMPS routines, while __145__ identified RPCs lack an implementation. The highest number of RPCs per routine is __129__ (_SDEC_), the median is __2.0__, the lowest is __1__. __1,434 (80.56%)__ routines implement only active RPCs, __281__ only inactive RPCs (candidates for deletion?), while __65__ implement a mix of active and inactive RPCs.

The (outliers) that implement the most RPCs are ...

\# | \# RPCs | Routine(s)
--- | --- | ---
1 | 129 | SDEC
2 | 43 | ORWTPP
3 | 39 | OREVNTX1
4 | 27 | ORQQPXRM, ORWGRPC, ORWPCE2
5 | 24 | ORWPCE
6 | 23 | ORWPT, ORWU
7 | 22 | ORQQCN2, VEJDATL
8 | 21 | ORWDX, __ORWTIU__ [INACTIVE], VIABRPC
9 | 20 | ORWLRR
10 | 19 | DSIUTL1, __SDOERPC__ [INACTIVE]
11 | 18 | DSIFCNS1
12 | 17 | DSIROI6
13 | 16 | DSIROI1, ORWDXA, RMIMRP
14 | 15 | __AXARDGUI__ [INACTIVE], __DSIQUTL9__ [INACTIVE], __NUPABCL2__ [INACTIVE]
15 | 14 | DVBAB1, __MAGDRPC1__ [INACTIVE], ORWDFH
16 | 13 | DSICXPR, DSIVXPR, __ORAM1__ [INACTIVE], ORQQCN1, ORQQPX, ORWDPS1, ORWDPS33, TIUSRVA


### Packages
    
_Package_ is a sometimes inconsistently used breakdown of VistA into a set of cooperating applications. All but __246 (4.46%)__ RPCs are assigned to __77__ different packages, __19__ of which only have _inactive_ RPCs and __36__ more have a mix of active and inactive RPCs. 

Those with at least one active RPC are - note ORDER ENTRY has a huge proportion which MAY be due to redundant/overlapping purposes of individual RPCs ...

\# | Package | First Distributed RPC | Active RPCs | Inactive RPCs
--- | --- | --- | --- | ---
1 | ORDER ENTRY/RESULTS REPORTING | 1997-12-17 | 957 | 51
2 | IMAGING | 1996-04-14 | 448 | 67
3 | VENDOR - DOCUMENT STORAGE SYS | 1999-07-12 | 304 | 55
4 | SCHEDULING | 1996-05-30 | 272 | 50
5 | DSIY APAR | 2016-08-17 | 286 | 8
6 | ENCODER PRODUCT SUITE (EPS) | 2005-11-04 | 210 | 7
7 | ADVANCED PROSTHETICS ACQUISITION TOOL (APAT) | 2016-08-30 | 215 | 1
8 | RELEASE OF INFORMATION - DSSI | 2003-01-28 | 133 | 23
9 | FEE BASIS CLAIMS SYSTEM | 2009-12-22 | 148 | 7
10 | TEXT INTEGRATION UTILITIES | 1997-06-20 | 120 | 4
11 | DENTAL | 2000-10-26 | 91 | 28
12 | MENTAL HEALTH | 2000-01-13 | 78 | 16
13 | VA CERTIFIED COMPONENTS - DSSI | 2003-01-06 | 79 | 11
14 | DSIT TELECARE RECORD MANAGER | 2003-08-12 | 67 | 22
15 | AUTOMATED MED INFO EXCHANGE | 2001-06-21 | 79 | 3
16 | CLINICAL CASE REGISTRIES | 2002-03-06 | 58 | 23
17 | INSURANCE CAPTURE BUFFER | 2008-01-14 | 75 | 5
18 | DSIB CARIBOU CLC SUITE | 2017-03-15 | 71 | &nbsp;
19 | SPINAL CORD DYSFUNCTION | 2010-09-14 | 66 | &nbsp;
20 | ASISTS | 2002-07-09 | 64 | 1
21 | PROSTHETICS | 2002-12-18 | 58 | &nbsp;
22 | SHIFT CHANGE HANDOFF TOOL | 2008-05-13 | 57 | &nbsp;
23 | MENTAL HEALTH SUITE, DSS INC. | 2009-01-30 | 54 | &nbsp;
24 | BAR CODE MED ADMIN | 1999-08-06 | 43 | 5
25 | EVENT CAPTURE | 2001-07-05 | 44 | &nbsp;
26 | VISTA INTEGRATION ADAPTER | 2016-02-12 | 42 | &nbsp;
27 | REGISTRATION | 2000-02-01 | 18 | 23
28 | KERNEL | 1996-05-24 | 23 | 14
29 | DSIQ - VCM | 2011-07-13 | 30 | 5
30 | RPC BROKER | 1996-05-24 | 19 | 14
31 | GEN. MED. REC. - VITALS | 2002-10-28 | 18 | 14
32 | VPS KIOSK | 2012-08-16 | 29 | &nbsp;
33 | CLINICAL PROCEDURES | 2003-05-29 | 19 | 5
34 | VISTALINK | 2003-09-30 | 11 | 11
35 | DATA BRIDGE | 2011-04-19 | 19 | 1
36 | FUNCTIONAL INDEPENDENCE | 2003-04-15 | 19 | &nbsp;
37 | CLINICAL REMINDERS | 2001-05-17 | 3 | 16
38 | PCE PATIENT CARE ENCOUNTER | 2014-04-24 | 1 | 18
39 | VISUAL AID FOR CLINIC APPOINTMENTS (VISN 20) | 2011-11-22 | 18 | &nbsp;
40 | DSIG | 2016-11-09 | 17 | &nbsp;
41 | VISUAL IMPAIRMENT SERVICE TEAM | 2003-02-18 | 4 | 13
42 | HEALTHEVET DESKTOP | 2004-01-16 | 12 | 4
43 | VBECS | 2009-04-23 | 14 | &nbsp;
44 | MOBILE SCHEDULING APPLICATIONS | 2016-08-25 | 12 | &nbsp;
45 | R1 SURGERY SCHEDULE VIEWER | 2012-07-13 | 11 | &nbsp;
46 | VA FILEMAN | 1997-04-07 | 10 | &nbsp;
47 | INTEGRATED BILLING | 2001-05-31 | 1 | 8
48 | PATIENT REPRESENTATIVE | 2007-01-24 | 6 | &nbsp;
49 | ELECTRONIC SIGNATURE | 2006-07-14 | 5 | &nbsp;
50 | QUASAR | 2003-10-27 | 4 | 1
51 | VIRTUAL PATIENT RECORD | 2011-08-04 | 2 | 2
52 | EMERGENCY DEPARTMENT | 2010-09-02 | 3 | &nbsp;
53 | REMOTE ORDER/ENTRY SYSTEM | 2003-09-26 | 1 | 2
54 | IFCAP | 2006-07-19 | 3 | &nbsp;
55 | CONSULT/REQUEST TRACKING | 1997-12-17 | 1 | 2
56 | INTEGRATED PATIENT FUNDS | 2007-02-06 | 2 | &nbsp;
57 | NATIONAL HEALTH INFO NETWORK | 2010-10-15 | 1 | &nbsp;
58 | CW GUIMAIL | 1999-09-20 | 1 | &nbsp;


The 'inactive-only' Packages are ...

\# | Package | First Distributed RPC | RPCs (Inactive)
--- | --- | --- | ---
1 | HEALTH MANAGEMENT PLATFORM | 2016-02-23 | 56
2 | NATIONAL VISTA SUPPORT | 2003-06-17 | 44
3 | PATIENT ASSESSMENT DOCUM | 2012-02-24 | 36
4 | CARE MANAGEMENT | 2004-01-16 | 31
5 | CAPACITY MANAGEMENT TOOLS | 2004-03-31 | 28
6 | MASTER PATIENT INDEX VISTA | 2002-07-12 | 21
7 | AUTOMATED INFO COLLECTION SYS | 1997-02-12 | 16
8 | REAL TIME LOCATION SYSTEM | 2016-05-26 | 13
9 | MY HEALTHEVET | 2006-07-18 | 8
10 | RADIOLOGY/NUCLEAR MEDICINE | 2010-06-03 | 7
11 | CLINICAL INFO RESOURCE NETWORK | 2002-06-07 | 6
12 | OUTPATIENT PHARMACY | 2017-10-24 | 3
13 | PAID | 2012-02-17 | 2
14 | TOOLKIT | 2008-11-21 | 2
15 | ONCOLOGY | 2011-08-09 | 1
16 | ENROLLMENT APPLICATION SYSTEM | 2007-11-27 | 1
17 | WOUNDED INJURED ILL WARRIORS | 2008-12-30 | 1
18 | NATIONAL DRUG FILE | 2010-02-12 | 1
19 | BENEFICIARY TRAVEL | 2013-02-03 | 1


