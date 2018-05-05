<template>
  <div class="appnavbar">

    <div>
      <b-navbar toggleable="md" type="dark" variant="primary"> 
        <b-navbar-brand> <b> Autostep Controller </b> </b-navbar-brand>
      </b-navbar>
    </div>

    <div>
      <b-nav tabs>
        <b-nav-item to="configuration">
          <b> Configuration </b>
        </b-nav-item>
        <b-nav-item to="moverun">
          <b> Move/Run </b>
        </b-nav-item>
        <b-nav-item to="sinusoid">
          <b> Sinusoid </b>
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
