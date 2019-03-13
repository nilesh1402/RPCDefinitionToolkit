## RPC Options of 442 Classified
    
Based on active (SO) users use.
    
\# | Type | \#
--- | --- | ---
1 | Users | 232,661
2 | SO Users with RPC Options | 71,359
3 | SO Users with other than RPC Options | 335
4 | Options | 94
5 | Pure Alone Options | 7
6 | Singleton Alone Options (NEVER COMBINED) | 0
7 | Pure Qualifier Options - NEVER on their own | 80
8 | Other Qualifier Options - < 15% on their own (so not _Pure Alones_) | 7



There are 7 _Pure Alones_, options that can exist on their own (> 15% of users with them have only them)

\# | Option | Total Users | By 0 Users | Alone Users | CPRS Combos | Other Combos | Quals | Alone Quals | Top Quals
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | OR CPRS GUI CHART | 50,362 | 48,753 | 11,276 (22.39%) | &nbsp; | &nbsp; | 93 | 6 (6.45%) | DVBA CAPRI GUI (30,577), MAG WINDOWS (28,144), VPR APPLICATION PROXY (8,009)
2 | MAG WINDOWS | 47,033 | 45,629 | 9,462 (20.12%) | 28,144 (59.84%) | 9,427 (20.04%) | 90 | 6 (6.67%) | DVBA CAPRI GUI (29,118), OR CPRS GUI CHART (28,144), VPR APPLICATION PROXY (4,868)
3 | KPA VRAM GUI | 1,125 | 1,111 | 590 (52.44%) | 17 (1.51%) | 518 (46.04%) | 6 | 2 (33.33%) | DVBA CAPRI GUI (523)
4 | MAGJ VISTARAD WINDOWS | 267 | 265 | 65 (24.34%) | 70 (26.22%) | 132 (49.44%) | 12 | 2 (16.67%) | DVBA CAPRI GUI (175), MAG WINDOWS (113), OR CPRS GUI CHART (70)
5 | DSIY ABOVE PAR | 31 | 3 | 16 (51.61%) | 10 (32.26%) | 5 (16.13%) | 67 | 4 (5.97%) | &nbsp;
6 | RMPR PURCHASE ORDER GUI | 18 | 2 | 4 (22.22%) | 13 (72.22%) | 1 (5.56%) | 63 | 4 (6.35%) | &nbsp;
7 | OOPS GUI EMPLOYEE | 9 | &nbsp; | 2 (22.22%) | 7 (77.78%) | &nbsp; | 64 | 4 (6.25%) | &nbsp;


__Note__:
    
  * _KPA VRAM GUI_ belongs to __VistA Remote Access Management (VRAM) Graphical User Interface (GUI)__ according to this [patch](https://github.com/OSEHRA/VistA/blob/master/Packages/Kernel/Patches/XU_8.0_629/XU-8_SEQ-502_PAT-629.TXT). It has a 8995 application entry and seems to sync credentials from the VBA 'VistA' to a local VistA - check out the RPCs it allows. Note that half its users are stand alone while the rest use CAPRI and very few use CPRS.
  * _MAGJ VISTARAD WINDOWS_ is a __VistARad__ option according [to](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf). Additionally, note that the _Rad/Nuc Med Personnel menu_ defines further user permissions (where stored?) and there are a series of security keys guarding actions.
  * _MAG WINDOWS_ for __VistA Imaging and Capture Software__ according to [this](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf). Note that ala Rad, there are keys to further restrict options.
  * _DSIY ABOVE PAR_ belongs to __Above PAR (APAR)__ by the [TRM](https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=7725)
  * _RMPR PURCHASE ORDER GUI_ is part of __PROSTHETICS PURCHASE ORDER GUI__
  * _OOP GUI EMPLOYEE_ is from __ASISTS__ which is being decommissioned in Jan 2019.
  
