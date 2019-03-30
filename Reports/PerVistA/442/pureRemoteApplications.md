## Named Applications (ie/ application name set)

Named application account for <span class='yellowIt'>565,670 (51.14%)</span> sign ons.

__TODO__: see if IPs from remote alones add up BEFORE doing JLV isolation from other remote apps! ie/ x 2

\# | remote application | sign ons | stations | users | users w 100/200 station | with only app unset | alone | alone sign ons | alone activity
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
1 | VISTA IMAGING DISPLAY | 233,091 | 129 | 30,318 | &nbsp; | 9,314 (30.72%) | 12,593 (41.54%) | 29,384 (12.61%) | 2006_95 (2007), 2006_82 (743), 2006_81 (203), 409_831 (2), 403_54 (1), 810_1 (1)
2 | VISTAWEB-PROD | 204,265 | 130 | 33,978 | 100 (7,767) | 4,255 (12.52%) | 15,526 (45.69%) | 43,493 (21.29%) | 53_69 (380), 396_4 (40), 8989_5 (11), 301_7 (6), 410 (4), 3_077 (2), 154 (1), 409_831 (1), 391_31 (1)
3 | CAPRI | 92,400 | 116 | 7,139 | &nbsp; | 22 (0.31%) | 1,344 (18.83%) | 6,306 (6.82%) | 396_4 (17), 413_1 (8), 8989_5 (2), 3_077 (1), 301_7 (1), 2260 (1)
4 | VISTA IMAGING VIX | 33,518 | 3 | 5 | 200 (3) | 3 (60.0%) | 2 (40.0%) | 5 (0.01%) | 2006_95 (4)
5 | VISTA IMAGING VISTARAD | 1,136 | 35 | 191 | &nbsp; | 73 (38.22%) | 98 (51.31%) | 266 (23.42%) | 2006_82 (266)
6 | VISTA IMAGING AWIV | 1,035 | 37 | 153 | 100 (44) | &nbsp; | &nbsp; | &nbsp; | &nbsp;
7 | VISTA IMAGING TELEREADER | 224 | 2 | 16 | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp;
8 | VRAM | 1 | 1 | 1 | &nbsp; | &nbsp; | 1 (100.0%) | 1 (100.0%) | &nbsp;


__VISTA IMAGING VIX__ is special with two key users, _CVIX_USER_ and _CVIX MHVUSER_ both of which comes from Austin (200). Note that the IPs used for VIX are local to the system and not from 200. <span class='yellowIt'>2</span> other users also have _VISTA IMAGING VIX_.

\# | Key VIX User | IEN | Sign ons | Activity
--- | --- | --- | --- | ---
1 | CVIX MHVUSER | 520815969 | 51,961 | 2006_81 (1), 2006_82 (1404), 2006_95 (141858)
2 | CVIX USER | 520752187 | 1,194 | 2006_95 (46)


__TODO__: see the one Workstation (2006_81) - what is it? Do all the Sessions (2006_82) belong to it?

Sign on details for CVIX, MHVUSER - main IP accounts for all 2001's and most 200's. Other IPs have workstation set and use 200. SSN 2001 doesn't set remote app, has LOA 1 - 200 always has 2. The device (TCP or NULL) doesn't seem to have a pattern but needs more work ...

<dl>
<dt>Number of Days</dt><dd>302</dd>
<dt>By Day Stats</dt><dd>{'std': 57.08974122496646, 'max': 379, 'quartileOne': 120.25, 'oht': 351.5, 'total': 51961, 'count': 302, 'min': 53, 'median': 181.5, 'iqr': 92.5, 'hasOutliers': False, 'quartileThree': 212.75, 'gtoht': 2, 'ohto': 490.25, 'mean': 172.05629139072849}</dd>
<dt>IPs</dt><dd>{"10.208.151.136": 15, "10.152.80.125": 51862, "10.208.151.137": 32, "10.208.151.134": 22, "10.208.151.135": 30}</dd>
<dt>Stations</dt><dd>200 [33,186], 2001 [18,775]</dd>
<dt>Count Props</dt><dd>{"19": 18775, "20": 33087, "21": 99}</dd>
<dt>With Remote App</dt><dd>33186</dd>
<dt>With 'workstation_name'</dt><dd>99</dd>
<dt>Devices</dt><dd>{"NULL": 47534, "TCP": 4427}</dd>
<dt>Level of Assurances</dt><dd>{"1": 18775, "2": 33186}</dd>
<dt>Groups</dt><dd>20557</dd>
<dt>Gap</dt><dd>0:01:40</dd>
<dt>Gap Stats</dt><dd>{'std': 31.45726401681242, 'max': 989.0, 'quartileOne': 5.0, 'oht': 50.0, 'total': 424408.0, 'count': 20556, 'min': 0.0, 'median': 11.0, 'iqr': 18.0, 'hasOutliers': True, 'quartileThree': 23.0, 'gtoht': 1709, 'gtohto': 827, 'ohto': 77.0, 'mean': 20.646429266394239}</dd>
<dt>Singletons</dt><dd>9900</dd>
<dt>MultiStation Groups</dt><dd>23</dd>
</dl>



CVIX,USER is smaller ...

Number of Days
:    115

By Day Stats
:    {'std': 7.3230815664916387, 'max': 29, 'quartileOne': 4.0, 'oht': 29.0, 'total': 1194, 'count': 115, 'min': 1, 'median': 9.0, 'iqr': 10.0, 'hasOutliers': False, 'quartileThree': 14.0, 'ohto': 44.0, 'mean': 10.382608695652173}

IPs
:    {"10.206.8.88": 1, "10.152.80.125": 1191, "10.206.8.77": 1, "10.206.8.86": 1}

Stations
:    200 [326], 2001 [868]

Count Props
:    {"19": 868, "20": 326}

With Remote App
:    326

With 'workstation_name'
:    0

Devices
:    {"NULL": 879, "TCP": 315}

Level of Assurances
:    {"1": 868, "2": 326}

Groups
:    996

Gap
:    0:01:40

Gap Stats
:    {'std': 286.68663853135223, 'max': 1421.0, 'quartileOne': 12.5, 'oht': 242.5, 'total': 150807.0, 'count': 995, 'min': 0.0, 'median': 39.0, 'iqr': 92.0, 'hasOutliers': True, 'quartileThree': 104.5, 'gtoht': 141, 'gtohto': 115, 'ohto': 380.5, 'mean': 151.56482412060302}

<dl>
<dt>Singletons</dt><dd>843</dd>
<dt>MultiStation Groups</dt><dd>0</dd>
</dl>


__TODO__: distinguish levels of assurance, device (TCP or not), workstation or not.
