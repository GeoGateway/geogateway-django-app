<template>
  <div class="w-100 p-2 bg-light text-left">
    <b-alert :show="true">
      <b-link @click="gnssInfo=true" href="#">
        <b-icon icon="info-circle-fill"/>
      </b-link>&ensp;
      About GNSS data Analysis
    </b-alert>

    <span class="inputLabel">Outputs <hr class="sectionLine"/></span>
    <br>
    <b-card>
      <div v-if="gnssLayers.length!==0 && !activeGnssQuery">
        <strong>Output</strong>
        <div v-for="layer in gnssLayers" :key="layer.name">
          <b-card v-if="layer.type !== 'table.txt'">
            <b-form-checkbox :value="layer.active" v-model="layer.active"
                             @change="showHideLayers(layer.active, layer)">
              <span class="checkbox-label"> <a :href="layer.url">{{ layer.pre }} {{ layer.type }}</a> </span>
            </b-form-checkbox>
          </b-card>
          <div v-else><a style="color:#EB9040;" target="_blank" :href="layer.url">{{ layer.name }}</a></div>
        </div>
      </div>
      <div v-else><span style="color:#95ABB1;">No models applied!</span></div>
    </b-card>


    <span class="inputLabel">Functions <hr class="sectionLine"/></span>
    <br>

    <span class="inputLabel">GNSS data models</span>
    <br>

    <!-- <label for="sel1">Select list:</label> -->
    <select class="form-control" v-model="kmltype_sel" id="kmltype_sel">
      <option disabled value='null'>Select a GNSS data model</option>
      <option value='getvelocities'>Velocities</option>
      <option value='getcoseismic'>Coseismic</option>
      <option value='getpostseismic'>Postseismic</option>
      <option value='getdisplacement'>Displacement</option>
      <option value='getmodel'>Model</option>
    </select>

    <div v-if="kmltype_sel!=null">
      <b-button style="margin-top: 10px; margin-bottom: 10px;" v-if="!geometryActive" id="sp_windowpicker"
                class="btn_blue" @click="gnssDrawRect()">
        Draw an area on the map
      </b-button>
      <b-button v-if="gnssLayers.length>0 || areaLayer!=null" class="btn_white" id="clearGnss" @click="clearGnss()">
        Clear Layers
      </b-button>
      <br/>

      <div v-if="geometryActive">
        <br/>
        <b-button class="btn_white" @click="drawListenerOff">
          Unselect 'Draw an Area'
        </b-button>
        <br/>
      </div>
      <br>
      <span class="inputLabel">Center Latitude</span>
      <b-input-group>
        <b-form-input v-model="gs_latitude" name="gs_latitude"></b-form-input>
      </b-input-group>

      <span class="inputLabel">Center Longitude</span>
      <b-input-group>
        <b-form-input v-model="gs_longitude" placeholder="" name="gs_longitude"></b-form-input>
      </b-input-group>

      <span class="inputLabel">Longitude Span</span>
      <b-input-group>
        <b-form-input v-model="gs_width" name="gs_width" placeholder="1 degree"></b-form-input>
      </b-input-group>

      <span class="inputLabel">Latitude Span</span>
      <b-input-group>
        <b-form-input v-model="gs_height" placeholder="1 degree" name="gs_height"></b-form-input>
      </b-input-group>

      <span v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'"
            class="inputLabel">Epoch</span>
      <div class="input-group" id="epoch_show"
           v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'">
        <b-input-group>
          <b-form-input v-model="gs_epoch" placeholder="YYYY-MM-DD" name="gs_epoch"></b-form-input>
        </b-input-group>
      </div>

      <span v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'"
            class="inputLabel">Epoch 1</span>
      <b-input-group v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'">
        <b-form-input v-model="gs_epoch1" placeholder="YYYY-MM-DD" name="gs_epoch1"></b-form-input>
      </b-input-group>

      <span v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'"
            class="inputLabel">Epoch 2 </span>
      <b-input-group v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'">
        <b-form-input v-model="gs_epoch2" placeholder="YYYY-MM-DD" name="gs_epoch2"></b-form-input>
      </b-input-group>

      <span class="inputLabel">Ref. Site</span>
      <b-input-group>
        <b-form-input v-model="gs_refsite" placeholder="4-letter code" name="gs_refsite"></b-form-input>
        <b-input-group-append>
          <b-button variant="outline-primary" href="https://sideshow.jpl.nasa.gov/post/tables/table2.html"
                    target="_blank">Stations
          </b-button>
        </b-input-group-append>
      </b-input-group>

      <span class="inputLabel">Scale</span>
      <b-input-group>
        <b-form-input v-model="gs_scale" placeholder="320 mm/yr/deg" name="gs_scale"></b-form-input>
      </b-input-group>

      <span v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'" class="inputLabel">Coseismic Win.</span>
      <b-input-group v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'">
        <b-form-input v-model="gs_ctwin" name="gs_ctwin" placeholder="0.1 years"></b-form-input>
      </b-input-group>

      <span v-if="this.kmltype_sel === 'getpostseismic' " class="inputLabel">Postseismic Win.</span>
      <b-input-group v-if="this.kmltype_sel === 'getpostseismic' ">
        <b-form-input v-model="gs_ptwin" name="gs_ptwin" placeholder="2 years"></b-form-input>
      </b-input-group>

      <span v-if="this.kmltype_sel === 'getdisplacement'" class="inputLabel">Av. Win. 1</span>
      <b-input-group v-if="this.kmltype_sel === 'getdisplacement'">
        <b-form-input v-model="gs_dwin1" name="gs_dwin1" placeholder="10 days"></b-form-input>
      </b-input-group>

      <span v-if="this.kmltype_sel === 'getdisplacement'" class="inputLabel">Av. Win. 2</span>
      <b-input-group v-if="this.kmltype_sel === 'getdisplacement'">
        <b-form-input v-model="gs_dwin2" name="gs_dwin2" placeholder="10 days"></b-form-input>
      </b-input-group>

      <span class="inputLabel">Output Prefix</span>
      <b-input-group>
        <b-form-input v-model="gs_outputprefix" name="gs_outputprefix"></b-form-input>
      </b-input-group>
      <b-col class="miscOptions">
        <b-row class="checkbox" style="text-align: left" v-if="this.kmltype_sel === 'getdisplacement'">
          <label class="checkbox">
            <input v-model="gs_analysisCenter" name="analysisCenter" type="checkbox" id="gs_analysisCenter"/>
            Use NGL data
          </label>
        </b-row>


        <b-row class="checkbox" style="text-align: left">
          <label class="checkbox">
            <b-form-checkbox v-model="markerSize" name="vabs" type="checkbox" id="markerSize"/>
            Minimize Marker Size
          </label>
        </b-row>
        <b-row class="checkbox" style="text-align: left">
          <label class="checkbox">
            <input v-model="gs_vabs" name="vabs" type="checkbox" id="gs_vabs" value=""/>
            Display absolute verticals
          </label>
        </b-row>
        <b-row class="checkbox" style="text-align: left">
          <label class="checkbox">
            <input v-model="gs_eon" name="mon" type="checkbox" id="gs_eon" value=""/>
            Include error ellipses
          </label>
        </b-row>


        <b-row>
          <button class="btn btn-success" id="gs_submit" name="submit" type="submit"
                  v-on:click.prevent="runButtonClick()"> Run
          </button>
        </b-row>
        <br/>
        <b-row>
          <div style="float: left; text-align: left"><strong>Data source: <br/><a
              href="https://sideshow.jpl.nasa.gov/post/series.html" target="_blank">GNSS Time Series</a></strong>
          </div>
        </b-row>
      </b-col>

      <b-col>
      </b-col>


      <div v-if="activeGnssQuery" style="overflow: hidden">
        <br/>
        <b-spinner variant="success" label="Spinning"></b-spinner>
      </div>
      <br/>
    </div>

    <!-- info  popup -->
    <b-modal
        v-model="gnssInfo"
        title="GNSS">
      <p class="my-4">
        Global Navigation Satellite System (GNSS) is any satellite
        constellation which provides positioning, navigation, and
        timing (PNT) services on a global or regional basis (Other
        Global Navigation Satellite Systems (GNSS), 2020). One of the
        systems GNSS includes is the United States-owned Global Positioning
        System (GPS).
      </p>

      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>

  </div>
</template>

<script>

import {bus} from '@/main'
import axios from 'axios'
import {mapFields} from '../utils/mapFields';
import L from "leaflet";

export default {

  name: "GNSS-tools",
  data() {
    return {
      gnssInfo: false,
      areaLayer: null,
    }
  },
  computed: {
    ...mapFields([
      'gnss.selected',
      'gnss.kmltype_sel',
      'gnss.gs_latitude',
      'gnss.gs_longitude',
      'gnss.gs_width',
      'gnss.gs_height',
      'gnss.gs_epoch',
      'gnss.gs_epoch1',
      'gnss.gs_epoch2',
      'gnss.gs_refsite',
      'gnss.gs_scale',
      'gnss.gs_ctwin',
      'gnss.gs_ptwin',
      'gnss.gs_dwin1',
      'gnss.gs_dwin2',
      'gnss.gs_outputprefix',
      'gnss.kmlData',
      'gnss.gs_eon',
      'gnss.gs_vabs',
      'gnss.gs_analysisCenter',
      'gnss.ranLayers',
      'gnss.activeLayers',
      'gnss.markerSize',
      'gnss.layersActive',
      'gnss.activeGnssQuery',
      'gnss.geometryActive',
      'gnss.gnssLayers',

      'map.drawControl',
      'map.globalMap',
      'map.layers',
    ])

  },
  mounted() {
    bus.on('gnssDrawQuery', (maxLat, minLon, minLat, maxLon, centerLat, centerLng) =>
        this.setRect(maxLat, minLon, minLat, maxLon, centerLat, centerLng));
    this.kmltype_sel = null;
  },
  beforeUnmount() {
    bus.off('gnssDrawQuery');
  },

  methods: {
    showHideLayers(active, layer) {
      let name = layer.pre + layer.type;
      if (active) {
        this.globalMap.addLayer(this.layers[name])
      } else {
        this.globalMap.removeLayer(this.layers[name]);
      }

    },
    runButtonClick() {
      let vm = this;
      if (vm.areaLayer != null) {
        vm.globalMap.removeLayer(vm.areaLayer);
        vm.areaLayer = null;
      }
      this.rungpsservice();
    },
    rungpsservice() {
      this.activeGnssQuery = true;
      var vm = this;
      var fileNameH, fileNameV, fileNameT, folder, props;
      //var markerSize = this.markerSize;
      var verticalUrl, horizontalUrl, tableUrl;
      var prefix = this.gs_outputprefix;
      if (this.kmltype_sel === '') {
        alert("Please select as least one plot!");
      } else {

        for (var i = 0; i < this.gnssLayers.length; i++) {
          var splitPrefix = this.gnssLayers[i].name.split('_')[0];
          if (splitPrefix === this.gs_outputprefix) {
            continue;
            //alert('There is already an existing query with that name, please rename and resubmit');
            //return;
          }
        }
        // this.layerCheckbox = true;
        if (this.gs_analysisCenter == true) {
          this.gs_analysisCenter = "NGL";
        } else {
          this.gs_analysisCenter = "";
        }
        const baseURI = '/geogateway_django_app/gps_service'
        //request JSON dict of GPS_service details with query params from form
        axios.get(baseURI, {
          params: {
            //
            "function": this.kmltype_sel,
            "lat": this.gs_latitude,
            "lon": this.gs_longitude,
            //"width":$('#gs_width').val(),
            //"height":$('#gs_height').val(),
            "width": this.gs_width,
            "height": this.gs_height,
            "epoch": this.gs_epoch,
            "epoch1": this.gs_epoch1,
            "epoch2": this.gs_epoch2,
            "scale": this.gs_scale,
            "ref": this.gs_refsite,
            "ct": this.gs_ctwin,
            "pt": this.gs_ptwin,
            "dwin1": this.gs_dwin1,
            "dwin2": this.gs_dwin2,
            "prefix": this.gs_outputprefix,
            //need default false value?
            "mon": this.markerSize,
            "eon": this.gs_eon,
            "vabs": this.gs_vabs,
            "analysisCenter": this.gs_analysisCenter,
            //
          }
        })
            //use JSON results (filename and folder) to request raw kml text
            .then(function (response) {
              props = response.data;
              console.log(props);
              if (!(typeof props === 'object')) {
                vm.activeGnssQuery = false;
                alert("Somthing wrong, please check input paramters!");
                return;
              }

              function getExtension(f) {
                var parts = f.split('_');
                return parts[parts.length - 1];
              }

              for (var i = 0; i < 3; i++) {
                var ext = getExtension(props.urls[i]);
                if (ext == 'vertical.kml') {
                  verticalUrl = props.urls[i];
                  fileNameV = props.results[i];
                } else if (ext == 'horizontal.kml') {
                  horizontalUrl = props.urls[i];
                  fileNameH = props.results[i];
                } else if (ext == 'table.txt') {
                  tableUrl = props.urls[i];
                  fileNameT = props.results[i];
                }
              }

              folder = props.folder;
              prefix = (1 + Math.floor(vm.gnssLayers.length / 3)).toString() + prefix;
              vm.gnssLayers.push({
                pre: prefix,
                name: fileNameT,
                folder: folder,
                active: true,
                url: tableUrl,
                type: 'table.txt',
              })
              vm.gnssLayers.push({
                pre: prefix,
                name: fileNameH,
                folder: folder,
                active: true,
                url: horizontalUrl,
                type: 'horizontal.kml',
              })
              vm.gnssLayers.push({
                pre: prefix,
                name: fileNameV,
                folder: folder,
                active: true,
                url: verticalUrl,
                type: 'vertical.kml',
              })
              const kmlURI = '/geogateway_django_app/get_kml'
              axios.get(kmlURI, {
                params: {
                  "file": fileNameH,
                  "folder": folder
                },
                responseType: 'text',
                //emit raw kml text to parent map component
              }).then(function (response) {
                // console.log(toGeoJSON.kml(response.data));
                let hName = prefix + 'horizontal.kml';
                vm.addGnssLayer(response.data, hName);

              })
              axios.get(kmlURI, {
                params: {
                  "file": fileNameV,
                  "folder": folder
                },
                responseType: 'text',
                //emit raw kml text to parent map component
              }).then(function (response) {
                // console.log(toGeoJSON.kml(response.data));
                // var geojson = toGeoJSON.kml((new DOMParser()).parseFromString(response.data, 'text/xml'))
                // console.log(geojson)
                let vName = prefix + 'vertical.kml';
                vm.addGnssLayer(response.data, vName);
                //console.log(markerSize)
                vm.activeGnssQuery = false;
              })
            })
        this.layersActive = true;
      }

    },
    addGnssLayer(file, type) {
      this.kmlText(file, type);
    },
    kmlText(text, layerName) {
      const parser = new DOMParser();
      const kml = parser.parseFromString(text, 'text/xml');
      this.layers[layerName] = new L.KML(kml);
      this.globalMap.addLayer(this.layers[layerName]);

    },
    drawToolbar() {
      this.geometryActive = true;

      new L.Draw.Rectangle(this.globalMap, this.drawControl.options.rectangle).enable();

      this.drawListener('gnss');
    },
    gnssDrawRect() {
      this.geometryActive = true;
      let vm = this;
      vm.rectDraw = new L.Draw.Rectangle(vm.globalMap, vm.drawControl.options.rectangle);
      vm.rectDraw.enable();
      vm.globalMap.on('draw:created', function (e) {
        if (vm.areaLayer != null) {
          vm.globalMap.removeLayer(vm.areaLayer)
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
          vm.areaLayer = layer;
          vm.rectDraw = null;
          bus.emit('gnssDrawQuery', vm.maxLat, vm.minLon, vm.minLat, vm.maxLon, vm.centerLat, vm.centerLng)
          vm.geometryActive = false;
        }
      });

    },
    drawListenerOff() {
      this.geometryActive = false;

      this.rectDraw.disable();
    },
    clearGnss() {
      let vm = this;
      if (vm.areaLayer != null) {
        vm.globalMap.removeLayer(vm.areaLayer);
        vm.areaLayer = null;
      }
      this.layersActive = false;
      for (var i = 0; i < this.gnssLayers.length; i++) {
        let curr = this.gnssLayers[i];
        if (curr.type !== 'table.txt') {
          let name = curr.pre + curr.type;
          this.globalMap.removeLayer(this.layers[name]);
        }
      }

      this.gs_latitude = null;
      this.gs_longitude = null;
      this.gs_width = null;
      this.gs_height = null;
      this.gnssLayers = [];
    },
    setRect(maxLat, minLon, minLat, maxLon, centerLat, centerLng) {
      this.gs_latitude = centerLat.toFixed(5);
      this.gs_longitude = centerLng.toFixed(5);
      this.gs_height = Math.abs(maxLat - minLat).toFixed(5);
      this.gs_width = Math.abs(maxLon - minLon).toFixed(5);
    }

  },
}
</script>

<style scoped>

.input-group {
  width: 100%;
}

strong {
  color: #343a40;
}

.miscOptions {
  float: left;
  width: 50%;
}

.outputLayers {
  /*color: #343a40;*/
  margin-left: 55%;
  font-size: 14px;
  width: 40%;
  border: 2px solid #416c41;
  box-sizing: border-box;
  border-radius: 0px;
  background-color: #bad7ff;
  text-align: left;
  margin-right: auto;
  padding: 5px;
  position: absolute;
}

</style>
