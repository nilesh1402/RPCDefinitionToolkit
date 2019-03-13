## RPC Options of 640 Classified
    
Based on active (SO) users use.
    
\# | Type | \#
--- | --- | ---
1 | Users | 360,773
2 | SO Users with RPC Options | 129,791
3 | SO Users with other than RPC Options | 1,630
4 | Options | 93
5 | Pure Alone Options | 9
6 | Singleton Alone Options (NEVER COMBINED) | 0
7 | Pure Qualifier Options - NEVER on their own | 58
8 | Other Qualifier Options - < 15% on their own (so not _Pure Alones_) | 26



There are 9 _Pure Alones_, options that can exist on their own (> 15% of users with them have only them)

\# | Option | Total Users | By 0 Users | Alone Users | CPRS Combos | Other Combos | Quals | Alone Quals | Top Quals
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | OR CPRS GUI CHART | 97,449 | 92,061 | 19,320 (19.83%) | &nbsp; | &nbsp; | 88 | 8 (9.09%) | DVBA CAPRI GUI (63,534), MAG WINDOWS (56,139), VPR APPLICATION PROXY (18,924)
2 | MAG WINDOWS | 83,406 | 81,526 | 12,756 (15.29%) | 56,139 (67.31%) | 14,511 (17.4%) | 80 | 6 (7.5%) | DVBA CAPRI GUI (57,352), OR CPRS GUI CHART (56,139), VPR APPLICATION PROXY (11,411)
3 | PSB GUI CONTEXT - USER | 2,059 | 171 | 578 (28.07%) | 1,159 (56.29%) | 322 (15.64%) | 69 | 5 (7.25%) | OR CPRS GUI CHART (1,159), DVBA CAPRI GUI (632), EC GUI CONTEXT (307), MAG WINDOWS (306), VPR APPLICATION PROXY (248)
4 | KPA VRAM GUI | 1,259 | 1,232 | 633 (50.28%) | 33 (2.62%) | 593 (47.1%) | 21 | 3 (14.29%) | DVBA CAPRI GUI (598)
5 | MAGJ VISTARAD WINDOWS | 414 | 408 | 85 (20.53%) | 130 (31.4%) | 199 (48.07%) | 4 | 2 (50.0%) | DVBA CAPRI GUI (268), MAG WINDOWS (202), OR CPRS GUI CHART (130)
6 | DSIY ABOVE PAR | 124 | 6 | 71 (57.26%) | 28 (22.58%) | 25 (20.16%) | 32 | 3 (9.38%) | DSIVA APAT (40), OR CPRS GUI CHART (28)
7 | VBECS VISTALINK CONTEXT | 38 | 3 | 6 (15.79%) | 21 (55.26%) | 11 (28.95%) | 11 | 2 (18.18%) | &nbsp;
8 | R2PBC GUI CONTEXT | 3 | 1 | 2 (66.67%) | 1 (33.33%) | &nbsp; | 2 | 1 (50.0%) | &nbsp;
9 | XU EPCS EDIT DATA | 3 | &nbsp; | 1 (33.33%) | 2 (66.67%) | &nbsp; | 23 | 2 (8.7%) | &nbsp;


__Note__:
    
  * _KPA VRAM GUI_ belongs to __VistA Remote Access Management (VRAM) Graphical User Interface (GUI)__ according to this [patch](https://github.com/OSEHRA/VistA/blob/master/Packages/Kernel/Patches/XU_8.0_629/XU-8_SEQ-502_PAT-629.TXT). It has a 8995 application entry and seems to sync credentials from the VBA 'VistA' to a local VistA - check out the RPCs it allows. Note that half its users are stand alone while the rest use CAPRI and very few use CPRS.
  * _MAGJ VISTARAD WINDOWS_ is a __VistARad__ option according [to](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf). Additionally, note that the _Rad/Nuc Med Personnel menu_ defines further user permissions (where stored?) and there are a series of security keys guarding actions.
  * _MAG WINDOWS_ for __VistA Imaging and Capture Software__ according to [this](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf). Note that ala Rad, there are keys to further restrict options.
  * _DSIY ABOVE PAR_ belongs to __Above PAR (APAR)__ by the [TRM](https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=7725)
  * _RMPR PURCHASE ORDER GUI_ is part of __PROSTHETICS PURCHASE ORDER GUI__
  * _OOP GUI EMPLOYEE_ is from __ASISTS__ which is being decommissioned in Jan 2019.
  
