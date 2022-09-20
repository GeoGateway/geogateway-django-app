<template>
  <div style="max-width: 300px;" class="h-100 d-flex flex-column">
    <div class="text-right bg-light">
      <b-button variant="link" v-b-toggle="`navbar-toolbar-toggle`" class="v-100">
        <b-icon icon="x" class="when-open"></b-icon>
        <b-icon icon="arrow-right-short" class="when-closed"></b-icon>
      </b-button>
    </div>
    <b-collapse ref="toolbarToggle" class="w-100 flex-fill bg-light p-2 overflow-auto" id="navbar-toolbar-toggle" :visible="true">
      <router-view></router-view>
    </b-collapse>

  </div>
</template>

<script>
import {bus} from '../main'
import L from 'leaflet'
import {mapFields} from 'vuex-map-fields';

export default {
  name: "ToolBar",
  data() {
    return {
      toolbar: true,
      toggleButton: null,
      nav: true,
    }
  },
  mounted() {
    bus.$on('ToPage', (page) =>
        this.toPage(page));
    bus.$on('CloseBar', () => {
      if (this.toolbar) {
        this.closeBar();
      }
    });
    bus.$on('OpenBar', () => {
      if (!this.toolbar) {
        this.toolbar = true;
      }
    });
    bus.$on('navClosed', () => {
      this.nav = false;
    });
  },
  computed: {
    ...mapFields(['uavsar.overview', 'map.globalMap', 'map.layers', 'uavsar.overviewLegend'])
  },
  methods: {
    closeBar() {
      this.toolbar = false;
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
      this.$refs.toolbarToggle.show = true;
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