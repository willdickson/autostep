<template>

  <div class="sinusoid">
    <br>
    <b-container fluid>
      <b-row>
         <b-col>

           <br> 

           <b-button variant="outline-primary" style="width:80px;" v-on:click="onRun"> 
             Run
           </b-button>

           &nbsp; &nbsp;

           <b-button variant="outline-primary" style="width:80px;" v-on:click="onStop"> 
             Stop
           </b-button>

           <br> 
           <br> 
           <br> 


           <b-form  
             v-on:reset.prevent 
             v-on:submit.prevent
             >
             <b-form-group label="Amplitude" >
              <b-input-group prepend="&deg" class="w-25">
                <b-form-input 
                  type="number" 
                  v-bind:value="sinusoidParams.amplitude" 
                  v-bind:step="0.1"
                  v-on:input="updateStoreObject(Number($event), 'sinusoidParams', 'amplitude')"
                  > 
                </b-form-input>
              </b-input-group>
             </b-form-group>

             <b-form-group label="Period" >
              <b-input-group prepend="s" class="w-25">
                <b-form-input 
                  type="number" 
                  v-bind:value="sinusoidParams.period" 
                  v-bind:step="0.1"
                  v-on:input="updateStoreObject(Number($event), 'sinusoidParams', 'period')"
                  > 
                </b-form-input>
              </b-input-group>
             </b-form-group>

             <b-form-group label="Phase" >
              <b-input-group prepend="&deg" class="w-25">
                <b-form-input 
                  type="number" 
                  v-bind:value="sinusoidParams.phase" 
                  v-bind:step="0.1"
                  v-on:input="updateStoreObject(Number($event), 'sinusoidParams', 'phase')"
                  > 
                </b-form-input>
              </b-input-group>
             </b-form-group>

             <b-form-group label="Offset" >
              <b-input-group prepend="&deg" class="w-25">
                <b-form-input 
                  type="number" 
                  v-bind:value="sinusoidParams.offset" 
                  v-bind:step="0.1"
                  v-on:input="updateStoreObject(Number($event), 'sinusoidParams', 'offset')"
                  > 
                </b-form-input>
              </b-input-group>
             </b-form-group>

             <b-form-group label="Cycles" >
              <b-input-group prepend="#" class="w-25">
                <b-form-input 
                  type="number" 
                  v-bind:value="sinusoidParams.num_cycle" 
                  v-on:input="updateStoreObject(Number($event), 'sinusoidParams', 'num_cycle')"
                  > 
                </b-form-input>
              </b-input-group>
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

  name: 'Sinusoid',

  data () {
    return {
      dummyAmplitude: 100.0,
      dummyPeriod: 1.0,
      dummyPhase: 90.0,
      dummyOffset: 0.0,
      dummyNumberOfCycles: 1,
    }
  },

  computed: {
    ...mapState([
      'socket',
      'driveState',
      'sinusoidParams',
      ]),
    ...mapGetters([
    ]),
  },

  methods: {

    onRun() {
      console.log('onRun ' + JSON.stringify(this.sinusoidParams));
      this.$store.commit('setPositionTimerEnabled', false);

      this.$store.commit('setObjectProperty', {
        objectName: 'navbarDisabled', 
        propertyName: 'configuration', 
        value: true
      });

      this.$store.commit('setObjectProperty', {
        objectName: 'navbarDisabled', 
        propertyName: 'move', 
        value: true
      });

      this.socket.emit('runSinusoid', this.sinusoidParams);
    },

    onStop() {
      console.log('onStop');
      this.socket.emit('stopMotion', {});
    },

    updateStoreObject(value,objectName,propertyName) { 
      this.$store.commit('setObjectProperty',{value,objectName,propertyName});
      console.log(JSON.stringify(this[objectName]))
    },
  },

}
</script>

<style scoped>
</style>
