<template>
    <div id="tabs">
        <b-tabs v-model="tabIndex" small pills card>
            <b-tab><template #title> <span style="font-size:14px"><strong>Map Tools</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <b-tab><template #title> <span style="font-size:14px"><strong>UAVSAR</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <b-tab><template #title> <span style="font-size:14px"><strong>GNSS</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <b-tab><template #title> <span style="font-size:14px"><strong>Seismicity</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <!-- <b-tab><template #title> <span style="font-size:14px"><strong>Nowcast</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab> -->
            <b-tab><template #title> <span style="font-size:14px"><strong>Magnitude</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <b-tab><template #title> <span style="font-size:14px"><strong>Disloc</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
<!--            <b-tab title="Saves" disabled><b-card-text><router-view></router-view></b-card-text></b-tab>-->
            <b-tab><template #title> <span style="font-size:14px"><strong>Studies</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <b-tab><template #title> <span style="font-size:14px"><strong>3D Imaging</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <b-tab><template #title> <span style="font-size:14px"><strong>Feedback</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
            <b-tab><template #title> <span style="font-size:14px"><strong>Help</strong></span></template><b-card-text><router-view></router-view></b-card-text></b-tab>
        </b-tabs>
    </div>
</template>

<script>
    import 'vue-router'
    import L from 'leaflet'
    import { mapFields } from 'vuex-map-fields';
    export default {
        name: "ToolTabs",
        components: {
        },
        
        data (){
            return {
                tabIndex: 0,
            }
        },
        
        created() {
            this.directUrl(this.tabUrl);
        },
        watch: {
            tabIndex: function(val){
                this.toPage(val);
            },
            tabUrl: function(val){
                this.directUrl(val);
            }
        },
        computed: {
            tabUrl: function(){
                return this.$route.fullPath;
            },
          ...mapFields(['uavsar.overview', 'map.globalMap', 'map.layers', 'uavsar.overviewLegend'])
        },
        methods: {
            toPage(page){
                var route ='';
                switch (page) {
                    case 0:
                        route = '/maptools';
                        break;
                    case 1:
                        route = '/uavsar';
                        if(!this.overview) {
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
                    // case 4:
                    //     route ='/nowcast';
                    //     break;
                    case 4:
                        route =  '/momentmagnitude';
                        break;
                    case 5:
                        route = '/disloc';
                        break;
                    case 6:
                        route= '/specialstudies';
                        break;
                    case 7:
                        route= '/3dimaging';
                        break;
                    case 8:
                        route = '/report';
                        break;
                    case 9:
                        route = '/help';
                        break;
                }
                if (this.$route.path !== route) {
                    this.$router.push(route)}
            },

          uavsarOverview(){
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
            directUrl(page) {
                var index = null;
                switch (page) {
                    case "/maptools":
                        index = 0;
                        break;
                    case "/uavsar":
                        index = 1;
                        break;
                    case "/gnss":
                        index = 2;
                        break;
                    case "/seismicity":
                        index = 3;
                        break;
                    // case "/nowcast":
                    //     index = 4;
                    //     break;
                    case "/momentmagnitude":
                        index = 4;
                        break;
                    case "/disloc":
                        index = 5;
                        break;
                    case "/specialstudies":
                        index = 6;
                        break;
                    case "/3dimaging":
                        index = 7;
                        break;
                    case "/report":
                        index = 8;
                        break;
                    case "/help":
                        index = 9;
                        break;
                }
                if (this.tabIndex!=index){
                    this.tabIndex = index;
                }
            },
        }
    }
</script>

<style >
    #tabs {
        width: auto;
        background-color: #e6e6ff;

    }
 
    .tab-text {
        width: auto;
        position: relative;
        align-content: center;
        height: 100% ;
        overflow: auto;
    }
 
    h3 {
    font-size: 20px !important;
    }

    .nav-pills .nav-link.active {
        background-color: #343a40;

    }
    .nav-link.tab {
        color: #343a40;
    }

    label {
        color: #343a40 ;
    }
    p {
        color: #343a40;
    }
</style>
