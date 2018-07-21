"use strict";
import Vue from 'vue'
import Vuex from 'vuex'
import {configOptions} from './config_options.js'
import {getDefaultValues} from './config_tools.js'
let _ = require('lodash');

Vue.use(Vuex);

export const store = new Vuex.Store({
  //strict: true,
  state: {
    socket: null,
    configChanged: false,
    configOptions: configOptions,
    configValues: getDefaultValues(configOptions),
    driveState: { enabled: true, running: false, position: 0},
    runJogParams: {jogValue: 10, moveValue: 0},
    sinusoidParams: {amplitude: 30, period: 2.5, phase: 90.0, offset: 0.0, num_cycle: 1}, 
    positionTimerEnabled: true,
    navbarDisabled: {configuration: false, move: false, sinusoid: false},
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

    setDriveState(state, value) {
      state.driveState = value;
    },

    setRunJogParams(state, params) {
      state.runJogParams = params;
      console.log('setRunJogParams');
    },

    setObjectProperty(state, payload)
    {
      state[payload['objectName']][payload['propertyName']] = payload['value'];
    },

    setPositionTimerEnabled(state,value) {
      state.positionTimerEnabled = value;
      state.socket.emit('setPositionTimerEnabled', {value: value});
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


