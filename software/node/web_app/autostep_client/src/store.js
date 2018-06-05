"use strict";
import Vue from 'vue'
import Vuex from 'vuex'
import {configOptions} from './config_options.js'
import {getDefaultValues} from './config_tools.js'
let _ = require('lodash');

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    socket: null,
    configChanged: false,
    configOptions: configOptions,
    configValues: getDefaultValues(configOptions),
  },

  mutations: {

    setSocket(state, socket) {
      state.socket = socket;
    },

    setConfigChanged(state, value) {
      state.configChanged = value;
    },

    setConfigValues(state, newConfigValues) {
      state.configValues = newConfigValues;
    },

  },

  getters: {

    configDisabled: (state, getters) => {
      let disabledValues = {};
      for (let key in state.configValues) {
        if (_.includes(['threshold', 'kvalRun', 'kvalHold', 'kvalAccel', 'kvalDecel'], key)) {
          disabledValues[key] = !state.configValues.voltCurrOptionsEnable;
        } else {
          disabledValues[key] = false;
        }
      }
      return disabledValues;
    },

    configValid: (state, getters) => {
      let isValid = {};
      for (let key in state.configValues) {
        if (state.configOptions[key].type === 'number') {
          isValid[key] = _.isFinite(Number(state.configValues[key]));
        } else {
          isValid[key] = true;
        }
      }
      return isValid;
    },

    configAllValid: (state, getters) => {
      return !_.every(getters.configValid);
    },

  },

});


