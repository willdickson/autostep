<template>
  <div class="appnavbar">

    <div>
      <b-navbar toggleable="md" type="dark" variant="primary"> 
        <b-navbar-brand> <b> Autostep Controller </b> </b-navbar-brand>
      </b-navbar>
    </div>

    <div>
      <b-nav tabs>
        <b-nav-item to="configuration" v-bind:disabled="navbarDisabled.configuration">
          <b> Configuration </b>
        </b-nav-item>
        <b-nav-item to="move" v-bind:disabled="navbarDisabled.move">
          <b> Move/Jog </b>
        </b-nav-item>
        <b-nav-item to="sinusoid" v-bind:disabled="navbarDisabled.sinusoid">
          <b> Sinusoid </b>
        </b-nav-item>
      </b-nav>
    </div>

  </div>
</template>

<script>

import {mapState} from 'vuex';

export default {
  name: 'AppNavBar',
  data () {
    return {
    }
  },
  computed: {
    ...mapState(['navbarDisabled']),
  },
}

</script>

<style scoped>
</style>
