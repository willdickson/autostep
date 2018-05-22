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
    configOptions: configOptions,
    configValues: getDefaultValues(configOptions),
  },

  mutations: {

    setSocket(state, socket) {
      state.socket = socket;
    },

    setConfigValues(state, newConfigValues) {
      state.configValues = newConfigValues;
    },
  },

  getters: {
    configDisabled: (state, getters) => {
      let disabledValues = {};
      for (let key in state.configValues) {
        if (_.includes(['OCThreshold', 'kvalRun', 'kvalHold', 'kvalAccel', 'kvalDecel'], key)) {
          disabledValues[key] = !state.configValues.voltCurrOptionsEnable;
        } else {
          disabledValues[key] = false;
        }
      }
      return disabledValues;
    },
  },

});


