'use strict';

const fs = require("fs");
const _ = require("lodash");

/*
 * Crude - write out metaRPCMeta with [a] list of meta RPCs, [b] list of files they use, [c] files per RPC with files
 *
 * Relies on VDP nonClinicalRPCs (so doesn't take upgraded definitions in VAM) and
 * *** WARNING ***, nonClinicalRPC git isn't complete. Hence need to fix files/type
 * of definitions below (see INCLUDE_NCGIT_MISSING)
 * 
 * ** WILL BE REMOVED WITH BUILD 2 ** as approach not needed (move to Mongo done)
 *
 * A/C for issues with Meta RPC descriptions
 *
 * Note: Lex files (757*) are missing and will have to be added manually later
 */

// Note: many may have been fixed (list made mid Sept 2017)
const FILE_FIXES = {

    "ORWDAL32 ALLERGY MATCH": ["120.82", "50.6", "50.67", "50.416", "50.605", "50.68"], // 120.83 -> 120.82
    "ORQQPL PROB COMMENTS": ["9000011", "9000011.11"], // extra 0 but also this is a clinical RPC so why in meta set?
    "XUS PKI GET UPN": ["501"], // not 501.1
    "ORWDXM FORMID": ["101.41", "100.98", "9.4"], // 100.41 -> 101.41
    "ORWGRPC TESTSPEC": ["60"], // from 60.01 to 60
    "XUS PKI GET UPN": ["200"], // 501 is the field #, not the file #
    "GMV PARAMETER": ["8989_5", "8989.3", "8989.51", "8989.518"], // added 8989_5, parameter values
    "ORWDX DLGDEF": ["101.41"], // 101.412 is a multiple
    
    "ORQQPL INIT USER": ["125.99", "49", "200"], // 125.99 added to other two already there
    
    "TIU TEMPLATE GETROOTS": ["8927"],
   
    "ORWPCE GET SET OF CODES": ["9000010_11", "9000010_12", "9000010_16", "9000010_23", "9000010_13"] // very unusual returns enums/set of codes (should be in files?)

};

/*
 Left in ORWPT_CLINRNG as despite ORWPT, it returns range of dates for clinics (hard coded!)
 */
const EXCLUDE_AS_CLINICAL = [
    "ORQQPL PROB COMMENTS", // about clinical problems
    "ORWDPS32 AUTH", // references Order 100 which is clinical
    "ORCNOTE GET TOTAL", // for 8925, clinical documents
    "TIU GET DEFAULT PROVIDER", // though one of many srcs of default provider, 8925, clinical doc is still there
    "TIU REQUIRES COSIGNATURE", // references 8925
    "ORWPCE NOTEVSTR", // clinical 8925
    
    "ORWDPS1 ODSLCT", // takes DFN - was mischar'ed before 1.1 as NONCLINICAL
    
    "ORWPT SHARE", // sets TMPs for other routines (in Pei list but probably out of scope) - was in NC but shouldn't have been
    "ORPRF CLEAR", // clears TMP for PRF for this $J ie/ for this session. In VISTA item.
    
    "ORWCV POLL", // may be out of scope completely when done ie/ VISTA only	 	 	 	 	 
    "ORWCV START", // may be out of scope completely when done,
    
    "ORWDX LOCK", // locking put to Clinical Work - Order lock but used for Allergy too
    "ORWDX UNLOCK",
    
    "ORWDPS2 DAY2QTY" // PAT passed in but may just be inserted in Formatted Result. Either way - clinical and for pharmacy.
];

const PARAM_FIXES = {
    "ORWGRPC TESTSPEC": [] // none 
};

// All in Coversheet flow as Meta NC but weren't in NC GIT (or MIM before)
// includes VISTA only's just for completeness with Meta's
const INCLUDE_NCGIT_MISSING = [

    // not in old captures - PARAM: ORWCH BOUNDS
    { id: "ORWCH_SAVESIZ", name: "ORWCH SAVESIZ", parameters: ["ORWCH BOUNDS"], complexity: "LOW", "rpcType": "CHANGE" },
    
    { id: "ORWPCE_I10IMPDT", name: "ORWPCE I10IMPDT", complexity: "MEDIUM", "rpcType": "READ" }, // was in out of scope - Lexicon
    
    { id: "ORWRP_GET_DEFAULT_PRINTER", name: "ORWRP GET DEFAULT PRINTER", parameters: ["ORWDP WINPRINT DEFAULT", "ORWDP DEFAULT PRINTER"], complexity: "LOW", "rpcType": "READ"  }, // was in out of scope
    
    { id: "ORWU_NPHASKEY", name: "ORWU NPHASKEY", complexity: "LOW", "rpcType": "READ"  }, // was in auth/out of scope - XUSEC
    
    { id: "ORWU_OVERDL", name: "ORWU OVERDL", parameters: ["ORPARAM OVER DATELINE"], complexity: "LOW", "rpcType": "READ" }, // not known
    
    { id: "XUS_DIVISION_GET", name: "XUS DIVISION GET", files: ["200", "4"], complexity: "MEDIUM", "rpcType": "READ"  }, // wasn't in nc GIT though clearly NC and needed

    { id: "XUS DIVISION SET", name: "XUS DIVISION SET", complexity: "MEDIUM", rpcType: "CHANGE", files: ["200", "4"] },
    
    { id: "XUS_AV_CODE", name: "XUS AV CODE", files: ["200"], "rpcType": "UTILITY" }, // mixed in Router but mainly VISTA
    
    { id: "XWB_CREATE_CONTEXT", name: "XWB CREATE CONTEXT", files: ["19"], complexity: "HIGH", rpcType: "CHANGE" }, // will go into VISTA only but want in total meta list (note: files/parameters list may not be complete
    
    { id: "XWB_DEFERRED_CLEARALL", name: "XWB DEFERRED CLEARALL", rpcType: "UTILITY" }, // will go into VISTA only but want in total meta list
    
    { id: "ORWPCE_ACTIVE_CODE", name: "ORWPCE ACTIVE CODE", rpcType: "READ" }, // lexicon data, used in Problem domain
    
    { id: "TIU_TEMPLATE_GETROOTS", name: "TIU TEMPLATE GETROOTS", rpcType: "READ" }, // used in Allergy, will push to B3 for TIU

    { id: "ORQPT_DEFAULT_LIST_SORT", name: "ORQPT DEFAULT LIST SORT", rpcType: "READ", "parameters": ["ORLP DEFAULT LIST ORDER"], complexity: "LOW" },

    { id: "ORWPT_DFLTSRC", name: "ORWPT DFLTSRC", rpcType: "READ", "parameters": ["ORLP DEFAULT LIST SOURCE"], complexity: "LOW" }
    
];

// from static look at params - should do automatically (all but 801.5 there already)
const FILES_IN_PARAM_VALUE_DOMAINS = ["811.7", "101.41", "100.03", "100.98", "801.5", "101.24"];

const metaEmulatorModelCore = require('../../../nonClinicalRPCs/prototypes').rpcEmulatorModel;
// for now: utilities not like others - not in default unified emulator model - need to add
const metaUtilityEmulatorModel = require('../../../nonClinicalRPCs/prototypes/utility').rpcEmulatorModel;
const metaEmulatorModel = metaEmulatorModelCore.concat(metaUtilityEmulatorModel);
const metaEmulatorModelPlus = metaEmulatorModel.concat(INCLUDE_NCGIT_MISSING);

// Does this agree with the 'files' list or is it bigger?
const metaVDMModel = require('../../../nonClinicalRPCs/prototypes').vdmModel;

let fls = new Set();
let flsByRPC = {};
let rpcs = [];
let params = new Set();
let paramsByRPC = {};
let rpcProps = {};
for (var rpcMeta of metaEmulatorModelPlus) {
    if (_.includes(EXCLUDE_AS_CLINICAL, rpcMeta.name)) {
        console.log("Must exclude %s Clinical RPC", rpcMeta.name)
        continue;
    }
    rpcs.push(rpcMeta.name);

    let rpcFiles = [];
    if (FILE_FIXES.hasOwnProperty(rpcMeta.name)) {
        rpcFiles = FILE_FIXES[rpcMeta.name];
        console.log("Fix %s", FILE_FIXES[rpcMeta.name]);
        console.log("\t... %s", rpcMeta.files);
    }
    else {
        if (
            (rpcMeta.hasOwnProperty("files")) &&
            !((rpcMeta.files.length === 0) || ((rpcMeta.files.length === 1) && (rpcMeta.files[0].length === 0)))
            ) 
        {
            rpcFiles = rpcMeta.files.filter(function(fl) {return ((fl.length > 0) && (!/[A-Z]/.test(fl)));});
        }
    }
    if (rpcFiles.length !== 0) {
        // split up fls - sometimes "X,Y" not "X","Y" and replace _ with .
        let nrpcFiles = [];
        for (var fl of rpcFiles) {
            if (/\,/.test(fl)) {
                for (var sfl of fl.split(/\, */)) {
                    nrpcFiles.push(sfl.replace("_", "."));
                }
            }
            else {
                nrpcFiles.push(fl.replace("_", "."));
            }
        }
        flsByRPC[rpcMeta.name] = [];
        for (var fl of nrpcFiles) {
            fls.add(fl);
            flsByRPC[rpcMeta.name].push(fl);
        }
    }

    if (PARAM_FIXES.hasOwnProperty(rpcMeta.name)) {
        rpcMeta.parameters = PARAM_FIXES[rpcMeta.name];
    }
    if (!rpcMeta.hasOwnProperty("parameters") || (rpcMeta.parameters.length === 0))
        continue;
    // VARIABLE is a particular parameter
    if ((rpcMeta.parameters.length === 1) && (rpcMeta.parameters[0] === "VARIABLE"))
        continue;
    paramsByRPC[rpcMeta.name] = [];
    for (var param of rpcMeta.parameters) {
        params.add(param);
        paramsByRPC[rpcMeta.name].push(param);
    }

    let props = {};
    ["complexity", "rpcType", "domain"].forEach(function(prop) {
        if (rpcMeta.hasOwnProperty(prop)) {
            props[prop] = rpcMeta[prop];
        }
    });
    rpcProps[rpcMeta.name] = props;
}

// For those missing from NC Git but needed for Coversheet



// add manually to files for files referenced in parameters
new Set(FILES_IN_PARAM_VALUE_DOMAINS).forEach(fls.add, fls);

console.log("RPCs:", rpcs.length);
console.log("Files:", fls.size);
console.log("RPCs with Files:", Object.keys(flsByRPC).length);
console.log("Parameters:", params.size);
console.log("RPCs with parameters:", Object.keys(paramsByRPC).length);

/*
 Some are utils but some should get files defns (TODO)

 # ORWPCE GET SET OF CODES (should take certain files but we don't seem to bound them)
 # ORWLEX GETFREQ ... no lex spec'ed but should be
 */
let rpcsNone = rpcs.filter(x => !(_.has(flsByRPC, x) || _.has(paramsByRPC, x)));
console.log("RPCs with neither files nor parameters:", rpcsNone.length);
console.log("\t", rpcsNone.sort());

let metaRPCMeta = {files: Array.from(fls), rpcs: rpcs, params: Array.from(params), filesByRPC: flsByRPC, paramsByRPC: paramsByRPC, rpcProps: rpcProps};
fs.writeFile("metaRPCMeta.json", JSON.stringify(metaRPCMeta, null, 4));

/*
  EXTRA: use VDM definition of NC RPC - see which are NOT in files of RPCs (and extras
  like 757. Seem to be either [a] patient files or [b] extraneous files not used by
  any emulated RPC but were used in early (conor) tests.

  When look at VDM model in code, see file/class defns that go unused in the RPC defns
  ... issue?
 
    "800": ["ORQQPXRM REMINDER WEB"], // CLINICAL REMINDERS PARAMETERS
    "34": [], // ? don't see any for radiology's CONTRACT/SHARING AGREEMENTS
    "3.5": [],
    "45.7": [], // treating speciality - surprising absence
    "119.9": ["ORWDFH OPDIETS"], 
    "123.3": ["ORQQCN DEFAULT REQUEST REASON", "ORQQCN EDIT DEFAULT REASON"],
    "142.5": ["ORWRP2 HS COMP FILES"],
    "79.3": ["ORWDRA32 IMTYPSEL"],
    "40.5": [],
    "79.2": ["ORWDRA32 IMTYPSEL"],
    "69.9": ["ORWLRR PARAM"], # lab setup
    "100.9": ["ORWTPR NOTDESC"],
    "100.5": ["OREVNTX ACTIVE"],
    "100.8": ["ORWTPR OCDESC"],
    "125.12": ["ORQQPL USER PROB LIST"],
    "8925.95": [], // TIU Document Parameters - probably just missing as not doing captures for docs
    "8925.99": [], // another TIU config
    "8925.98": ["TIU GET DS TITLES"], 
    "9999999.17": ["ORWPCE GET TREATMENT TYPE"],
    "790.1": ["ORQQPXRM GET WH REPORT TEXT"]
    
  Also some files (81, 81.1) are only referenced indirectly - but surely some RPCs use 
  them directly?
  
  ... TODO: revisit when get full scope (omissions should show up)

let metaVDMIds = metaVDMModel.map(x => x.fmId);
console.log("VDM Files - not in files:", metaVDMIds.filter(x => !fls.has(x)));
 */ 



