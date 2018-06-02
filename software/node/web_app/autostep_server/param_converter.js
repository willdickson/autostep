"use strict";
const _ = require('lodash');


const SPECIAL_KEYS = ['kval', 'jogMode', 'maxMode'];
const OMITTED_KEYS = ['voltCurrOptionsEnalbe'];

let containsSubStringFromArray = function(testString,testArray) { 
  let testVal = false;
  let subStringMatch = null;
  for (let i=0; i<testArray.length; i++) { 
    let subString = testArray[i];
      if (_.includes(testString,subString)) {
        testVal = true;
        subStringMatch = subString;
        break;
      }
    }
  return testVal;
};


let convertParamsAppToDev = function(paramsApp) {
  let paramsDev = {};
  for (let key in paramsApp) {
    if (containsSubStringFromArray(key,OMITTED_KEYS)) {
      continue;
    } else if (containsSubStringFromArray(key,SPECIAL_KEYS) ) {
      console.log(key);
    } else {
      paramsDev[key] = paramsApp[key];
    }
  }
  return paramsDev;
};

let convertParamsDevToApp = function(paramsDev) {
  let paramsApp = _.omit(paramsDev, ...SPECIAL_KEYS);
  for (let i=0; i<SPECIAL_KEYS.length; i++) {
    let key = SPECIAL_KEYS[i];
    for (let subKey in paramsDev[key]) {
      let newKey = key + _.upperFirst(subKey);
      paramsApp[newKey] = paramsDev[key][subKey];
    }
  }
  return paramsApp;
};

module.exports = {convertParamsAppToDev, convertParamsDevToApp};


