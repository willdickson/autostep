<template>
  <div id="app">
    <AppNavBar/>
    <br>
    <b-container fluid>
      <b-row>
        <b-col>
          <router-view> </router-view>
        </b-col>
      </b-row>
  </b-container>
  </div>
</template>

<script>

import AppNavBar from './components/AppNavBar'

export default {
  name: 'App',
  components: {
    AppNavBar
  }
}
</script>

<style> </style>
