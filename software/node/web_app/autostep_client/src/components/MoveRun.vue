<template>
  <div class="moverun"> 
    <br>
    <b-container fluid>
      <b-row>
         <b-col>

           <b-form  
             inline
             v-on:reset.prevent 
             v-on:submit.prevent
             >

            <b-button 
              v-on:click="onJogNeg" 
              variant="outline-primary" > 
              - Jog  
            </b-button>

            &nbsp;
            &nbsp;

            <b-button 
              v-on:click="onJogPos" 
              variant="outline-primary"> 
              Jog +
            </b-button>



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
      msg: 'Move/Run'
    }
  },
  computed: {
    ...mapState([
      'socket',
      'configValues',
      ]),
    ...mapGetters([
    ]),
  },
  methods: {
    onJogNeg() {
    },
    onJogPos() {
    },
  },
}
</script>

<style scoped>
</style>
