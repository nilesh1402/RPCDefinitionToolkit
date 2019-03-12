## RPC Interface Definition for 999
    
### Source Data Details

\# | File | Total | Count Processed
--- | --- | --- | ---
1 | 3.081 | 4 | 4
2 | 9.4 | 142 | 142
3 | 9.6 | 10,348 | 10,348
4 | 9.7 | 10,273 | 10,273
5 | 19 | 10,446 | 108
6 | 200 | 72 | 52
7 | 8994 | 3,676 | 3,676


### Basic Summary

There are __3,750__ RPCs, __2,803 (74.75%)__ of which are active. The first RPCs were distributed on _1996-05-24_, the last on _2017-11-07_. The last installation happened on _2018-02-22_.
    
RPCs are marked inactive in stages ...

\# | Stage | \# At/After
--- | --- | ---
1 | Total | 3,750
2 | 8994 Full Entry | 3,674
3 | Installed Build | 3,204
4 | Has Current Option | 2,803


### RPC Distribution by Year
    
481 RPCs have no 'first distributed' date as their first builds lacked a date. Here is RPC distribution year by year, along with the small amount of deletion too. Note that only __69 (1.84%)__ RPCs are formally deleted though __947 (25.25%)__ should be.

\# | Year | Added \# | Deleted \# | Inactive \#
--- | --- | --- | --- | ---
1 | 2017 | 70 (2.14%) | &nbsp; | 1 (1.43%)
2 | 2016 | 277 (8.47%) | 13 | 29 (10.47%)
3 | 2015 | 71 (2.17%) | &nbsp; | 12 (16.9%)
4 | 2014 | 11 (0.34%) | &nbsp; | &nbsp;
5 | 2013 | 201 (6.15%) | &nbsp; | 10 (4.98%)
6 | 2012 | 75 (2.29%) | &nbsp; | 17 (22.67%)
7 | 2011 | 44 (1.35%) | &nbsp; | 3 (6.82%)
8 | 2010 | 168 (5.14%) | &nbsp; | 28 (16.67%)
9 | 2009 | 64 (1.96%) | &nbsp; | 6 (9.38%)
10 | 2008 | 110 (3.36%) | &nbsp; | 3 (2.73%)
11 | 2007 | 98 (3.0%) | &nbsp; | 7 (7.14%)
12 | 2006 | 121 (3.7%) | 2 | 14 (11.57%)
13 | 2005 | 113 (3.46%) | 13 | 38 (33.63%)
14 | 2004 | 276 (8.44%) | 4 | 46 (16.67%)
15 | 2003 | 161 (4.93%) | 2 | 25 (15.53%)
16 | 2002 | 310 (9.48%) | 22 | 76 (24.52%)
17 | 2001 | 365 (11.17%) | 8 | 33 (9.04%)
18 | 2000 | 346 (10.58%) | 1 | 14 (4.05%)
19 | 1999 | 45 (1.38%) | 4 | 13 (28.89%)
20 | 1998 | 22 (0.67%) | &nbsp; | &nbsp;
21 | 1997 | 252 (7.71%) | &nbsp; | 37 (14.68%)
22 | 1996 | 69 (2.11%) | &nbsp; | 54 (78.26%)


### MUMPS Routine Implementation
    
__3674__ RPCs are implemented in __1203__ separate MUMPS routines, while __76__ identified RPCs lack an implementation. The highest number of RPCs per routine is __128__ (_SDEC_), the median is __2.0__, the lowest is __1__. __884 (73.48%)__ routines implement only active RPCs, __286__ only inactive RPCs (candidates for deletion?), while __33__ implement a mix of active and inactive RPCs.

The (outliers) that implement the most RPCs are ...

\# | \# RPCs | Routine(s)
--- | --- | ---
1 | 128 | SDEC
2 | 43 | ORWTPP
3 | 39 | OREVNTX1
4 | 27 | ORQQPXRM, ORWGRPC, ORWPCE2
5 | 24 | ORWPCE
6 | 23 | ORWPT, ORWU
7 | 22 | ORQQCN2
8 | 21 | ORWDX, VIABRPC
9 | 20 | ORWLRR
10 | 19 | __SDOERPC__ [INACTIVE]
11 | 18 | __DSIFCNS1__ [INACTIVE]
12 | 17 | __DSIROI6__ [INACTIVE]
13 | 16 | __DSIROI1__ [INACTIVE], __ORWDXA__ [INACTIVE], RMIMRP
14 | 15 | __NUPABCL2__ [INACTIVE]
15 | 14 | DVBAB1, __MAGDRPC1__ [INACTIVE], ORWDFH
16 | 13 | __DSICXPR__ [INACTIVE], ORAM1, ORQQCN1, ORQQPX, ORWDPS1, ORWDPS33, TIUSRVA


### Packages
    
_Package_ is a sometimes inconsistently used breakdown of VistA into a set of cooperating applications. All but __475 (12.67%)__ RPCs are assigned to __61__ different packages, __10__ of which only have _inactive_ RPCs and __26__ more have a mix of active and inactive RPCs. 

Those with at least one active RPC are - note ORDER ENTRY has a huge proportion which MAY be due to redundant/overlapping purposes of individual RPCs ...

\# | Package | First Distributed RPC | Active RPCs | Inactive RPCs
--- | --- | --- | --- | ---
1 | ORDER ENTRY/RESULTS REPORTING | 1997-12-17 | 995 | 13
2 | IMAGING | 2001-06-29 | 445 | 27
3 | SCHEDULING | 1996-05-30 | 208 | 113
4 | TEXT INTEGRATION UTILITIES | 1997-06-20 | 118 | 6
5 | MENTAL HEALTH | 2000-01-13 | 78 | 16
6 | AUTOMATED MED INFO EXCHANGE | 2001-06-21 | 79 | 3
7 | CLINICAL CASE REGISTRIES | 2002-05-15 | 58 | 23
8 | SPINAL CORD DYSFUNCTION | 2010-09-14 | 66 | &nbsp;
9 | ASISTS | 2002-07-09 | 64 | 1
10 | PROSTHETICS | 2002-12-18 | 58 | &nbsp;
11 | SHIFT CHANGE HANDOFF TOOL | 2008-05-13 | 57 | &nbsp;
12 | HEALTH MANAGEMENT PLATFORM | 2016-02-23 | 41 | 15
13 | BAR CODE MED ADMIN | 1999-08-06 | 43 | 5
14 | EVENT CAPTURE | 2001-07-05 | 44 | &nbsp;
15 | VISTA INTEGRATION ADAPTER | 2016-02-12 | 42 | &nbsp;
16 | REGISTRATION | 2000-02-01 | 19 | 21
17 | PATIENT ASSESSMENT DOCUM | 2012-08-01 | 34 | 2
18 | KERNEL | 1996-05-24 | 31 | 4
19 | RPC BROKER | 1996-05-24 | 26 | 7
20 | GEN. MED. REC. - VITALS | 2002-10-28 | 32 | &nbsp;
21 | CARE MANAGEMENT | 2004-01-16 | 26 | 5
22 | VPS KIOSK | 2012-08-16 | 29 | &nbsp;
23 | CAPACITY MANAGEMENT TOOLS | 2004-03-22 | 27 | 1
24 | CLINICAL PROCEDURES | 2004-05-21 | 23 | 1
25 | VISTALINK | 2003-09-30 | 11 | 11
26 | FUNCTIONAL INDEPENDENCE | 2003-04-15 | 19 | &nbsp;
27 | CLINICAL REMINDERS | 2001-05-17 | 4 | 15
28 | PCE PATIENT CARE ENCOUNTER | 2014-04-24 | 14 | 5
29 | VISUAL IMPAIRMENT SERVICE TEAM | 2003-02-18 | 4 | 13
30 | HEALTHEVET DESKTOP | 2004-01-16 | 12 | 4
31 | VBECS | 2009-04-23 | 14 | &nbsp;
32 | REAL TIME LOCATION SYSTEM | 2016-05-26 | 13 | &nbsp;
33 | MOBILE SCHEDULING APPLICATIONS | 2016-08-25 | 12 | &nbsp;
34 | VA FILEMAN | 1998-02-28 | 10 | &nbsp;
35 | MY HEALTHEVET | 2006-07-18 | 8 | &nbsp;
36 | PATIENT REPRESENTATIVE | 2007-01-24 | 6 | &nbsp;
37 | ELECTRONIC SIGNATURE | 2006-07-14 | 5 | &nbsp;
38 | QUASAR | 2003-10-27 | 4 | 1
39 | VIRTUAL PATIENT RECORD | 2011-08-04 | 2 | 2
40 | OUTPATIENT PHARMACY | 2017-10-24 | 3 | &nbsp;
41 | EMERGENCY DEPARTMENT | 2010-09-02 | 3 | &nbsp;
42 | IFCAP | 2007-04-27 | 3 | &nbsp;
43 | MASH UTILITIES | 2015-12-16 | 3 | &nbsp;
44 | CONSULT/REQUEST TRACKING | 1997-12-17 | 1 | 2
45 | REMOTE ORDER/ENTRY SYSTEM | 2003-09-26 | 1 | 2
46 | PAID | 2012-02-17 | 2 | &nbsp;
47 | INTEGRATED PATIENT FUNDS | 2007-02-06 | 2 | &nbsp;
48 | WOUNDED INJURED ILL WARRIORS | 2008-12-30 | 1 | &nbsp;
49 | NATIONAL HEALTH INFO NETWORK | 2010-10-15 | 1 | &nbsp;
50 | NATIONAL DRUG FILE | 2010-02-12 | 1 | &nbsp;
51 | NOIS | 1998-09-06 | 1 | &nbsp;


The 'inactive-only' Packages are ...

\# | Package | First Distributed RPC | RPCs (Inactive)
--- | --- | --- | ---
1 | DENTAL | 2001-08-28 | 91
2 | MASTER PATIENT INDEX VISTA | 2002-07-12 | 20
3 | AUTOMATED INFO COLLECTION SYS | 1997-02-12 | 16
4 | INTEGRATED BILLING | 2001-05-31 | 9
5 | RADIOLOGY/NUCLEAR MEDICINE | 2010-06-03 | 7
6 | CLINICAL INFO RESOURCE NETWORK | 2002-06-07 | 6
7 | TOOLKIT | 2008-11-21 | 2
8 | ONCOLOGY | 2011-08-09 | 1
9 | ENROLLMENT APPLICATION SYSTEM | 2007-11-27 | 1
10 | BENEFICIARY TRAVEL | 2013-02-03 | 1


