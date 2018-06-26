<template>
  <div class="configuration"> 

    <br>
    <b-container fluid>

      <b-row>
         <b-col>

           <b-form  
             v-on:reset.prevent 
             v-on:submit.prevent
             >

            <b-button 
              v-on:click="onGetValues" 
              variant="outline-primary"> 
              Get Values  
            </b-button>

            &nbsp;
            &nbsp;

            <b-button 
              v-on:click="onSetValues" 
              variant="outline-primary" 
              v-bind:disabled="configAllValid"> 
              Set Values 
            </b-button>

            &nbsp;
            &nbsp;

            <span 
              v-if="configChanged" 
              class="text-warning"> 
              Parameters Changed! 
            </span>

            <br> <br> <br>

            <b-form-group 
              v-for="(item,key) in configOptions" 
              v-bind:label="getItemLabel(item)" 
              v-bind:key="item.label">

              <b-form-select 
                v-if="item.type==='select'" 
                v-model="configValues[key]" 
                v-bind:options="item.options" 
                v-bind:disabled="configDisabled[key]" 
                v-on:change="onConfigChange"
                required  
                class="w-25">
              </b-form-select>

              <b-form-input 
                v-if="item.type==='number'"  
                v-model="configValues[key]"  
                v-bind:state="configValid[key]" 
                v-on:change="onConfigChange"
                required 
                class="w-25">
              </b-form-input>

              <b-form-checkbox 
                v-if="item.type==='checkbox'" 
                v-model="configValues[key]" 
                v-on:change="onCheckboxChange(key)">
                {{item.label}} 
                <span 
                  v-if="configValues[key]" 
                  class="text-danger"> 
                  - warning could damage drive! 
                </span>

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
      'configChanged',
      'configOptions',
      'configValues',
      ]),
    ...mapGetters([
      'configDisabled',
      'configValid',
      'configAllValid',
    ]),
  },

  methods: {

    onGetValues() {
      console.log('onGetValues');
      console.log(this.configAllValid);
      this.socket.emit('getConfigValuesRequest', this.configValues);
    },

    onSetValues() {
      console.log('onSetValues');
      let configValuesToSend = {};
      for (let key in this.configValues) {
        if (!this.configDisabled[key]) {
          if (this.configOptions[key].type === 'number') {
            configValuesToSend[key] = Number(this.configValues[key]);
          } else {
            configValuesToSend[key] = this.configValues[key];
          }
        }
      }
      this.socket.emit('setConfigValuesRequest', configValuesToSend);
    },

    onConfigChange() {
      this.$store.commit('setConfigChanged', true);
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
