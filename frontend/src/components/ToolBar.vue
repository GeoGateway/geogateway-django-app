<template>
  <div style="max-width: 300px; height: 100vh;" class="flex column">
    <div class="text-right bg-light">
      <q-btn 
        flat 
        round 
        @click="toolbarVisible = !toolbarVisible" 
        class="v-100"
        :icon="toolbarVisible ? 'close' : 'keyboard_arrow_right'"
        color="primary"
      />
    </div>
    <q-slide-transition>
      <div v-show="toolbarVisible" ref="toolbarToggle" class="full-width col bg-grey-2 q-pa-sm" style="overflow-y: auto; max-height: calc(100vh - 50px); padding-bottom: 100px;">
        <router-view></router-view>
      </div>
    </q-slide-transition>

  </div>
</template>

<script>
import {bus} from '../main'
import L from 'leaflet'
import {mapFields} from '../utils/mapFields';

export default {
  name: "ToolBar",
  data() {
    return {
      toolbarVisible: true,
      toggleButton: null,
      nav: true,
    }
  },
  mounted() {
    bus.on('ToPage', (page) =>
        this.toPage(page));
    bus.on('CloseBar', () => {
      if (this.toolbarVisible) {
        this.closeBar();
      }
    });
    bus.on('OpenBar', () => {
      if (!this.toolbarVisible) {
        this.toolbarVisible = true;
      }
    });
    bus.on('navClosed', () => {
      this.nav = false;
    });
  },
  beforeUnmount() {
    bus.off('ToPage');
    bus.off('CloseBar');
    bus.off('OpenBar');
    bus.off('navClosed');
  },
  computed: {
    ...mapFields(['uavsar.overview', 'map.globalMap', 'map.layers', 'uavsar.overviewLegend'])
  },
  methods: {
    closeBar() {
      this.toolbarVisible = false;
    },
    toPage(page) {
      var route = '';
      switch (page) {
        case 0:
          route = '/maptools';
          break;
        case 1:
          route = '/uavsar';
          if (!this.overview) {
            this.overview = true;
            this.uavsarOverview();
          }
          break;
        case 2:
          route = '/gnss';
          break;
        case 3:
          route = '/seismicity';
          break;
          //case 4:
          //    route ='/nowcast';
          //    break;
        case 4:
          route = '/momentmagnitude';
          break;
        case 5:
          route = '/disloc';
          break;
        case 6:
          route = '/specialstudies';
          break;
        case 7:
          route = '/3dimaging';
          break;
        case 8:
          route = '/ckfusion';
          break;
        case 9:
          route = '/report';
          break;
        case 10:
          route = '/help';
          break;
      }
      if (this.$route.path !== route) {
        this.$router.push(route)
      }
    },
    uavsarOverview() {
      this.layers['uavsarWMS'] = L.tileLayer.wms('https://data.geo-gateway.org/geoserver00/InSAR/wms?', {
            layers: 'InSAR:thumbnailmosaic',
            transparent: true,
            format: 'image/png',
            zIndex: 2
          }
      );
      this.overviewLegend = L.control({position: 'bottomleft'});
      this.overviewLegend.onAdd = function () {
        var div = L.DomUtil.create('div', 'overviewLegend');
        div.innerHTML = '<img src=' + 'https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/uavsarlegend.png' + '>';
        return div;
      };
      this.overviewLegend.addTo(this.globalMap);

      this.globalMap.addLayer(this.layers['uavsarWMS'])
      this.layers['uavsarWMS'].setOpacity(.7);
    },
  },
  watch: {
    $route() {
      // Ensure toolbar is visible when route changes
      this.toolbarVisible = true;
    }
  }
}
</script>

<style scoped>

/*#sidebar-1 {*/
/*  height: 100%;*/
/*  !*width: 27%;*!*/
/*  width: fit-content;*/
/*  overflow-y: scroll;*/
/*  float: left;*/
/*  background: none;*/
/*  -webkit-transition: none;*/
/*  transition: none;*/
/*}*/

/*#toolbar {*/
/*  padding: 10px;*/
/*}*/

/*.nav-toggle {*/
/*  pointer-events: auto;*/
/*  color: #2F7CF6;*/
/*  background: #FFFFFF;*/
/*}*/

/*#toolbarContent {*/
/*  margin-top: 3%;*/
/*}*/

/*.togbutton {*/
/*  background-color: #862e9c;*/
/*  color: #efefef;*/
/*  border: none;*/
/*  text-align: center;*/
/*  padding: 10px 20px;*/
/*  border-radius: 5px;*/
/*}*/


</style>