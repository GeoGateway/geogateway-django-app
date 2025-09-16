<template>
  <div class="w-100 p-2 bg-light text-left">
    <q-banner class="bg-info text-white q-mb-md">
      <q-btn flat @click="gnssInfo=true" color="white">
        <q-icon name="info" class="q-mr-sm"/>
        About GNSS data Analysis
      </q-btn>
    </q-banner>

    <span class="inputLabel">Outputs <hr class="sectionLine"/></span>
    <br>
    <q-card class="q-mb-md">
      <q-card-section>
        <div v-if="gnssLayers.length!==0 && !activeGnssQuery">
          <strong>Output</strong>
          <div v-for="layer in gnssLayers" :key="layer.name">
            <q-card v-if="layer.type !== 'table.txt'" class="q-mt-sm">
              <q-card-section>
                <q-checkbox :model-value="layer.active" @update:model-value="val => { layer.active = val; showHideLayers(val, layer); }">
                  <span class="checkbox-label"> <a :href="layer.url">{{ layer.pre }} {{ layer.type }}</a> </span>
                </q-checkbox>
              </q-card-section>
            </q-card>
            <div v-else><a style="color:#EB9040;" target="_blank" :href="layer.url">{{ layer.name }}</a></div>
          </div>
        </div>
        <div v-else><span style="color:#95ABB1;">No models applied!</span></div>
      </q-card-section>
    </q-card>


    <span class="inputLabel">Functions <hr class="sectionLine"/></span>
    <br>

    <span class="inputLabel">GNSS data models</span>
    <br>

    <q-select
      v-model="kmltype_sel"
      :options="[
        { label: 'Velocities', value: 'getvelocities' },
        { label: 'Coseismic', value: 'getcoseismic' },
        { label: 'Postseismic', value: 'getpostseismic' },
        { label: 'Displacement', value: 'getdisplacement' },
        { label: 'Model', value: 'getmodel' }
      ]"
      option-value="value"
      option-label="label"
      emit-value
      map-options
      outlined
      label="Select a GNSS data model"
      class="q-mb-md"
    />

    <div v-if="kmltype_sel!=null">
      <q-btn style="margin-top: 10px; margin-bottom: 10px;" v-if="!geometryActive" id="sp_windowpicker"
                class="btn_blue" color="primary" @click="gnssDrawRect()">
        Draw an area on the map
      </q-btn>
      <q-btn v-if="gnssLayers.length>0 || areaLayer!=null" class="btn_white" color="secondary" @click="clearGnss()">
        Clear Layers
      </q-btn>
      <br/>

      <div v-if="geometryActive">
        <br/>
        <q-btn class="btn_white" color="secondary" @click="drawListenerOff">
          Unselect 'Draw an Area'
        </q-btn>
        <br/>
      </div>
      <br>
      <span class="inputLabel">Center Latitude</span>
      <q-input
        v-model="gs_latitude"
        name="gs_latitude"
        outlined
        class="q-mb-sm"
      />

      <span class="inputLabel">Center Longitude</span>
      <q-input
        v-model="gs_longitude"
        name="gs_longitude"
        outlined
        class="q-mb-sm"
      />

      <span class="inputLabel">Longitude Span</span>
      <q-input
        v-model="gs_width"
        name="gs_width"
        placeholder="1 degree"
        outlined
        class="q-mb-sm"
      />

      <span class="inputLabel">Latitude Span</span>
      <q-input
        v-model="gs_height"
        placeholder="1 degree"
        name="gs_height"
        outlined
        class="q-mb-sm"
      />

      <span v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'"
            class="inputLabel">Epoch</span>
      <div id="epoch_show"
           v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'">
        <q-input
          v-model="gs_epoch"
          placeholder="YYYY-MM-DD"
          name="gs_epoch"
          outlined
          class="q-mb-sm"
        />
      </div>

      <span v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'"
            class="inputLabel">Epoch 1</span>
      <q-input
        v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'"
        v-model="gs_epoch1"
        placeholder="YYYY-MM-DD"
        name="gs_epoch1"
        outlined
        class="q-mb-sm"
      />

      <span v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'"
            class="inputLabel">Epoch 2 </span>
      <q-input
        v-if="this.kmltype_sel === 'getdisplacement' || this.kmltype_sel === 'getmodel'"
        v-model="gs_epoch2"
        placeholder="YYYY-MM-DD"
        name="gs_epoch2"
        outlined
        class="q-mb-sm"
      />

      <span class="inputLabel">Ref. Site</span>
      <div class="row q-gutter-sm q-mb-sm">
        <q-input
          v-model="gs_refsite"
          placeholder="4-letter code"
          name="gs_refsite"
          outlined
          class="col"
        />
        <q-btn
          color="primary"
          outline
          href="https://sideshow.jpl.nasa.gov/post/tables/table2.html"
          target="_blank"
        >
          Stations
        </q-btn>
      </div>

      <span class="inputLabel">Scale</span>
      <q-input
        v-model="gs_scale"
        placeholder="320 mm/yr/deg"
        name="gs_scale"
        outlined
        class="q-mb-sm"
      />

      <span v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'" class="inputLabel">Coseismic Win.</span>
      <q-input
        v-if="this.kmltype_sel === 'getcoseismic' || this.kmltype_sel === 'getpostseismic'"
        v-model="gs_ctwin"
        name="gs_ctwin"
        placeholder="0.1 years"
        outlined
        class="q-mb-sm"
      />

      <span v-if="this.kmltype_sel === 'getpostseismic' " class="inputLabel">Postseismic Win.</span>
      <q-input
        v-if="this.kmltype_sel === 'getpostseismic'"
        v-model="gs_ptwin"
        name="gs_ptwin"
        placeholder="2 years"
        outlined
        class="q-mb-sm"
      />

      <span v-if="this.kmltype_sel === 'getdisplacement'" class="inputLabel">Av. Win. 1</span>
      <q-input
        v-if="this.kmltype_sel === 'getdisplacement'"
        v-model="gs_dwin1"
        name="gs_dwin1"
        placeholder="10 days"
        outlined
        class="q-mb-sm"
      />

      <span v-if="this.kmltype_sel === 'getdisplacement'" class="inputLabel">Av. Win. 2</span>
      <q-input
        v-if="this.kmltype_sel === 'getdisplacement'"
        v-model="gs_dwin2"
        name="gs_dwin2"
        placeholder="10 days"
        outlined
        class="q-mb-sm"
      />

      <span class="inputLabel">Output Prefix</span>
      <q-input
        v-model="gs_outputprefix"
        name="gs_outputprefix"
        outlined
        class="q-mb-sm"
      />
      <div class="miscOptions">
        <div class="checkbox q-mb-sm" style="text-align: left" v-if="this.kmltype_sel === 'getdisplacement'">
          <q-checkbox
            v-model="gs_analysisCenter"
            name="analysisCenter"
            id="gs_analysisCenter"
            label="Use NGL data"
          />
        </div>

        <div class="checkbox q-mb-sm" style="text-align: left">
          <q-checkbox
            v-model="markerSize"
            name="vabs"
            id="markerSize"
            label="Minimize Marker Size"
          />
        </div>
        <div class="checkbox q-mb-sm" style="text-align: left">
          <q-checkbox
            v-model="gs_vabs"
            name="vabs"
            id="gs_vabs"
            label="Display absolute verticals"
          />
        </div>
        <div class="checkbox q-mb-sm" style="text-align: left">
          <q-checkbox
            v-model="gs_eon"
            name="mon"
            id="gs_eon"
            label="Include error ellipses"
          />
        </div>


        <div class="row">
          <q-btn color="positive" id="gs_submit" name="submit" type="submit"
                  @click.prevent="runButtonClick()">
            Run
          </q-btn>
        </div>
        <br/>
        <div class="row">
          <div style="float: left; text-align: left"><strong>Data source: <br/><a
              href="https://sideshow.jpl.nasa.gov/post/series.html" target="_blank">GNSS Time Series</a></strong>
          </div>
        </div>
      </div>

      <div>
      </div>


      <div v-if="activeGnssQuery" style="overflow: hidden">
        <br/>
        <q-spinner color="positive" size="lg" />
      </div>
      <br/>
    </div>

    <!-- info  popup -->
    <q-dialog
        v-model="gnssInfo">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">GNSS</div>
        </q-card-section>
        <q-card-section>
          <p>
            Global Navigation Satellite System (GNSS) is any satellite
            constellation which provides positioning, navigation, and
            timing (PNT) services on a global or regional basis (Other
            Global Navigation Satellite Systems (GNSS), 2020). One of the
            systems GNSS includes is the United States-owned Global Positioning
            System (GPS).
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
