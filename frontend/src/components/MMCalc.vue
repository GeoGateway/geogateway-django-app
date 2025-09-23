<template>
  <div class="full-width q-pa-sm bg-grey-2 text-left">
    <q-banner class="bg-info text-white q-mb-md">
      <q-btn 
        flat 
        dense 
        @click="mmInfo=true" 
        icon="info" 
        color="white"
        class="q-mr-sm"
      />
      About Moment Magnitude Calculator
    </q-banner>

    <hr/>
    <q-input
      v-model="mm_length"
      label="Length"
      placeholder="12.5"
      outlined
      class="q-mb-md"
    >
      <template v-slot:append>
        <span class="text-caption">km</span>
      </template>
    </q-input>
    <q-input
      v-model="mm_width"
      label="Width"  
      placeholder="10"
      outlined
      class="q-mb-md"
    >
      <template v-slot:append>
        <span class="text-caption">km</span>
      </template>
    </q-input>
    <q-input
      v-model="mm_slip"
      label="Slip"
      placeholder="0.45"
      outlined
      class="q-mb-md"
    >
      <template v-slot:append>
        <span class="text-caption">m</span>
      </template>
    </q-input>
    <q-input
      v-model="mm_shear"
      label="Shear Modulus"
      placeholder="3"
      outlined
      class="q-mb-md"
    >
      <template v-slot:append>
        <span class="text-caption">10<sup>11</sup> dyne/cm<sup>2</sup></span>
      </template>
    </q-input>
    <br/>
    <q-btn @click="runMMC()" color="positive" class="q-mb-md">Calculate</q-btn>
    <br/>
    <div v-show="SM != null && MM != null">
      <br/>
      <hr/>
      <h6><strong> Seismic Moment: </strong> {{ this.SM }}</h6>
      <h6><strong> Moment Magnitude: </strong> {{ this.MM }}</h6>
    </div>

    <q-dialog v-model="mmInfo">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Moment Magnitude Calculator</div>
        </q-card-section>
        
        <q-card-section class="q-pt-none">
          <p>
            Magnitude is the physical size of an earthquake.
            Both seismic moment and moment magnitude <strong>(MW)</strong>
            can be calculated using GeoGateway's moment magnitude calculator.
          </p>
        </q-card-section>
        
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import {mapFields} from '../utils/mapFields';

export default {
  name: "MMCalc",
  data() {
    return {
      mmInfo: false,
    };
  },
  computed: {
    // mm_length: 249,
    // mm_width: 120.0,
    // mm_slip: 23,
    // mm_shear: 3,
    // SM: null,
    // MM: null,
    ...mapFields(['mmcalc.mm_length', 'mmcalc.mm_width', 'mmcalc.mm_slip', 'mmcalc.mm_shear', 'mmcalc.SM', 'mmcalc.MM'])
  },
  methods: {
    runMMC() {
      this.SM = (this.mm_length * this.mm_width * this.mm_slip * this.mm_shear * 1e23).toExponential(1);
      this.MM = (2 / 3 * Math.log(this.SM) / Math.log(10) - 10.7).toFixed(1);
    }
  }
}
</script>

<style scoped>
h6 {

}
</style>