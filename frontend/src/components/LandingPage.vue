<template>
<div ref="landingPage" class="scrollable">
    
    <div id="homePage" class="full-height" >
            <div class="row" id="header">
                <div class="col"> <img id="logo" src="../assets/logo.png" alt="GeoGateway Logo"> </div>
                <div class="col"> <q-btn flat class="title-btn" @click="scrollTo('features')">Features</q-btn></div>
                <div class="col"> <q-btn flat class="title-btn" @click="scrollTo('userRes')">User Resources</q-btn></div>
                <div class="col"> <q-btn flat class="title-btn" @click="scrollTo('publications')">Publications</q-btn></div>
                <div class="col"> <q-btn flat class="title-btn" @click="scrollTo('contributors')">Contributors</q-btn></div>
                <div class="col"> <q-btn flat class="title-btn" @click="scrollTo('dataAttr')">Data Attribution</q-btn></div>
            </div>
            <span class="align-items-center" id="geogatewayTitle">
                GeoGateway
            </span><br>
            <span class="align-items-center" id="geogatewayDesc">
                A search and analysis gateway to geodetic imaging data for scientific discovery, 
            field use and disaster response
            </span>
            <q-btn class="geogateway-button" @click="goToMap('/maptools')">Go to Map Tools</q-btn>
    </div>

    <div id="features" ref="features">
        <span class="section-head">Features</span>
        <br>
        <span class="section">Tools for Analysis, Modeling and Response </span>
        <div class="section-content">
            <div class="row">
                <div class="col inner-section">
                <q-btn round class="btn-circle" @click="goToMap('/maptools')">
                        <q-icon name="map" />
                    </q-btn><br>
                    <span class="feature-title">Map Tools</span><br>
                    <span class="feature-desc">Map tools are integrated from different sources/references</span>
                </div>
                <div class="col inner-section">

                    <q-btn round class="btn-circle" @click="goToMap('/uavsar')">
                        <q-icon name="map" />
                    </q-btn><br>
                    <span class="feature-title">UAVSAR</span><br>
                    <span class="feature-desc">UAVSAR is an airborne, L-band, fully polarimetric radar, mounted 
                    to the belly of a piloted Gulfstream III aircraft</span>
                </div>
                <div class="col inner-section">
                <q-btn round class="btn-circle" @click="goToMap('/gnss')">
                        <q-icon name="map" />
                    </q-btn><br>
                    <span class="feature-title">GNSS</span><br>
                    <span class="feature-desc">Global Navigation Satellite System (GNSS) is any satellite 
                    constellation which provides positioning</span>
                </div>
            </div>
            <div class="row">
                <div class="col inner-section">
                    <q-btn round class="btn-circle" @click="goToMap('/seismicity')">
                        <q-icon name="map" />
                    </q-btn><br>
                    <span class="feature-title">Seismicity</span><br>
                    <span class="feature-desc">The seismicity tab allows users to display earthquakes in a region over a specified period.</span>
                </div>
                <!--
                <div class="col inner-section">
                <b-button class="btn btn-circle" @click="goToMap('/nowcast')">
                        <i class="fas fa-map"></i>
                    </b-button><br>
                    <span class="feature-title">Nowcast</span><br>
                    <span class="feature-desc">GeoGateway’s Nowcast tab consists of useful tools to evaluate earthquake hazard</span>
                </div>
                -->
                <div class="col inner-section">
                <q-btn round class="btn-circle" @click="goToMap('/momentmagnitude')">
                        <q-icon name="map" />
                    </q-btn><br>
                    <span class="feature-title">Magnitude</span><br>
                    <span class="feature-desc">Magnitude is the physical size of an earthquake. </span>
                </div>
            </div>
            <br><br>
            
        </div>
    </div>

    <div id="userRes" ref="userRes" class="">
        <span class="section-head">User Resources</span><br>
        <span class="section">Learn how to use GeoGateway</span>
        <div class="section-content">
        <div class="row">
            <div class="col">
                <img id="userGuide" src="../assets/userGuide.png" alt="User Guide"> <br>
                <a class="user-res-title" target="_blank" href="https://github.com/GeoGateway/GeoGatewayStaticResources/raw/master/documents/GeoGateway_User_Guide.pdf">User Guide</a><br>
                <span class="user-res-desc">The user guide has detailed information on all our map tools</span>
            </div>
            <div class="col">
                <img id="tutorials" src="../assets/tutorials.png" alt="Tutorials"> <br>
                <a class="user-res-title" target="_blank" href="https://www.youtube.com/channel/UC0_bNEBxRWH2qBULDl6cB7Q/featured"> Tutorials</a><br>
                <span class="user-res-desc">Watch tutorials to understand how to use GeoGateway</span>
            </div>
            <div class="col">
                <img id="exercises" src="../assets/exercises.png" alt="Excersies"> <br>
                <a class="user-res-title" target="_blank" href="https://github.com/GeoGateway/GeoGatewayStaticResources/raw/master/documents/GeoGateway_Exercises.pdf">Exercises</a><br>
                <span class="user-res-desc">Our thoughtfully designed exercises let you master GeoGateway</span>
            </div>
        </div>
        </div>
    </div>

    <div id="publications" ref="publications">
        <div class="row">
            <div class="col">
                <span class="section-head">Publications</span><br>
                <span class="section">See how GeoGateway is being used</span>
            </div>
        </div>
        <div class="section-content">
        <div class="row">
            <div class="col inner-section">
                <span class="pub-title">Earth Science Informatics (2021)</span><br>
                 <a class="pub-link" target="_blank" href="https://doi.org/10.1007/s12145-020-00561-7">Improving access to geodetic imaging crustal deformation data using GeoGateway</a> <br>
                <span class="pub">Donnellan, A., Parker, J., Heflin, M. et al.</span>
                <hr class="pub-hr">
            </div>
            <div class="col inner-section">
                <span class="pub-title">Earth and Space Science (2020)</span><br>
                <a class="pub-link" target="_blank" href="https://doi.org/10.1029/2019EA000644">Automated Estimation and Tools to Extract Positions, Velocities, Breaks...</a><br>
                <span class="pub">Heflin, M., Donnellan, A., Parker, J. et al.</span>
                <hr class="pub-hr">
            </div>
            <div class="col inner-section">
                <span class="pub-title">Earth and Space Science (2021)</span><br>
                 <a class="pub-link" target="_blank" href="https://doi.org/10.1002/essoar.10506047.1">Buried Aseismic Slip and Off‐Fault Deformation on the Southernmost San Andreas...</a><br>
                <span class="pub">Donnellan, A., Parker, J., Heflin, M. et al.</span>
                <hr class="pub-hr">
            </div>
            </div>
        </div>
    </div>

    <div id="contributors" ref="contributors">
        <span class="section-head">Contributors</span><br>
        <span class="section">The team behind GeoGateway</span><br>
        <div class="section-content">
        <Contributors/>
        </div>
    </div>

    <div id="dataAttr" ref="dataAttr" >
        <span class="section-head">Data Data Attribution</span><br>
        <span class="section">We integrate map data from different sources</span> 
    <div class="section-content">
        <div class="row">
            <q-table 
                class="tbl" 
                :data="items.slice(0, perPage)" 
                :columns="columns"
                hide-header
                flat
            >
                <template v-slot:body-cell-source="props">
                  <q-td :props="props">
                     <a :href="props.row.link" target="_blank" rel="noreferrer noopener">{{props.row.text}}</a>
                  </q-td>
                </template>
            </q-table>
        </div><br>
            <q-btn @click="toggleRows()">
                {{rowButtonText()}}
            </q-btn>
        </div>
    </div>
</div>
</template>

<script>
import {bus} from '../main';
import Contributors from "./Contributors";
export default {
  name: "LandingPage",
  components: {
    Contributors,
  },
  data() {
      return {
          perPage: 6,
          columns: [
          {
            name: 'tool',
            label: 'Tool',
            field: 'tool',
            align: 'left'
          },
          {
            name: 'source',
            label: 'Data Source / Reference',
            field: 'source',
            align: 'left'
          }
        ],
        items: [
          { tool: 'UCERF3 faults', text: 'USGS Open-File Report 2013–1165', link: 'https://pubs.usgs.gov/of/2013/1165/'},
          { tool: 'USGS Quarternary faults', text: 'https://doi.org/10.5066/F7S75FJM', link: 'https://doi.org/10.5066/F7S75FJM'},
          { tool: 'Show state boundaries', text: 'Cartographic Boundary shapefiles', link: 'https://www.census.gov/geographies/mapping-files/2010/geo/carto-boundary-file.html'},
          { tool: 'Show coastlines', text: 'Natural Earth Data', link: 'https://www.naturalearthdata.com/'},
          { tool: 'UAVSAR', text: 'Alaska Satellite Facility - ASF, Donnellan et al. 2010', link: 'https://asf.alaska.edu/'},
          { tool: 'GNSS', text: 'GPS.gov, Heflin et al. 2020', link: 'https://www.gps.gov/systems/gnss/'},
          { tool: 'Seismicity', text: ' earthquake.usgs.gov/earthquakes/map/', link: 'https://earthquake.usgs.gov/earthquakes/map/'},
          { tool: 'Nowcast', text: 'Open Hazards Group', link: 'https://www.openhazards.com/'},
          //{ tool: 'Magnitude', text: 'GPS.gov, Heflin et al. 2020', link: 'https://www.gps.gov/systems/gnss/'},
          //{ tool: 'Discloc', text: 'GPS.gov, Heflin et al. 2020', link: 'https://www.gps.gov/systems/gnss/'},
          { tool: '3D Imaging', text: 'Seismological Research Letters', link: 'https://doi.org/10.1785/0220190274'},
          ]
      }
    },
  methods:{
    scrollTo(section){
        var element = this.$refs[section];
        var top = element.offsetTop;
        this.$refs.landingPage.scrollTo(0, top);
    },
    goToMap(feature){
        bus.$emit('switchPage', feature);
    },
    toggleRows(){
        if(this.perPage<this.items.length){
            this.perPage=this.items.legth;
        }else{
            this.perPage=6;
        }
    },
    rowButtonText(){
        if(this.perPage<this.items.length){
            return "See All";
        }else{
            return "See Less";
        }
    }
  },
}

</script>
<style>
#homePage{
    color: #FFFFFF;
    background: url('../assets/AdobeStock_288622149.png') no-repeat center center;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
    padding-left: 0px;
    margin-left:0px;
    background-color: rgba(12, 12, 12, 0.56);
    background-blend-mode: multiply;
}
#header{
    padding-top:25px;
    margin-bottom: 15%
}
#geogatewayTitle{
    font-style: normal;
    font-weight: bold;
    font-size: 60px;
    line-height: 90px;
    text-align: center;
    color: #FFFFFF;
    margin-bottom: 3%;
}
#geogatewayDesc{
    font-style: normal;
    font-weight: normal;
    font-size: 38px;
    line-height: 60px;
    text-align: center;
    color: #FFFFFF;
    display: inline-block;
    padding-left: 20%;
    padding-right: 20%;
    margin-bottom: 10%;
}
#features{
    padding:50px;
    padding-left: 100px;
    padding-right: 100px;
    margin-top:5%;
}
#userRes{
    background: #F9FAFC;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;

    padding-left: 100px;
    padding-right: 100px;
}
#publications a.active{
    color: #007BFE;
    text-decoration:none;
    padding-left: 100px;
    padding-right: 100px;
}
#dataAttr{
    padding-left: 100px;
    padding-right: 100px;
}
#contributors-inner{
    x-overfolw:
}
.title-btn{
    background-color: transparent !important;
    border-color:  transparent !important;
    color: #FFFFFF;
}
.geogateway-button{
    color: #FFFFFF;
    background-color: #007BFE;
    border-color: #007BFE;
    margin-bottom: 3%;
}
.full-height{
    min-height: 100vh;
}
.scrollable{
    height: 100%;
    overflow-y: scroll;
}
.feature-title{
    display: inline-block;
    font-style: normal;
    font-weight: 600;
    font-size: 32px;
    line-height: 44px;
    text-align: center;
    color: #000000;
    margin-top: 20px;
    margin-bottom: 15px;
}
.feature-desc{
    display: inline-block;
    font-style: normal;
    font-weight: normal;
    font-size: 20px;
    line-height: 160%;
    text-align: center;
    color: #000000;
    margin-bottom: 50px;;
}
.btn-circle{
    width: 70px;
    height: 70px;
    padding: 10px 16px;
    border-radius: 35px;
    font-size: 24px;
    line-height: 1.33;
    color: #007bfe;
    background: rgba(0, 123, 254, 0.1);
    border-color:  transparent !important;
}
.user-res-title{
    display: inline-block;
    font-style: normal;
    font-weight: 600;
    font-size: 28px;
    line-height: 120%;
    color: #333333;
    margin-top: 15px;
}
.user-res-desc{
    display: inline-block;
    font-style: normal;
    font-weight: normal;
    font-size: 20px;
    line-height: 160%;
    text-align: center;
    color: #000000;
    margin-bottom: 5%;
}
.pub-title{
    font-style: normal;
    font-weight: normal;
    font-size: 20px;
    line-height: 27px;
    text-transform: uppercase;
    color: #727272;
}
.pub-link{
    font-style: normal;
    font-weight: 600;
    font-size: 26px;
    line-height: 44px;
    color: #007BFE;
}
.pub{
    font-style: normal;
    font-weight: 600;
    font-size: 20px;
    line-height: 27px;
    color: #727272;
}
.pub-hr{
    background: #CFCFCF;
    height: 4px;
}
.section-head{
    font-style: normal;
    font-weight: 600;
    font-size: 24px;
    line-height: 33px;
    text-align: center;
    color: #858585;
    display: inline-block;
    margin-top: 8%;  
}
.section{
    font-style: normal;
    font-weight: 600;
    font-size: 40px;
    line-height: 70px;
    text-align: center;
    color: #202020;
}
.section-content{
    margin-top: 5%;
    margin-bottom: 3%;
}
.inner-section {
    padding-left: 100px;
    padding-right: 100px;
}
.tbl{
    width: 75%;
    margin: auto;
}
thead{
    background: #007BFE;
    border-radius: 5px;
    color: #ffffff;
}
::-webkit-scrollbar {
    width: 0;
    background: transparent;
}
</style>
