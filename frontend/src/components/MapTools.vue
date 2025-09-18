<template>
  <div class="full-width q-pa-sm bg-grey-2 text-left">
    <q-banner class="bg-info text-white q-mb-md">
      <q-btn 
        flat 
        dense 
        @click="mapToolsInfo=true" 
        icon="info" 
        color="white"
        class="q-mr-sm"
      />
      About Maptools
    </q-banner>

    <div class="full-width q-pt-sm q-pb-sm flex row text-grey-6">
      <div>Functions</div>
      <hr class="flex-fill"/>
    </div>

    <q-card class="q-mb-md">
      <q-card-section>
        <h5 class="orange">Faults</h5>
        <div class="text-center">
          <q-checkbox
              v-model="ucerf"
              @update:model-value="updateLayer('ucerf')"
              label="UCERF3 Fault Model"
              class="q-mr-sm"
          />
          <q-btn 
            flat 
            dense 
            round 
            icon="info" 
            @click.stop.prevent="openWindow('https://www.scec.org/ucerf')"
            color="primary"
            size="sm"
          />
        </div>
      </q-card-section>
        <q-card-section v-show="this.ucerf">
          <div class="card-text">
            Select a color for the fault
          </div>
          <q-option-group
            v-model="selectedColor"
            :options="[
              { label: 'Black', value: 'black' },
              { label: 'Yellow', value: 'yellow' },
              { label: 'Red', value: 'red' },
              { label: 'Grey', value: 'grey' }
            ]"
            @update:model-value="updateColor"
            color="primary"
            class="q-mt-sm"
            inline
          />
        </q-card-section>
    </q-card>

    <q-card class="q-mb-md">
      <q-card-section>
        <h5 class="orange">Quaternary Faults</h5>
        <div class="text-center">
          <q-checkbox
              v-model="qfaults"
              @update:model-value="updateLayer('qfaults')"
              label="Quaternary Faults"
              class="q-mr-sm"
          />
          <q-btn 
            flat 
            dense 
            round 
            icon="info" 
            @click.stop.prevent="openWindow('https://doi.org/10.5066/F7S75FJM')"
            color="primary"
            size="sm"
          />
        </div>
      </q-card-section>
      <q-card-section v-show="this.qfaults">
        <div class="card-text q-mb-sm">Source: USGS Faults Database</div>
        <q-option-group
          v-model="qfaults_selected"
          :options="[
            { label: 'Historic (150 yr)', value: 'historic', color: '#ff0000' },
            { label: 'Latest Quaternary (15,000 yr)', value: 'latest Quaternary', color: '#ffaa00' },
            { label: 'Late Quaternary (130,000 yr)', value: 'late Quaternary', color: '#55ff00' },
            { label: 'Middle and Late Quaternary (750,000 yr)', value: 'middle and late Quaternary', color: '#0070ff' },
            { label: 'Undifferentiated Quaternary (1.6 millions yr)', value: 'undifferentiated Quaternary', color: '#000000' },
            { label: 'Unspecified Age', value: 'unspecified', color: '#dfe000' },
            { label: 'Class B', value: 'class B', color: '#9c9c9c' }
          ]"
          @update:model-value="updateqfaults"
          color="primary"
          type="checkbox"
        />
      </q-card-section>
    </q-card>

    <q-card class="q-mb-md">
      <q-card-section>
        <h5 class="red">Geology</h5>
        <div class="text-center">
          <q-checkbox
              v-model="kml"
              @update:model-value="updateLayer('kml')"
              label="KML/KMZ Uploader"
              class="q-mr-sm"
          />
          <q-btn 
            flat 
            dense 
            round 
            icon="info" 
            @click="kmlInfo=true"
            color="primary"
            size="sm"
          />
        </div>
      </q-card-section>

      <q-card-section v-if="this.kml">
        <h6>KML/KMZ File Upload</h6>
        <p>Upload a KML or KMZ from your local file system</p>

        <div class="invisible">
          <q-file
              id="file"
              ref="file"
              @update:model-value="handleFileUpload"
              accept=".kml,.kmz"
              filled
          />

          <q-btn @click="submitFile()" color="primary">Submit</q-btn>
        </div>

        <div class="w-100 q-pa-sm">
          <q-btn 
            outline 
            color="primary" 
            class="full-width" 
            @click="triggerFileUploadClick"
            :disable="kmlFile"
            icon="upload"
          >
            <span>Upload a KML/KMZ file</span>
          </q-btn>
        </div>

        <div v-for="(entry, entryId) in kmlLayers" :key="entryId" class="w-100 q-mt-sm">
          <q-checkbox 
            :model-value="entry.active"
            @update:model-value="(val) => kmlLayerChange({...entry, active: val})"
            :label="entry.name"
            class="full-width"
          />
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-mb-md">
      <q-card-section>
        <h5 class="green">Topology</h5>
        <div class="row maptool">
          <q-checkbox
              v-model="boundaries"
              @update:model-value="updateLayer('boundaries')"
              id="boundaries"
              label="Show State Boundaries"
              class="q-mr-sm"
          />
          <span class="icon is-right" style="pointer-events: all;" @click="boundariesInfo=true">
          <i class="clickable fas fa-info-circle"></i>
        </span>
        </div>
      </q-card-section>
    </q-card>

    <q-card class="q-mb-md">
      <q-card-section>
        <h5 class="green">Topology</h5>
        <div class="row maptool">
          <q-checkbox
              v-model="coasts"
              @update:model-value="updateLayer('coasts')"
              id="coasts"
              label="Show Coastlines"
              class="q-mr-sm"
          />
          <span class="icon is-right" style="pointer-events: all;" @click="coastlinesInfo=true">
          <i class="clickable fas fa-info-circle"></i>
        </span>
        </div>
      </q-card-section>
    </q-card>

    <q-card class="q-mb-md">
      <q-card-section>
        <h5 class="green">Topology</h5>
        <div class="row">
          <q-checkbox
              v-model="currLoc"
              @update:model-value="getLocation()"
              id="loc"
              label="Show Current Location"
              class="q-mr-sm"
          />
          <span class="icon is-right" style="pointer-events: all;" @click="currentLocationInfo=true">
          <i class="clickable fas fa-info-circle"></i>
        </span>
        </div>
      </q-card-section>
    </q-card>

    <!-- info  popups -->
    <q-dialog
        v-model="mapToolsInfo">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">Map Tools</div>
        </q-card-section>
        <q-card-section>
          <p>
            Map tools contains multiple functions allowing users to display different faults and topographical
            features, as well as upload KML and KMZ files.
          </p>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
        v-model="kmlInfo">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">KML Information</div>
        </q-card-section>
        <q-card-section>
          <p>
            KML (Keyhole Markup Language) is a file format used to display geographic data.
          </p>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
        v-model="boundariesInfo">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">State Boundaries</div>
        </q-card-section>
        <q-card-section>
          <p>
            Display USA state boundaries on the map.
          </p>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
        v-model="coastlinesInfo">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">Coastlines</div>
        </q-card-section>
        <q-card-section>
          <p>
            Display coastlines on the map.
          </p>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
        v-model="currentLocationInfo">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">Current Location</div>
        </q-card-section>
        <q-card-section>
          <p>
            Mark your current location on the map.
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
import axios from "axios";
import {mapFields} from '../utils/mapFields';
import L from 'leaflet';

axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
export default {
  name: "MapTools",
  data() {
    return {
      mapToolsInfo: false,
      kmlInfo: false,
      boundariesInfo: false,
      coastlinesInfo: false,
      currentLocationInfo: false,
      ucerfUrlGrey: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_grey.kml",
      ucerfUrlBlack: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_black.kml",
      ucerfUrlRed: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_red.kml",
      ucerfUrlYellow: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_yellow.kml",
      boundariesUrl: 'https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/gz_2010_us_040_00_20m.kml',
      coastsUrl: 'https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ne_50m_coastline.kml',
      userLocationPin: null, //vuex-map-fields does not correctly reference variables inside of event listeners
      //selectedColor: 'grey',
      qfaults_selected: ["historic", "late Quaternary", "undifferentiated Quaternary", "unspecified", "class B", "middle and late Quaternary", "latest Quaternary"],
    }
  },
  computed: {
    // ucerf: false,
    // boundaries: false,
    // coasts: false,
    // kml: false,
    // kmlFile: null,
    // value: 50,
    // kmlLayers: [],
    ...mapFields(['mapTools.kmlLayers', 'mapTools.boundaries', 'mapTools.ucerf', 'mapTools.qfaults',
      'mapTools.coasts', 'mapTools.kml', 'mapTools.kmlFile', 'mapTools.selected', 'mapTools.currLoc',
      'mapTools.userLocationCirc', 'mapTools.selectedColor',
      // 'maTools.userLocationPin',
      'mapTools.locActive',

      'map.globalMap',
      'map.layers'])
  },
  watch: {
    qfaults_selected: {
      handler() {
        //console.log(val); // or this.selectedFruits
        this.updateqfaults();
      },
      deep: true
    }
  },
  mounted() {

    bus.on('currentLocation', () => {
      if (this.userLocationCirc) {
        this.globalMap.addLayer(this.userLocationCirc);
      }
      if (this.userLocationPin) {
        this.globalMap.addLayer(this.userLocationPin);
      }
      this.locActive = true;
    });

  },
  beforeUnmount() {
    bus.off('currentLocation');
  },
  methods: {
    dragFile(e) {
      this.File = e.dataTransfer.files;
    },
    // updateOpacity(value){
    //   bus.$emit('stateBoundaryOpacity', (value/100))
    // },
    toggle() {
      bus.emit('ToggleBar');
    },
    kmlLayerChange(entry) {
      console.log(entry.active);
      if (entry.active) {
        bus.emit('addExisting', entry.name);
      } else {
        bus.emit('RemoveLayer', entry.name);
      }
    },
    getLocation() {
      if (!this.locActive) {
        this.globalMap.on('locationfound', this.onLocationFound);
        this.globalMap.locate({setView: false, watch: false})
        this.locActive = true;
      } else {
        if (this.userLocationPin) {
          this.userLocationPin.remove();
        }
        this.locActive = false;
      }
    },
    onLocationFound(e) {
      this.userLocationPin = L.marker([e.latitude, e.longitude]).bindPopup('You are here').addTo(this.globalMap);
      // this.userLocationCirc = L.circle([e.latitude, e.longitude], e.accuracy / 2, {
      //   weight: 1,
      //   color: 'blue',
      //   fillColor: '#cacaca',
      //   fillOpacity: 0.2
      // }).addTo(this.globalMap);
      // console.log(userLocationPin, userLocationCirc);
      this.globalMap.off('locationfound');

    },
    updateColor(selected) {
      //this.selected = selected;
      bus.emit('RemoveLayer', 'ucerfL');
      this.updateLayer('ucerf', selected)
    },
    updateqfaults() {
      var filterstr = "";
      // filter by age
      console.log(this.qfaults_selected);
      if (this.qfaults_selected.length == 1) {
        filterstr = "age like '" + this.qfaults_selected[0] + "'";
      }
      if (this.qfaults_selected.length > 1 && this.qfaults_selected.length < 7) {
        filterstr = "age IN " + "('" + this.qfaults_selected.join("','") + "')";
      }
      const qfaultsLayer = this.layers['qfaultsWMS'];
      if (qfaultsLayer && this.globalMap.hasLayer(qfaultsLayer)) {
        qfaultsLayer.remove();
      }
      if (this.qfaults_selected.length == 0) {
        return;
      }
      if (filterstr == "") {
        this.layers['qfaultsWMS'] = L.tileLayer.wms('https://data.geo-gateway.org/geoserver00/InSAR/wms?', {
          layers: 'InSAR:Qfaults_US_Database',
          transparent: true,
          format: 'image/png',
          zIndex: 10,
          //cql_filter: filterstr,
        });
      } else {
        this.layers['qfaultsWMS'] = L.tileLayer.wms('https://data.geo-gateway.org/geoserver00/InSAR/wms?', {
          layers: 'InSAR:Qfaults_US_Database',
          transparent: true,
          format: 'image/png',
          zIndex: 10,
          cql_filter: filterstr,
        });
      }
      this.globalMap.addLayer(this.layers['qfaultsWMS']);
    },

    updateLayer(l, color) {
      switch (l) {
        case 'ucerf':
          if (this.ucerf) {
            var url;
            if (color === 'black') {
              url = this.ucerfUrlBlack
            } else if (color === 'red') {
              url = this.ucerfUrlRed;
            } else if (color === 'yellow') {
              url = this.ucerfUrlYellow;
            } else url = this.ucerfUrlGrey;
            bus.emit('UrlAddLayer', url, 'ucerfL');
          } else bus.emit('RemoveLayer', 'ucerfL');
          break;
        case 'kml':
          break;
        case 'boundaries':
          if (this.boundaries) {
            bus.emit('UrlAddLayer', this.boundariesUrl, 'boundariesL');
          } else bus.emit('RemoveLayer', 'boundariesL');
          break;
        case 'coasts':
          if (this.coasts) {
            bus.emit('UrlAddLayer', this.coastsUrl, 'coastsL');
          } else bus.emit('RemoveLayer', 'coastsL');
          break;
        case 'qfaults':
          if (this.qfaults) {
            this.updateqfaults();
          } else {
            const qfaultsLayer = this.layers['qfaultsWMS'];
            if (qfaultsLayer && this.globalMap.hasLayer(qfaultsLayer)) {
              qfaultsLayer.remove();
            }
          }
          break;
      }
    },
    openWindow(link) {
      window.open(link);
    },
    triggerFileUploadClick() {
      this.$refs.file.$refs.input.click();
    },
    async handleFileUpload(event) {
      this.kmlFile = event.target.files[0];
      await this.submitFile();
      this.kmlFile = null;
      this.$refs.file.reset();
    },
    async submitFile() {
      var fileName = this.kmlFile['name'];

      function getExtension(filename) {
        console.log(filename);
        var parts = filename.split('.');
        return parts[parts.length - 1];
      }

      var uploadUrl;
      var ext = getExtension(fileName);
      if (ext == 'kmz') {
        uploadUrl = '/geogateway_django_app/kmz_upload/'
      } else {
        uploadUrl = '/geogateway_django_app/kml_upload/'
      }
      console.log(uploadUrl);
      let formData = new FormData();
      formData.append('file', this.kmlFile);
      this.kmlLayers.push({name: fileName, active: true})
      await axios.post(uploadUrl, formData
      ).then(function (response) {
        bus.emit('addkmlUploadLayer', response.data, fileName);
      })
          .catch(function (response) {
            console.log(response)
            console.log('FAILURE!!');
          });
    },
  },
}
</script>

<style scoped lang="scss">
@use "sass:color";
@use "../styles.scss" as *;

.fileEntry {
  width: auto;
  height: auto;
  box-sizing: border-box;
  font-size: 15px;
  border-radius: 8px;
  background-color: #8494A3;
  margin-bottom: 5px;
}

/*a:link, a:visited {*/
/*  color: black;*/
/*  text-decoration: underline;*/
/*  display: inline-block;*/
/*}*/


.maptool {
  text-align: center;
  width: max-content;
  padding: 5px;
}

.card-text {
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 19px;
  display: flex;
  align-items: center;
  color: #95ABB1;
}

.clickable {
  cursor: pointer;
}

.visible {
  visibility: unset;
}

.invisible {
  visibility: hidden;
  position: fixed;
  top: -10000px;
}

button.file-upload-button {
  background-color: color.scale($primary, $lightness: 49%);
  border: 2px dashed color.scale($primary, $lightness: 35%);
  border-radius: 5px;
  padding: 20px 10px;

  &:hover, &:active, &:focus {
    background-color: color.scale($primary, $lightness: 48%);
    border: 2px dashed color.scale($primary, $lightness: 25%);
  }

  &:disabled {
    background-color: color.scale($secondary, $lightness: 48%);
    border: 2px dashed color.scale($secondary, $lightness: 25%);
  }
}

</style>
