## 9999 Support of B1

__Purpose__: 9999 must be expanded to cover all B1 RPCs including Parameter scopes (where possible/available) and the various simple file lookups. Consult the _console logs_ to ensure appropriate entries are covered. The summary report for 9999 must cover all of the scenarios it handles from Parameters (done and not) to Files and extent of entries and why (from Parameters OR explicit as RPCs explicit). For files, the properties supported (as a % need to be noted - preferably define in a formal 'reduction' JSON).

__Background__: the "reduced MVDM" of VICS should support only that data required by RPCs/Services and no more. This means reducing not only the meta files of VISTA but also properties of those files. The exact reduction must be precisely defined by B2 but even in B1, an outline for its _70_ must be available. The reduction definition represents the amount of data that needs to be synchronized between a VISTA and National Services in order to migrate to National Services.

__Note__: bold below if need to enhance 9999.

\# | Emulation | Nature | Support | B1?
--- | --- | --- | --- | ---
1 | [gmv-convert-date](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/gmv-convert-date.js) | Utility | N/A | Not B1
2 | [gmv-dll-version](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/gmv-dll-version.js) | Simple PAR GET | SUPPORTED | B1
3 | [gmv-get-current-time](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/gmv-get-current-time.js) | Utility - __question on time zone__ | N/A | B1
4 | [gmv-get-vital-type-ien](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/gmv-get-vital-type-ien.js) | Simple Id from Label | SUPPORTED - __check index speed__ | B1
5 | [orb-sort-method](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orb-sort-method.js) | Simple PAR GET | SUPPORTED | B1
6 | [ordea-deatext](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/ordea-deatext.js) | Simple PAR GET | SUPPORTED | B1 
7 | [orevntx-1-dlgien](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orevntx-1-dlgien.js) | Simple Id from Label | SUPPORTED??? (101.41) -- look at captures | B1
8 | [orimo-iscloc](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orimo-iscloc.js) | Check (is this locn of type clinic) | SUPPORTED (yep added type44 to Locations) | B1
9 | [orq-null-list](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orq-null-list.js) | STUB/HARD CODED | N/A | B1
10 | [orqorb-sort](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orqorb-sort.js) | Simple PAR GET (some formatting) | SUPPORTED | B1
11 | [orqpt-default-list-source](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orqpt-default-list-source.js) | Many PAR GET | SUPPORTED in USER but no SERVICE assertions | B1
12 | [orqqcn2-get-context](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orqqcn2-get-context.js) | Simple PAR GET | SUPPORTED (not in SYS but yes in PKG and USR) | B1
13 | [orqqpx-new-reminders-active](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orqqpx-new-reminders-active.js) | Simple PAR GET | SUPPORTED (SYS, USR but not SERVICE) | B1
14 | [orwch-ldfont](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwch-ldfont.js) | Simple PAR GET | SUPPORTED (in USR and USR only scope called) | B1
15 | [orwch-loadall](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwch-loadall.js) | Multi PAR GETLST | SUPPORTED (GETLST to GET for USR) | B1
16 | [orwch-loadsiz](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwch-loadsiz.js) | Simple PAR GET | SUPPORTED | B1
17 | [orwcirn-autordv](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwcirn-autordv.js) | Simple PAR GET | NOT (ORWRP CIRN AUTOMATIC not set in any scope) | B1
18 | __[orwcom-orderobj](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwcom-orderobj.js)__ | Simple PAR GET and record lookup (with IEN of 101.15). 101.15 missing as no parameter assertion. | NOT (ORWCOM ORDER ACCEPTED not set in any scope) | B1
19 | __[orwcom-ptobj](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwcom-ptobj.js)__ | Simple PAR GET and record lookup (with IEN of 101.15). 101.15 missing as no parameter assertion | NOT (ORWCOM PATIENT SELECTED not set in any scope) | B1
20 | __[orwcv1-coversheet-list](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwcv1-coversheet-list.js)__ | File Get but lot's of args input | NO (need 101.24) | B1 
21 | __[orwdal32-clinuser](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdal32-clinuser.js)__ | PAR GET in multiple contexts including CLS which involves a lookup of this parameter by CLS in general and a match of that to user's class | (Barely) SUPPORTED - _OR ALLERGY ENTERED IN ERROR_ only set for SYS, not USR or CLS | B1
22 | __[orwdal32-def](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdal32-def.js)__ | File Data Get | NO (need 120.83 - national meta, 120.84 - singleton, keying off a 3 part lookup) | B1
23 | __[orwdal32-site-params](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdal32-site-params.js)__ | Simple 120.84 property get | NO (need 120.84) | NOT B1
24 | [orwdba-1-bastatus](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdba-1-bastatus.js) | Simple Install (9.7) and PARAMETER GET | PARTIAL (no install but have SYS parameter) | NOT B1?
25 | [orwdps-32-valqty](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdps-32-valqty.js) | UTILITY | N/A | B1
26 | [orwdps-32-valroute](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdps-32-valroute.js) | Record lookup by name combos | NO (need file) | B1 
27 | [orwdra-32-loctype](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdra-32-loctype.js) | One Property of Record | SUPPORTED (put type in 44) | B1
28 | [orwdx2-dcreason](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdx-2-dcreason.js) | walks file and a parameter (for sorting) | PARTIAL (but parameter not set in any scope) | B1
29 | __[orwdx-dgnm](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdx-dgnm.js)__ | Simple lookup by name (100.98) | NO? (need 100.98) and must cover captures | B1
30 | [orwdx-wrlst](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdx-wrlst.js) | MULTI PARAM LOOKUP | PARTIAL SUPPORT (need 101.41 too) | B1 
31 | [orwdxc-on](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdxc-on.js) | Simple PAR GET | SUPPORTED | B1
32 | __[orwdxm-mstyle](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdxm-mstyle.js)__ | Simple PAR GET | NO as though define at Parameter level, RPC only asks at SYS | B1
33 | [orwdxvb3-colltim](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdxvb3-colltim.js) | Simple PAR GET | SUPPORTED (at PKG level but not SYS level) | B1
34 | [orwdxvb3-swpanel](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwdxvb3-swpanel.js) | Simple PAR GET | SUPPORTED (at PKG level but not SYS level) | B1
35 | __[orwor-pkisite](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwor-pkisite.js)__ | Simplish check of one property off 100.7, probably a singleton as looks up for site - 'ON' for nodeVISTA. | NO (need 100.7) | B1
36 | [orworb-get-sort](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orworb-get-sort.js) | MULTI Parameter GET | SUPPORTED | B1
37 | [orwordg-ien](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwordg-ien.js) | simple id lookup by name | Partial Support (100.98) | B1
38 | [orwpce-always-checkout](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-always-checkout.js) | Simple Parameter Get | Supported (but no exs) | B1
39 | [orwpce-anytime](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-anytime.js) | Simple Parameter GET | Supported (exs exist) | B1
40 | [orwpce-askpce](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-askpce.js) | Simple Parameter Get | Supported - note RPC allows user to be passed in but exclude this | B1
41 | [orwpce-auto-visit-type-select](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-auto-visit-type-select.js) | Simple PAR GET | Supported (but no assertions for any context) | B1
42 | [orwpce-get-education-topics](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-get-education-topics.js) | List active entries | No (need 9999999.) - only label, isActive | B1
43 | [orwpce-get-exam-type](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-get-exam-type.js) | List active entries | No (need 9999999.) | B1
44 | __[orwpce-get-excluded](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-get-excluded.js)__ | SINGLE PARAMETER GET (can choose) GETLST | Not in Parameter Set! | B1
45 | [orwpce-get-health-factors-ty](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-get-health-factors-ty.js) | Lists active entries (can exclude categories) - uses local status field. Need isActive and Category | NO (need 9999999.) | B1
46 | [orwpce-get-immunization-type](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-get-immunization-type.js) | Lists active entries (doesn't use SCREEN - local status field. Used properly in this and other lookups. Though another chance to consider Mongo $SORT) | NO (need 9999999.14) | B1
47 | __[orwpce-get-set-of-codes](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-get-set-of-codes.js)__ | get codes from FM schema | NO - idea of enum management or set of code service | B1
48 | [orwpce-get-skin-test-type](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce-get-skin-test-type.js) | List active entries | NO (need 9999999.14) | B1
49 | [orwpce1-noncount](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpce1-noncount.js) | Simple one Property get of 44 | Partial as 44 | B1
50 | [orwps-reason](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwps-reason.js) | GETALL Parameter LST | Supported | B1
51 | [orwpt-clinrng](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpt-clinrng.js) | HARD CODED LIST (but could be list of codes) | N/A | B1
52 | [orwpt16-pscnvt](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwpt16-pscnvt.js) | HARD CODED DUMMY | N/A | B1
53 | [orwsr-show-surg-tab](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwsr-show-surg-tab.js) | Simple Parameter and Patch lookup | Partial Support | B1
54 | [orwtpd-1-geteafl](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwtpd-1-geteafl.js) | Simple Parameter GET | SUPPORTED | B1
55 | [orwtpd-1-getedats](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwtpd-1-getedats.js) | Multi Parameter Get | SUPPORTED - Have at Package, User but Not System | __NOT B1?__
56 | [orwtpo-csarngd](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwtpo-csarngd.js) | Simple 2 Parameter Get | Supported (have data) | B1
57 | [orwtpo-getimgd](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwtpo-getimgd.js) | Simple Parameter Get | Supported | B1
58 | __[orwu 1 newloc](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-1-newloc.js)__ | simple list of 44, same as clinloc | NO (need active props) | __NOT B1?__
59 | __[orwu clinloc](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-clinloc.js)__ | simple list of 44, same as newloc  | NO (need active props) | __NOT B1?__
60 | [orwu-dt](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-dt.js) | UTILITY | N/A | B1
61 | __[orwu-param](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-param.js)__ | Any Single Value Parameter GET | IN THEORY | B1
62 | [orwu-toolmenu](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-toolmenu.js) | Simple Parameter GET | SUPPORTED | B1
63| [orwu-valdt](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-valdt.js) | Utility | N/A | B1
64 | [orwu-validsig](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-validsig.js) | UTILITY | N/A | __NOT B1?__
65 | [orwu-versrv](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/orwu-versrv.js) | Simple (but hacky) inside property lookup | NO (need property - break it out) | __NOT B1?__
66 | [tiu-get-print-name](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/tiu-get-print-name.js) | simple property get | NO (need property) | __NOT B1?__
67 | [tiu-template-access-level](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/tiu-template-access-level.js) | MULTI-PARAM GET | SUPPORTED | B1
68 | [tiu-template-get-defaults](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/tiu-template-get-defaults.js) | SIMPLE PARAM GET | SUPPORTED | B1
69 | __[xus-get-user-info](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/xus-get-user-info.js)__ | Record 200 lookup | PARTIAL SUPPORT (need to add fields) | B1
70 | __[xus-pki-get-upn](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/xus-pki-get-upn.js)__ | Simple one property get | NO (add property to 200) | B1
71 | [xwb-get-broker-info](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/xwb-get-broker-info.js) | One property of KSP | SUPPORTED | __NOT B1?__

__Extra Not Count__: [xwb-im-here](https://github.com/vistadataproject/VICSServer/blob/master/emulation/models/xwb-im-here.js)