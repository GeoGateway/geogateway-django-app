<template>
  <div class="w-100 p-2 bg-light text-left">
    <b-alert :show="true">
      <b-link @click="mapToolsInfo=true" href="#">
        <b-icon icon="info-circle-fill"/>
      </b-link>&ensp;
      About Maptools
    </b-alert>

    <div class="w-100 pt-2 pb-2 d-flex flex-row text-secondary">
      <div>Functions</div>
      <hr class="flex-fill"/>
    </div>

    <b-card>
      <b-col>
        <h5 class="orange">Faults</h5>
        <b-row class="text-center">
          <b-form-checkbox
              v-model="ucerf"
              @change="updateLayer('ucerf')"
              id="ucerf"
          ><label for="ucerf"> UCERF3 Fault Model</label>&ensp;
          </b-form-checkbox>
          <a href="" v-on:click.stop.prevent="openWindow('https://www.scec.org/ucerf')">
            <i class="fas fa-info-circle"></i>
          </a>
        </b-row>
      </b-col>
      <div v-show="this.ucerf">
        <span class="card-text">
          Select a color for the falut
        </span>
        <b-form-radio-group v-model="selectedColor">

          <b-row>
            <b-col>
              <b-form-radio label="black" name="some-radios" value="black" v-model="selectedColor"
                            @change="updateColor('black')"><p>black</p></b-form-radio>
            </b-col>
            <b-col>
              <b-form-radio label="yellow" name="some-radios" value="yellow" v-model="selectedColor"
                            @change="updateColor('yellow')"><p>yellow</p></b-form-radio>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-radio label="red" name="some-radios" value="red" v-model="selectedColor"
                            @change="updateColor('red')"><p>red</p></b-form-radio>
            </b-col>
            <b-col>
              <b-form-radio label="grey" name="some-radios" value="grey" v-model="selectedColor"
                            @change="updateColor('grey')"><p>grey</p></b-form-radio>
            </b-col>
          </b-row>
        </b-form-radio-group>
      </div>
    </b-card>

    <b-card>
      <b-col>
        <h5 class="orange">Faults</h5>
        <b-row>
          <b-form-checkbox
              type="checkbox"
              v-model="qfaults"
              @change="updateLayer('qfaults')"
              id="qfaults"
          ><label for="boundaries">Quaternary Faults</label>&ensp;
          </b-form-checkbox>
          <a href="" v-on:click.stop.prevent="openWindow('https://doi.org/10.5066/F7S75FJM')">
            <i class="fas fa-info-circle"></i>
          </a>
        </b-row>
      </b-col>
      <div id="div_qfautls" v-show="this.qfaults" align="left">
        <br><span class="card-text">Source: USGS Faults Database</span>
        <!-- <img src="../assets/qfaultslegend.jpg" alt="qfaults_legend" width="80%" height="80%" style="border:1px solidblack"> -->
        <b-form-group>
          <b-form-checkbox-group
              id="qfaults_type"
              v-model="qfaults_selected"
              stacked
          >
            <b-form-checkbox value="historic"><span style="color:#ff0000;font-weight: bold;">&#9473;&#9473;</span>
              Historic (150 yr)
            </b-form-checkbox>
            <b-form-checkbox value="latest Quaternary"><span
                style="color:#ffaa00;font-weight: bold;">&#9473;&#9473;</span> Latest Quaternary (15,000 yr)
            </b-form-checkbox>
            <b-form-checkbox value="late Quaternary"><span
                style="color:#55ff00;font-weight: bold;">&#9473;&#9473;</span> Late Quaternary (130,000 yr)
            </b-form-checkbox>
            <b-form-checkbox value="middle and late Quaternary"><span style="color:#0070ff;font-weight: bold;">&#9473;&#9473;</span>
              Middle and Late Quaternary (750,000 yr)
            </b-form-checkbox>
            <b-form-checkbox value="undifferentiated Quaternary"><span style="color:#000000;font-weight: bold;">&#9473;&#9473;</span>
              Undifferentiated Quaternary (1.6 millions yr)
            </b-form-checkbox>
            <b-form-checkbox value="unspecified"><span style="color:#dfe000;font-weight: bold;">&#9473;&#9473;</span>
              Unspecified Age
            </b-form-checkbox>
            <b-form-checkbox value="class B"><span style="color:#9c9c9c;font-weight: bold;">&#9473;&#9473;</span>
              Class B
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
      </div>
    </b-card>

    <b-card>
      <b-col>
        <h5 class="red">Geology</h5>
        <b-row>
          <b-form-checkbox
              type="checkbox"
              v-model="kml"
              @change="updateLayer('kml')"
              id="kml"
          ><label for="kml">KML/KMZ Uploader</label>&ensp;
          </b-form-checkbox>
          <span class="icon is-right" syle="pointer-events: all;" @click="kmlInfo=true">
          <i class="clickable fas fa-info-circle"></i>
        </span>
        </b-row>
      </b-col>

      <div v-if="this.kml">
        <br/>
        <h4>KML/KMZ File Upload</h4>
        <p>Upload a KML or KMZ from your local file system</p>

        <div class="invisible">
          <b-form-file
              no-traverse
              id="file"
              ref="file"
              @change="handleFileUpload"
              placeholder="Upload a KML/KMZ file"
          ></b-form-file>

          <b-button @click="submitFile()">Submit</b-button>
        </div>

        <div class="w-100 p-2">
          <b-button variant="outline-secondary" class="file-upload-button w-100" v-on:click="triggerFileUploadClick"
                    :disabled="kmlFile">
            <span class="text-primary">UPLOAD</span>&nbsp;<span class="text-secondary">a KML/KMZ file.</span>
          </b-button>
        </div>

        <div v-for="(entry, entryId) in kmlLayers" :key="entryId" class="w-100 d-flex flex-row mt-1">
          <div class="p-1">
            <b-form-checkbox type="checkbox" :id="`kmlLayers-${entryId}`" v-model="entry.active"
                             @change="kmlLayerChange(entry)" class="flex-fill">
              {{ entry.name }}
            </b-form-checkbox>
          </div>
        </div>
        <!--            <div v-if="boundaries">-->
        <!--                <label for="opacity">Example range with min and max</label>-->
        <!--                <b-form-input id="opacity" @change="updateOpacity(value)" v-model="value" type="range" min="0" max="100"></b-form-input>-->
        <!--                <div class="mt-2">Value: {{ value }}</div>-->
        <!--            </div>-->
      </div>


    </b-card>
    <b-card>
      <b-col>
        <h5 class="green">Topology</h5>
        <b-row class="maptool">
          <b-form-checkbox
              type="checkbox"
              v-model="boundaries"
              @change="updateLayer('boundaries')"
              id="boundaries"
          ><label for="boundaries">Show State Boundaries</label>&ensp;
          </b-form-checkbox>
          <span class="icon is-right" syle="pointer-events: all;" @click="boundariesInfo=true">
          <i class="clickable fas fa-info-circle"></i>
        </span>
        </b-row>
      </b-col>
    </b-card>

    <b-card>
      <b-col>
        <h5 class="green">Topology</h5>
        <b-row class="maptool">
          <b-form-checkbox
              type="checkbox"
              v-model="coasts"
              @change="updateLayer('coasts')"
              id="coasts"
          ><label for="coasts">Show Coastlines</label>&ensp;
          </b-form-checkbox>
          <span class="icon is-right" syle="pointer-events: all;" @click="coastlinesInfo=true">
          <i class="clickable fas fa-info-circle"></i>
        </span>
        </b-row>
      </b-col>
    </b-card>

    <b-card>
      <b-col>
        <h5 class="green">Topology</h5>
        <b-row>
          <b-form-checkbox
              type="checkbox"
              v-model="currLoc"
              @change="getLocation()"
              id="loc"
          ><label for="loc">Show Current Location</label>&ensp;
          </b-form-checkbox>
          <span class="icon is-right" syle="pointer-events: all;" @click="currentLocationInfo=true">
          <i class="clickable fas fa-info-circle"></i>
        </span>
        </b-row>
      </b-col>
    </b-card>

    <!-- info  popups -->
    <b-modal
        v-model="mapToolsInfo"
        title="Map Tools">
      <p class="my-4">
        Map tools contains multiple funtions allowing users to display different faults and topographical
        features, as well as upload KML and KMZ files.
      </p>
      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>

    <b-modal
        v-model="kmlInfo">
      <p class="my-4">
        KML (Keyhole Markup Language) is a file format used to display geographic data.
      </p>
      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>

    <b-modal
        v-model="boundariesInfo">
      <p class="my-4">
        Display USA state boundaries on the map.
      </p>
      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>

    <b-modal
        v-model="coastlinesInfo">
      <p class="my-4">
        Display coastlines on the map.
      </p>
      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>

    <b-modal
        v-model="currentLocationInfo">
      <p class="my-4">
        Mark your current location on the map.
      </p>
      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>
  </div>
</template>

<script>
import {bus} from '../main'
import axios from "axios";
import {mapFields} from 'vuex-map-fields';
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
    qfaults_selected() {
      //console.log(val); // or this.selectedFruits
      this.updateqfaults();
    }
  },
  mounted() {

    bus.$on('currentLocation', () => {
      this.globalMap.addLayer(this.userLocationCirc);
      this.globalMap.addLayer(this.userLocationPin);
      this.locActive = true;
    });

  },
  methods: {
    dragFile(e) {
      this.File = e.dataTransfer.files;
    },
    // updateOpacity(value){
    //   bus.$emit('stateBoundaryOpacity', (value/100))
    // },
    toggle() {
      bus.$emit('ToggleBar');
    },
    kmlLayerChange(entry) {
      console.log(entry.active);
      if (entry.active) {
        bus.$emit('addExisting', entry.name);
      } else {
        bus.$emit('RemoveLayer', entry.name);
      }
    },
    getLocation() {
      if (!this.locActive) {
        this.globalMap.on('locationfound', this.onLocationFound);
        this.globalMap.locate({setView: false, watch: false})
        this.locActive = true;
      } else {
        this.userLocationPin.remove();
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
      bus.$emit('RemoveLayer', 'ucerfL');
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
      if (this.globalMap.hasLayer(this.layers['qfaultsWMS'])) {
        this.layers['qfaultsWMS'].remove();
      }
      if (this.qfaults_selected.length == 0) {
        return;
      }
      if (filterstr == "") {
        this.layers['qfaultsWMS'] = L.tileLayer.wms('https://archive.geo-gateway.org/geoserver/InSAR/wms?', {
          layers: 'InSAR:Qfaults_US_Database',
          transparent: true,
          format: 'image/png',
          zIndex: 10,
          //cql_filter: filterstr,
        });
      } else {
        this.layers['qfaultsWMS'] = L.tileLayer.wms('https://archive.geo-gateway.org/geoserver/InSAR/wms?', {
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
            bus.$emit('UrlAddLayer', url, 'ucerfL');
          } else bus.$emit('RemoveLayer', 'ucerfL');
          break;
        case 'kml':
          break;
        case 'boundaries':
          if (this.boundaries) {
            bus.$emit('UrlAddLayer', this.boundariesUrl, 'boundariesL');
          } else bus.$emit('RemoveLayer', 'boundariesL');
          break;
        case 'coasts':
          if (this.coasts) {
            bus.$emit('UrlAddLayer', this.coastsUrl, 'coastsL');
          } else bus.$emit('RemoveLayer', 'coastsL');
          break;
        case 'qfaults':
          if (this.qfaults) {
            this.updateqfaults();
          } else {
            this.layers['qfaultsWMS'].remove();
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
        bus.$emit('addkmlUploadLayer', response.data, fileName);
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
// Bootstrap and its default variables
@import '~bootstrap/scss/bootstrap';
// BootstrapVue and its default variables
@import '~bootstrap-vue/src/index.scss';

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
  background-color: lighten($primary, 49%);
  border: 2px dashed lighten($primary, 35%);
  border-radius: 5px;
  padding: 20px 10px;

  &:hover, &:active, &:focus {
    background-color: lighten($primary, 48%);
    border: 2px dashed lighten($primary, 25%);
  }

  &:disabled {
    background-color: lighten($secondary, 48%);
    border: 2px dashed lighten($secondary, 25%);
  }
}

</style>
