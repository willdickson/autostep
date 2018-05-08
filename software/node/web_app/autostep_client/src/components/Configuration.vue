<template>
  <div class="configuration"> 

    <br>
    <b-container fluid>

      <b-row>
         <b-col>
          <b-form  v-on:reset.prevent v-on:submit.prevent>

            <b-button v-on:click="onGetValues" variant="outline-primary"> Get Values  </b-button>
            &nbsp;
            &nbsp;
            <b-button v-on:click="onSetValues" variant="outline-primary"> Set Values </b-button>
            <br> <br> <br>
            <b-form-group v-for="(item,key) in configOptions" v-bind:label="getItemLabel(item)" v-bind:key="item.label" >
              <b-form-select v-if="item.type==='select'" v-bind:options="item.options" v-model="configValues[key]" required  class="w-25">
              </b-form-select>
              <b-form-input v-if="item.type==='number'"  v-model="configValues[key]"  required class="w-25">
              </b-form-input>
              <b-form-checkbox v-if="item.type==='checkbox'">
                {{item.label}}
              </b-form-checkbox>
            </b-form-group>

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
      msg: 'Configuration',
    }
  },
  computed: {
    ...mapState([
      'configOptions',
      'configValues',
      'configDisabled',
      ]),
  },
  methods: {
    onGetValues() {
      console.log('onGetValues');
      console.log(this.configValues);
      console.log(JSON.stringify(this.configValues));
    },
    onSetValues() {
      console.log('onSetValues');
    },
    getItemLabel(item) {
      if (item.type === 'checkbox') {
        return '';
      } else {
        return item.label;
      }
    },
    getItemActive(item,key) {
      return false;
    }
  },
}
</script>

<style scoped>
</style>
