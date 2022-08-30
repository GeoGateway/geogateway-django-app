<template>
  <div class="tab-window">
    <h3>Map Tools</h3>
    <hr>
    <div>
      <input
          type="checkbox"
          v-model="ucerf"
          @change="updateLayer('ucerf')"
          id="ucerf"
      ><label for="ucerf"> UCERF3 Fault Model</label>&ensp;
      <a href="" v-on:click.stop.prevent="openWindow('https://www.scec.org/ucerf')">
      <i class="fas fa-info-circle"></i>
      </a>
      <br/>
      <input
          type="checkbox"
          v-model="qfaults"
          @change="updateLayer('qfaults')"
          id="qfaults"
      ><label for="boundaries">Quaternary Faults</label>&ensp;
      <a href="" v-on:click.stop.prevent="openWindow('https://doi.org/10.5066/F7S75FJM')">
      <i class="fas fa-info-circle"></i>
      </a>
      <br/>
      <input
          type="checkbox"
          v-model="kml"
          @change="updateLayer('kml')"
          id="kml"
      ><label for="kml">KML/KMZ Uploader</label>
      <br/>
      <input
          type="checkbox"
          v-model="boundaries"
          @change="updateLayer('boundaries')"
          id="boundaries"
      ><label for="boundaries">Show State Boundaries</label>&ensp;
      <a href="" v-on:click.stop.prevent="openWindow('https://www.census.gov/geographies/mapping-files/2010/geo/carto-boundary-file.html')">
      <i class="fas fa-info-circle"></i>
      </a>
      <br/>
      <input
          type="checkbox"
          v-model="coasts"
          @change="updateLayer('coasts')"
          id="coasts"
      ><label for="coasts">Show Coastlines</label>&ensp;
      <a href="" v-on:click.stop.prevent="openWindow('https://www.naturalearthdata.com/downloads/50m-physical-vectors/')">
      <i class="fas fa-info-circle"></i>
      </a>
      <br/>
      <input
          type="checkbox"
          v-model="currLoc"
          @change="getLocation()"
          id="loc"
      ><label for="loc">Show Current Location</label>
      <br/>
    </div>
    <div id="tools-show">
      <div v-show="this.ucerf">
        Select faults display color
        <b-form-radio-group v-model="selectedColor">
          <b-form-radio label="black" name="some-radios" value="black" v-model="selectedColor" @change="updateColor('black')"><p>black</p></b-form-radio>
          <b-form-radio label="red" name="some-radios" value="red" v-model="selectedColor" @change="updateColor('red')"><p>red</p></b-form-radio>
          <b-form-radio label="yellow" name="some-radios" value="yellow" v-model="selectedColor" @change="updateColor('yellow')"><p>yellow</p></b-form-radio>
          <b-form-radio label="grey" name="some-radios" value="grey" v-model="selectedColor" @change="updateColor('grey')"><p>grey</p></b-form-radio>
        </b-form-radio-group>
      </div>

      <div id="div_qfautls" v-show="this.qfaults" style="padding-left: 60px;" align="left">
          <br><div align="center"><a target="_blank" href="https://www.usgs.gov/natural-hazards/earthquake-hazards/faults">Source: USGS Faults Database</a></div>
          <!-- <img src="../assets/qfaultslegend.jpg" alt="qfaults_legend" width="80%" height="80%" style="border:1px solidblack"> -->
          <b-form-group>
          <b-form-checkbox-group
            id="qfaults_type"
            v-model="qfaults_selected"
            stacked
          >
          <b-form-checkbox value="historic"><span style="color:#ff0000;font-weight: bold;">&#9473;&#9473;</span> Historic (150 yr)</b-form-checkbox>
          <b-form-checkbox value="latest Quaternary" ><span style="color:#ffaa00;font-weight: bold;">&#9473;&#9473;</span> Latest Quaternary (15,000 yr)</b-form-checkbox>
          <b-form-checkbox value="late Quaternary"><span style="color:#55ff00;font-weight: bold;">&#9473;&#9473;</span> Late Quaternary (130,000 yr)</b-form-checkbox>
          <b-form-checkbox value="middle and late Quaternary"  ><span style="color:#0070ff;font-weight: bold;">&#9473;&#9473;</span> Middle and Late Quaternary (750,000 yr)</b-form-checkbox>
          <b-form-checkbox value="undifferentiated Quaternary" ><span style="color:#000000;font-weight: bold;">&#9473;&#9473;</span> Undifferentiated Quaternary (1.6 millions yr)</b-form-checkbox>
          <b-form-checkbox value="unspecified" ><span style="color:#dfe000;font-weight: bold;">&#9473;&#9473;</span> Unspecified Age</b-form-checkbox>
          <b-form-checkbox value="class B" ><span style="color:#9c9c9c;font-weight: bold;">&#9473;&#9473;</span> Class B</b-form-checkbox>
          </b-form-checkbox-group>
          </b-form-group>
      </div>
      <div v-if="this.kml">
        <br />
        <h4>KML/KMZ File Upload</h4>
        <p>Upload a KML or KMZ from your local file system</p>
        <label>File
          <input  type="file" id="file" ref="file" @change="handleFileUpload"/>
        </label>
        <button @click="submitFile()">Submit</button>
        <div v-for="entry in kmlLayers" :key="entry" >
          <div class="fileEntry" >
            <input type="checkbox" v-model="entry.active" @change="kmlLayerChange(entry)" > <span style="font-size: 15px; color: #222222">{{entry.name}}</span><br>
          </div>
        </div>
        <!--            <div v-if="boundaries">-->
        <!--                <label for="opacity">Example range with min and max</label>-->
        <!--                <b-form-input id="opacity" @change="updateOpacity(value)" v-model="value" type="range" min="0" max="100"></b-form-input>-->
        <!--                <div class="mt-2">Value: {{ value }}</div>-->
        <!--            </div>-->
      </div>
    </div>
  </div>
</template>

<script>
import {bus} from '../main'
import axios from "axios";
import { mapFields } from 'vuex-map-fields';
import L from 'leaflet';
axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
export default {
  name: "MapTools",
  data() {
    return {
      ucerfUrlGrey: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_grey.kml",
      ucerfUrlBlack: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_black.kml",
      ucerfUrlRed: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_red.kml",
      ucerfUrlYellow: "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ucerf3_yellow.kml",
      boundariesUrl: 'https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/gz_2010_us_040_00_20m.kml',
      coastsUrl: 'https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/ne_50m_coastline.kml',
      userLocationPin: null, //vuex-map-fields does not correctly reference variables inside of event listeners
      //selectedColor: 'grey',
      qfaults_selected:["historic", "late Quaternary", "undifferentiated Quaternary", "unspecified", "class B", "middle and late Quaternary", "latest Quaternary"],
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
    // updateOpacity(value){
    //   bus.$emit('stateBoundaryOpacity', (value/100))
    // },
    kmlLayerChange(entry){
      console.log(entry.active);
      if(entry.active) {
        bus.$emit('addExisting', entry.name);
      }else {
        bus.$emit('RemoveLayer', entry.name);
      }
    },
    getLocation(){
      if(!this.locActive) {
        this.globalMap.on('locationfound', this.onLocationFound);
        this.globalMap.locate({setView: false, watch: false})
        this.locActive = true;
      }else {
        this.userLocationPin.remove();
        this.locActive = false;
      }
    },
    onLocationFound(e){
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
    updateColor(selected){
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
      this.layers['qfaultsWMS'] = L.tileLayer.wms('https://data.geo-gateway.org/geoserver00/InSAR/wms?', {
        layers: 'InSAR:Qfaults_US_Database',
        transparent: true,
        format: 'image/png',
        zIndex: 10,
        //cql_filter: filterstr,
      }); } else {
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

    updateLayer(l, color){
      switch (l) {
        case 'ucerf':
          if(this.ucerf) {
            var url;
            if(color === 'black'){
              url = this.ucerfUrlBlack
            }else if(color === 'red'){
              url = this.ucerfUrlRed;
            }else if(color === 'yellow'){
              url = this.ucerfUrlYellow;
            }else url = this.ucerfUrlGrey;
            bus.$emit('UrlAddLayer', url, 'ucerfL');
          }else bus.$emit('RemoveLayer', 'ucerfL');
          break;
        case 'kml':
          break;
        case 'boundaries':
          if(this.boundaries) {
            bus.$emit('UrlAddLayer', this.boundariesUrl, 'boundariesL');
          }else bus.$emit('RemoveLayer', 'boundariesL');
          break;
        case 'coasts':
          if(this.coasts) {
            bus.$emit('UrlAddLayer', this.coastsUrl, 'coastsL');
          }else bus.$emit('RemoveLayer', 'coastsL');
          break;
        case 'qfaults':
          if(this.qfaults) {
            this.updateqfaults();
          } else {this.layers['qfaultsWMS'].remove();}
          break;
      }
    },
    openWindow(link){
        window.open(link);
    },
    handleFileUpload(event){
      this.kmlFile = event.target.files[0];
    },
    submitFile(){
      var fileName = this.kmlFile['name'];
      function getExtension(filename) {
        var parts = filename.split('.');
        return parts[parts.length - 1];
      }
      var uploadUrl;
      var ext = getExtension(fileName);
      if(ext == 'kmz'){
        uploadUrl = '/geogateway_django_app/kmz_upload/'
      }else {
        uploadUrl = '/geogateway_django_app/kml_upload/'
      }
      let formData = new FormData();
      formData.append('file', this.kmlFile);
      this.kmlLayers.push({name: fileName, active: true})
      axios.post( uploadUrl, formData
      ).then(function(response){
        bus.$emit('addkmlUploadLayer', response.data, fileName);
      })
          .catch(function(response){
            console.log(response)
            console.log('FAILURE!!');
          });
    },
  },
}
</script>

<style scoped>
.fileEntry {
  width: auto;
  height: auto;
  box-sizing: border-box;
  font-size: 15px;
  border-radius: 8px;
  background-color: #8494A3;
  margin-bottom: 5px;
}
a:link, a:visited {
  color: black;
  text-decoration: underline;
  display: inline-block;
}
</style>
