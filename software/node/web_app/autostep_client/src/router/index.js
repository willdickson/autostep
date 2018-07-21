import Vue from 'vue'
import Router from 'vue-router'
import Configuration from '@/components/Configuration'
import MoveRun from '@/components/Move'
import Sinusoid from '@/components/Sinusoid'

Vue.use(Router);

export default new Router({
  routes: [
  {
    path: '/',
    redirect: Configuration
  },
  {
    path: '/configuration',
    name: 'Configuration',
    component: Configuration
  },
  {
    path: '/move',
    name: 'Move',
    component: MoveRun
  },
  {
    path: '/sinusoid',
    name: 'Sinusoid',
    component: Sinusoid
  }
  ]
});
