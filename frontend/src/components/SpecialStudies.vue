<template>
  <div class="w-100 p-2 bg-light text-left">
    <q-banner class="bg-info text-white q-mb-md">
      <q-btn 
        flat 
        dense 
        @click="specstudInfo=true" 
        icon="info" 
        color="white"
        class="q-mr-sm"
      />
      About Special Studies
    </q-banner>

    <hr>
    <div align="left">

      <q-card class="q-mb-md">
        <q-card-section>
          <q-checkbox
            v-model="woolseyfire"
            @update:model-value="loadwoolfire"
            label="Southern California Woolsey Fire"
            class="text-weight-bold"
          />
        </q-card-section>
        <q-card-section v-show="this.woolseyfire">
          <p>Southern California's Woolsey Fire on Nov. 15 observed with UAVSAR</p>
          <div class="q-pl-md">
            <q-checkbox 
              :model-value="woof_checkbox.includes(0)" 
              @update:model-value="updatewoof('0')"
              class="q-mb-sm"
            >
              <span class="q-ml-sm">
                <a target="_blank" href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/CAVNC-091023_WOOLSEY_11-18-2018_55900_AM.kmz">
                  Woolsey fire perimeter (11-18-2018)
                </a>
              </span>
            </q-checkbox>
            <q-checkbox 
              :model-value="woof_checkbox.includes(1)" 
              @update:model-value="updatewoof('1')"
              class="q-mb-sm"
            >
              <span class="q-ml-sm">
                <a target="_blank" href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/CAVNC-090993_Hill_11-12-2018_91400_PM.kmz">
                  Hill fire perimeter (11-12-2018)
                </a>
              </span>
            </q-checkbox>
            <q-checkbox 
              :model-value="woof_checkbox.includes(2)" 
              @update:model-value="updatewoof('2')"
              class="q-mb-sm"
            >
              <span class="q-ml-sm">
                <a target="_blank" href="http://gf2.ucs.indiana.edu/stage/CA_Fires/SanAnd_08525_18076-003_18083-003_0036d_s01_L090HH_01.cor.tiff">
                  UAVSAR Correlation Image 1 (geotiff)
                </a>
              </span>
            </q-checkbox>
            <q-checkbox 
              :model-value="woof_checkbox.includes(3)" 
              @update:model-value="updatewoof('3')"
              class="q-mb-sm"
            >
              <span class="q-ml-sm">
                <a target="_blank" href="http://gf2.ucs.indiana.edu/stage/CA_Fires/SanAnd_26526_18080-006_18083-000_0011d_s01_L090HH_01.cor.tiff">
                  UAVSAR Correlation Image 2 (geotiff)
                </a>
              </span>
            </q-checkbox>
          </div>
          <small>Experimental products: JPL/Caltech/GeoGateway</small>
        </q-card-section>
      </q-card>


      <q-card class="q-mb-md">
        <q-card-section>
          <q-checkbox
            v-model="wildfire"
            @update:model-value="loadwildfire"
            label="Wildfire and debris flows"
            class="text-weight-bold"
          />
        </q-card-section>
        <q-card-section v-show="this.wildfire">
          <p>Montecito debris flows observed with UAVSAR</p>
          <div class="q-pl-md">
            <q-checkbox 
              :model-value="wilf_checkbox.includes(0)" 
              @update:model-value="updatewilf('0')"
              class="q-mb-sm"
            >
              <span class="q-ml-sm">
                <a target="_blank" href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/wildfire_ModifiedUAVSAR.kmz">
                  UAVSAR enhanced image pair (Nov-2-2017, Feb-5-2018) Orange
                </a>
              </span>
            </q-checkbox>
            <q-checkbox 
              :model-value="wilf_checkbox.includes(1)" 
              @update:model-value="updatewilf('1')"
              class="q-mb-sm"
            >
              <span class="q-ml-sm">
                <a target="_blank" href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/wildfire_ModifiedCorrelation.kmz">
                  UAVSAR enhanced image coherence (Feb-5-2018) Purple
                </a>
              </span>
            </q-checkbox>
            <q-checkbox 
              :model-value="wilf_checkbox.includes(2)" 
              @update:model-value="updatewilf('2')"
              class="q-mb-sm"
            >
              <span class="q-ml-sm">
                <a target="_blank" href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/wildfire_NIT_result.kmz">
                  Rapid change detection with optical images (Dec-28-2017/Jan-13-2018)
                </a>
              </span>
            </q-checkbox>
          </div>
          <small>Experimental products: JPL/Caltech/GeoGateway</small>
        </q-card-section>
      </q-card>
    </div>

    <!-- info  popup -->
    <q-dialog v-model="specstudInfo">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Special Studies</div>
        </q-card-section>
        
        <q-card-section class="q-pt-none">
          <p class="my-4">
            GeoGateway's Special Studies tab lists products for demonstration purposes.
            The study includes wildfire burn areas and debris flows imaged with UAVSAR
            following the Southern California 2018 Woolsey Fire and the 2017 Montecito,
            California fire.
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
import {bus} from '../main'
import {mapFields} from '../utils/mapFields';
import axios from "axios";

axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  name: "SpecialStudies",
  data: function () {
    return {
      specstudInfo: false,
      woolseyfire: false,
      woof_checkbox: [],
      woofurls: ["https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/CAVNC-091023_WOOLSEY_11-18-2018_55900_AM.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/CAVNC-090993_Hill_11-12-2018_91400_PM.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/SanAnd_08525_18076-003_18083-003_0036d_s01_L090HH_01.cor.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/SanAnd_26526_18080-006_18083-000_0011d_s01_L090HH_01.cor.kml"
      ],
      wildfire: false,
      wilfurls: ["https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/wildfire_ModifiedUAVSAR.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/wildfire_ModifiedCorrelation.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/wildfire_NIT_result.kml"
      ],
      wilf_checkbox: [],
    };
  },
  computed: {
    ...mapFields([
      'map.globalMap',
    ])
  },
  methods: {

    loadwoolfire() {
      if (this.woolseyfire) {
        this.globalMap.setView([34.14773, -118.84833], 10);
        this.woof_checkbox.push("0");
        this.updatewoof("0");
        this.woof_checkbox.push("1");
        this.updatewoof("1");
      } else {
        var i = this.woof_checkbox.length;
        while (i--) {
          var code = this.woof_checkbox[i];
          this.woof_checkbox.splice(i, 1);
          this.updatewoof(code);
        }
      }
    },


    // update woolseyfire
    updatewoof(val) {
      var vp = parseInt(val);
      var wlayerName = 'wool' + val + "L";
      if (this.woof_checkbox.includes(val)) {
        bus.emit('UrlAddLayer', this.woofurls[vp], wlayerName);
      } else bus.emit('RemoveLayer', wlayerName);
    },


    loadwildfire() {
      if (this.wildfire) {
        this.globalMap.setView([34.440, -119.61328], 13);
        this.wilf_checkbox.push("0");
        this.updatewilf("0");
      } else {
        var i = this.wilf_checkbox.length;
        while (i--) {
          var code = this.wilf_checkbox[i];
          this.wilf_checkbox.splice(i, 1);
          this.updatewilf(code);
        }
      }
    },
    updatewilf(val) {
      var vp = parseInt(val);
      var wlayerName = 'wilf' + val + "L";
      if (this.wilf_checkbox.includes(val)) {
        bus.emit('UrlAddLayer', this.wilfurls[vp], wlayerName);
      } else bus.emit('RemoveLayer', wlayerName);
    },
  },

}
</script>

<style scoped>

table {
  border-collapse: collapse;
  border: 1px solid black;
  width: 100%;
}

td {
  text-align: left;
  padding: 2px;
}

label {
  padding: 5px;
}

</style>
