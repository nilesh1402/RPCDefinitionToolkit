# CPRS RPC Analysis/Breakdown

Sources of information:
  * CPRS Source
  * VISTA Source - RPC entry points
  * file 8994 from VISTA
and manual categorization/description.

Approach is to collect meta data in jsons and then generate markdown(s) from that.

__Key Generated Report__: [CPRS RPC Breakdown](http://vistadataproject.info/artifacts/cprsRPCBreakdown/bdStart)
... also generates stats and RPC test code

## Assembling RPC List

  * CPRS Source
  * Option [OR CPRS GUI CHART](http://localhost:9000/rambler#19-8552)

## Source of CPRS

First run _parseCPRSSource_, then _parseCPRSExe_.

From [CPRS Chart](https://github.com/OSEHRA/VistA/tree/master/Packages/Order%20Entry%20Results%20Reporting/CPRS/CPRS-Chart) and [Vitals DLL](https://www.osehra.org/document/guis-used-automatic-functional-testing).

__Note__: current version is 30.16 - the # of CPRS RPCs we have in reports reflects this source code. OSEHRA's check in had this comment ...

> Update to the latest version of CPRS source code available from the
> foia-vista.osehra.org download site.  This code was taken from the
> "CPRS 30A emergency patch scrubbed.zip" download.

and the exe available from OSEHRA (CPRSChart.exe) which has RPCs not in the source.

Note: more pascal source code is in the [RPC Broker](https://github.com/OSEHRA/VistA/tree/1ce23e76b0d904d0a77912671ef60c581acde582/Packages/RPC%20Broker/BDK) on OSEHRA and Chris Uyehara has [FOIA CPRS on bitbucket](https://bitbucket.org/ckuyehar/foia-cprs/src/d2cdc796fa71eafbd7e1a67861b96ef586b48c2d/CPRS-Chart/rProbs.pas?at=OR_30_280&fileviewer=file-view-default#rProbs.pas-39).

How CPRS-Chart retrieved

A sparce git checkout ...

```text
>> cd /tmp
>> mkdir CPRS
>> cd CPRS
>> git init
Initialized empty Git repository in /private/tmp/CPRS/.git/
>> git remote add -f origin https://github.com/OSEHRA/VistA.git
Updating origin
remote: Counting objects: 13376, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 13376 (delta 0), reused 0 (delta 0), pack-reused 13372
Receiving objects: 100% (13376/13376), 30.82 MiB | 2.06 MiB/s, done.
Resolving deltas: 100% (5175/5175), done.
From https://github.com/OSEHRA/VistA
 * [new branch]      dashboard  -> origin/dashboard
 * [new branch]      foia       -> origin/foia
 * [new branch]      hooks      -> origin/hooks
 * [new branch]      master     -> origin/master
 * [new tag]         OSEHRA-CPRS-v28 -> OSEHRA-CPRS-v28
>> git config core.sparseCheckout true
>> echo "Packages/Order Entry Results Reporting/CPRS/CPRS-Chart" >> .git/info/sparse-checkout
>> git pull origin master
From https://github.com/OSEHRA/VistA
 * branch            master     -> FETCH_HEAD
>> ls Packages/Order\ Entry\ Results\ Reporting/CPRS/CPRS-Chart/
BA				fDCSumm.pas			fMedCopy.dfm			fPtSelDemog.pas			fxLists.dfm
CMakeLists.txt			fDCSummProps.dfm		fMedCopy.pas			fPtSelMsg.dfm			fxLists.pas
...
>> mv Packages/Order\ Entry\ Results\ Reporting/CPRS/CPRS-Chart .

```
