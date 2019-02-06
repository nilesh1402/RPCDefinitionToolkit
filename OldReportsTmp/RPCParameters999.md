# VISTA 999 - Parameters used by in scope CPRS RPCs

## Parameters (82), Assertions (132) and RPCs (54)

Number of Parameters with no Assertions: 40 out of 82

Note - Parameter Entities (8989_518) with no parameters - support for these entity types can be removed from the VICS Parameter Service: DEVICE, ROOM-BED, TEAM (OE_RR)

Some Entity Numbers (context for how many of a type have parameters): Users (68) - Location (10) - Package (142). User \#'s are the most telling - populated systems have a lot of explicit user settings for some parameters.

\# | Parameter | Assertions | Description | By Entity Type(s) | Instance Non 1 | Domain | RPC(s)
--- | --- | --- | --- | --- | --- | --- | ---
1 | ORWOR CATEGORY SEQUENCE | 19 | Multiple instances of this parameter combine to form a list of the display groups shown in the order ... | PACKAGE (19), SYSTEM (0), USER (0) | __19__ (10, 100 ...) | 100.98 | ORWORDG MAPSEQ
2 | GMV GUI VERSION | 17 | This parameter is used to store the application:versions that are compatible with the current server ... | SYSTEM (17) | __16__ (VITALS.EXE:5.0.0.0, VITALS.EXE:5.0.1.0 ...) | &nbsp; | GMV PARAMETER
3 | ORWOR WRITE ORDERS LIST | 13 | ***This parameter has been superseded by ORWDX WRITE ORDERS LIST.*** Currently, the GUI references o ... | DIVISION (0), LOCATION (0), PACKAGE (13), SERVICE (0), SYSTEM (0), USER (0) | __13__ (10, 20 ...) | 101.41 | ORWDX WRLST
4 | GMV DLL VERSION | 11 | This parameter is used to store the DLL versions that are compatible with the current server version ... | SYSTEM (11) | __7__ (GMV\_VITALSVIEWENTER.DLL:v. 01\/20\/06 09:08, GMV\_VITALSVIEWENTER.DLL:v. 01\/21\/11 12:52 ...) | &nbsp; | GMV DLL VERSION, GMV PARAMETER
&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
5 | PXRM CPRS LOOKUP CATEGORIES | 8 | Returns an array of reminder categories which can then be used within GUI reminder processing. | DIVISION (0), LOCATION (0), PACKAGE (0), SERVICE (0), SYSTEM (8), USER (0) | __7__ (10, 4 ...) | 811.7 | ORQQPXRM REMINDER CATEGORIES
6 | ORWCV1 COVERSHEET LIST | 8 | This parameter allows a custom view of the Cover sheet in the CPRS Gui. | DIVISION (0), PACKAGE (8), SYSTEM (0), USER (0) | __7__ (2, 3 ...) | 101.24 | ORWCV START, ORWCV1 COVERSHEET LIST
&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
7 | ORWOR COVER RETRIEVAL NEW | 6 | This parameter controls whether each cover sheet section is loaded in the foreground or background. | PACKAGE (6), SYSTEM (0) | __6__ (28, 30 ...) | &nbsp; | ORWCV START
8 | ORWG GRAPH VIEW | 6 | This parameter is used internally to store graph views. Graph views are edited using the Define View ... | SYSTEM (6), USER (0) | __6__ (ANY MICROBIOLOGY, BCMA AND VITALS ...) | &nbsp; | ORWGRPC ALLVIEWS
&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
9 | ORWT TOOLS MENU | 4 | This parameter may be used to identify which items should appear on the tools menu which is displaye ... | DIVISION (0), LOCATION (0), PACKAGE (4), SERVICE (0), SYSTEM (0), USER (0) | __3__ (2, 3 ...) | &nbsp; | ORWU TOOLMENU
10 | ORWD NONVA REASON | 4 | This parameter lists the reasons and statements for ordering/documenting  a non-VA medication.  Non- ... | DIVISION (0), PACKAGE (4), SYSTEM (0) | __3__ (2, 3 ...) | &nbsp; | ORWPS REASON
&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
11 | ORWG GRAPH SETTING | 3 | Used as preference of graph default styles and sources. Deletion of this value at the Package level  ... | PACKAGE (1), SYSTEM (2), USER (0) | &nbsp; | &nbsp; | ORWGRPC GETPREF
&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
12 | ORWPCE ANYTIME ENCOUNTERS | 2 | Allows encounter data to be entered at any time, even when a note is not being edited. | DIVISION (0), SERVICE (1), SYSTEM (1), USER (0) | &nbsp; | &nbsp; | ORWPCE ANYTIME
13 | ORWOR SHOW SURGERY TAB | 2 | Should the Surgery tab be shown in the GUI? ((0=No, 1=Yes) | DIVISION (0), PACKAGE (1), SERVICE (0), SYSTEM (1), USER (0) | &nbsp; | &nbsp; | ORWSR SHOW SURG TAB
&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
14 | ORWOR BROADCAST MESSAGES | 1 | This parameter may be used to disable the use of windows messaging to notify other applications of C ... | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWU USERINFO
15 | ORWOR AUTO CLOSE PT MSG | 1 | This parameter controls how long the patient messages window displays before automatically closing.  ... | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWU USERINFO
16 | ORWDXM ORDER MENU STYLE | 1 | Determines whether GUI order menus include mnemonics. | PACKAGE (1), SYSTEM (0) | &nbsp; | &nbsp; | ORWDXM MSTYLE
17 | ORWDX WRITE ORDERS LIST | 1 | This parameter is used to identify a menu in the ORDER DIALOG file that will be used as the list of  ... | DIVISION (0), LOCATION (0), SERVICE (0), SYSTEM (1), USER (0) | &nbsp; | 101.41 | ORWDX WRLST
18 | ORWOR TIMEOUT COUNTDOWN | 1 | This value is the number of seconds used for the countdown when the timeout notification window appe ... | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWU USERINFO
19 | ORWDQ QUICK VIEW | 1 | This parameter contains the name of a personal quick order list for a specific display group. | DIVISION (0), LOCATION (0), PACKAGE (1), SERVICE (0), SYSTEM (0), USER (0) | __1__ (38) | &nbsp; | ORWUL QV4DG
20 | ORWOR DISABLE HOLD ORDERS | 1 | This parameter will prevent orders from being placed on hold. | PACKAGE (1), SYSTEM (0) | &nbsp; | &nbsp; | ORWU USERINFO
21 | ORB SORT METHOD | 1 | Method for sorting notifications when displayed in the CPRS GUI. Methods include: by Patient, Messag ... | DIVISION (0), PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORB SORT METHOD, ORQORB SORT, ORWORB GETSORT, ORWORB SETSORT
22 | ORCH CONTEXT NOTES | 1 | &nbsp; | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWTIU GET TIU CONTEXT
23 | ORCH CONTEXT PROBLEMS | 1 | &nbsp; | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORQQPL INIT USER
24 | ORCH CONTEXT ORDERS | 1 | &nbsp; | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWOR VWGET
25 | ORCH CONTEXT CONSULTS | 1 | &nbsp; | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORQQCN2 GET CONTEXT
26 | ORCH CONTEXT REPORTS | 1 | &nbsp; | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWTPO GETIMGD
27 | ORWOR DISABLE ORDERING | 1 | This parameter disables writing orders and taking actions on orders in the GUI. | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWU USERINFO
28 | ORWDPS ROUTING DEFAULT | 1 | This will be the default value for Pickup in the Outpatient Medications GUI ordering dialog. | LOCATION (0), SYSTEM (1) | &nbsp; | &nbsp; | ORWDPS1 ODSLCT
29 | ORQQCSDR CS RANGE START | 1 | Returns the relative date to start listing visits for a patient on the  Cover Sheet.  For example, ' ... | DIVISION (0), PACKAGE (1), SERVICE (0), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWTPO CSARNGD
30 | ORQQCSDR CS RANGE STOP | 1 | Returns the relative date to stop listing visits for a patient on the  Cover Sheet.  For example, 'T ... | DIVISION (0), PACKAGE (1), SERVICE (0), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWTPO CSARNGD
31 | ORQQEAPT ENC APPT START | 1 | Returns the relative number of days before Today to begin listing  appointments (0=Today, 1=Today-1  ... | DIVISION (0), PACKAGE (1), SERVICE (0), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWTPD1 GETEDATS
32 | ORQQEAFL ENC APPT FUTURE LIMIT | 1 | Number of days from Today when warning is given to user upon selection of a future appointment for E ... | DIVISION (0), PACKAGE (1), SYSTEM (0) | &nbsp; | &nbsp; | ORWTPD1 GETEAFL
33 | OR ALLERGY ENTERED IN ERROR | 1 | This parameter will control whether or not a user has access to the entered in error functionality a ... | CLASS (0), DIVISION (0), SYSTEM (1), USER (0) | &nbsp; | &nbsp; | ORWDAL32 CLINUSER
34 | OR VBECS REMOVE COLL TIME | 1 | This parameter can be used to remove any defaults for Collection Times in the VBECS Order Dialog.  A ... | DIVISION (0), PACKAGE (1), SYSTEM (0) | &nbsp; | &nbsp; | ORWDXVB3 COLLTIM
35 | OR VBECS DIAGNOSTIC PANEL 1ST | 1 | This paramter will switch the location of the Diagnostic and Component panels on the VBECS Order Dia ... | DIVISION (0), PACKAGE (1), SYSTEM (0) | &nbsp; | &nbsp; | ORWDXVB3 SWPANEL
36 | OR DEA TEXT | 1 | This parameter allows sites to set what exactly they would like the  message to be that is shown on  ... | SYSTEM (1) | &nbsp; | &nbsp; | ORDEA DEATEXT
37 | ORQQPL SUPPRESS CODES | 1 | This parameter determines whether the user will be shown SNOMED CT and  ICD codes when searching for ... | DIVISION (0), PACKAGE (1), SERVICE (0), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORQQPL INIT USER
38 | PXRM GUI REMINDERS ACTIVE | 1 | Indicate if Interactive Reminders are Active.  Enter 0 (No) or 1 (Yes). | DIVISION (0), SERVICE (0), SYSTEM (1), USER (0) | &nbsp; | &nbsp; | ORQQPX NEW REMINDERS ACTIVE
39 | ORWPCE ASK ENCOUNTER UPDATE | 1 | When signing a note in the CPRS GUI, this parameter is used to determine under what conditions to re ... | DIVISION (0), LOCATION (0), PACKAGE (0), SERVICE (0), SYSTEM (1), USER (0) | &nbsp; | &nbsp; | ORWPCE ASKPCE
40 | ORWOR AUTOSAVE NOTE | 1 | This parameter determines how many seconds should elapse between each auto-save of a note that is be ... | PACKAGE (1), SYSTEM (0), USER (0) | &nbsp; | &nbsp; | ORWU USERINFO
41 | GMV WEBLINK | 1 | This parameter contains the web address for the Vitals Measurments home page.  This can be modified  ... | SYSTEM (1) | &nbsp; | &nbsp; | GMV PARAMETER
42 | GMV TEMPLATE | 1 | &nbsp; | DIVISION (0), LOCATION (0), SYSTEM (1), USER (0) | __1__ (DAILY VITALS) | &nbsp; | GMV MANAGER, GMV PARAMETER
&nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
43 | ORWDPS SUPPRESS DISPENSE MSG | 0 | &nbsp; | SYSTEM | &nbsp; | &nbsp; | ORWDPS1 ODSLCT
44 | ORWOR ENABLE VERIFY | 0 | This parameter controls whether nurses are allowed to verify orders in the GUI.  The default value i ... | PACKAGE, SYSTEM, USER | &nbsp; | &nbsp; | ORWU USERINFO
45 | ORLP DEFAULT LIST SOURCE | 0 | Default preference for patient list source.  Valid values include:   T:Team/Personal List W:Ward Lis ... | SERVICE, USER | &nbsp; | &nbsp; | ORQPT DEFAULT LIST SOURCE
46 | ORLP DEFAULT WARD | 0 | Ward for default list of patients. | SERVICE, USER | &nbsp; | 42 | ORQPT DEFAULT LIST SOURCE
47 | ORLP DEFAULT TEAM | 0 | Team/Personal list to be default source of patients. | SERVICE, USER | &nbsp; | 100.21 | ORQPT DEFAULT LIST SOURCE
48 | ORLP DEFAULT CLINIC MONDAY | 0 | Clinic identified as a default source for patients on Monday. | SERVICE, USER | &nbsp; | 44 | ORQPT DEFAULT LIST SOURCE
49 | ORLP DEFAULT PROVIDER | 0 | Provider who is basis for building the Provider List of patients. | SERVICE, USER | &nbsp; | 200 | ORQPT DEFAULT LIST SOURCE
50 | ORLP DEFAULT SPECIALTY | 0 | Treating Specialty used as a source for patients on the Specialty List. | SERVICE, USER | &nbsp; | 45.7 | ORQPT DEFAULT LIST SOURCE
51 | ORLP DEFAULT CLINIC TUESDAY | 0 | Clinic to be default for determining patient list on Tuesdays. | SERVICE, USER | &nbsp; | 44 | ORQPT DEFAULT LIST SOURCE
52 | ORLP DEFAULT CLINIC WEDNESDAY | 0 | Clinic to be default source of Wednesday's patient list. | SERVICE, USER | &nbsp; | 44 | ORQPT DEFAULT LIST SOURCE
53 | ORLP DEFAULT CLINIC THURSDAY | 0 | Clinic to be default source of Thursday's patient list. | SERVICE, USER | &nbsp; | 44 | ORQPT DEFAULT LIST SOURCE
54 | ORLP DEFAULT CLINIC FRIDAY | 0 | Clinic to be default source of Friday's patient list. | SERVICE, USER | &nbsp; | 44 | ORQPT DEFAULT LIST SOURCE
55 | ORLP DEFAULT CLINIC SATURDAY | 0 | Clinic to be default source of Saturday's patient list. | SERVICE, USER | &nbsp; | 44 | ORQPT DEFAULT LIST SOURCE
56 | ORLP DEFAULT CLINIC SUNDAY | 0 | Clinic to be default source of Sunday's patient list. | SERVICE, USER | &nbsp; | 44 | ORQPT DEFAULT LIST SOURCE
57 | ORK SYSTEM ENABLE/DISABLE | 0 | Parameter determines if any order checking will occur.  'E' or 'Enable' indicates order checking is  ... | DIVISION, PACKAGE, SYSTEM | &nbsp; | &nbsp; | ORWDXC ON
58 | ORWCH BOUNDS | 0 | This parameter records bounds (position & size) information for the forms and controls in CPRSChart  ... | PACKAGE, USER | &nbsp; | &nbsp; | ORWCH LOADALL, ORWCH LOADSIZ, ORWCH SAVEALL
59 | ORWCH WIDTH | 0 | This records the width property for a control in CPRSChart (Patient Chart GUI).  In particular, it i ... | PACKAGE, USER | &nbsp; | &nbsp; | ORWCH LOADALL, ORWCH SAVEALL
60 | ORWCH COLUMNS | 0 | This records the widths of each column in a grid type control.  The column withs are entered from le ... | PACKAGE, USER | &nbsp; | &nbsp; | ORWCH LOADALL, ORWCH SAVEALL
61 | ORWOR TIMEOUT CHART | 0 | This value overrides the user's DTIME only in the case of the CPRS chart, Windows version (CPRSChart ... | DIVISION, SYSTEM, USER | &nbsp; | &nbsp; | ORWU USERINFO
62 | OR BILLING AWARENESS STATUS | 0 | Status of Billing Awareness Utilization | SYSTEM | &nbsp; | &nbsp; | ORWDBA1 BASTATUS
63 | ORQQEAPT ENC APPT STOP | 0 | Returns the relative number of days from Today to stop listing  appointments (0=Today, 1=Today+1 Day ... | DIVISION, PACKAGE, SERVICE, SYSTEM, USER | &nbsp; | &nbsp; | ORWTPD1 GETEDATS
64 | PXRM GEC STATUS CHECK | 0 | &nbsp; | TEAM, USER, USER | &nbsp; | 801.5 | ORWU USERINFO
65 | ORB SORT DIRECTION | 0 | Direction for sorting notifications when displayed in the CPRS GUI.  Directions include: Forward and ... | USER | &nbsp; | &nbsp; | ORWORB GETSORT, ORWORB SETSORT
66 | ORWRP CIRN AUTOMATIC | 0 | This parameter determines if Remote patient queries are done automatically for all sites.  The value ... | DIVISION, PACKAGE, SYSTEM, USER | &nbsp; | &nbsp; | ORWCIRN AUTORDV
67 | OR DC REASON LIST | 0 | This parameter determines the sequence sites want the order DC reasons  to  appear. Sites do not nee ... | SYSTEM | &nbsp; | 100.03 | ORWDX2 DCREASON
68 | TIU PERSONAL TEMPLATE ACCESS | 0 | This parameter is used to specify access to personal templates.  A setting  of READ ONLY allows the  ... | DIVISION, LOCATION, SERVICE, SYSTEM, USER | &nbsp; | &nbsp; | TIU TEMPLATE ACCESS LEVEL
69 | TIU TEMPLATE ACCESS BY CLASS | 0 | This parameter is used to specify access to personal templates for a  specific user class.  A settin ... | SYSTEM | &nbsp; | &nbsp; | TIU TEMPLATE ACCESS LEVEL
70 | ORCH INITIAL TAB | 0 | This parameter identifies the tab that should be initially displayed when CPRS first starts.  If ORC ... | DIVISION, PACKAGE, SYSTEM, USER | &nbsp; | &nbsp; | ORWU USERINFO
71 | ORCH USE LAST TAB | 0 | When this parameter is set to yes, CPRS will open to the last selected tab whenever changing patient ... | DIVISION, PACKAGE, SYSTEM, USER | &nbsp; | &nbsp; | ORWU USERINFO
72 | ORWOR DISABLE WEB ACCESS | 0 | When this parameter is set to yes, web links in the CPRS GUI will be disabled or hidden. | DIVISION, PACKAGE, SYSTEM, USER | &nbsp; | &nbsp; | ORWU USERINFO
73 | ORWCH FONT SIZE | 0 | This saves the preferred font size for CPRS Chart. | DIVISION, SYSTEM, USER | &nbsp; | &nbsp; | ORWCH LDFONT, ORWCH SAVFONT
74 | TIU DEFAULT TEMPLATES | 0 | Default Template for Notes;Consults;DC Summ tabs | USER | &nbsp; | &nbsp; | TIU TEMPLATE GET DEFAULTS, TIU TEMPLATE SET DEFAULTS
75 | ORWPCE DISABLE AUTO CHECKOUT | 0 | Disables the automatic checkout of encounters that do not have a diagnosis, procedure or provider in ... | DIVISION, LOCATION, SERVICE, SYSTEM, USER | &nbsp; | &nbsp; | ORWPCE ALWAYS CHECKOUT
76 | ORWPCE DISABLE AUTO VISIT TYPE | 0 | When set to Yes, this parameter prevents the automatic selection of a Type of Visit on the Visit Tab ... | DIVISION, LOCATION, SERVICE, SYSTEM, USER | &nbsp; | &nbsp; | ORWPCE AUTO VISIT TYPE SELECT
77 | ORWCOM PATIENT SELECTED | 0 | COM Object to Activate on CPRS GUI Patient Selection | DIVISION, SERVICE, SYSTEM, USER | &nbsp; | 101.15 | ORWCOM PTOBJ
78 | ORWCOM ORDER ACCEPTED | 0 | COM Objects to activate on order acceptance | DIVISION, SERVICE, SYSTEM, USER | &nbsp; | 101.15 | ORWCOM ORDEROBJ
79 | GMV ALLOW USER TEMPLATES | 0 | &nbsp; | SYSTEM | &nbsp; | &nbsp; | GMV MANAGER, GMV PARAMETER
80 | GMV DEFAULT VALUES | 0 | &nbsp; | USER | &nbsp; | &nbsp; | GMV PARAMETER
81 | GMV TEMPLATE DEFAULT | 0 | &nbsp; | DIVISION, LOCATION, SYSTEM, USER | &nbsp; | &nbsp; | GMV MANAGER, GMV PARAMETER
82 | GMV USER DEFAULTS | 0 | This parameter is used to store a users default parameter settings.  Each  setting is defined on the ... | USER | &nbsp; | &nbsp; | GMV PARAMETER, GMV USER

## RPCs w/parameters

with files, 18 - not simple parameter retrieves and so more complex.

Build 1 RPCs - 32 out of 54 which have parameters. Many B1 RPCs are Parameter-Centric check all parameter-only's are

\# | RPC | Parameters | Files | Is Build 1
--- | --- | --- | --- | ---
1 | ORQPT DEFAULT LIST SOURCE | 12 (ORLP DEFAULT CLINIC FRIDAY, ORLP DEFAULT CLINIC MONDAY, ORLP DEFAULT CLINIC SATURDAY, ORLP DEFAULT CLINIC SUNDAY, ORLP DEFAULT CLINIC THURSDAY, ORLP DEFAULT CLINIC TUESDAY, ORLP DEFAULT CLINIC WEDNESDAY, ORLP DEFAULT LIST SOURCE, ORLP DEFAULT PROVIDER, ORLP DEFAULT SPECIALTY, ORLP DEFAULT TEAM, ORLP DEFAULT WARD) | &nbsp; | &nbsp;
2 | ORWU USERINFO | 12 (ORCH INITIAL TAB, ORCH USE LAST TAB, ORWOR AUTO CLOSE PT MSG, ORWOR AUTOSAVE NOTE, ORWOR BROADCAST MESSAGES, ORWOR DISABLE HOLD ORDERS, ORWOR DISABLE ORDERING, ORWOR DISABLE WEB ACCESS, ORWOR ENABLE VERIFY, ORWOR TIMEOUT CHART, ORWOR TIMEOUT COUNTDOWN, PXRM GEC STATUS CHECK) | 4 (101.13, 389.9, 4.2, 8989.3) | &nbsp;
3 | GMV PARAMETER | 8 (GMV ALLOW USER TEMPLATES, GMV DEFAULT VALUES, GMV DLL VERSION, GMV GUI VERSION, GMV TEMPLATE, GMV TEMPLATE DEFAULT, GMV USER DEFAULTS, GMV WEBLINK) | 4 (8989.3, 8989.5, 8989.51, 8989.518) | &nbsp;
4 | ORWCH SAVEALL | 3 (ORWCH BOUNDS, ORWCH COLUMNS, ORWCH WIDTH) | &nbsp; | &nbsp;
5 | GMV MANAGER | 3 (GMV ALLOW USER TEMPLATES, GMV TEMPLATE, GMV TEMPLATE DEFAULT) | 7 (120.51, 120.52, 120.53, 200, 4, 4.2, 44) | &nbsp;
6 | ORWCH LOADALL | 3 (ORWCH BOUNDS, ORWCH COLUMNS, ORWCH WIDTH) | &nbsp; | __BUILD 1__
7 | ORWDX WRLST | 2 (ORWDX WRITE ORDERS LIST, ORWOR WRITE ORDERS LIST) | 2 (101.41, 200) | &nbsp;
8 | ORWDPS1 ODSLCT | 2 (ORWDPS ROUTING DEFAULT, ORWDPS SUPPRESS DISPENSE MSG) | 2 (101.42, 550) | &nbsp;
9 | ORWTPD1 GETEDATS | 2 (ORQQEAPT ENC APPT START, ORQQEAPT ENC APPT STOP) | &nbsp; | __BUILD 1__
10 | TIU TEMPLATE ACCESS LEVEL | 2 (TIU PERSONAL TEMPLATE ACCESS, TIU TEMPLATE ACCESS BY CLASS) | &nbsp; | &nbsp;
11 | ORWTPO CSARNGD | 2 (ORQQCSDR CS RANGE START, ORQQCSDR CS RANGE STOP) | &nbsp; | __BUILD 1__
12 | ORWORB SETSORT | 2 (ORB SORT DIRECTION, ORB SORT METHOD) | &nbsp; | __BUILD 1__
13 | ORWCV START | 2 (ORWCV1 COVERSHEET LIST, ORWOR COVER RETRIEVAL NEW) | 1 (101.24) | &nbsp;
14 | ORQQPL INIT USER | 2 (ORCH CONTEXT PROBLEMS, ORQQPL SUPPRESS CODES) | 3 (125.99, 200, 49) | &nbsp;
15 | ORWORB GETSORT | 2 (ORB SORT DIRECTION, ORB SORT METHOD) | &nbsp; | __BUILD 1__
16 | ORWPS REASON | 1 (ORWD NONVA REASON) | &nbsp; | __BUILD 1__
17 | ORWORDG MAPSEQ | 1 (ORWOR CATEGORY SEQUENCE) | 1 (100.98) | &nbsp;
18 | ORWSR SHOW SURG TAB | 1 (ORWOR SHOW SURGERY TAB) | 1 (9.4) | &nbsp;
19 | ORQQPX NEW REMINDERS ACTIVE | 1 (PXRM GUI REMINDERS ACTIVE) | &nbsp; | __BUILD 1__
20 | ORWCH SAVFONT | 1 (ORWCH FONT SIZE) | &nbsp; | __BUILD 1__
21 | ORWOR VWGET | 1 (ORCH CONTEXT ORDERS) | 1 (100.98) | &nbsp;
22 | ORWCOM PTOBJ | 1 (ORWCOM PATIENT SELECTED) | &nbsp; | __BUILD 1__
23 | TIU TEMPLATE GET DEFAULTS | 1 (TIU DEFAULT TEMPLATES) | &nbsp; | __BUILD 1__
24 | ORWCOM ORDEROBJ | 1 (ORWCOM ORDER ACCEPTED) | &nbsp; | &nbsp;
25 | ORWPCE ALWAYS CHECKOUT | 1 (ORWPCE DISABLE AUTO CHECKOUT) | &nbsp; | __BUILD 1__
26 | ORWDXVB3 SWPANEL | 1 (OR VBECS DIAGNOSTIC PANEL 1ST) | &nbsp; | __BUILD 1__
27 | ORWDXVB3 COLLTIM | 1 (OR VBECS REMOVE COLL TIME) | &nbsp; | __BUILD 1__
28 | ORB SORT METHOD | 1 (ORB SORT METHOD) | &nbsp; | __BUILD 1__
29 | ORQQPXRM REMINDER CATEGORIES | 1 (PXRM CPRS LOOKUP CATEGORIES) | 3 (801.41, 811.7, 811.9) | &nbsp;
30 | ORWPCE ANYTIME | 1 (ORWPCE ANYTIME ENCOUNTERS) | &nbsp; | __BUILD 1__
31 | ORWGRPC GETPREF | 1 (ORWG GRAPH SETTING) | &nbsp; | __BUILD 1__
32 | ORWCH LOADSIZ | 1 (ORWCH BOUNDS) | &nbsp; | __BUILD 1__
33 | GMV USER | 1 (GMV USER DEFAULTS) | &nbsp; | __BUILD 1__
34 | ORWCIRN AUTORDV | 1 (ORWRP CIRN AUTOMATIC) | &nbsp; | __BUILD 1__
35 | ORWDX2 DCREASON | 1 (OR DC REASON LIST) | 3 (100.02, 100.03, 9.4) | &nbsp;
36 | ORQQCN2 GET CONTEXT | 1 (ORCH CONTEXT CONSULTS) | &nbsp; | __BUILD 1__
37 | ORWCH LDFONT | 1 (ORWCH FONT SIZE) | &nbsp; | __BUILD 1__
38 | ORWDAL32 CLINUSER | 1 (OR ALLERGY ENTERED IN ERROR) | 2 (8930, 8930.3) | &nbsp;
39 | ORWTPO GETIMGD | 1 (ORCH CONTEXT REPORTS) | &nbsp; | __BUILD 1__
40 | ORWCV1 COVERSHEET LIST | 1 (ORWCV1 COVERSHEET LIST) | 1 (101.24) | &nbsp;
41 | GMV DLL VERSION | 1 (GMV DLL VERSION) | &nbsp; | __BUILD 1__
42 | ORWDBA1 BASTATUS | 1 (OR BILLING AWARENESS STATUS) | 1 (9.7) | &nbsp;
43 | ORWTIU GET TIU CONTEXT | 1 (ORCH CONTEXT NOTES) | 1 (8926) | &nbsp;
44 | ORWGRPC ALLVIEWS | 1 (ORWG GRAPH VIEW) | 3 (60, 68, 69.2) | &nbsp;
45 | ORWPCE AUTO VISIT TYPE SELECT | 1 (ORWPCE DISABLE AUTO VISIT TYPE) | &nbsp; | __BUILD 1__
46 | ORDEA DEATEXT | 1 (OR DEA TEXT) | &nbsp; | __BUILD 1__
47 | ORQORB SORT | 1 (ORB SORT METHOD) | &nbsp; | __BUILD 1__
48 | ORWU TOOLMENU | 1 (ORWT TOOLS MENU) | &nbsp; | __BUILD 1__
49 | ORWDXM MSTYLE | 1 (ORWDXM ORDER MENU STYLE) | &nbsp; | __BUILD 1__
50 | ORWUL QV4DG | 1 (ORWDQ QUICK VIEW) | 3 (100.98, 101.41, 101.44) | &nbsp;
51 | TIU TEMPLATE SET DEFAULTS | 1 (TIU DEFAULT TEMPLATES) | &nbsp; | __BUILD 1__
52 | ORWTPD1 GETEAFL | 1 (ORQQEAFL ENC APPT FUTURE LIMIT) | &nbsp; | __BUILD 1__
53 | ORWPCE ASKPCE | 1 (ORWPCE ASK ENCOUNTER UPDATE) | &nbsp; | __BUILD 1__
54 | ORWDXC ON | 1 (ORK SYSTEM ENABLE/DISABLE) | &nbsp; | __BUILD 1__

