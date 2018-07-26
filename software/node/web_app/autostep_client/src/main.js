import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import io from 'socket.io-client'
import App from './App'
import {store} from './store'
import {mapState} from 'vuex';
import _ from 'lodash';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);

new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>',
  computed: {
    ...mapState([
      'configValues',
      'positionTimerEnabled',
      ]),
  },
  mounted: function() {

    // Setup socket
    let socket = null;
    if (location.port === '8080') {
      // Using the development server
      //socket = io.connect('http://localhost:5000');
      socket = io('http://localhost:5000',{transports:['websocket']});
    } else {
      // Served by webapp
      socket = io.connect('http://' + document.domain  + ':' + location.port, {transports:['websocket']});
    }
    store.commit('setSocket', socket);
    socket.on('getConfigValuesResponse', (data) => {
      this.$store.commit('setConfigValues',data);
    });
    socket.on('setConfigValuesResponse', (data) => {
      this.$store.commit('setConfigChanged', false);
    });
    socket.on('getPositionResponse', (data) => {
      let value = data.position;
      let payload = {value: data.position, objectName: 'driveState', propertyName: 'position'};
      this.$store.commit('setObjectProperty',payload);
    });
    let resetAfterTrajectory = () => {
        this.$store.commit('setPositionTimerEnabled', true);
        this.$store.commit('setObjectProperty', {
          objectName: 'navbarDisabled', 
          propertyName: 'configuration', 
          value: false 
        });
        this.$store.commit('setObjectProperty', {
          objectName: 'navbarDisabled', 
          propertyName: 'move', 
          value: false 
        });
    };
    socket.on('stopMotionResponse', (data) => {
      resetAfterTrajectory();
    });
    socket.on('trajectoryData', (data) => {
      if ((data === null) || _.isEmpty(data) ) {
        resetAfterTrajectory();
      } else {
        this.$store.commit('updatePositionData',{t: data.t, p: data.p});
      }
    });
    socket.emit('enableDrive', {});
    socket.emit('getConfigValuesRequest', this.configValues);
    this.$store.commit('setPositionTimerEnabled', this.positionTimerEnabled);
    socket.emit('setPositionTimerEnabled', {value: this.positionTimerEnabled});
  }
});
