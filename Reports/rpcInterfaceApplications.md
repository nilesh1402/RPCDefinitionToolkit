## VA VistA RPC Interface Applications
    
The following is incomplete. Except for a small number of 'remote applications', VistA doesn't note the application logging in. The following was mainly built up by examining options and user patterns (IP sources etc) and marrying this information with static artifacts like the Monograph. 
    
\# | Application | Used in | Options | Monograph? | 8994.5 Entry? | Note
--- | --- | --- | --- | --- | --- | ---
1 | Above PAR (APAR) | &nbsp; | &nbsp; | YES | &nbsp; | The option _DSIY ABOVE PAR_ belongs to __Above PAR (APAR)__ by the [TRM](https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=7725)
2 | Automated Safety Incident Surveillance Tracking System (ASISTS) | &nbsp; | &nbsp; | YES | &nbsp; | The option _OOP GUI EMPLOYEE_ is from __ASISTS__ which is being decommissioned in Jan 2019
3 | __CAPRI__ | 442 (123,711), 640 (370,606) | DVBA CAPRI GUI | YES | YES | &nbsp;
4 | Caribou Community Living Care (CLC) Suite (Caribou) | &nbsp; | &nbsp; | YES | &nbsp; | &nbsp;
5 | Computerized Patient Record System (CPRS) | &nbsp; | &nbsp; | YES | &nbsp; | &nbsp;
6 | Dental Record Manager (DRM) Plus | &nbsp; | &nbsp; | YES | &nbsp; | &nbsp;
7 | Joint Legacy Viewer (JLV) | &nbsp; | &nbsp; | YES | &nbsp; | &nbsp;
8 | PROSTHETICS PURCHASE ORDER GUI | &nbsp; | &nbsp; | &nbsp; | &nbsp; | _RMPR PURCHASE ORDER GUI_ is an option of this app - is this 'APAT' in the monograph?
9 | __VISTA IMAGING AWIV__ | 442 (3,313), 640 (5,101) | MAG WINDOWS | &nbsp; | YES | &nbsp;
10 | __VISTA IMAGING DISPLAY__ | 442 (246,073), 640 (1,018,438) | MAG WINDOWS | &nbsp; | YES | in monograph (as are other imaging apps) as 'VistA Imaging System'
11 | __VISTA IMAGING TELEREADER__ | 442 (255) | MAG WINDOWS | &nbsp; | YES | &nbsp;
12 | __VISTA IMAGING VISTARAD__ | 442 (1,137), 640 (3,708) | MAGJ VISTARAD WINDOWS | &nbsp; | YES | See  [to](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf) with _MAGJ VISTARAD WINDOWS_ as its key option
13 | __VISTA IMAGING VIX__ | 442 (33,569), 640 (90,565) | MAG WINDOWS | &nbsp; | YES | &nbsp;
14 | __VISTAWEB-PROD__ | 442 (348,332), 640 (1,228,270) | OR CPRS GUI CHART | &nbsp; | YES | &nbsp;
15 | __VRAM__ | 442 (24,686), 640 (38,453) | KPA VRAM GUI | &nbsp; | YES | __VistA Remote Access Management (VRAM) Graphical User Interface (GUI)__ according to this [patch](https://github.com/OSEHRA/VistA/blob/master/Packages/Kernel/Patches/XU_8.0_629/XU-8_SEQ-502_PAT-629.TXT). It has a 8995 application entry and seems to sync credentials from the VBA 'VistA' to a local VistA - check out the RPCs it allows. Note that half its users are stand alone while the rest use CAPRI and very few use CPRS.


