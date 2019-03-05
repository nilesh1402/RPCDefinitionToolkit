## RPC Options of 640 
    
Key is that nearly all RPCs need to be in Options or else they can't be invoked. But there's more - they need to have code behind them (from builds); they need to be in 8994; and a (recent) user must have an option they belong to. The following examines RPCs in terms of options and then the overlap of that set with the other ways an RPC can be active.

Of 161 RPC Broker Options, 7 are removed and 7 have no RPCs defined, leaving 147 active covering 4,943 RPCs. But 11 of these are NOT in the list of Active RPCs according to the build system (see table below for where they appear). More importantly, the build system declares 418 active RPCs which don't appear in any option - requiring an option would further subset the active RPC list. 0 of the active RPCs are NOT in 8994 and 438 of 8994 are not active RPCs. There are 414 RPCs NOT in options but in both 8994 and Builds - broadly builds and 8994 agree but options exclude (this last statement applies to all but FOIA which has a messed up 8994).

\# | Option | Count RPCs | Exclusive RPCs | Key Required | RPCs not in Builds
--- | --- | --- | --- | --- | ---
1 | OR CPRS GUI CHART | 1,051 | 312 | &nbsp; | &nbsp;
2 | VEJDWPB CORE RPCS | 823 | 40 | &nbsp; | &nbsp;
3 | DSIVA APAT | 415 | 217 | &nbsp; | &nbsp;
4 | VEJDPTF SIGNON | 405 | 55 | &nbsp; | &nbsp;
5 | VEJD PCE RECORD MANAGER | 398 | 7 | &nbsp; | &nbsp;
6 | VEJD AUDIT REPORT MANAGER | 303 | 36 | &nbsp; | &nbsp;
7 | DSIY ABOVE PAR | 286 | 103 | &nbsp; | &nbsp;
8 | VEJDPTF ADMINISTRATOR | 269 | 8 | &nbsp; | &nbsp;
9 | MAG WINDOWS | 258 | 175 | &nbsp; | &nbsp;
10 | DSIU MENTAL HEALTH SUITE | 244 | 56 | &nbsp; | &nbsp;
11 | DENTV DSS DRM GUI | 222 | 92 | &nbsp; | &nbsp;
12 | SDECRPC | 204 | 184 | &nbsp; | &nbsp;
13 | DSIR MENU OPTIONS | 197 | 133 | &nbsp; | &nbsp;
14 | VEJDSAT TELECARE GIU | 188 | 5 | &nbsp; | &nbsp;
15 | VIAB WEB SERVICES OPTION | 178 | 42 | &nbsp; | &nbsp;
16 | DSIT TELECARE RECORD MANAGER | 156 | 57 | &nbsp; | &nbsp;
17 | DSIV DOCMANAGER | 148 | 74 | &nbsp; | &nbsp;
18 | MAG DICOM VISA | 147 | 130 | &nbsp; | &nbsp;
19 | DSIF FEEBASIS | 145 | 43 | &nbsp; | &nbsp;
20 | DVBA CAPRI GUI | 143 | 74 | &nbsp; | &nbsp;
21 | DSIF FEEBASIS PAYMENT | 140 | 47 | &nbsp; | &nbsp;
22 | OR BCMA ORDER COM | 133 | 18 | &nbsp; | &nbsp;
23 | VEJD VG FOR QM MEDREC | 128 | 15 | &nbsp; | &nbsp;
24 | DSIB CP MENU | 118 | 50 | &nbsp; | &nbsp;
25 | DSIHD VISTA GATEWAY | 115 | 3 | &nbsp; | &nbsp;
26 | VEJD ROI MENU OPTIONS | 106 | 21 | &nbsp; | &nbsp;
27 | SCMC PCMM GUI WORKSTATION | 96 | 78 | &nbsp; | &nbsp;
28 | YS BROKER1 | 93 | 77 | &nbsp; | &nbsp;
29 | DSIG CNT USER | 92 | 8 | &nbsp; | &nbsp;
30 | MAG DICOM GATEWAY FULL | 87 | 24 | &nbsp; | 1
31 | DSIQ VCM | 87 | 32 | &nbsp; | &nbsp;
32 | CRHD SHIFT CHANGE HANDOFF | 77 | 57 | &nbsp; | &nbsp;
33 | SPN GENERAL USER RPC | 68 | 66 | &nbsp; | &nbsp;
34 | OOPS GUI EMPLOYEE | 65 | 64 | &nbsp; | &nbsp;
35 | ROR GUI | 65 | 57 | &nbsp; | &nbsp;
36 | NUPA ASSESSMENT GUI | 62 | 34 | &nbsp; | &nbsp;
37 | EC GUI CONTEXT | 59 | 43 | &nbsp; | &nbsp;
38 | RMPR PURCHASE ORDER GUI | 58 | 30 | &nbsp; | &nbsp;
39 | MAG DICOM GATEWAY VIEW | 56 | 0 | &nbsp; | 1
40 | AMOJ VL T38 | 55 | 53 | &nbsp; | &nbsp;
41 | JLV WEB SERVICES | 54 | 1 | &nbsp; | &nbsp;
42 | ORRCM REPORTING | 50 | 8 | &nbsp; | &nbsp;
43 | ORAM ANTICOAGULATION CONTEXT | 50 | 35 | &nbsp; | &nbsp;
44 | PSB GUI CONTEXT - USER | 48 | 33 | &nbsp; | &nbsp;
45 | MAGJ VISTARAD WINDOWS | 47 | 28 | &nbsp; | &nbsp;
46 | ORRCMC QUERY TOOL | 44 | 8 | &nbsp; | &nbsp;
47 | NVSS SYSTEM MONITOR | 41 | 41 | &nbsp; | &nbsp;
48 | DSIHH DATABRIDGE | 39 | 16 | __DSIHH ADMIN__ | &nbsp;
49 | VPS KIOSK INTERFACE | 36 | 29 | &nbsp; | &nbsp;
50 | RMIMFIM | 35 | 19 | &nbsp; | &nbsp;
51 | GMV V/M GUI | 35 | 14 | &nbsp; | &nbsp;
52 | DSIT CALL LOG REPORTER | 34 | 5 | &nbsp; | &nbsp;
53 | AXAWPBGUI RADNUC | 34 | 24 | &nbsp; | &nbsp;
54 | R1ENING GUI CONTEXT | 33 | 30 | &nbsp; | &nbsp;
55 | ORRCMC DASHBOARD | 32 | 18 | &nbsp; | &nbsp;
56 | KMPD CM DEVELOPER TOOLS | 32 | 27 | &nbsp; | &nbsp;
57 | R1RARNU GUI CONTEXT | 30 | 20 | &nbsp; | &nbsp;
58 | MAGTP WORKLIST MGR | 29 | 13 | &nbsp; | &nbsp;
59 | DSIB MDS MENU | 29 | 21 | &nbsp; | &nbsp;
60 | VEJD PCE RECORD ADMINISTRATOR | 27 | 0 | &nbsp; | &nbsp;
61 | RMPR GUI DOR | 27 | 3 | &nbsp; | &nbsp;
62 | MD HEMODIALYSIS USER | 18 | 9 | &nbsp; | &nbsp;
63 | AXVVA VISUAL AID CLIN APPS | 18 | 18 | __AXVVA ALL LOCS__ | &nbsp;
64 | R1OREPI GUI CONTEXT | 18 | 18 | &nbsp; | &nbsp;
65 | SCMC PCMMR APP PROXY MENU | 17 | 9 | &nbsp; | &nbsp;
66 | DVBA CONTRACTED 2507 EXAM GUI | 16 | 0 | &nbsp; | &nbsp;
67 | XHDXC DESKTOP | 15 | 11 | &nbsp; | &nbsp;
68 | ACKQROES3E | 15 | 3 | &nbsp; | &nbsp;
69 | MAG UTILITY | 15 | 8 | &nbsp; | &nbsp;
70 | XU EPCS EDIT DATA | 15 | 1 | __XUEPCSEDIT__ | &nbsp;
71 | KPA VRAM GUI | 15 | 1 | &nbsp; | &nbsp;
72 | XUS SIGNON | 14 | 0 | &nbsp; | &nbsp;
73 | ACKQROES3 | 14 | 0 | &nbsp; | &nbsp;
74 | AMOJ VISTALINK EQP INV | 14 | 14 | &nbsp; | &nbsp;
75 | VBECS VISTALINK CONTEXT | 14 | 14 | &nbsp; | &nbsp;
76 | XOBV VISTALINK TESTER | 13 | 10 | &nbsp; | &nbsp;
77 | RMPF ROES3 | 13 | 1 | &nbsp; | &nbsp;
78 | DSIP CR MENU | 13 | 4 | &nbsp; | &nbsp;
79 | VIAA01 RTLS RPC MENU | 13 | 13 | &nbsp; | &nbsp;
80 | XQAL GUI ALERTS | 12 | 1 | &nbsp; | &nbsp;
81 | MBAA SCHEDULING CALENDAR VIEW | 12 | 0 | &nbsp; | &nbsp;
82 | DSIG HF MAPPER | 12 | 0 | &nbsp; | &nbsp;
83 | CW MAIL | 11 | 1 | &nbsp; | &nbsp;
84 | ALT INTRANET RPCS | 11 | 8 | &nbsp; | &nbsp;
85 | MWVS MEDICAL DOMAIN WEB SVCS | 11 | 1 | &nbsp; | &nbsp;
86 | TIU MED GUI RPC V2 | 11 | 9 | &nbsp; | &nbsp;
87 | R1SRL OR SCHEDULE VIEWER | 11 | 11 | &nbsp; | &nbsp;
88 | DGRR GUI PATIENT LOOKUP | 10 | 7 | &nbsp; | &nbsp;
89 | MAG DICOM QUERY RETRIEVE | 10 | 0 | &nbsp; | &nbsp;
90 | R1XUM MENUS | 10 | 10 | &nbsp; | &nbsp;
91 | __AOXNT LOCAL GUI__ [NOT ACTIVE] | 9 | 9 | &nbsp; | 9
92 | MD GUI MANAGER | 9 | 0 | &nbsp; | &nbsp;
93 | ANRVJ_BLINDREHAB | 9 | 4 | &nbsp; | &nbsp;
94 | XWB BROKER EXAMPLE | 8 | 5 | &nbsp; | &nbsp;
95 | MD GUI USER | 8 | 0 | &nbsp; | &nbsp;
96 | MHV CLIENT | 8 | 8 | &nbsp; | &nbsp;
97 | AOX IDENTIFIER USER | 8 | 0 | &nbsp; | &nbsp;
98 | AOX IDENTIFIER ADMIN | 8 | 0 | &nbsp; | &nbsp;
99 | MAGKAT | 8 | 1 | &nbsp; | &nbsp;
100 | APGK ALL RPCS | 7 | 4 | &nbsp; | &nbsp;
101 | R1SDCI | 7 | 7 | &nbsp; | &nbsp;
102 | SCMC PCMMR WEB USER MENU | 7 | 0 | &nbsp; | &nbsp;
103 | XWB EGCHO | 6 | 3 | &nbsp; | &nbsp;
104 | SD WAIT LIST GUI | 6 | 6 | &nbsp; | &nbsp;
105 | R2PBC GUI CONTEXT | 6 | 6 | &nbsp; | &nbsp;
106 | ORRCMC PATIENT TASK | 5 | 4 | &nbsp; | &nbsp;
107 | ORRCMC GENERAL | 5 | 2 | &nbsp; | &nbsp;
108 | XOBE ESIG USER | 5 | 1 | &nbsp; | &nbsp;
109 | MDCP GATEWAY CONTEXT | 5 | 4 | &nbsp; | &nbsp;
110 | VAFCTF RPC CALLS | 4 | 0 | &nbsp; | &nbsp;
111 | ARHCWEB1 DOMAIN ADMIN CONTEXT | 4 | 4 | __ARHCWEB1 DOMAIN ADMIN__ | &nbsp;
112 | XUS KAAJEE WEB LOGON | 4 | 4 | &nbsp; | &nbsp;
113 | QACI PATS RPC ACCESS | 4 | 4 | &nbsp; | &nbsp;
114 | R1ENINU1 GUI CONTEXT | 4 | 4 | &nbsp; | &nbsp;
115 | XUS IAM USER PROVISIONING | 4 | 4 | &nbsp; | &nbsp;
116 | ARH WINRMS BROKER CONTEXT | 3 | 0 | &nbsp; | &nbsp;
117 | RMPR PFFS GUI | 3 | 3 | &nbsp; | &nbsp;
118 | PRCHL GUI | 3 | 3 | &nbsp; | &nbsp;
119 | EDPF TRACKING SYSTEM | 3 | 2 | &nbsp; | &nbsp;
120 | PSO WEB SERVICES OPTION | 3 | 3 | &nbsp; | &nbsp;
121 | XWB RPC TEST | 2 | 0 | &nbsp; | &nbsp;
122 | RMPR NPPD GUI | 2 | 1 | &nbsp; | &nbsp;
123 | ARHCATA PICIS CARESUITE | 2 | 1 | &nbsp; | &nbsp;
124 | ORRCMC SIGN LIST | 2 | 0 | &nbsp; | &nbsp;
125 | ARHCWEB1 STENTOR CONTEXT | 2 | 1 | &nbsp; | &nbsp;
126 | PRPF RPC UTILS | 2 | 2 | &nbsp; | &nbsp;
127 | QACV PATS RPC ACCESS | 2 | 2 | &nbsp; | &nbsp;
128 | NHIN APPLICATION PROXY | 2 | 0 | &nbsp; | &nbsp;
129 | VPR APPLICATION PROXY | 2 | 1 | &nbsp; | &nbsp;
130 | PRSN VANOD EXTRACT | 2 | 2 | &nbsp; | &nbsp;
131 | XUSSPKI UPN SET | 2 | 0 | &nbsp; | &nbsp;
132 | MAG SYS-WIN WRKS | 1 | 0 | &nbsp; | &nbsp;
133 | OOPS GUI EMPLOYEE HEALTH MENU | 1 | 0 | &nbsp; | &nbsp;
134 | __PSA GUI UPLOAD__ [NOT ACTIVE] | 1 | 1 | __PSA ORDERS__ | 1
135 | ARHCWEB1 ALL USER APPS | 1 | 1 | &nbsp; | &nbsp;
136 | PXRM REMINDER GUI | 1 | 1 | &nbsp; | &nbsp;
137 | ARHCATIM PICIS IMAGE BATCH | 1 | 1 | &nbsp; | &nbsp;
138 | DGRR PATIENT SERVICE QUERY | 1 | 1 | &nbsp; | &nbsp;
139 | XUPS VISTALINK | 1 | 1 | &nbsp; | &nbsp;
140 | WII RPCS | 1 | 1 | &nbsp; | &nbsp;
141 | PSN VISTALINK CONTEXT | 1 | 1 | &nbsp; | &nbsp;
142 | EDPS BOARD CONTEXT | 1 | 0 | &nbsp; | &nbsp;
143 | XUS KAAJEE PROXY LOGON | 1 | 1 | &nbsp; | &nbsp;
144 | MD CLIO | 1 | 0 | &nbsp; | &nbsp;
145 | XUS IAM USER BINDING | 1 | 0 | &nbsp; | &nbsp;
146 | HMP PATIENT ACTIVITY | 1 | 1 | &nbsp; | &nbsp;
147 | CG FMQL QP USER | 1 | 1 | &nbsp; | &nbsp;


__Note__: must examine Key's effect on options if present.

TODO: add if in User / UserSO