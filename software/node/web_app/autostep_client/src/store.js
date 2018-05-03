"use strict";
import Vue from 'vue'
import Vuex from 'vuex'
import {configOptions} from './config_options.js'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    socket: null,
    configOptions: configOptions,
  },

  mutations: {

    setSocket(state, socket) {
      state.socket = socket;
    },
  }

});


