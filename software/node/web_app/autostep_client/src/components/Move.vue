<template>
  <div class="move"> 

    <br>

    <b-container fluid>

      <b-row>
         <b-col>

           <h4 class="font-weight-bold">  Current Position: &nbsp {{Math.round(driveState['position'])}} &deg </h4> 

           <br>
           <br>

           <b-button variant="outline-primary" style="width:80px;" v-on:click="onZero"> 
             Zero
           </b-button>

           &nbsp; &nbsp;

           <b-button variant="outline-primary" style="width:80px;" v-on:click="onHome"> 
             Home
           </b-button>

           &nbsp; &nbsp;

           <b-button variant="outline-primary" style="width:80px;" v-on:click="onDebug"> 
             Debug
           </b-button>

           <br>
           <br>
           <br>
              

           <b-form  
             v-on:reset.prevent 
             v-on:submit.prevent
             >

             <b-form-group size="lg">
               <b-form-checkbox 
                 v-bind:checked="driveState.enabled"
                 v-on:input="onEnabled">
                 Drive Enabled
              </b-form-checkbox>
             </b-form-group>

             <br>

             <b-form-group size="lg">
               <b-form-checkbox 
                 v-bind:checked="positionTimerEnabled"
                 v-on:input="onPositionTimerEnabled">
                 Position Timer
              </b-form-checkbox>
             </b-form-group>

             <br>

             <b-form-group label="Move To Position" >
              <b-input-group prepend="&deg" class="w-25">
                <b-form-input 
                  type="number" 
                  v-bind:value="runJogParams.moveValue" 
                  v-on:input="updateStoreObject(Number($event), 'runJogParams', 'moveValue')"
                  > 
                </b-form-input>
                <b-input-group-append>
                  <b-btn variant="outline-primary" v-on:click="onMove"> Go </b-btn>
                </b-input-group-append>
              </b-input-group>
             </b-form-group>

             <br>

             <b-form-group label="Jog Position" >
              <b-input-group prepend="&deg" class="w-25">
                <b-form-input 
                  type="number" 
                  v-bind:value="runJogParams.jogValue"
                  v-on:input="updateStoreObject(Number($event), 'runJogParams', 'jogValue')"
                  > 
                </b-form-input>
                <b-input-group-append>
                  <b-btn variant="outline-primary" v-on:click="onJog(-runJogParams.jogValue)"> - </b-btn>
                  <b-btn variant="outline-primary" v-on:click="onJog(runJogParams.jogValue)"> + </b-btn>
                </b-input-group-append>
              </b-input-group>
             </b-form-group>

             <br>

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

  name: 'Move',

  data () {
    return {
    }
  },

  computed: {
    ...mapState([
      'socket',
      'configValues',
      'driveState',
      'runJogParams',
      'positionTimerEnabled',
      ]),
    ...mapGetters([
    ]),
  },

  methods: {
    onDebug() {
      console.log('onDebug ' + this.driveState['enabled']);
      console.log(JSON.stringify(this.configValues))
      this.socket.emit('getPosition',{});
    }, 
    onZero() {
      console.log('onZero');
      this.socket.emit('setPosition', {value: 0});
    },
    onHome() {
      console.log('onHome');
    },
    onMove() {
      console.log('onMove ' + this.runJogParams['moveValue']);
      const moveParams = {moveValue: Number(this.runJogParams['moveValue'])};
      console.log(moveParams);
      this.socket.emit('moveToPosition', moveParams);
    },
    onJog(value) {
      console.log('onJog ' + this.runJogParams['jogValue']);
      const jogParams = {jogValue: value};
      this.socket.emit('jogPosition', jogParams);
    },
    onEnabled(value) {
      console.log('onEnabled ' + value);
      this.updateStoreObject(value,'driveState','enabled');

    },
    onPositionTimerEnabled(value) {
      console.log('onEnabled ' + value);
      this.$store.commit('setPositionTimerEnabled', value);
      console.log(JSON.stringify(this.positionTimerEnabled));
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
