## RPC Options of 442 
    
Key is that nearly all RPCs need to be in Options or else they can't be invoked. But there's more - they need to have code behind them (from builds); they need to be in 8994; and a (recent) user must have an option they belong to. The following examines RPCs in terms of options and then the overlap of that set with the other ways an RPC can be active.

Of 151 RPC Broker Options, 3 are removed and 7 have no RPCs defined, leaving 141 active covering 4,799 RPCs. But 3 of these are NOT in the list of Active RPCs according to the build system (see table below for where they appear). More importantly, the build system declares 435 active RPCs which don't appear in any option - requiring an option would further subset the active RPC list. 0 of the active RPCs are NOT in 8994 and 440 of 8994 are not active RPCs. There are 432 RPCs NOT in options but in both 8994 and Builds.

\# | Option | Count RPCs | Exclusive RPCs | Key Required | RPCs not in Builds
--- | --- | --- | --- | --- | ---
1 | OR CPRS GUI CHART | 1,051 | 307 | &nbsp; | &nbsp;
2 | VEJDWPB CORE RPCS | 824 | 54 | &nbsp; | &nbsp;
3 | DSIVA APAT | 415 | 217 | &nbsp; | &nbsp;
4 | VEJDPTF SIGNON | 405 | 55 | &nbsp; | &nbsp;
5 | VEJD PCE RECORD MANAGER | 398 | 7 | &nbsp; | &nbsp;
6 | VEJD AUDIT REPORT MANAGER | 303 | 36 | &nbsp; | &nbsp;
7 | DSIY ABOVE PAR | 286 | 103 | &nbsp; | &nbsp;
8 | VEJDPTF ADMINISTRATOR | 269 | 8 | &nbsp; | &nbsp;
9 | DSIU MENTAL HEALTH SUITE | 244 | 56 | &nbsp; | &nbsp;
10 | MAG WINDOWS | 242 | 161 | &nbsp; | &nbsp;
11 | DENTV DSS DRM GUI | 213 | 84 | &nbsp; | &nbsp;
12 | SDECRPC | 203 | 183 | &nbsp; | &nbsp;
13 | DSIR MENU OPTIONS | 196 | 132 | &nbsp; | &nbsp;
14 | VEJDSAT TELECARE GIU | 188 | 5 | &nbsp; | &nbsp;
15 | VIAB WEB SERVICES OPTION | 178 | 44 | &nbsp; | &nbsp;
16 | DSIT TELECARE RECORD MANAGER | 156 | 57 | &nbsp; | &nbsp;
17 | DSIV DOCMANAGER | 148 | 74 | &nbsp; | &nbsp;
18 | MAG DICOM VISA | 146 | 130 | &nbsp; | &nbsp;
19 | DSIF FEEBASIS | 145 | 44 | &nbsp; | &nbsp;
20 | DVBA CAPRI GUI | 144 | 76 | &nbsp; | &nbsp;
21 | DSIF FEEBASIS PAYMENT | 140 | 47 | &nbsp; | &nbsp;
22 | OR BCMA ORDER COM | 133 | 18 | &nbsp; | &nbsp;
23 | HMP UI CONTEXT | 119 | 38 | &nbsp; | &nbsp;
24 | DSIB CP MENU | 118 | 50 | &nbsp; | &nbsp;
25 | DSIHF VISTA GATEWAY | 114 | 6 | &nbsp; | &nbsp;
26 | YS BROKER1 | 93 | 77 | &nbsp; | &nbsp;
27 | DSIG CNT USER | 93 | 8 | &nbsp; | &nbsp;
28 | MAG DICOM GATEWAY FULL | 87 | 24 | &nbsp; | 1
29 | DSIQ VCM | 87 | 32 | &nbsp; | &nbsp;
30 | CRHD SHIFT CHANGE HANDOFF | 77 | 57 | &nbsp; | &nbsp;
31 | SPN GENERAL USER RPC | 68 | 66 | &nbsp; | &nbsp;
32 | OOPS GUI EMPLOYEE | 65 | 64 | &nbsp; | &nbsp;
33 | ROR GUI | 65 | 57 | &nbsp; | &nbsp;
34 | NUPA ASSESSMENT GUI | 62 | 34 | &nbsp; | &nbsp;
35 | EC GUI CONTEXT | 59 | 44 | &nbsp; | &nbsp;
36 | RMPR PURCHASE ORDER GUI | 58 | 30 | &nbsp; | &nbsp;
37 | MAG DICOM GATEWAY VIEW | 56 | 0 | &nbsp; | 1
38 | ORRCM REPORTING | 50 | 8 | &nbsp; | &nbsp;
39 | ORAM ANTICOAGULATION CONTEXT | 50 | 35 | &nbsp; | &nbsp;
40 | PSB GUI CONTEXT - USER | 48 | 38 | &nbsp; | &nbsp;
41 | MAGJ VISTARAD WINDOWS | 47 | 28 | &nbsp; | &nbsp;
42 | ORRCMC QUERY TOOL | 44 | 8 | &nbsp; | &nbsp;
43 | NVSS SYSTEM MONITOR | 41 | 41 | &nbsp; | &nbsp;
44 | DSIHH DATABRIDGE | 39 | 16 | __DSIHH ADMIN__ | &nbsp;
45 | VA NURS OUTCOMES DATA (VANOD) | 38 | 38 | &nbsp; | &nbsp;
46 | VPS KIOSK INTERFACE | 36 | 29 | &nbsp; | &nbsp;
47 | GMV V/M GUI | 35 | 14 | &nbsp; | &nbsp;
48 | RMIMFIM | 35 | 19 | &nbsp; | &nbsp;
49 | DSIT CALL LOG REPORTER | 34 | 5 | &nbsp; | &nbsp;
50 | R1ENING GUI CONTEXT | 33 | 30 | &nbsp; | &nbsp;
51 | ORRCMC DASHBOARD | 32 | 18 | &nbsp; | &nbsp;
52 | KMPD CM DEVELOPER TOOLS | 32 | 27 | &nbsp; | &nbsp;
53 | MAGTP WORKLIST MGR | 29 | 13 | &nbsp; | &nbsp;
54 | DSIB MDS MENU | 29 | 21 | &nbsp; | &nbsp;
55 | RMPR GUI DOR | 27 | 3 | &nbsp; | &nbsp;
56 | APGKNU ENTRY | 23 | 15 | &nbsp; | &nbsp;
57 | MD HEMODIALYSIS USER | 18 | 9 | &nbsp; | &nbsp;
58 | AXVVA VISUAL AID CLIN APPS | 18 | 18 | &nbsp; | &nbsp;
59 | R1OREPI GUI CONTEXT | 18 | 18 | &nbsp; | &nbsp;
60 | SCMC PCMMR APP PROXY MENU | 17 | 11 | &nbsp; | &nbsp;
61 | DVBA CONTRACTED 2507 EXAM GUI | 16 | 0 | &nbsp; | &nbsp;
62 | DSIG HF MAPPER | 16 | 0 | &nbsp; | &nbsp;
63 | HMP SYNCHRONIZATION CONTEXT | 16 | 5 | &nbsp; | &nbsp;
64 | ACKQROES3E | 15 | 3 | &nbsp; | &nbsp;
65 | XHDXC DESKTOP | 15 | 11 | &nbsp; | &nbsp;
66 | MAG UTILITY | 15 | 8 | &nbsp; | &nbsp;
67 | KPA VRAM GUI | 15 | 1 | &nbsp; | &nbsp;
68 | XU EPCS EDIT DATA | 15 | 1 | __XUEPCSEDIT__ | &nbsp;
69 | XUS SIGNON | 14 | 1 | &nbsp; | &nbsp;
70 | ACKQROES3 | 14 | 0 | &nbsp; | &nbsp;
71 | VBECS VISTALINK CONTEXT | 14 | 14 | &nbsp; | &nbsp;
72 | APGKNU ADDITION | 14 | 7 | &nbsp; | &nbsp;
73 | RMPF ROES3 | 13 | 1 | &nbsp; | &nbsp;
74 | XOBV VISTALINK TESTER | 13 | 10 | &nbsp; | &nbsp;
75 | DSIP CR MENU | 13 | 4 | &nbsp; | &nbsp;
76 | VIAA01 RTLS RPC MENU | 13 | 13 | &nbsp; | &nbsp;
77 | XQAL GUI ALERTS | 12 | 1 | &nbsp; | &nbsp;
78 | MBAA SCHEDULING CALENDAR VIEW | 12 | 0 | &nbsp; | &nbsp;
79 | TIU MED GUI RPC V2 | 11 | 9 | &nbsp; | &nbsp;
80 | MWVS MEDICAL DOMAIN WEB SVCS | 11 | 1 | &nbsp; | &nbsp;
81 | R1ENINL1 INVENTORY IMPORT CTXT | 11 | 11 | &nbsp; | &nbsp;
82 | R1SRL OR SCHEDULE VIEWER | 11 | 11 | &nbsp; | &nbsp;
83 | CW MAIL | 11 | 1 | &nbsp; | &nbsp;
84 | DGRR GUI PATIENT LOOKUP | 10 | 7 | &nbsp; | &nbsp;
85 | MAG DICOM QUERY RETRIEVE | 10 | 0 | &nbsp; | &nbsp;
86 | R1XUM MENUS | 10 | 10 | &nbsp; | &nbsp;
87 | ZZ TEMPO EXTRACT | 9 | 0 | &nbsp; | &nbsp;
88 | ANRVJ_BLINDREHAB | 9 | 4 | &nbsp; | &nbsp;
89 | MD GUI MANAGER | 9 | 0 | &nbsp; | &nbsp;
90 | XWB BROKER EXAMPLE | 8 | 5 | &nbsp; | &nbsp;
91 | ANU HS DOWNLOAD | 8 | 1 | &nbsp; | &nbsp;
92 | MHV CLIENT | 8 | 8 | &nbsp; | &nbsp;
93 | MD GUI USER | 8 | 0 | &nbsp; | &nbsp;
94 | MAGKAT | 8 | 1 | &nbsp; | &nbsp;
95 | APGK ALL RPCS | 8 | 1 | &nbsp; | &nbsp;
96 | R1SDCI | 7 | 7 | &nbsp; | &nbsp;
97 | SCMC PCMMR WEB USER MENU | 7 | 0 | &nbsp; | &nbsp;
98 | XWB EGCHO | 6 | 3 | &nbsp; | &nbsp;
99 | SD WAIT LIST GUI | 6 | 6 | &nbsp; | &nbsp;
100 | R1UTTFU GUI CONTEXT | 6 | 6 | &nbsp; | &nbsp;
101 | ORRCMC PATIENT TASK | 5 | 4 | &nbsp; | &nbsp;
102 | ORRCMC GENERAL | 5 | 2 | &nbsp; | &nbsp;
103 | XOBE ESIG USER | 5 | 1 | &nbsp; | &nbsp;
104 | MDCP GATEWAY CONTEXT | 5 | 4 | &nbsp; | &nbsp;
105 | VAFCTF RPC CALLS | 4 | 0 | &nbsp; | &nbsp;
106 | XUS KAAJEE WEB LOGON | 4 | 4 | &nbsp; | &nbsp;
107 | QACI PATS RPC ACCESS | 4 | 4 | &nbsp; | &nbsp;
108 | R1ENINU1 GUI CONTEXT | 4 | 4 | &nbsp; | &nbsp;
109 | XUS IAM USER PROVISIONING | 4 | 4 | &nbsp; | &nbsp;
110 | RMPR PFFS GUI | 3 | 3 | &nbsp; | &nbsp;
111 | PRCHL GUI | 3 | 3 | &nbsp; | &nbsp;
112 | EDPF TRACKING SYSTEM | 3 | 2 | &nbsp; | &nbsp;
113 | HMP APPLICATION PROXY | 3 | 0 | &nbsp; | &nbsp;
114 | PSO WEB SERVICES OPTION | 3 | 3 | &nbsp; | &nbsp;
115 | XWB RPC TEST | 2 | 0 | &nbsp; | &nbsp;
116 | RMPR NPPD GUI | 2 | 1 | &nbsp; | &nbsp;
117 | ORRCMC SIGN LIST | 2 | 0 | &nbsp; | &nbsp;
118 | PRPF RPC UTILS | 2 | 2 | &nbsp; | &nbsp;
119 | QACV PATS RPC ACCESS | 2 | 2 | &nbsp; | &nbsp;
120 | NHIN APPLICATION PROXY | 2 | 0 | &nbsp; | &nbsp;
121 | VPR APPLICATION PROXY | 2 | 1 | &nbsp; | &nbsp;
122 | PRSN VANOD EXTRACT | 2 | 2 | &nbsp; | &nbsp;
123 | XUSSPKI UPN SET | 2 | 0 | &nbsp; | &nbsp;
124 | FSC RPC | 1 | 1 | &nbsp; | &nbsp;
125 | __WWW WEBTOP__ [NOT ACTIVE] | 1 | 1 | &nbsp; | 1
126 | __PSA GUI UPLOAD__ [NOT ACTIVE] | 1 | 1 | __PSA ORDERS__ | 1
127 | OOPS GUI EMPLOYEE HEALTH MENU | 1 | 0 | &nbsp; | &nbsp;
128 | MAG SYS-WIN WRKS | 1 | 0 | &nbsp; | &nbsp;
129 | PXRM REMINDER GUI | 1 | 1 | &nbsp; | &nbsp;
130 | XUPS VISTALINK | 1 | 1 | &nbsp; | &nbsp;
131 | DGRR PATIENT SERVICE QUERY | 1 | 1 | &nbsp; | &nbsp;
132 | WII RPCS | 1 | 1 | &nbsp; | &nbsp;
133 | PSN VISTALINK CONTEXT | 1 | 1 | &nbsp; | &nbsp;
134 | EDPS BOARD CONTEXT | 1 | 0 | &nbsp; | &nbsp;
135 | XUS KAAJEE PROXY LOGON | 1 | 1 | &nbsp; | &nbsp;
136 | MD CLIO | 1 | 0 | &nbsp; | &nbsp;
137 | XUS IAM USER BINDING | 1 | 0 | &nbsp; | &nbsp;
138 | HMP PATIENT ACTIVITY | 1 | 0 | &nbsp; | &nbsp;
139 | HMP WB PTDEM | 1 | 1 | &nbsp; | &nbsp;
140 | HMP WB DOMAINS | 1 | 0 | &nbsp; | &nbsp;
141 | CG FMQL QP USER | 1 | 1 | &nbsp; | &nbsp;


TODO: add if in User / UserSO and # 8994 missing