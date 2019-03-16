## VA VistA RPC Interface Applications
    
The following is incomplete. Except for a small number of 'remote applications', VistA doesn't note the application logging in. The following was mainly built up by examining options and user patterns (IP sources etc) and marrying this information with static artifacts like the Monograph. 
    
\# | Application | Used in | Monograph? | 8994.5 Entry? | Note
--- | --- | --- | --- | --- | ---
1 | Above PAR (APAR) | &nbsp; | YES | &nbsp; | The option _DSIY ABOVE PAR_ belongs to __Above PAR (APAR)__ by the [TRM](https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=7725)
2 | Automated Safety Incident Surveillance Tracking System (ASISTS) | &nbsp; | YES | &nbsp; | The option _OOP GUI EMPLOYEE_ is from __ASISTS__ which is being decommissioned in Jan 2019
3 | __CAPRI__ | 442 (123,711), 640 (370,606) | &nbsp; | YES | &nbsp;
4 | Caribou Community Living Care (CLC) Suite (Caribou) | &nbsp; | YES | &nbsp; | &nbsp;
5 | Compensation and Pension Record Interchange (CAPRI) | &nbsp; | YES | &nbsp; | &nbsp;
6 | Computerized Patient Record System (CPRS) | &nbsp; | YES | &nbsp; | &nbsp;
7 | Dental Record Manager (DRM) Plus | &nbsp; | YES | &nbsp; | &nbsp;
8 | Joint Legacy Viewer (JLV) | &nbsp; | YES | &nbsp; | &nbsp;
9 | PROSTHETICS PURCHASE ORDER GUI | &nbsp; | &nbsp; | &nbsp; | _RMPR PURCHASE ORDER GUI_ is an option of this app - is this 'APAT' in the monograph?
10 | __VISTA IMAGING AWIV__ | 442 (3,313), 640 (5,101) | &nbsp; | YES | &nbsp;
11 | __VISTA IMAGING DISPLAY__ | 442 (246,073), 640 (1,018,438) | &nbsp; | YES | in monograph (as are other imaging apps) as 'VistA Imaging System'
12 | __VISTA IMAGING TELEREADER__ | 442 (255) | &nbsp; | YES | &nbsp;
13 | __VISTA IMAGING VISTARAD__ | 442 (1,137), 640 (3,708) | &nbsp; | YES | See  [to](https://www.va.gov/vdl/documents/clinical/vista_imaging_sys/imginstallgd_f.pdf) with _MAGJ VISTARAD WINDOWS_ as its key option
14 | __VISTA IMAGING VIX__ | 442 (33,569), 640 (90,565) | &nbsp; | YES | &nbsp;
15 | __VISTAWEB-PROD__ | 442 (348,332), 640 (1,228,270) | &nbsp; | YES | &nbsp;
16 | __VRAM__ | 442 (24,686), 640 (38,453) | &nbsp; | YES | __VistA Remote Access Management (VRAM) Graphical User Interface (GUI)__ according to this [patch](https://github.com/OSEHRA/VistA/blob/master/Packages/Kernel/Patches/XU_8.0_629/XU-8_SEQ-502_PAT-629.TXT). It has a 8995 application entry and seems to sync credentials from the VBA 'VistA' to a local VistA - check out the RPCs it allows. Note that half its users are stand alone while the rest use CAPRI and very few use CPRS.


