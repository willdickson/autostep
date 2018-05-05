<template>
  <div class="configuration"> 

    <br>
    <b-container fluid>

      <b-row>
         <b-col>
          <b-form>

            <b-form-group v-for="item in configOptions" v-bind:label="item.label" v-bind:key="item.label" class="w-50" horizontal >
              <b-form-select v-if="item.type=='select'" v-bind:options="item.options" required class="w-50">
              </b-form-select>
              <b-form-input v-if="item.type=='number'" required  class="w-50" >
              </b-form-input>
            </b-form-group>

            <br>
            <b-button type="submit" variant="outline-primary"> Set Values </b-button>
            &nbsp;
            <b-button type="reset"  variant="outline-primary"> Get Values  </b-button>

          </b-form>
        </b-col>

      </b-row>
    </b-container>

  </div>
</template>

<script>

import {mapState} from 'vuex';

export default {
  name: 'Configuration',
  data () {
    return {
      msg: 'Configuration'
    }
  },
  computed: {
    ...mapState([
      'configOptions'
    ])
  }
}
</script>

<style scoped>
</style>
