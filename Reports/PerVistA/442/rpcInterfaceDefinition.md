## RPC Interface Definition for 442
    
### Source Data Details

\# | File | Total | Count Processed
--- | --- | --- | ---
1 | 3.081 | 10,610,771 | 73,050
2 | 9.4 | 310 | 301
3 | 9.6 | 10,774 | 10,774
4 | 9.7 | 11,462 | 11,462
5 | 19 | 14,324 | 151
6 | 200 | 256,024 | 232,661
7 | 8994 | 5,239 | 5,239


### Basic Summary

There are __5,376__ RPCs, __4,458 (82.92%)__ of which are active. The first RPCs were distributed on _1996-05-24_, the last on _2017-12-13_. The last installation happened on _2018-03-01_.
    
RPCs are marked inactive in stages ...

\# | Stage | \# At/After
--- | --- | ---
1 | Total | 5,376
2 | 8994 Full Entry | 5,235
3 | Installed Build | 5,226
4 | Has currently used Active Option | 4,458


### RPC Distribution by Year
    
19 RPCs have no 'first distributed' date as their first builds lacked a date. Here is RPC distribution year by year, along with the small amount of deletion too. Note that only __134 (2.49%)__ RPCs are formally deleted though __918 (17.08%)__ should be.

\# | Year | Added \# | Deleted \# | Inactive \#
--- | --- | --- | --- | ---
1 | 2018 | 1 (0.02%) | &nbsp; | &nbsp;
2 | 2017 | 178 (3.32%) | 1 | 5 (2.81%)
3 | 2016 | 856 (15.98%) | 13 | 85 (9.93%)
4 | 2015 | 176 (3.29%) | 12 | 51 (28.98%)
5 | 2014 | 78 (1.46%) | 3 | 4 (5.13%)
6 | 2013 | 275 (5.13%) | 3 | 26 (9.45%)
7 | 2012 | 197 (3.68%) | 1 | 85 (43.15%)
8 | 2011 | 145 (2.71%) | &nbsp; | 18 (12.41%)
9 | 2010 | 247 (4.61%) | &nbsp; | 30 (12.15%)
10 | 2009 | 146 (2.73%) | 1 | 13 (8.9%)
11 | 2008 | 173 (3.23%) | 5 | 84 (48.55%)
12 | 2007 | 189 (3.53%) | 2 | 11 (5.82%)
13 | 2006 | 164 (3.06%) | 2 | 35 (21.34%)
14 | 2005 | 356 (6.65%) | 21 | 64 (17.98%)
15 | 2004 | 309 (5.77%) | 4 | 74 (23.95%)
16 | 2003 | 419 (7.82%) | 5 | 57 (13.6%)
17 | 2002 | 400 (7.47%) | 23 | 100 (25.0%)
18 | 2001 | 313 (5.84%) | 33 | 40 (12.78%)
19 | 2000 | 347 (6.48%) | 1 | 13 (3.75%)
20 | 1999 | 45 (0.84%) | 4 | 11 (24.44%)
21 | 1998 | 22 (0.41%) | &nbsp; | &nbsp;
22 | 1997 | 252 (4.7%) | &nbsp; | 35 (13.89%)
23 | 1996 | 69 (1.29%) | &nbsp; | 58 (84.06%)


### MUMPS Routine Implementation
    
__5235__ RPCs are implemented in __1727__ separate MUMPS routines, while __141__ identified RPCs lack an implementation. The highest number of RPCs per routine is __128__ (_SDEC_), the median is __2.0__, the lowest is __1__. __1,417 (82.05%)__ routines implement only active RPCs, __243__ only inactive RPCs (candidates for deletion?), while __67__ implement a mix of active and inactive RPCs.

The (outliers) that implement the most RPCs are ...

\# | \# RPCs | Routine(s)
--- | --- | ---
1 | 128 | SDEC
2 | 43 | ORWTPP
3 | 39 | OREVNTX1
4 | 27 | ORQQPXRM, ORWGRPC, ORWPCE2
5 | 24 | ORWPCE
6 | 23 | ORWPT, ORWU
7 | 22 | ORQQCN2, VEJDATL
8 | 21 | ORWDX, VIABRPC
9 | 20 | ORWLRR
10 | 19 | DSIUTL1, __SDOERPC__ [INACTIVE]
11 | 18 | DSIFCNS1
12 | 17 | DSIROI6
13 | 16 | DSIROI1, ORWDXA, RMIMRP
14 | 15 | __DSIQUTL9__ [INACTIVE], __NUPABCL2__ [INACTIVE]
15 | 14 | DVBAB1, __MAGDRPC1__ [INACTIVE], ORWDFH
16 | 13 | DSICXPR, DSIVXPR, ORAM1, ORQQCN1, ORQQPX, ORWDPS1, ORWDPS33, TIUSRVA, VANOD04


### Packages
    
_Package_ is a sometimes inconsistently used breakdown of VistA into a set of cooperating applications. All but __118 (2.19%)__ RPCs are assigned to __81__ different packages, __19__ of which only have _inactive_ RPCs and __39__ more have a mix of active and inactive RPCs. 

Those with at least one active RPC are - note ORDER ENTRY has a huge proportion which MAY be due to redundant/overlapping purposes of individual RPCs ...

\# | Package | First Distributed RPC | Active RPCs | Inactive RPCs
--- | --- | --- | --- | ---
1 | ORDER ENTRY/RESULTS REPORTING | 1997-12-17 | 993 | 15
2 | IMAGING | 2002-03-19 | 433 | 40
3 | VENDOR - DOCUMENT STORAGE SYS | 2001-03-12 | 262 | 61
4 | SCHEDULING | 1996-05-30 | 191 | 130
5 | DSIY APAR | 2016-08-17 | 286 | 8
6 | ENCODER PRODUCT SUITE (EPS) | 2005-11-04 | 210 | 7
7 | ADVANCED PROSTHETICS ACQUISITION TOOL (APAT) | 2016-08-30 | 215 | 1
8 | FEE BASIS CLAIMS SYSTEM | 2001-03-12 | 153 | 10
9 | RELEASE OF INFORMATION - DSSI | 2003-01-28 | 132 | 23
10 | TEXT INTEGRATION UTILITIES | 1997-06-20 | 120 | 4
11 | DENTAL | 2001-03-08 | 83 | 28
12 | MENTAL HEALTH | 2000-01-13 | 78 | 16
13 | VA CERTIFIED COMPONENTS - DSSI | 2003-02-03 | 79 | 11
14 | DSIT TELECARE RECORD MANAGER | 2005-04-25 | 67 | 22
15 | AUTOMATED MED INFO EXCHANGE | 2001-06-21 | 79 | 3
16 | CLINICAL CASE REGISTRIES | 2002-05-15 | 58 | 23
17 | INSURANCE CAPTURE BUFFER | 2008-01-14 | 75 | 5
18 | DSIB CARIBOU CLC SUITE | 2017-03-15 | 71 | &nbsp;
19 | SPINAL CORD DYSFUNCTION | 2010-09-14 | 66 | &nbsp;
20 | ASISTS | 2002-07-09 | 64 | 1
21 | PROSTHETICS | 2002-12-18 | 58 | &nbsp;
22 | HEALTH MANAGEMENT PLATFORM | 2016-02-23 | 40 | 16
23 | MENTAL HEALTH SUITE, DSS INC. | 2010-11-15 | 54 | &nbsp;
24 | NATIONAL VISTA SUPPORT | 2001-02-08 | 41 | 8
25 | BAR CODE MED ADMIN | 1999-08-06 | 43 | 5
26 | EVENT CAPTURE | 2001-07-05 | 44 | &nbsp;
27 | VISTA INTEGRATION ADAPTER | 2016-02-12 | 42 | &nbsp;
28 | REGISTRATION | 2000-02-01 | 19 | 21
29 | VA NURSING OUTCOMES DATABASE PROJECT | 2005-11-22 | 38 | &nbsp;
30 | KERNEL | 1996-05-24 | 24 | 11
31 | DSIQ - VCM | 2011-12-12 | 30 | 5
32 | RPC BROKER | 1996-05-24 | 20 | 13
33 | GEN. MED. REC. - VITALS | 2002-10-28 | 17 | 15
34 | VPS KIOSK | 2012-08-16 | 29 | &nbsp;
35 | DSIG | 2011-10-17 | 18 | 7
36 | CLINICAL PROCEDURES | 2004-05-21 | 14 | 10
37 | DATA BRIDGE | 2012-01-27 | 22 | 1
38 | VISTALINK | 2003-09-30 | 11 | 11
39 | FUNCTIONAL INDEPENDENCE | 2003-04-15 | 19 | &nbsp;
40 | CLINICAL REMINDERS | 2001-05-17 | 3 | 16
41 | PCE PATIENT CARE ENCOUNTER | 2014-04-24 | 14 | 5
42 | VISUAL AID FOR CLINIC APPOINTMENTS (VISN 20) | 2011-11-22 | 18 | &nbsp;
43 | VISUAL IMPAIRMENT SERVICE TEAM | 2003-02-18 | 4 | 13
44 | HEALTHEVET DESKTOP | 2004-01-16 | 12 | 4
45 | VBECS | 2009-04-23 | 14 | &nbsp;
46 | MOBILE SCHEDULING APPLICATIONS | 2016-08-25 | 12 | &nbsp;
47 | R5 VBA IMPORT TOOL | 2012-07-31 | 11 | &nbsp;
48 | R1 SURGERY SCHEDULE VIEWER | 2012-07-13 | 11 | &nbsp;
49 | VA FILEMAN | 1998-02-28 | 10 | &nbsp;
50 | INTEGRATED BILLING | 2001-05-31 | 1 | 8
51 | PATIENT REPRESENTATIVE | 2007-01-24 | 6 | &nbsp;
52 | ELECTRONIC SIGNATURE | 2006-07-14 | 5 | &nbsp;
53 | QUASAR | 2003-10-27 | 4 | 1
54 | VIRTUAL PATIENT RECORD | 2011-08-04 | 2 | 2
55 | EMERGENCY DEPARTMENT | 2010-09-02 | 3 | &nbsp;
56 | REMOTE ORDER/ENTRY SYSTEM | 2003-09-26 | 1 | 2
57 | IFCAP | 2007-04-27 | 3 | &nbsp;
58 | CONSULT/REQUEST TRACKING | 1997-12-17 | 1 | 2
59 | INTEGRATED PATIENT FUNDS | 2007-02-06 | 2 | &nbsp;
60 | ANU HS DOWNLOAD | 2000-11-08 | 1 | &nbsp;
61 | CW GUIMAIL | 2005-07-22 | 1 | &nbsp;
62 | NOIS | 1998-01-31 | 1 | &nbsp;


The 'inactive-only' Packages are ...

\# | Package | First Distributed RPC | RPCs (Inactive)
--- | --- | --- | ---
1 | SHIFT CHANGE HANDOFF TOOL | 2008-05-13 | 57
2 | PATIENT ASSESSMENT DOCUM | 2012-02-24 | 36
3 | CARE MANAGEMENT | 2004-01-16 | 31
4 | CAPACITY MANAGEMENT TOOLS | 2004-03-31 | 28
5 | MASTER PATIENT INDEX VISTA | 2002-07-12 | 21
6 | AUTOMATED INFO COLLECTION SYS | 1997-02-12 | 16
7 | REAL TIME LOCATION SYSTEM | 2016-05-26 | 13
8 | MY HEALTHEVET | 2006-07-18 | 8
9 | RADIOLOGY/NUCLEAR MEDICINE | 2010-06-03 | 7
10 | CLINICAL INFO RESOURCE NETWORK | 2002-06-07 | 6
11 | OUTPATIENT PHARMACY | 2017-10-24 | 3
12 | PAID | 2012-02-17 | 2
13 | TOOLKIT | 2008-11-21 | 2
14 | ONCOLOGY | 2011-08-09 | 1
15 | ENROLLMENT APPLICATION SYSTEM | 2007-11-27 | 1
16 | WOUNDED INJURED ILL WARRIORS | 2008-12-30 | 1
17 | NATIONAL HEALTH INFO NETWORK | 2010-10-15 | 1
18 | NATIONAL DRUG FILE | 2010-02-12 | 1
19 | BENEFICIARY TRAVEL | 2013-02-03 | 1


