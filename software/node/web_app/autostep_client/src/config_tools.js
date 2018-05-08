"use strict";

export function getDefaultValues(configOptions) {
  let defaultValues = {};
  for (let item in configOptions) {
    defaultValues[item] = configOptions[item].defaultValue;
  }
  return defaultValues;
};
