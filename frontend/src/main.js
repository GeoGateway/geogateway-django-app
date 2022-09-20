import Vue from 'vue';
import App from './App.vue';
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue';
import MapTools from "./components/MapTools";
import GNSS from './components/GNSS'
import MMCalc from "./components/MMCalc";
//import Nowcast from "./components/Nowcast";
import Seismicity from "./components/Seismicity";
import Saves  from "./components/Saves";
import UAVSAR from "./components/UAVSAR";
import report from "./components/report";
import help from "./components/help";
import Disloc from "./components/Disloc";
import SpecialStudies from "./components/SpecialStudies";
import ThreeDImaging from "./components/ThreeDImaging";
import CKFusion from "./components/CKFusion";
import VueRouter from 'vue-router';
import 'leaflet/dist/leaflet.css';
import "leaflet-kml";
import {store} from "./store/store";
import resize from "vue-element-resize-detector";
import LandinigPage from "./components/LandingPage";
import MyMap from "./components/MyMap";

Vue.use(VueRouter);
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(resize);
Vue.config.silent = true

export const bus = new Vue();

Vue.config.productionTip = false;
Vue.config.devtools = true;

import 'leaflet/dist/leaflet.css';
import VueResource from 'vue-resource';



const routes = [
  {name: 'home', path:'/', components: {mainPage: LandinigPage}},
  {name: 'map', path:'/map', components: {mainPage: MyMap},
  children: [
  {name: 'maptools', path: '/maptools', component: MapTools },
  {name: 'gnss', path: '/gnss', component: GNSS },
  {name: 'momentmagnitude', path: '/momentmagnitude', component: MMCalc },
  //{name: 'nowcast', path: '/nowcast', component: Nowcast },
  {name: 'seismicity', path: '/seismicity', component: Seismicity },
  {name: 'disloc', path: '/disloc', component: Disloc },
  {name: 'mapsaves', path: '/mapsaves', component: Saves },
  {name: 'uavsar', path: '/uavsar', component: UAVSAR },
  {name: 'specialstudies', path: '/specialstudies', component: SpecialStudies },
  {name: '3dimaging', path: '/3dimaging', component: ThreeDImaging },
  {name: 'ckfusion', path: '/ckfusion', component: CKFusion },
  {name: 'report', path: '/report', component: report },
  {name: 'help', path: '/help', component: help },
  ]}
]


const router = new VueRouter({
  routes,
})
Vue.use(VueResource);
// Vue.prototype.$http = axios;
Vue.http.options.emulateJSON = true;





// initialize router

new Vue({
  router,
  store: store,
  render: h => h(App),
}).$mount('#app');
