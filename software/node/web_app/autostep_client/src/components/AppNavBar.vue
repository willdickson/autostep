<template>
  <div class="appnavbar">
    <b-navbar toggleable="md" type="dark" variant="primary"> 
      <b-navbar-brand> Autostep </b-navbar-brand>

      <b-navbar-nav>
        <b-nav-item-dropdown text="Option" right>
          <b-dropdown-item to="configuration">
            Configuration
          </b-dropdown-item>
          <b-dropdown-item to="moverun">
            Move/Run
          </b-dropdown-item>
          <b-dropdown-item to="sinusoid">
            Sinusoid
          </b-dropdown-item>
        </b-nav-item-dropdown>

      </b-navbar-nav>

    </b-navbar>


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
