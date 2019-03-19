## VA VistA RPC Interface Definition 
    
There are __5,630__ RPCs, __4,551 (80.83%)__ of which are active. The first RPCs were distributed on _1996-04-14_, the last on _2018-05-22_. The last installation happened on _2018-06-19_.
    
RPCs are marked inactive in stages ...

\# | Stage | \# At/After
--- | --- | ---
1 | Total | 5,630
2 | 8994 Full Entry | 5,468
3 | Installed Build | 5,436
4 | Has currently used Active Option | 4,551


### RPC Distribution by Year
    
57 RPCs have no 'first distributed' date as their first builds lacked a date - the other 5,573 all have dates. Here is RPC distribution year by year, along with the small amount of deletion too. Note that only __150 (2.66%)__ RPCs are formally deleted though __1,079 (19.17%)__ should be.

\# | Year | Added \# | Deleted \# | Inactive \#
--- | --- | --- | --- | ---
1 | 2018 | 30 (0.54%) | &nbsp; | 3 (10.0%)
2 | 2017 | 184 (3.3%) | 1 | 7 (3.8%)
3 | 2016 | 872 (15.65%) | 13 | 136 (15.6%)
4 | 2015 | 197 (3.53%) | 12 | 60 (30.46%)
5 | 2014 | 78 (1.4%) | 3 | 4 (5.13%)
6 | 2013 | 268 (4.81%) | 3 | 30 (11.19%)
7 | 2012 | 175 (3.14%) | 1 | 82 (46.86%)
8 | 2011 | 182 (3.27%) | &nbsp; | 47 (25.82%)
9 | 2010 | 234 (4.2%) | &nbsp; | 83 (35.47%)
10 | 2009 | 289 (5.19%) | 1 | 19 (6.57%)
11 | 2008 | 163 (2.92%) | 5 | 15 (9.2%)
12 | 2007 | 133 (2.39%) | 2 | 27 (20.3%)
13 | 2006 | 177 (3.18%) | 2 | 47 (26.55%)
14 | 2005 | 242 (4.34%) | 21 | 78 (32.23%)
15 | 2004 | 322 (5.78%) | 4 | 83 (25.78%)
16 | 2003 | 345 (6.19%) | 5 | 81 (23.48%)
17 | 2002 | 363 (6.51%) | 22 | 104 (28.65%)
18 | 2001 | 305 (5.47%) | 12 | 17 (5.57%)
19 | 2000 | 410 (7.36%) | 22 | 38 (9.27%)
20 | 1999 | 201 (3.61%) | 7 | 14 (6.97%)
21 | 1998 | 24 (0.43%) | 3 | 3 (12.5%)
22 | 1997 | 268 (4.81%) | &nbsp; | 36 (13.43%)
23 | 1996 | 111 (1.99%) | 11 | 27 (24.32%)


### MUMPS Routine Implementation
    
__5468__ RPCs are implemented in __1803__ separate MUMPS routines, while __162__ identified RPCs lack an implementation. The highest number of RPCs per routine is __129__ (_SDEC_), the median is __2.0__, the lowest is __1__. __1,449 (80.37%)__ routines implement only active RPCs, __289__ only inactive RPCs (candidates for deletion?), while __65__ implement a mix of active and inactive RPCs.

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
16 | 13 | DSICXPR, DSIVXPR, __ORAM1__ [INACTIVE], ORQQCN1, ORQQPX, ORWDPS1, ORWDPS33, TIUSRVA, VANOD04


### Packages
    
_Package_ is a sometimes inconsistently used breakdown of VistA into a set of cooperating applications. All but __283 (5.03%)__ RPCs are assigned to __82__ different packages, __19__ of which only have _inactive_ RPCs and __37__ more have a mix of active and inactive RPCs. 

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
8 | FEE BASIS CLAIMS SYSTEM | 2007-11-20 | 148 | 10
9 | RELEASE OF INFORMATION - DSSI | 2003-01-28 | 133 | 23
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
28 | VA NURSING OUTCOMES DATABASE PROJECT | 2005-11-22 | 38 | &nbsp;
29 | KERNEL | 1996-05-24 | 23 | 14
30 | DSIQ - VCM | 2011-07-13 | 30 | 5
31 | RPC BROKER | 1996-05-24 | 19 | 14
32 | GEN. MED. REC. - VITALS | 2002-10-28 | 18 | 14
33 | VPS KIOSK | 2012-08-16 | 29 | &nbsp;
34 | DSIG | 2015-03-27 | 18 | 7
35 | CLINICAL PROCEDURES | 2003-05-29 | 19 | 5
36 | DATA BRIDGE | 2011-04-19 | 22 | 1
37 | VISTALINK | 2003-09-30 | 11 | 11
38 | FUNCTIONAL INDEPENDENCE | 2003-04-15 | 19 | &nbsp;
39 | CLINICAL REMINDERS | 2001-05-17 | 3 | 16
40 | PCE PATIENT CARE ENCOUNTER | 2014-04-24 | 1 | 18
41 | VISUAL AID FOR CLINIC APPOINTMENTS (VISN 20) | 2011-11-22 | 18 | &nbsp;
42 | VISUAL IMPAIRMENT SERVICE TEAM | 2003-02-18 | 4 | 13
43 | HEALTHEVET DESKTOP | 2004-01-16 | 12 | 4
44 | VBECS | 2009-04-23 | 14 | &nbsp;
45 | MOBILE SCHEDULING APPLICATIONS | 2016-08-25 | 12 | &nbsp;
46 | R5 VBA IMPORT TOOL | 2012-07-31 | 11 | &nbsp;
47 | R1 SURGERY SCHEDULE VIEWER | 2012-07-13 | 11 | &nbsp;
48 | VA FILEMAN | 1997-04-07 | 10 | &nbsp;
49 | INTEGRATED BILLING | 2001-05-31 | 1 | 8
50 | PATIENT REPRESENTATIVE | 2007-01-24 | 6 | &nbsp;
51 | ELECTRONIC SIGNATURE | 2006-07-14 | 5 | &nbsp;
52 | QUASAR | 2003-10-27 | 4 | 1
53 | VIRTUAL PATIENT RECORD | 2011-08-04 | 2 | 2
54 | EMERGENCY DEPARTMENT | 2010-09-02 | 3 | &nbsp;
55 | REMOTE ORDER/ENTRY SYSTEM | 2003-09-26 | 1 | 2
56 | IFCAP | 2006-07-19 | 3 | &nbsp;
57 | MASH UTILITIES | 2015-12-16 | 3 | &nbsp;
58 | CONSULT/REQUEST TRACKING | 1997-12-17 | 1 | 2
59 | INTEGRATED PATIENT FUNDS | 2007-02-06 | 2 | &nbsp;
60 | NATIONAL HEALTH INFO NETWORK | 2010-10-15 | 1 | &nbsp;
61 | ANU HS DOWNLOAD | 2000-11-08 | 1 | &nbsp;
62 | CW GUIMAIL | 1999-09-20 | 1 | &nbsp;
63 | NOIS | 1998-01-31 | 1 | &nbsp;


The 'inactive-only' Packages are ...

\# | Package | First Distributed RPC | RPCs (Inactive)
--- | --- | --- | ---
1 | HEALTH MANAGEMENT PLATFORM | 2016-02-23 | 56
2 | NATIONAL VISTA SUPPORT | 2001-02-08 | 49
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


### Source Information for Integrated Definition
    
The integrated interface definition combines RPC definitions from multiple real VistA and FOIA. Overall __1,880 (33.39%)__ RPCs are not in FOIA.

\# | Station | RPCs | Definition Contribution
--- | --- | --- | ---
1 | 442 | 5,376 | 103
2 | 640 | 5,520 | 5,520
3 | 999 | 3,750 | 7


