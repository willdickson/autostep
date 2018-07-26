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

           &nbsp; &nbsp;


           <b-button variant="outline-primary" style="width:100px;" v-on:click="onClear"> 
             Clear Plot
           </b-button>

           &nbsp; &nbsp;

           <b-button variant="outline-primary" style="width:80px;" v-on:click="onDebug"> 
            Debug 
           </b-button>

           &nbsp; &nbsp;

           <br>
           <br>

           Max Velocity (&deg/s): {{maxVelocity.toFixed(0)}} &nbsp; &nbsp; Max Acceleration (&deg/s<sup>2</sup>): {{maxAcceleration.toFixed(0)}}

           <div ref="positionPlot"> </div>


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
      positionPlotLayout: { 
        xaxis: { 
          title: 'time (sec)', 
          zeroline: true, 
        }, 
        yaxis: { 
          title: 'position (deg)', 
          zeroline: true,
        },
        width: 1200,
        height: 500,
        showlegend: false,
      },
      haveDataTrace: false,
    }
  },

  computed: {
    ...mapState([
      'socket',
      'driveState',
      'sinusoidParams',
      'positionData',
      ]),
    ...mapGetters([
      'maxVelocity',
      'maxAcceleration',
    ]),
    lengthPositionData() {
      return this.positionData.t.length;
    },
  },

  watch: {
    lengthPositionData(newLength, oldLength) {
      let xNew = this.positionData.t.slice(oldLength, newLength); 
      let yNew = this.positionData.p.slice(oldLength, newLength); 
      if (this.haveDataTrace) { 
        Plotly.extendTraces(this.$refs.positionPlot,{x: [xNew], y: [yNew]},[1]); 
      } else { 
        let plotData = { 
          x: xNew, 
          y: yNew, 
          mode: 'lines', 
          visible: true,
        }; 
        Plotly.plot(this.$refs.positionPlot, [plotData], this.positionPlotLayout); 
        this.haveDataTrace = true;
      }
    },
  },

  methods: {

    onRun() {
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

      this.deleteAllTraces();
      this.addSinusoidPlot();
      this.haveDataTrace = false;
      this.socket.emit('runSinusoid', this.sinusoidParams);
    },

    onStop() {
      this.socket.emit('stopMotion', {});
    },

    updateStoreObject(value,objectName,propertyName) { 
      this.$store.commit('setObjectProperty',{value,objectName,propertyName});
      this.deleteAllTraces();
      this.addSinusoidPlot();
    },

    deleteAllTraces() {
      let num = this.$refs.positionPlot.data.length;
      for (let i=0; i<num; i++) {
        Plotly.deleteTraces(this.$refs.positionPlot, 0);
      }
    },

    onDebug() {
      const amplitude = this.sinusoidParams['amplitude'];
      const period = this.sinusoidParams['period'];
      const phase = this.sinusoidParams['phase'];
      const phaseRad = phase*Math.PI/180.0;
      const offset = this.sinusoidParams['offset'];
      const numCycle = this.sinusoidParams['num_cycle'];

      const maxVel = (2.0*Math.PI/period)*amplitude;
      const maxAcc = Math.pow((2.0*Math.PI/period),2)*amplitude;
      console.log('maxVel: ' + maxVel);
      console.log('maxAcc: ' + maxAcc);
    },

    onClear() {
      this.deleteAllTraces();
      this.addSinusoidPlot();
    },

    addSinusoidPlot() {
      const amplitude = this.sinusoidParams['amplitude'];
      const period = this.sinusoidParams['period'];
      const phase = this.sinusoidParams['phase'];
      const phaseRad = phase*Math.PI/180.0;
      const offset = this.sinusoidParams['offset'];
      const numCycle = this.sinusoidParams['num_cycle'];

      const ptsPerCycle = 100;
      const numPts = ptsPerCycle*numCycle;
      const tStop = period*numCycle;

      let dt = tStop/numPts;
      let tValues = []
      let pValues = [];
      for (let i=0; i<numPts; i++)
      {
        let t = i*dt;
        let p = amplitude*Math.sin(2.0*Math.PI*t/period + phaseRad) + offset;
        tValues.push(t);
        pValues.push(p);
      }

      let positionPlotData = {
        x: tValues, 
        y: pValues, 
        mode: 'lines', 
        visible: true,
      };

      Plotly.plot(this.$refs.positionPlot, [positionPlotData], this.positionPlotLayout);
    },

  },

  mounted() {
    this.addSinusoidPlot();
  },

}
</script>

<style scoped>
</style>
