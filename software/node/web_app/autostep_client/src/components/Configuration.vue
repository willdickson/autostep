<template>
  <div class="configuration"> 

    <br>
    <b-container fluid>
      <b-row>
        <b-col cols="4">

          <b-form>

            <!--
            <b-form-group>

            </b-form-group>
            -->


            <b-form-group label="Fullsteps/Revolution">
              <b-form-input>
              </b-form-input>
            </b-form-group>

            <b-form-group label="Step Mode">
              <b-form-input>
              </b-form-input>
            </b-form-group>

            <b-form-group label="Over Current Threshold">
              <b-form-input>
              </b-form-input>
            </b-form-group>


          </b-form>
        </b-col>

      </b-row>
    </b-container>

  </div>
</template>

<script>
export default {
  name: 'Configuration',
  data () {
    return {
      msg: 'Configuration'
    }
  }
}
</script>

<style scoped>
</style>
