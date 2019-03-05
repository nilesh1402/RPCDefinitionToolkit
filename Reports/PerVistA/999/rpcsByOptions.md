## RPC Options of 999 
    
Key is that nearly all RPCs need to be in Options or else they can't be invoked. But there's more - they need to have code behind them (from builds); they need to be in 8994; and a (recent) user must have an option they belong to. The following examines RPCs in terms of options and then the overlap of that set with the other ways an RPC can be active.

Of 108 RPC Broker Options, 3 are removed and 8 have no RPCs defined, leaving 97 active covering 2,808 RPCs. But 4 of these are NOT in the list of Active RPCs according to the build system (see table below for where they appear). More importantly, the build system declares 404 active RPCs which don't appear in any option - requiring an option would further subset the active RPC list. 2 of the active RPCs are NOT in 8994 and 870 of 8994 are not active RPCs. There are 401 RPCs NOT in options but in both 8994 and Builds - broadly builds and 8994 agree but options exclude (this last statement applies to all but FOIA which has a messed up 8994).

\# | Option | Count RPCs | Exclusive RPCs | Key Required | RPCs not in Builds
--- | --- | --- | --- | --- | ---
1 | OR CPRS GUI CHART | 1,051 | 734 | &nbsp; | &nbsp;
2 | MAG WINDOWS | 241 | 163 | &nbsp; | &nbsp;
3 | SDECRPC | 203 | 183 | &nbsp; | &nbsp;
4 | VIAB WEB SERVICES OPTION | 178 | 44 | &nbsp; | &nbsp;
5 | MAG DICOM VISA | 146 | 130 | &nbsp; | &nbsp;
6 | DVBA CAPRI GUI | 144 | 80 | &nbsp; | &nbsp;
7 | OR BCMA ORDER COM | 133 | 18 | &nbsp; | &nbsp;
8 | HMP UI CONTEXT | 119 | 38 | &nbsp; | &nbsp;
9 | YS BROKER1 | 93 | 77 | &nbsp; | &nbsp;
10 | MAG DICOM GATEWAY FULL | 87 | 24 | &nbsp; | 3
11 | CRHD SHIFT CHANGE HANDOFF | 77 | 57 | &nbsp; | &nbsp;
12 | SPN GENERAL USER RPC | 68 | 66 | &nbsp; | &nbsp;
13 | OOPS GUI EMPLOYEE | 65 | 64 | &nbsp; | &nbsp;
14 | ROR GUI | 65 | 57 | &nbsp; | &nbsp;
15 | NUPA ASSESSMENT GUI | 62 | 34 | &nbsp; | &nbsp;
16 | EC GUI CONTEXT | 59 | 44 | &nbsp; | &nbsp;
17 | RMPR PURCHASE ORDER GUI | 58 | 30 | &nbsp; | &nbsp;
18 | MAG DICOM GATEWAY VIEW | 56 | 0 | &nbsp; | 3
19 | ORRCM REPORTING | 50 | 8 | &nbsp; | &nbsp;
20 | ORAM ANTICOAGULATION CONTEXT | 50 | 35 | &nbsp; | &nbsp;
21 | PSB GUI CONTEXT - USER | 48 | 38 | &nbsp; | &nbsp;
22 | MAGJ VISTARAD WINDOWS | 47 | 28 | &nbsp; | &nbsp;
23 | ORRCMC QUERY TOOL | 44 | 8 | &nbsp; | &nbsp;
24 | VPS KIOSK INTERFACE | 36 | 29 | &nbsp; | &nbsp;
25 | GMV V/M GUI | 35 | 14 | &nbsp; | &nbsp;
26 | RMIMFIM | 35 | 19 | &nbsp; | &nbsp;
27 | ORRCMC DASHBOARD | 32 | 18 | &nbsp; | &nbsp;
28 | KMPD CM DEVELOPER TOOLS | 32 | 27 | &nbsp; | &nbsp;
29 | MAGTP WORKLIST MGR | 29 | 13 | &nbsp; | &nbsp;
30 | RMPR GUI DOR | 27 | 3 | &nbsp; | &nbsp;
31 | MD HEMODIALYSIS USER | 18 | 9 | &nbsp; | &nbsp;
32 | SCMC PCMMR APP PROXY MENU | 17 | 11 | &nbsp; | &nbsp;
33 | HMP SYNCHRONIZATION CONTEXT | 16 | 5 | &nbsp; | &nbsp;
34 | ACKQROES3E | 15 | 3 | &nbsp; | &nbsp;
35 | XHDXC DESKTOP | 15 | 11 | &nbsp; | &nbsp;
36 | MAG UTILITY | 15 | 8 | &nbsp; | &nbsp;
37 | XU EPCS EDIT DATA | 15 | 1 | __XUEPCSEDIT__ | &nbsp;
38 | XUS SIGNON | 14 | 3 | &nbsp; | &nbsp;
39 | ACKQROES3 | 14 | 0 | &nbsp; | &nbsp;
40 | VBECS VISTALINK CONTEXT | 14 | 14 | &nbsp; | &nbsp;
41 | RMPF ROES3 | 13 | 1 | &nbsp; | &nbsp;
42 | XOBV VISTALINK TESTER | 13 | 10 | &nbsp; | &nbsp;
43 | VIAA01 RTLS RPC MENU | 13 | 13 | &nbsp; | &nbsp;
44 | XQAL GUI ALERTS | 12 | 1 | &nbsp; | &nbsp;
45 | MBAA SCHEDULING CALENDAR VIEW | 12 | 0 | &nbsp; | &nbsp;
46 | TIU MED GUI RPC V2 | 11 | 9 | &nbsp; | &nbsp;
47 | MWVS MEDICAL DOMAIN WEB SVCS | 11 | 1 | &nbsp; | &nbsp;
48 | DGRR GUI PATIENT LOOKUP | 10 | 7 | &nbsp; | &nbsp;
49 | MAG DICOM QUERY RETRIEVE | 10 | 0 | &nbsp; | &nbsp;
50 | MD GUI MANAGER | 9 | 0 | &nbsp; | &nbsp;
51 | ANRVJ_BLINDREHAB | 9 | 4 | &nbsp; | &nbsp;
52 | XWB BROKER EXAMPLE | 8 | 5 | &nbsp; | &nbsp;
53 | MD GUI USER | 8 | 0 | &nbsp; | &nbsp;
54 | MHV CLIENT | 8 | 8 | &nbsp; | &nbsp;
55 | MAGKAT | 8 | 1 | &nbsp; | &nbsp;
56 | SCMC PCMMR WEB USER MENU | 7 | 0 | &nbsp; | &nbsp;
57 | XWB EGCHO | 6 | 3 | &nbsp; | &nbsp;
58 | SD WAIT LIST GUI | 6 | 6 | &nbsp; | &nbsp;
59 | ORRCMC PATIENT TASK | 5 | 4 | &nbsp; | &nbsp;
60 | ORRCMC GENERAL | 5 | 2 | &nbsp; | &nbsp;
61 | XOBE ESIG USER | 5 | 5 | &nbsp; | &nbsp;
62 | MDCP GATEWAY CONTEXT | 5 | 4 | &nbsp; | &nbsp;
63 | VAFCTF RPC CALLS | 4 | 0 | &nbsp; | &nbsp;
64 | XUS KAAJEE WEB LOGON | 4 | 4 | &nbsp; | &nbsp;
65 | QACI PATS RPC ACCESS | 4 | 4 | &nbsp; | &nbsp;
66 | XUS IAM USER PROVISIONING | 4 | 4 | &nbsp; | &nbsp;
67 | RMPR PFFS GUI | 3 | 3 | &nbsp; | &nbsp;
68 | PRCHL GUI | 3 | 3 | &nbsp; | &nbsp;
69 | EDPF TRACKING SYSTEM | 3 | 2 | &nbsp; | &nbsp;
70 | utMUNIT | 3 | 3 | &nbsp; | &nbsp;
71 | HMP APPLICATION PROXY | 3 | 0 | &nbsp; | &nbsp;
72 | PSO WEB SERVICES OPTION | 3 | 3 | &nbsp; | &nbsp;
73 | XWB RPC TEST | 2 | 0 | &nbsp; | &nbsp;
74 | RMPR NPPD GUI | 2 | 1 | &nbsp; | &nbsp;
75 | ORRCMC SIGN LIST | 2 | 0 | &nbsp; | &nbsp;
76 | PRPF RPC UTILS | 2 | 2 | &nbsp; | &nbsp;
77 | QACV PATS RPC ACCESS | 2 | 2 | &nbsp; | &nbsp;
78 | NHIN APPLICATION PROXY | 2 | 0 | &nbsp; | &nbsp;
79 | VPR APPLICATION PROXY | 2 | 1 | &nbsp; | &nbsp;
80 | PRSN VANOD EXTRACT | 2 | 2 | &nbsp; | &nbsp;
81 | XUSSPKI UPN SET | 2 | 0 | &nbsp; | &nbsp;
82 | MAG SYS-WIN WRKS | 1 | 0 | &nbsp; | &nbsp;
83 | OOPS GUI EMPLOYEE HEALTH MENU | 1 | 0 | &nbsp; | &nbsp;
84 | __PSA GUI UPLOAD__ [NOT ACTIVE] | 1 | 1 | __PSA ORDERS__ | 1
85 | PXRM REMINDER GUI | 1 | 1 | &nbsp; | &nbsp;
86 | FSC RPC | 1 | 1 | &nbsp; | &nbsp;
87 | XUPS VISTALINK | 1 | 1 | &nbsp; | &nbsp;
88 | DGRR PATIENT SERVICE QUERY | 1 | 1 | &nbsp; | &nbsp;
89 | WII RPCS | 1 | 1 | &nbsp; | &nbsp;
90 | PSN VISTALINK CONTEXT | 1 | 1 | &nbsp; | &nbsp;
91 | EDPS BOARD CONTEXT | 1 | 0 | &nbsp; | &nbsp;
92 | XUS KAAJEE PROXY LOGON | 1 | 1 | &nbsp; | &nbsp;
93 | MD CLIO | 1 | 0 | &nbsp; | &nbsp;
94 | XUS IAM USER BINDING | 1 | 0 | &nbsp; | &nbsp;
95 | HMP PATIENT ACTIVITY | 1 | 0 | &nbsp; | &nbsp;
96 | HMP WB PTDEM | 1 | 1 | &nbsp; | &nbsp;
97 | HMP WB DOMAINS | 1 | 0 | &nbsp; | &nbsp;


__Note__: must examine Key's effect on options if present.

TODO: add if in User / UserSO