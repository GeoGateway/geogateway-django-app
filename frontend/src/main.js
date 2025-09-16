import { createApp, configureCompat } from 'vue';
import { Quasar, QBtn, QIcon, QTable, QTd, QTh, QTr, QCard, QCardSection, QCardActions, QBanner, QCheckbox, QDialog, QOptionGroup, QSlideTransition, QDrawer, QList, QItem, QItemSection, QToolbar, QToolbarTitle, QSpace, QInput, QFile, QSpinner, QSelect, QDate, QSlider, QLayout, QPage, QPageContainer, QHeader } from 'quasar';
import quasarLang from 'quasar/lang/en-US';
import quasarIconSet from 'quasar/icon-set/material-icons';
import '@quasar/extras/material-icons/material-icons.css';
import 'quasar/dist/quasar.css';
import App from './App.vue';
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
import { createRouter, createWebHistory } from 'vue-router';
import 'leaflet/dist/leaflet.css';
import "leaflet-kml";
import {store} from "./store/store";
import mitt from 'mitt';
import { vResize } from './directives/resize';
import LandinigPage from "./components/LandingPage";
import MyMap from "./components/MyMap";

// Create event bus for component communication
export const bus = mitt();

import 'leaflet/dist/leaflet.css';



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


const router = createRouter({
  history: createWebHistory(),
  routes,
});





// Configure Vue 3 behavior to fix Quasar compatibility
configureCompat({
  COMPONENT_V_MODEL: false,
  INSTANCE_ATTRS_CLASS_STYLE: false,
  WATCH_ARRAY: false
});

// Create and mount Vue app
const app = createApp(App);

app.use(router);
app.use(store);
app.use(Quasar, {
  lang: quasarLang,
  iconSet: quasarIconSet,
  components: {
    QBtn,
    QIcon, 
    QTable,
    QTd,
    QTh,
    QTr,
    QCard,
    QCardSection,
    QCardActions,
    QBanner,
    QCheckbox,
    QDialog,
    QOptionGroup,
    QSlideTransition,
    QDrawer,
    QList,
    QItem,
    QItemSection,
    QToolbar,
    QToolbarTitle,
    QSpace,
    QInput,
    QFile,
    QSpinner,
    QSelect,
    QDate,
    QSlider,
    QLayout,
    QPage,
    QPageContainer,
    QHeader
  }
});

// Global properties (replacing Vue 2's Vue.prototype)
app.config.globalProperties.$bus = bus;

// Register global directives
app.directive('resize', vResize);

app.mount('#app');
