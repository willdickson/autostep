<template>
  <div class="configuration"> 

    <br>
    <b-container fluid>

      <b-row>
         <b-col>
          <b-form  v-on:reset.prevent v-on:submit.prevent>

            <b-button v-on:click="onGetValues" variant="outline-primary" > Get Values  </b-button>

            &nbsp;
            &nbsp;
            <b-button v-on:click="onSetValues" variant="outline-primary"> Set Values </b-button>
            <br> <br> <br>

            <b-form-group v-for="(item,key) in configOptions" v-bind:label="getItemLabel(item)" v-bind:key="item.label" >

              <b-form-select v-if="item.type==='select'" v-bind:options="item.options" v-model="configValues[key]" v-bind:disabled="configDisabled[key]" required  class="w-25">
              </b-form-select>

              <b-form-input v-if="item.type==='number'"  v-model="configValues[key]"  required class="w-25">
              </b-form-input>


              <b-form-checkbox v-if="item.type==='checkbox'" v-model="configValues[key]" v-on:change="onCheckboxChange(key)">
                {{item.label}} <span v-if="configValues[key]" class="text-warning"> - could damage drive!!! </span>
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
import {mapGetters} from 'vuex';

export default {
  name: 'Configuration',
  data () {
    return {
      dummy: false,
    }
  },
  computed: {
    ...mapState([
      'socket',
      'configOptions',
      'configValues',
      ]),
    ...mapGetters([
      'configDisabled',
    ]),
  },
  methods: {
    onGetValues() {
      console.log('onGetValues');
      //console.log(this.configValues);
      //console.log(JSON.stringify(this.configValues));
      //console.log(JSON.stringify(this.configDisabled));
      this.socket.emit('getConfigValuesRequest', {});
    },
    onSetValues() {
      console.log('onSetValues');
      this.socket.emit('setConfigValuesRequest', this.configValues);
    },
    onCheckboxChange(key) {
      if (key === 'voltCurrOptionsEnable') {
      }
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
