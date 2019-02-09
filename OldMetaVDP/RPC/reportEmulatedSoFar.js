#!/usr/bin/env node

'use strict';

const fs = require('fs');

/*
 * requires emulation code from rpcServer (mvdm module) to produce a json in /json for use
 * in reports
 *
 * TODO:
 * - unsupported RPCs is a hashmap ... look at how to dump keys ... add to unsupported
 * - when modelsClinical moved (same as nc etc) then remove special handling
 * - when (off plane) MVDM update and include MVDM git/module in here ... npm install mvdm
 */

// used by rpcQWorker.js to fill emulated RPCs
var CONFIG = require('../../../nodevista/rpcServer/cfg/config.js');
var unsupportedRPCs = require('../../../nodevista/rpcServer/unsupportedRPCs.js');

const RPCDIVISIONS = { // used in category division json
    "Clinical": "CLINICAL",
    "Non-Clinical": "NON CLINICAL",
    "Out-Of-Scope": "OUT OF SCOPE",
    "JS Utility": "NON CLINICAL"
};

/**
 * Generate JSON summary of emulated RPCs - based on nodevista/rpcServer/rpcQWorker.js, createDispatcher
 */
function assembleEmulation() {

    // Grab the emulator definition object array from the configuration
    const emulators = CONFIG.emulators || [];

    let vdmModels = [];
    let mvdmModels = [];
    let rpcsEmulatedByDivision = {};

    let DEFNS_LOCN = "../../../nodevista/rpcServer/";

    emulators.forEach((emulator) => {

        const name = emulator.name.split(" Emulator")[0] || 'UNKNOWN';

        if (!RPCDIVISIONS.hasOwnProperty(name)) {
            throw new Error(`Invalid type of RPC emulator ${name}`);
        }

        console.log(`Processing emulator: ${name}...`);

        try {

            // If that was successful, load all the models specified for this emulator via module paths
            const modelPaths = emulator.models || [];
            modelPaths.forEach((modelPath) => {

                // modelsClinical is not in MVDM but at rpcServer level. May move later.
                // ... nix node_modules and explicitly install mvdm here
                modelPath = /modelsClinical/.test(modelPath) ? DEFNS_LOCN + "modelsClinical" : DEFNS_LOCN + "node_modules/" + modelPath;

                console.log(`Loading models from ${modelPath} of ${name}`);

                // eslint-disable-next-line
                const model = require(modelPath);

                // For now, only processing RPCs emulated - will process VDMs later ie/ for file cover
                if (model.vdmModel) {
                    // add to existing vdm model list (VDM is a singleton)
                    vdmModels = vdmModels.concat(model.vdmModel);
                }
                if (model.mvdmModel) {

                    mvdmModels = mvdmModels.concat(model.mvdmModel);
                }
                if (model.rpcEmulatorModel) {
                    let division = RPCDIVISIONS[name];
                    if (!rpcsEmulatedByDivision.hasOwnProperty(division))
                        rpcsEmulatedByDivision[division] = {};
                    model.rpcEmulatorModel.forEach(function(defn) {
                        rpcsEmulatedByDivision[division][defn.name] = name;
                    });
                }
            });

            console.log(`Successfully processed emulator: ${name}`);
        } catch (e) {
            console.log(`ERROR processing emulator: ${name} - ${e.toString()}`);
        }
    });

    let fd = fs.openSync("json/rpcsEmulatedSoFar.json", "w");
    fs.writeSync(fd, JSON.stringify(rpcsEmulatedByDivision, null, 4));
    fs.closeSync(fd);

    console.log("JSON of emulated so far placed in /json");
}

assembleEmulation();
