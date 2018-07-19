<template>
  <div class="moverun"> 
    <br>
    <b-container fluid>
      <b-row>
         <b-col>

           <h4 class="font-weight-bold">  Current Position: &nbsp {{driveState['position']}} &deg </h4> 

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
               <b-form-checkbox v-model="driveState['enabled']" v-on:input="onEnabled">
                 Drive Enabled
              </b-form-checkbox>
             </b-form-group>

             <br>


             <b-form-group label="Move To Position" >
              <b-input-group prepend="&deg" class="w-25">
                <b-form-input type="number" v-model="runJogParams['moveValue']"> </b-form-input>
                <b-input-group-append>
                  <b-btn variant="outline-primary" v-on:click="onMove"> Go </b-btn>
                </b-input-group-append>
              </b-input-group>
             </b-form-group>

             <br>

             <b-form-group label="Jog Position" >
              <b-input-group prepend="&deg" class="w-25">
                <b-form-input type="number" v-model="runJogParams['jogValue']"> </b-form-input>
                <b-input-group-append>
                  <b-btn variant="outline-primary" v-on:click="onJog"> Go </b-btn>
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
  name: 'MoveRun',
  data () {
    return {
      enabled: "true",
    }
  },
  computed: {
    ...mapState([
      'socket',
      'configValues',
      'driveState',
      'runJogParams',
      ]),
    ...mapGetters([
    ]),
  },
  methods: {
    onDebug() {
      console.log('onDebug ' + this.driveState['enabled']);
    }, 
    onZero() {
      console.log('onZero');
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
    onJog() {
      console.log('onJog ' + this.runJogParams['jogValue']);
      const jogParams = {jogValue: Number(this.runJogParams['jogValue'])};
      this.socket.emit('jogPosition', jogParams);
    },
    onEnabled() {
      console.log('onEnabled ' + this.driveState['enabled']);
    },
  },
}
</script>

<style scoped>
</style>
