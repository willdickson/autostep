import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import io from 'socket.io-client'
import App from './App'
import {store} from './store'

Vue.config.productionTip = false;

Vue.use(BootstrapVue);

new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>',
  mounted: function() {

    // Setup socket
    let socket = null;
    if (location.port === '8080') {
      // Using the development server
      socket = io.connect('http://localhost:5000');
    } else {
      // Served by webapp
      socket = io.connect('http://' + document.domain  + ':' + location.port);
    }
    store.commit('setSocket', socket);
    socket.emit('testMessage', {data:'hello from client'});
  }
});
