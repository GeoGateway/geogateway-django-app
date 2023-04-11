<template>
  <div class="tab-window">
    <h3>UAVSAR</h3>
    <div class="topbuttonGroup">
      <div class="overviewButtonGroup">
        <b-button
            class="btn-sm"
            type="checkbox"
            id="overview"
            :pressed.sync="overview"
            @click="showOverview"
        ><span v-if="!overview">Show Overview</span>
          <span v-else>Hide Overview</span>
        </b-button>


        <!--      <div >-->
        <!--      <div class="toolInfo">-->
        <!--        <i>Fill one of the following fields or use map drawing tools to search catalog:</i>-->
        <!--      </div>-->
        <!--      <br />-->
        <b-button class="btn-sm" v-if="overview" variant="dark" @click="uavsarDrawRect()"><b-icon-pencil></b-icon-pencil> Draw Area</b-button>
        <b-button class="btn-sm" v-if="overview" variant="dark" @click="uavsarPinDrop()"><b-icon-hand-index></b-icon-hand-index> Drop Pin </b-button>
      </div>
      <!--      </div>-->
    </div>




    <div v-if="overview">
      <!--      <div class="toolInfo">-->
      <!--        <i>Fill one of the following fields or use map drawing tools to search catalog:</i>-->
      <!--      </div>-->
      <div v-if="geometryActive" >
        <br/>
        <b-button class="btn-sm" variant="warning" @click="drawListenerOff">
          <b-icon-x-circle></b-icon-x-circle>Cancel Selection</b-button>
        <br/>
      </div>
      <br/>
      <b-input-group class="input-group-sm" prepend="Flight name/path">
        <b-form-input v-model="flight_path" name="flight_path" placeholder=""></b-form-input>
      </b-input-group>

      <b-input-group class="input-group-sm" prepend="Latitude, Longitude">
        <b-form-input v-model="lat_lon" name="lat_lon" placeholder=""></b-form-input>
      </b-input-group><br/>
      <b-button class="btn-sm" variant="success" @click="uavsarQuery()">Search</b-button>
    </div>


    <div v-if="uavsarLayers.length !== 0 && !activeQuery">
      <br/>
      <b-container >
        <div class="layer-options">
          <b-row>
            <b-button class="btn-sm" @click="selDeselAll">
              Display/Hide All
            </b-button>
            <b-button class="btn-sm" @click="clearQuery" variant="warning">
              Clear Query
            </b-button>
          </b-row>
          <b-row style="margin-top: 5px">
            <div>
              <input type="date" id="start" name="trip-start" v-model="bracketDate">
            </div>
            <b-button @click="filterDate" variant="success" size="sm">Filter by Date</b-button>
            <b-button @click="clearFilters" variant="warning" size="sm">Clear Filter</b-button>
          </b-row>
          <b-checkbox style="text-align: left" v-model="alternateColoringChecked">Show alternate coloring if available</b-checkbox>
        </div>
      </b-container>


      <div id="queryWindow">

        <div class="collapsed"  v-for="entry in uavsarLayersFiltered" :key="entry.info['uid']" v-bind:style="{backgroundColor: entry.activeBackground}">
          <b-col>
           <input type="checkbox" v-model="entry.displayed" @change="kmlLayerChange(entry)"> Display/Hide <br> 
          </b-col>
          <b-col >
            <div id="selectableHeader"  @click="extendEntry(entry)" style="cursor:pointer;">
              <div><b style="font-size: 12px" id="dataname">{{entry.info['dataname']}}</b></div>
              <b-row class="justify-content-md-center">
              <b-col>
              <b style="font-size: 12px">{{entry.info['time1'].split(' ')[0]}} | {{entry.info['time2'].split(' ')[0]}}</b>
              </b-col>
              <b-col>
              <div id="rating">
                <div v-if="entry.info['rating'] === '0'">
                  <b-icon-star/>
                  <b-icon-star/>
                  <b-icon-star/>

                </div>
                <div v-else-if="entry.info['rating'] === '1'">
                  <b-icon-star-fill/>
                  <b-icon-star/>
                  <b-icon-star/>
                </div>
                <div v-else-if="entry.info['rating'] === '2'">
                  <b-icon-star-fill/>
                  <b-icon-star-fill/>
                  <b-icon-star/>
                </div>
                <div v-else-if="entry.info['rating'] === '3'">
                  <b-icon-star-fill/>
                  <b-icon-star-fill/>
                  <b-icon-star-fill/>
                </div>
              </div>              
              </b-col>
              </b-row>
 
            </div>
            <div v-if="extendingActive && entry.extended">
              <b-spinner type="grow" variant="warning">
              </b-spinner>
            </div>
            <div v-else-if="entry.extended && !extendingActive" class="extended" v-bind:style="{backgroundColor: extendedColor, border: extendedBorder }">

              <div class="extended">
                <b>Heading: </b> {{entry.info['heading']}}  <b>Radar Dir: </b> {{entry.info['radardirection']}} <br/>
                <!--                <i v->{{hasAlternateColoring ? 'Displaying alternate coloring' : 'Alternate coloring not found'}}</i>-->
              </div>
              <div v-if="layerFound">
                <b-input-group class="input-group-sm mb-2">
                  <i style="font-size: small;">Set Layer Opacity: <b>{{ opVal }}%</b></i>
                <b-form-input id="opacity" @change="updateOpacity(opVal)" v-model="opVal" type="range" min="0" max="100"></b-form-input>
                </b-input-group>
                <div v-if="LosPlotAvailable && layerFound" class="extended" id="active-plot" v-bind:style="{backgroundColor: extendedColor, border: extendedBorder }">
                  <b-input-group>
                    <b-input-group prepend="Start Lat/Lon" class="input-group-sm mb-2">
                      <b-form-input v-model="lat1" name="lat1" placeholder=""></b-form-input>
                      <b-form-input v-model="lon1" name="lon1" placeholder=""></b-form-input>
                    </b-input-group>
                  </b-input-group>
                  <b-input-group>
                    <b-input-group prepend="End Lat/Lon" class="input-group-sm mb-2">
                      <b-form-input v-model="lat2" name="lat2" placeholder=""></b-form-input>
                      <b-form-input v-model="lon2" name="lon2" placeholder=""></b-form-input>
                    </b-input-group>
                  </b-input-group>
                  <!--
                  <b-input-group prepend="LOS Length" class="input-group-sm">
                    <b-form-input v-model="losLength" name="length" placeholder=""></b-form-input>
                  </b-input-group>
                  <b-input-group prepend="Azimuth" class="input-group-sm">
                    <b-form-input v-model="azimuth" name="azimuth" placeholder=""></b-form-input>
                  </b-input-group> -->
                  <i style="font-size: small;">Profile Length: <b>{{ losLength }} km</b></i>  <span class="tab" />
                   <i style="font-size: small;">Azimuth: <b>{{ azimuth }}</b></i>
                  <b-row>
                    <b-col sm="auto">
                      <b-button class="btn-sm" variant="success" @click="updatePlotLineForm(activeEntry, lat1, lon1, lat2, lon2)">
                        <span >Update Plot</span>
                      </b-button>
                    </b-col>
                    <b-col  sm="auto">
                      <b-button class="btn-sm" variant="success" @click="downloadCSV(activeEntry)">
                        <span >Download Data</span>
                      </b-button>
                    </b-col>
                    <b-col  sm="auto">
                      <span  @click="openDataSource(entry.info['uid'])" style="cursor: pointer; color: #2e6da4; font-size: small;"><b><u>Data Source</u></b></span>
                    </b-col>
                  </b-row>
                </div>
              </div>

            </div>
          </b-col>
        </div>
      </div>
    </div>
    <div v-else-if="activeQuery" style="overflow: hidden">
      <br/>
      <b-spinner variant="success" label="Spinning"></b-spinner>
    </div>
  </div>
</template>

<script>
import {bus} from '../main'
import axios from "axios";
import 'leaflet-kmz';
import L from 'leaflet';
import 'leaflet-kml'
import { mapFields } from 'vuex-map-fields';



export default {
  name: "UAVSAR",
  data(){
    return {
      endIcon: new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_redA.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      }),
      startIcon: new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_blueB.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      }),
      pinDrop: null,
      rectDraw: null,
      areaLayer: null,
      pinLayer: null,
      tempFilter: [],
      tempLayers: [],
      geometryActive: false,
      wmsColorUrl: 'https://data.geo-gateway.org/geoserver/InSAR/wms?',
      wmsUrl: 'https://data.geo-gateway.org/geoserver/highres/wms?',
      altColorLegend: 'https://data.geo-gateway.org/uavsarlegend1/uid',
      piLegend: 'https://data.geo-gateway.org/kmz/highreslegend/pi_t.png',
      twoPiLegend: 'https://data.geo-gateway.org/kmz/highreslegend/2pi_t.png',
    }
  },

  directives: {

  },
  components: {


  },
  computed: {
    ...mapFields([
      'uavsar.overview',
      'uavsar.plottingMarkerEnd',
      'uavsar.plottingMarkerStart',
      'uavsar.plotLine',
      'uavsar.plotLat1',
      'uavsar.plotLon1',
      'uavsar.plotLat2',
      'uavsar.plotLon2',
      'uavsar.uavsarLatLon',
      'uavsar.uavsarEntry',
      'uavsar.flight_path',
      'uavsar.lat_lon',
      'uavsar.uavsarLayers',
      // 'uavsar.extendedColor',
      // 'uavsar.extendedBorder',
      'uavsar.alternateColoringChecked',
      'uavsar.extendingActive',
      'uavsar.layerFound',
      'uavsar.selDesel',
      'uavsar.LosPlotAvailable',
      'uavsar.lat1',
      'uavsar.lat2',
      'uavsar.lon1',
      'uavsar.lon2',
      'uavsar.losLength',
      'uavsar.azimuth',
      'uavsar.activePlot',
      'uavsar.csv_final',
      'uavsar.activeEntry',
      'uavsar.opVal',
      'uavsar.uid',
      'uavsar.extendedBorder',
      'uavsar.extendedColor',
      'uavsar.uavsarLayersFiltered',
      'uavsar.activeQuery',
      'uavsar.geomEntries',
      'uavsar.path',
      'uavsar.sortBy',
      'uavsar.uavsarHighResLayer',
      'uavsar.uavsarDisplayedLayers',
      'uavsar.hasAlternateColoring',
      'uavsar.hasHighresOverlay',
      'uavsar.activeBackground',
      'uavsar.dateFilter',
      'uavsar.bracketDate',
      'uavsar.currentExtendedEntry',
      'uavsar.overviewLegend',
      'uavsar.lowResKML',
      'uavsar.lowResDisplayed',
      //Map objects
      'map.globalMap',
      'map.layers',
      'map.drawControl',
      'map.uavsarLegend',
      'map.plotActive',
      'map.headingLegend',

    ])
  },
  mounted() {
    // window.addEventListener("keydown", function(e) {
    //   // space and arrow keys
    //   if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
    //     e.preventDefault();
    //   }
    // }, false);
    bus.$on('markPlace', (lat, lon) =>
        this.pointQuery(lat, lon));
    bus.$on('showOverview', () =>
        this.showOverview());
    bus.$on('getCSV', (entry, latlons)=>
        this.getCSV(entry, latlons));

    bus.$on('chartData', (csv)=>
        this.chartData(csv));
    // bus.$on('polyDrawn', (latlngs)=>
    //     this.polyQuery(latlngs));
    //tool argument for identifying currently active tool
    bus.$on('uavsarDrawQuery', (maxLat, minLon, minLat, maxLon, centerLat, centerLng)=>
        this.rectQuery(maxLat, minLon, minLat, maxLon, centerLat, centerLng));
    bus.$on('uavsarHighRes', (entry) =>
        this.uavsarHighRes(entry));
    bus.$on('resetPlot', () =>
        this.resetPlot());
  },
  methods: {

    uavsarDrawRect(){
      this.geometryActive = true;
      let vm = this;
      vm.rectDraw = new L.Draw.Rectangle(vm.globalMap, vm.drawControl.options.rectangle);
      vm.rectDraw.enable();
      vm.globalMap.on('draw:created', function (e) {
        if (vm.areaLayer!=null){
          vm.globalMap.removeLayer(vm.areaLayer);
          vm.areaLayer = null;
        }
        var type = e.layerType;
        if (type === 'rectangle') {
          var layer = e.layer;
          vm.globalMap.addLayer(layer);
          vm.centerLat = layer.getCenter().lat;
          vm.centerLng = layer.getCenter().lng;
          vm.maxLat = layer.getLatLngs()[0][1].lat;
          vm.maxLon = layer.getLatLngs()[0][2].lng;
          vm.minLat = layer.getLatLngs()[0][3].lat;
          vm.minLon = layer.getLatLngs()[0][0].lng;
          vm.globalMap.setView([vm.centerLat,vm.centerLng], 7);
          vm.rectDraw = null;
          vm.areaLayer = layer;
          vm.rectQuery(vm.maxLat, vm.minLon, vm.minLat, vm.maxLon, vm.centerLat, vm.centerLng);
          vm.geometryActive = false;
        }});

    },

    clearFilters(){
      Array.prototype.push.apply(this.uavsarLayersFiltered, this.uavsarLayers);

      this.bracketDate = ''
    },
    uavsarPinDrop(){
      this.geometryActive = true;
      var vm = this;
      this.pinDrop = new L.Draw.Marker(this.globalMap, this.drawControl.options.marker);
      this.pinDrop.enable();
      if (vm.pinLayer != null){
          vm.globalMap.removeLayer(vm.pinLayer);
          vm.pinLayer = null;
        }
      this.globalMap.on('draw:created', function (e) {
        vm.markerLayer = e.layer;
        vm.globalMap.addLayer(e.layer);
        var lat = e.layer.getLatLng().lat;
        var lng = e.layer.getLatLng().lng;
        vm.pinLayer=e.layer;
        vm.pointQuery(lat,lng);
        vm.pinDrop = null;
        vm.geometryActive = false;
      });
    },
    drawListenerOff(){
      this.geometryActive = false;
      if(this.pinDrop){
        this.pinDrop.disable();
      }if (this.rectDraw){
        this.rectDraw.disable();
      }
    },
    filterHeading(){
      var pathSearch = this.path;
      function checkPath(entry){
        return entry.info['heading'].includes(pathSearch);
      }
      this.uavsarLayersFiltered = this.uavsarLayers.filter(checkPath);
    },

    filterDate(){
      let vm = this;
      function checkDate(entry) {
        let d = entry.info['time1'].replaceAll('-', '/')
        let d2 = entry.info['time2'].replaceAll('-', '/')
        let b1 = new Date(d)
        let b2 = new Date(d2);
        let b3 = new Date(vm.bracketDate)
        return (b3 > b1 && b3 < b2);
      }
      if(this.bracketDate !== '') {
        this.uavsarLayersFiltered = this.uavsarLayers.filter(checkDate);
      }
    },


    sortEntries(){
      if(this.sortBy === 'rating') {
        this.uavsarLayersFiltered = this.uavsarLayers.sort((a, b) =>
            (a.info['rating'] > b.info['rating']) ? -1 : 1);
      }
    },

    uavsarQuery(){
      this.activeQuery = true;
      if(this.lat_lon === '') {
        if (this.flight_path === '') {
          alert('Please fill one of the input boxes');
        } else {
          this.flightPathQuery(this.flight_path);
        }
      }else {
        this.pointQuery(this.lat_lon.split(',')[0], this.lat_lon.split(',')[1]);
      }

    },


    openDataSource(uid){
      window.open('http://gf2.ucs.indiana.edu/quaketables/uavsar?uid='+uid, '_blank');
    },

    updateOpacity(value){
      this.uavsarHighResLayer.setOpacity((value/100));
    },
    chartData(csv){
      // let vm = this;
      // let csv;
      // axios.get(csvUrl).then(function(response){
      //   csv = response.data;
      // }).then(function (){
      var csv2=csv.split("\n");
      var csv_final="";
      for(var i=0;i<csv2.length;i++) {
        var csv3=csv2[i].split(",");
        //                console.log(csv2[i],csv3)
        if(csv3[2] && csv3[3] && csv3[5]) {
          csv_final+=csv3[2]+","+csv3[3]+ ","+csv3[5] + "\n";
        }
      }
//      console.log(csv_final);
      this.csv_final = csv_final;
      this.LosPlotAvailable= true;
      bus.$emit('activatePlot', csv_final);
      // });
    },

    getCSV(entry, latlon){
      let vm = this;
      var losLength = this.setLosLength(latlon);
      var azimuth = this.setAzimuth(latlon);
      this.losLength = losLength;
      this.azimuth = azimuth;
      this.lat1 = latlon[0].toFixed(5);
      this.lon1 = latlon[1].toFixed(5);
      this.lat2 = latlon[2].toFixed(5);
      this.lon2 = latlon[3].toFixed(5);

      axios.get('/geogateway_django_app/UAVSAR_csv/', {
        params: {
          //'entry':JSON.stringify(entry),
          'uid':entry['info']['uid'],
          'dataname':entry['info']['dataname'],
          'lat1':this.lat1,
          'lon1':this.lon1,
          'lat2':this.lat2,
          'lon2':this.lon2,
          'losLength':losLength,
          'azimuth':azimuth,
        }
      }).then(function (response){
        vm.chartData(response.data);

      })
    },

    downloadCSV(entry){
      
      var latlon = [this.plottingMarkerEnd.getLatLng().lat, this.plottingMarkerEnd.getLatLng().lng, this.plottingMarkerStart.getLatLng().lat, this.plottingMarkerStart.getLatLng().lng];

      var losLength = this.setLosLength(latlon);
      var azimuth = this.setAzimuth(latlon);
      this.losLength = losLength;
      this.azimuth = azimuth;
      this.lat1 = latlon[0].toFixed(5);
      this.lon1 = latlon[1].toFixed(5);
      this.lat2 = latlon[2].toFixed(5);
      this.lon2 = latlon[3].toFixed(5);
      var imagename = entry.info['dataname'];
      var csvname = imagename + ".csv";
      axios.get('/geogateway_django_app/los_download/', 
        
        {responseType: 'blob', 
        params: {
          'entry':JSON.stringify(entry),
          'lat1':this.lat1,
          'lon1':this.lon1,
          'lat2':this.lat2,
          'lon2':this.lon2,
          'losLength':losLength,
          'azimuth':azimuth,
        }
      }).then(function (response){
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', csvname);
        document.body.appendChild(link);
        link.click();
      })
    },
    findWithAttr(array, attr, value) {
      for(var i = 0; i < array.length; i += 1) {
        if(array[i][attr] === value) {
          return i;
        }
      }
      return -1;
    },
    extendEntry(entry){
      var vm = this;
      this.overviewLegend.remove();
      //Reset any previously extended entries.
      for(let i = 0; i < this.uavsarLayersFiltered.length; i++){
        this.uavsarLayersFiltered[i].extended = false;
	this.uavsarLayersFiltered[i].activeBackground = '#a8b4bf';
	//Also, unselect them
	this.uavsarLayersFiltered[i].displayed = false;	
      }
      if(this.uavsarHighResLayer !== null){
        this.globalMap.removeLayer(this.uavsarHighResLayer);
        this.uavsarLegend.remove();
        // this.headingLegend.remove();
      }
      //Now handle the selected entry
      if(!entry.extended) {
        this.extendingActive = true;
        if(this.plotActive){
          this.getCSV(entry, [this.plottingMarkerEnd.getLatLng().lat, this.plottingMarkerEnd.getLatLng().lng,
            this.plottingMarkerStart.getLatLng().lat, this.plottingMarkerStart.getLatLng().lng]);
        }
        this.activeEntry = entry;
        entry.clicked = true;
        entry.activeBackground = '#8494a3';
        entry.extended = true;
        var testURI = '/geogateway_django_app/UAVSAR_test/';

        //var layername = entry.info['uid'] + '_unw';
        //var dataname = entry.info['dataname'];

        //set current extended entry for keyup keydown change

        this.currentExtendedEntry = this.findWithAttr(this.uavsarLayersFiltered, 'extended', true);

        //get wms description and check for exception

        axios.get(testURI, {
          params: {
            'uid': entry.info['uid'],
            'dataname': entry.info['dataname'],
          }
        }).then( (response) => {
          var datajson = response.data;
          if (Object.prototype.hasOwnProperty.call(datajson, 'hasAlternateColoring')) {
            vm.hasAlternateColoring = true; }
          if (Object.prototype.hasOwnProperty.call(datajson, 'hasHighresOverlay')) {
            vm.hasHighresOverlay = true; }
          if (Object.prototype.hasOwnProperty.call(datajson, 'lowreskml')) {
            vm.lowResKML = datajson['lowreskml'];}

          if (vm.alternateColoringChecked) {
            vm.layerFound = true;
            vm.extendedColor = '#CCFFCC'
            vm.extendedBorder = '1px solid #ADD673'
            //vm.hasAlternateColoring = true;
            vm.uavsarHighRes(entry, vm.hasAlternateColoring, vm.hasHighresOverlay);

          } else {
            vm.layerFound = true;
            vm.extendedColor = '#CCFFCC'
            vm.extendedBorder = '1px solid #ADD673'
            //vm.hasAlternateColoring = false;
            vm.uavsarHighRes(entry, vm.hasAlternateColoring, vm.hasHighresOverlay);

          }
        });
      }
      entry.displayed=true;      
      vm.extendingActive = false;
    },

    //High Res KML's and CSV LOS plotting methods //////////////////////////////////
    uavsarHighRes(entry, hasAlternateColoring, hasHighresOverlay) {
      var latlon = entry.info.geometry.coordinates[0];
      for(var i = this.uavsarLayersFiltered.length-1; i >= 0; i--){
        this.uavsarLayersFiltered[i].displayed = false;
        this.kmlLayerChange(this.uavsarLayersFiltered[i]);
      }
      if (this.uavsarLegend !== null) {
        this.uavsarLegend.remove();
      }
      var baseURI, overlayType, legendExten, legendFinal;
      if(hasAlternateColoring && this.alternateColoringChecked) {
        baseURI = this.wmsColorUrl;
        overlayType = 'InSAR:';
        legendExten = entry.info['uid'] + '_unw_default.png';
        legendFinal = this.altColorLegend + legendExten;
      }else {
        baseURI = this.wmsUrl;
        overlayType = 'highres:'
        let uid = parseInt(entry.info['uid']);
        if(uid <= 369) {
          legendFinal = this.piLegend;
        }else {
          legendFinal = this.twoPiLegend;
        }
      }

      var layername = overlayType + 'uid' + entry.info['uid'] + '_unw'

      this.uavsarLatlon = latlon;
      this.uavsarEntry = entry;
      console.log(hasHighresOverlay);
      if (hasHighresOverlay) {
        this.uavsarHighResLayer = L.tileLayer.wms(baseURI, {
          layers: layername,
          transparent: true,
          format: 'image/png',
          zIndex: 11
        })
      } else {
        const parser = new DOMParser();
        const kml = parser.parseFromString(this.lowResKML, 'text/xml');
        const track = new L.KML(kml,{'ignorePlacemark':true});
        this.uavsarHighResLayer = track;
      }

      this.globalMap.addLayer(this.uavsarHighResLayer);
      //this.uavsarHighResLayer.setOpacity(.75)
      // zoom to image center
      var pos_list = entry.info['geometry']['coordinates'];
      var lon_sum = 0,lat_sum = 0;
      for (var j = 0; j < pos_list[0].length; j++) {
        lon_sum += pos_list[0][j][0];
        lat_sum += pos_list[0][j][1];
      }
      lon_sum = lon_sum / pos_list[0].length;
      lat_sum = lat_sum / pos_list[0].length;
      this.globalMap.setView([lat_sum,lon_sum],9);

      var headingLegendFinal;
      //var headingLegendBase = 'http://gf2.ucs.indiana.edu/direction_kml/'
      var headingLegendBase = 'https://data.geo-gateway.org/kmz/direction_kml/'
      var headingRounded = entry.info['heading'].split('.')[0];
      var radarDir = entry.info['radardirection'];
      var radarDirL;
      if(radarDir === 'Left'){
        radarDirL = 'left';
      }else {
        radarDirL = 'right';
      }
      headingLegendFinal = headingLegendBase + headingRounded + '_' + radarDirL + '.png';
      this.uavsarLegend = L.control({position: 'bottomleft'});
      this.uavsarLegend.onAdd = function () {
        var div = L.DomUtil.create('div', 'uavsarLegend');
        div.innerHTML = '<img src=' + legendFinal + '> <img style="width: 100px; height: 100px;" src=' + headingLegendFinal + ' >';
        return div;
      };
      this.uavsarLegend.addTo(this.globalMap);
      this.globalMap.on('click', this.markerClick);

    },
    markerClick(e) {
      var clickloc = e.latlng;

      var latlon = this.uavsarLatlon;
      var entry = this.uavsarEntry;

      var southwest = L.latLng(latlon[0][1], latlon[0][0]);
      var northeast = L.latLng(latlon[3][1], latlon[3][0]);

      //var rect = L.latLngBounds(southwest, northeast);

      //console.log(southwest, northeast, rect.contains(clickloc));

      this.placePlotMarkers(southwest, northeast, clickloc, latlon, entry);
    },


    updatePlotLineForm(entry, lat1, lon1, lat2, lon2) {
      this.plotActive = true;
      this.plottingMarkerStart.setLatLng([lat2, lon2]);
      this.plottingMarkerEnd.setLatLng([lat1, lon1]);
      //console.log(az, len);
      var latlon = [this.plottingMarkerEnd.getLatLng().lat, this.plottingMarkerEnd.getLatLng().lng, this.plottingMarkerStart.getLatLng().lat, this.plottingMarkerStart.getLatLng().lng]
      this.getCSV(entry, latlon);
    },

    updatePlotLine(entry) {
      this.updatePlotLineForm(entry, this.plottingMarkerEnd.getLatLng().lat, this.plottingMarkerEnd.getLatLng().lng, this.plottingMarkerStart.getLatLng().lat, this.plottingMarkerStart.getLatLng().lng)
    },
    placePlotMarkers(southwest, northeast, clickloc, latlon, entry) {
      if (this.plottingMarkerEnd == null) {
        this.plotActive = true;
        this.plotLat2 = clickloc.lat;
        this.plotLon2 = clickloc.lng;

        this.plotLat1 = latlon[2][1];
        this.plotLon1 = latlon[2][0];

        var factor = (this.plotLon1 - this.plotLon2) / 7;
        this.plotLon1 = this.plotLon2 + factor;
        this.plotLat1 = ((this.plotLat1 - this.plotLat2) / 5) + this.plotLat2


        this.plottingMarkerStart = L.marker([this.plotLat2, this.plotLon2],
            {draggable: true, icon: this.startIcon});
        // console.log(this.plottingMarker1)
        this.plottingMarkerEnd = L.marker([this.plotLat1, this.plotLon1],
            {draggable: true, icon: this.endIcon});

        this.plotLine = L.polyline([this.plottingMarkerEnd.getLatLng(), this.plottingMarkerStart.getLatLng()],
            {color: 'red'});

        this.plottingMarkerEnd.addTo(this.globalMap)
        this.plottingMarkerStart.addTo(this.globalMap)
        this.plotLine.addTo(this.globalMap)

        //for use inside event listener
        let vm = this;

        vm.plottingMarkerEnd.on('drag', function () {
          vm.plotLine.setLatLngs([vm.plottingMarkerEnd.getLatLng(), vm.plottingMarkerStart.getLatLng()]);
        })
        vm.plottingMarkerStart.on('drag', function () {
          vm.plotLine.setLatLngs([vm.plottingMarkerEnd.getLatLng(), vm.plottingMarkerStart.getLatLng()]);
        })

        this.plottingMarkerEnd.on('dragend', function () {
          vm.updatePlotLine(entry);
        })
        this.plottingMarkerStart.on('dragend', function () {
          vm.updatePlotLine(entry);
        })


        this.globalMap.off('click', this.markerClick);

        // this.globalMap.fitBounds([this.plotLat2, this.plotLon2], [this.plotLat1, this.plotLon1])

        this.getCSV(entry, [this.plotLat2, this.plotLon2, this.plotLat1, this.plotLon1]);
      }
    },

    resetPlot() {
      if(this.plottingMarkerEnd != null || this.plottingMarkerStart != null) {
        this.plottingMarkerEnd.remove();
        this.plottingMarkerStart.remove();
        this.plotLine.remove();
        this.plottingMarkerEnd = null;
        this.plottingMarkerStart = null;
        this.plotLine = null;
        this.plotActive = false;
      }

      this.LosPlotAvailable = false;
    },

    removeAreaLayer(){
      let vm = this;
      if (vm.areaLayer!=null){
        vm.globalMap.removeLayer(vm.areaLayer);
        vm.areaLayer = null;
      }
    },
    removePinLayer(){
      let vm=this;
      if (vm.pinLayer!=null){
        vm.globalMap.removeLayer(vm.pinLayer);
      }
      vm.pinLayer=null;
    },

    showPinLayer(){
      let vm = this;
        if (vm.pinLayer!=null){
          vm.globalMap.addLayer(vm.pinLayer);
        }
      
    },
    hidePinLayer(){
      let vm = this;
      if (vm.pinLayer!=null){
        vm.globalMap.removeLayer(vm.pinLayer);
      }
    },

/////////////////////////////////////////////////////////////////////


    /////// Global UAVSAR query methods
    selDeselAll(){
      for(var i = this.uavsarLayersFiltered.length-1; i >= 0; i--){
        this.uavsarLayersFiltered[i].displayed = this.selDesel;
        this.kmlLayerChange(this.uavsarLayersFiltered[i]);
      }
      this.selDesel = !this.selDesel;
    },
    clearQuery(){
      
/*
      //deselect all
      for(var j = this.uavsarLayersFiltered.length-1; j >= 0; j--){
        this.uavsarLayersFiltered[j].displayed = this.selDesel;
        this.kmlLayerChange(this.uavsarLayersFiltered[j]);
      }
      this.selDesel = false;
 */
      this.lat_lon = '';
      this.flight_path = '';
      for (var i = 0; i < this.uavsarLayersFiltered.length; i++) {
        let uid = this.uavsarLayersFiltered[i].info['uid'];
        if(this.globalMap.hasLayer(this.uavsarDisplayedLayers[uid])) {
          this.globalMap.removeLayer(this.uavsarDisplayedLayers[uid]);
        }

      }
      this.resetPlot();
      if(this.uavsarHighResLayer !== null){
        this.globalMap.removeLayer(this.uavsarHighResLayer);
        this.uavsarHighResLayer = null;
        this.uavsarLegend.remove();
      }
      //added from showOverview:
      this.tempFilter=[];
      this.tempLayers=[];
      this.showOverview();
      if (this.overviewLegend === null) {
        this.showOverviewLegend();
      } else {
        this.removeOverviewLegend();
        this.showOverviewLegend();
      }
      this.uavsarDisplayedLayers = [];
      this.uavsarLayersFiltered = [];
      this.uavsarLayers = [];
      this.extendedColor = null;
      this.extendedBorder = null;
      this.removePinLayer();

      

    },
    showOverview() {
      const _ = require('lodash');
      if (this.overview) {
        this.layers['uavsarWMS'] = L.tileLayer.wms('https://data.geo-gateway.org/geoserver00/InSAR/wms?', {
              layers: 'InSAR:thumbnailmosaic',
              transparent: true,
              format: 'image/png',
              zIndex: 10,
            }
        );
        if(!this.overviewLegend){this.showOverviewLegend();}
        
        if (this.tempLayers.length>0){
          this.uavsarLayers = this.tempLayers;
          console.log("if");
          console.log(this.tempLayers);
        }else{
            this.globalMap.addLayer(this.layers['uavsarWMS']);
            this.layers['uavsarWMS'].setOpacity(.7)
        }

        if (this.tempFilter!=[]){
          this.uavsarLayersFiltered = this.tempFilter;
        }
        this.showPinLayer();
        for (var i = 0; i < this.uavsarLayersFiltered.length; i++) {
        let uid = this.uavsarLayersFiltered[i].info['uid'];
        this.globalMap.addLayer(this.uavsarDisplayedLayers[uid]);
        }

      } else {

        for (i = 0; i < this.uavsarLayersFiltered.length; i++) {
        let uid = this.uavsarLayersFiltered[i].info['uid'];
        if(this.globalMap.hasLayer(this.uavsarDisplayedLayers[uid])) {
          this.globalMap.removeLayer(this.uavsarDisplayedLayers[uid]);
        }
        }
        
        //save user progress
        this.tempLayers= _.clone(this.uavsarLayers);
        this.tempFilter = _.cloneDeep(this.uavsarLayersFiltered);

        this.uavsarLayers = [];
        this.uavsarLayersFiltered = [];
        this.layers['uavsarWMS'].remove();
        this.LosPlotAvailable = false;
        this.overviewLegend.remove();
        this.overviewLegend = null;
        this.hidePinLayer();
      }
    },
    showOverviewLegend(){
      this.overviewLegend = L.control({position: 'bottomleft'});
      this.overviewLegend.onAdd = function () {
        var div = L.DomUtil.create('div', 'overviewLegend');
        div.innerHTML = '<img src=' + 'https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/uavsarlegend.png' + '>';
        return div;
      };
      this.overviewLegend.addTo(this.globalMap);
    },
    removeOverviewLegend() {
      this.overviewLegend.remove();
      this.overviewLegend = null;
    },
    flightPathQuery(path){
      this.activeQuery = true;
      var vm = this;
      if(this.overview) {
        var baseURI = '/geogateway_django_app/UAVSAR_flight/'
        axios.get(baseURI, {
          params: {
            //
            "type": "path",
            "queryStr": path.trim() + '',
          }
        }).then(function (response) {
          let entries = response.data;
          let baseURI = '/geogateway_django_app/UAVSAR_KML/'
          let promises = [];
          for (var i = 0; i < entries.length; i++) {
            promises.push(
                axios.get(baseURI, {
                  params: {
                    //
                    "json": JSON.stringify(entries[i]),
                  }
                }))
          }
          Promise.all(promises).then((responses) =>{
            if (vm.layers['uavsarWMS']) {
              vm.globalMap.removeLayer(vm.layers['uavsarWMS']);
            }
            for(let k = 0;k < responses.length;k++){
              let entry = responses[k].data;
              entry.activeBackground = '#a8b4bf';
              vm.uavsarLayers[k] = entry;
              vm.uavsarLayersFiltered[k] = entry;
              let uid = vm.uavsarLayers[k].info['uid'];

              const parser = new DOMParser();
              const kml = parser.parseFromString(vm.uavsarLayers[k].kml, 'text/xml');
              const track = new L.KML(kml,{'ignorePlacemark':true});
              vm.uavsarDisplayedLayers[uid] = track;
              vm.globalMap.addLayer(vm.uavsarDisplayedLayers[uid]);
            }
            vm.activeQuery = false;

          })
        })
      }
    },
    pointQuery(lat, lon){
      function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }

      this.globalMap.off('draw:created');
      this.activeQuery = true;
      var vm = this;

      //checking if input comes from marker placement or manual entry (numeric string)
      if(lat.substring && lon.substring){
        if(isNumber(lat) && isNumber(lon)){
          lat = parseFloat(lat)
          lon = parseFloat(lon)
        }
        else {
          alert('Please enter decimal point coordinates')
        }
      }
      lat = lat.toFixed(5)
      lon = lon.toFixed(5)
      if(this.overview) {
        this.lat_lon = lat.toString() + ',' + lon.toString();
        var queryStr = '(' + this.lat_lon + ')'
        var baseURI = '/geogateway_django_app/UAVSAR_geom/'
        axios.get(baseURI, {
          params: {
            //
            "type": "point",
            "queryStr": queryStr,
          }
        }).then(function (response) {
//          console.log(response.headers);
          let entries = response.data;
          let baseURI = '/geogateway_django_app/UAVSAR_KML/'
          let promises = [];
          for (var i = 0; i < entries.length; i++) {
            promises.push(
                axios.get(baseURI, {
                  params: {
                    //
                    "json": JSON.stringify(entries[i]),
                  }
                }))
          }
          Promise.all(promises).then((responses) =>{
            if (vm.layers['uavsarWMS']) {
              vm.globalMap.removeLayer(vm.layers['uavsarWMS']);

            }
            for(let k = 0;k < responses.length;k++){
              let entry = responses[k].data;
              entry.activeBackground = '#a8b4bf';
              //Use the $set function to make these arrays reactive. See https://vuejs.org/v2/guide/reactivity.html#For-Arrays	      
//              vm.uavsarLayers[k] = entry;
              vm.$set(vm.uavsarLayers,k,entry);
//              vm.uavsarLayersFiltered[k] = entry;
              vm.$set(vm.uavsarLayersFiltered,k,entry);
              let uid = vm.uavsarLayers[k].info['uid'];

              const parser = new DOMParser();
              const kml = parser.parseFromString(vm.uavsarLayers[k].kml, 'text/xml');
              const track = new L.KML(kml,{'ignorePlacemark':true});
              vm.uavsarDisplayedLayers[uid] = track;
              vm.globalMap.addLayer(vm.uavsarDisplayedLayers[uid]);
            }
            vm.removePinLayer();
            vm.activeQuery = false;
          })
        })
      }
    },

    // polyQuery(latlngs){
    //     this.activeQuery = true;
    //     var queryResponse;
    //     var queryStr = '';
    //     for(var i = 0;i<latlngs[0].length;i++){
    //         queryStr += '(' + latlngs[0][i].lat + ',' + latlngs[0][i].lng + '),'
    //     }
    //     queryStr = queryStr.replace(/,\s*$/, "");
    //
    //     var baseURI = '/geogateway_django_app/UAVSAR_geom/'
    //     axios.get(baseURI, {
    //         params: {
    //             //
    //             "type":'polygon',
    //             "queryStr":queryStr
    //         }
    //     }).then(function (response){
    //         queryResponse = response.data;
    //         bus.$emit('uavsarGeom', queryResponse)
    //         // bus.$emit('uavsarKMLs', this.uavsarLayersFiltered)
    //
    //     })
    // },
    rectQuery(maxLat, minLon, minLat, maxLon, centerLat, centerLng){
      this.activeQuery = true;
      var vm = this;
      this.globalMap.off('draw:created');

      if(this.overview) {
        console.log(centerLng, centerLat);
        var queryStr = '';
        queryStr += '(' + '(' + minLat.toFixed(3) + ',' + minLon.toFixed(3) + '),' + '(' + maxLat.toFixed(3) + ',' + maxLon.toFixed(3) + '))'
        var baseURI = '/geogateway_django_app/UAVSAR_geom/'
        axios.get(baseURI, {
          params: {
            //
            "type": 'rectangle',
            "queryStr": queryStr
          }
        }).then(function (response) {
          let entries = response.data;
          let baseURI = '/geogateway_django_app/UAVSAR_KML/'
          let promises = [];
          for (var i = 0; i < entries.length; i++) {
            promises.push(
                axios.get(baseURI, {
                  params: {
                    //
                    "json": JSON.stringify(entries[i]),
                  }
                }))
          }
          Promise.all(promises).then((responses) =>{
            if (vm.layers['uavsarWMS']) {
              vm.globalMap.removeLayer(vm.layers['uavsarWMS']);
            }
            for(let k = 0;k < responses.length;k++){
              let entry = responses[k].data;
              entry.activeBackground = '#a8b4bf';
              vm.uavsarLayers[k] = entry;
              vm.uavsarLayersFiltered[k] = entry;
              let uid = vm.uavsarLayers[k].info['uid'];

              const parser = new DOMParser();
              const kml = parser.parseFromString(vm.uavsarLayers[k].kml, 'text/xml');
              const track = new L.KML(kml,{'ignorePlacemark':true});
              vm.uavsarDisplayedLayers[uid] = track;
              vm.globalMap.addLayer(vm.uavsarDisplayedLayers[uid]);
            }
            vm.removeAreaLayer();
            vm.activeQuery = false;
          })
        })
      }
    },
    kmlLayerChange(entry){
      const uid = entry.info['uid'];
      if(entry.displayed) {
        this.globalMap.addLayer(this.uavsarDisplayedLayers[uid]);
      }else {
        this.globalMap.removeLayer(this.uavsarDisplayedLayers[uid]);
      }
    },

    setLosLength(latlon){
      var latStart = latlon[0];
      var lonStart = latlon[1];
      var latEnd = latlon[2];
      var lonEnd = latlon[3];

      var d2r = Math.PI / 180.0;
      var flatten = 1.0 / 298.247;
      var theFactor = d2r * Math.cos(d2r * latStart) * 6378.139 * (
          1.0 - Math.sin(d2r * latStart) * Math.sin(d2r * latStart) * flatten);

      var xdiff = (lonEnd - lonStart) * theFactor;
      var ydiff = (latEnd - latStart) * 111.32;

      var losLength = Math.sqrt(xdiff * xdiff + ydiff * ydiff);
      losLength = losLength.toFixed(3);
      return losLength;
    },
    setAzimuth(latlon){
      var swLat = latlon[0];
      var swLon = latlon[1];
      var neLat = latlon[2];
      var neLon = latlon[3];
      //Using http://www.movable-type.co.uk/scripts/latlong.html
      var d2r=Math.PI/180.0;
      var flatten=1.0/298.247;

      var theFactor=d2r* Math.cos(d2r * swLat) * 6378.139 * (1.0 - Math.sin(d2r * swLat) * Math.sin(d2r * swLat) * flatten);
      var x=(neLon-swLon)*theFactor;
      var y=(neLat-swLat)*111.32;

      var azimuth=Math.atan2(x,y)/d2r;
      azimuth=azimuth.toFixed(1);
      if(azimuth>180) azimuth=azimuth-360;
      if(azimuth<-180) azimuth=azimuth+360;

      return azimuth;
    }
  }
}
</script>

<style scoped>



.extended {
  width: auto;
  height: auto;
  box-sizing: border-box;
  font-size: 15px;
  border-radius: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
}
#active-plot {
  border-radius: 4px;
}
#dataname {
  width:100%;
  font-size:14px;
  word-break:break-all;

}
.entryWindow {
  width: 200px;
  height: 400px;
  overflow-y: auto;
}

#queryWindow {
  height: 700px;
  width: 100%;
  overflow-y: auto;
}
.overviewButtonGroup .active {
  color: #fff !important;
  background-color: #3388ff !important;
  border-color: #3388ff !important;

}
.headingLegend {
  width: 70px;
  height: 70px;
}
.collapsed {
  width: auto;
  height: auto;
  border: 2px solid #e6e6ff;
  box-sizing: border-box;
  border-radius: 4px;
  overflow-y: auto;
  /*A5B9CC*/
}
</style>

<style>


html, body {margin:0;padding:0;height:100%;}
.tab-window {
  background-color: #e6e6ff;
  height:100%;
  overflow-x: hidden;
  overflow-y: hidden;
}
h3, h4, h5 {
  color: #343a40;
}

.center {
  width: 50%;
  margin: 0 auto;
}

</style>
