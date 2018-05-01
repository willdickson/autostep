<template>
  <div class="appnavbar">

    <div>
      <b-navbar toggleable="md" type="dark" variant="primary"> 
        <b-navbar-brand> Autostep Controller</b-navbar-brand>
      </b-navbar>
    </div>

    <div>
      <b-nav tabs>
        <b-nav-item to="configuration">
          Configuration
        </b-nav-item>
        <b-nav-item to="moverun">
          Move/Run
        </b-nav-item>
        <b-nav-item to="sinusoid">
          Sinusoid
        </b-nav-item>
      </b-nav>
    </div>

  </div>
</template>

<script>
export default {
  name: 'AppNavBar',
  data () {
    return {
    }
  }
}
</script>

<style scoped>
</style>
