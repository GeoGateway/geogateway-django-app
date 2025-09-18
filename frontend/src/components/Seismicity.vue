<template>
  <div class="full-width q-pa-sm bg-grey-2 text-left">
    <q-banner class="bg-info text-white q-mb-md">
      <q-btn 
        flat 
        dense 
        @click="seismInfo=true" 
        icon="info" 
        color="white"
        class="q-mr-sm"
      />
      About Seismicity
    </q-banner>

    Recent Earthquakes from USGS

    <div id="panel_forecast" style="margin-top: 10px; margin-bottom:10px;">

      <span class="inputLabel">Recent Earthquakes from USGS</span>
      <hr>
      <q-option-group
        v-model="selected"
        @update:model-value="showSelected"
        :options="[
          {label: 'M > 1.0, Last Day', value: 'day'},
          {label: 'M > 2.5, Last Week', value: 'week'},
          {label: 'M > 4.5, Last Month', value: 'month'}
        ]"
        type="radio"
      />

      <!--        is this necessary? -->
      <!--        <input-->
      <!--                type="checkbox"-->
      <!--                v-model="showhide"-->
      <!--                @change="showSelected()"-->
      <!--                id="showhide"-->
      <!--        ><label for="showhide"> Show/Hide Selected Earthquakes</label>-->
      <!--        <br/>-->
      <br/>
      <!--
      <h5>Filter By Magnitude</h5>
      <select class="form-control" v-model="mFilter" id="mFilters" >
        <option value="0" selected>No Filter</option>
        <option value='5'>M > 5</option>
        <option value='6.5'> M > 6.5</option>
      </select>
      <br/>
      <h5>Filter By Depth</h5>
      <select class="form-control" v-model="dFilter" id="dFilters">
        <option value="0">No Filter</option>
        <option value='30'>Depth &#8804; 30km </option>
      </select>
      <hr/> -->


      <span class="inputLabel">Search Earthquake Catalog</span>
      <hr>
      <q-btn 
        id="sp_windowpicker" 
        color="primary" 
        @click="seisDrawRect()"
        class="q-mb-sm q-mr-sm"
      >
        Draw an area on the map
      </q-btn>
      <q-btn
        v-if="areaLayer!=null || 
              selected!=null || 
              geoUri !== '' || 
              kmlUri !== ''"
        color="white" 
        text-color="black"
        id="clearUsgs" 
        @click="clearUsgs()"
        class="q-mb-sm"
      >
        Clear USGS Layers
      </q-btn>
      <br/><br/>

      <q-input
        v-model="minLat"
        label="Min Lat"
        placeholder="32.0"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="minLon"
        label="Min Lon"
        placeholder="-130.0"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="maxLat"
        label="Max Lat"
        placeholder="1 degree"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="maxLon"
        label="Max Lon"
        placeholder="1 degree"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="startDate"
        label="Start Date"
        type="date"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="startTime"
        label="Starting Time"
        placeholder="HH:MM:SS"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="endDate"
        label="Ending Date"
        type="date"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="endTime"
        label="Ending Time"
        placeholder="HH:MM:SS"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="minMag"
        label="Minimum Magnitude"
        placeholder="e.g. 4.0"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="maxMag"
        label="Maximum Magnitude"
        placeholder="e.g. 8.0"
        outlined
        class="q-mb-md"
      />

      <q-input
        v-model="iconScale"
        label="Icon Display Scale"
        placeholder="1"
        outlined
        class="q-mb-md"
      />
      <br/>
      <q-btn 
        color="positive" 
        id="gs_submit" 
        @click="runSeismicity()"
        class="q-mb-md"
      >
        Search
      </q-btn>
      <br/>
      <br/>
      <div class="toolInfo" v-if="geoUri !== '' || kmlUri !== ''">
        <a :href="kmlUri">Download USGS KML</a>
        <br/>
        <a target="_blank" :href="geoUri">Download USGS GeoJSON</a>
      </div>
    </div>

    <!-- info  popup -->
    <q-dialog v-model="seismInfo">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Seismicity</div>
        </q-card-section>
        
        <q-card-section class="q-pt-none">
          <p class="my-4">
            The seismicity tab allows users to display earthquakes in a region over a specified
            period. The tab is split into two sections, "Recent Earthquakes from USGS" and
            "Search Earthquake Catalog."
          </p>
          <p>
            The tab allows users to view recent earthquakes from USGS data. The USGS data
            can also be found on the USGS website
            <strong><a href="https://earthquake.usgs.gov/earthquakes/map/"
                       target="_blank">earthquake.usgs.gov/earthquakes/map/</a></strong>
            . The displayed earthquake events are color coded with the hotter
            colors representing recent events and the cooler colors representing less recent
            events.
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
import axios from "axios";
import {bus} from '../main'
import 'leaflet-ajax';
import {mapFields} from '../utils/mapFields';
import L from "leaflet";

export default {
  name: "seismicity",
  data() {
    return {
      seismInfo: false,
      rectDraw: null,
      areaLayer: null,
    }
  },
  computed: {
    ...mapFields([
      'seismicity.day',
      'seismicity.week',
      'seismicity.month',
      'seismicity.mFilter',
      'seismicity.dFilter',
      'seismicity.minLat',
      'seismicity.minLon',
      'seismicity.maxLat',
      'seismicity.maxLon',
      'seismicity.startDate',
      'seismicity.startTime',
      'seismicity.endDate',
      'seismicity.endTime',
      'seismicity.minMag',
      'seismicity.maxMag',
      'seismicity.iconScale',
      'seismicity.selected',
      'seismicity.kmlUri',
      'seismicity.geoUri',
      'map.globalMap',
      'map.drawControl'
    ])
  },
  methods: {
    clearUsgs() {
      this.geoUri = '';
      this.kmlUri = '';
      bus.emit('ClearUsgs', 'usgs_layer');
      let vm = this;
      if (vm.areaLayer != null) {
        vm.globalMap.removeLayer(vm.areaLayer);
        vm.areaLayer = null;
      }
      this.selected = null;
      this.minLat = null;
      this.minLon = null;
      this.maxLat = null;
      this.maxLon = null;
    },
    showSelected(time) {
      var dFilter = this.dFilter;
      var mFilter = this.mFilter;
      var startD;
      var endD = new Date();
      var timeUrl;
      switch (time) {
        case 'day':
          timeUrl = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson'
          startD = new Date();
          startD.setDate(startD.getDate() - 1);
          break;
        case 'week':
          timeUrl = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson'
          startD = new Date();
          startD.setDate(startD.getDate() - 7);
          break;
        case 'month':
          timeUrl = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson'
          startD = new Date();
          //rough estimate of month ago
          startD.setDate(startD.getDate() - 30);
          break;
      }
      axios.get('/geogateway_django_app/seismicity', {
        params: {
          "fullUri": timeUrl,
        }
      }).then(function (response) {
        bus.emit('filterCat', response.data, dFilter, mFilter, 1, startD, endD)
      })
    },
    runSeismicity() {
      let vm = this;
      var iconScale = this.iconScale;
      var startD = new Date(this.startDate);
      var endD = new Date(this.endDate);
      var urlBase = "https://earthquake.usgs.gov/fdsnws/event/1/query?";
      var fullUri = urlBase + "format=geojson" + '&' +
          "starttime=" + this.startDate + 'T' + this.startTime + '&' +
          "endtime=" + this.endDate + 'T' + this.endTime + '&' +
          "minmagnitude=" + this.minMag + '&' +
          "minlatitude=" + this.minLat + '&' +
          "maxlatitude=" + this.maxLat + '&' +
          "minlongitude=" + this.minLon + '&' +
          "maxlongitude=" + this.maxLon;
      if (vm.areaLayer != null) {
        vm.globalMap.removeLayer(vm.areaLayer);
        vm.areaLayer = null;
      }
      this.kmlUri = fullUri.replace('geojson', 'kml');
      this.geoUri = fullUri;
      axios.get('/geogateway_django_app/seismicity', {
        params: {
          "fullUri": fullUri,
        }
      }).then(function (response) {
        bus.emit('filterCat', response.data, '', '', iconScale, startD, endD)
      })
    },
    seisDrawRect() {
      let vm = this;
      vm.rectDraw = new L.Draw.Rectangle(vm.globalMap, vm.drawControl.options.rectangle);
      vm.rectDraw.enable();
      vm.globalMap.on('draw:created', function (e) {
        var type = e.layerType;
        if (type === 'rectangle') {
          if (vm.areaLayer != null) {
            vm.globalMap.removeLayer(vm.areaLayer);
          }
          var layer = e.layer;
          vm.globalMap.addLayer(layer);
          vm.centerLat = layer.getCenter().lat;
          vm.centerLng = layer.getCenter().lng;
          vm.maxLat = layer.getLatLngs()[0][1].lat.toFixed(5);
          vm.maxLon = layer.getLatLngs()[0][2].lng.toFixed(5);
          vm.minLat = layer.getLatLngs()[0][3].lat.toFixed(5);
          vm.minLon = layer.getLatLngs()[0][0].lng.toFixed(5);
          vm.areaLayer = layer;
          vm.rectDraw = null;
          // vm.geometryActive = false;
        }
      });
    },
    // eslint-disable-next-line no-unused-vars
    setRect(maxLat, minLon, minLat, maxLon, centerLat, centerLng) {
      bus.emit('drawListenerOff')
      this.maxLat = maxLat;
      this.minLon = minLon;
      this.minLat = minLat;
      this.maxLon = maxLon;
    }
  }
}
</script>

<style scoped>
i {
  color: #2e6da4;
}

label {
  font-weight: bold;
}

/*#buttonText {*/
/*    color: white;*/
/*}*/
img {
  width: 80%;
  background-color: white;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  border-radius: 25px;
  height: 50px;
}
</style>