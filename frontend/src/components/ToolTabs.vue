<template>
  <b-collapse id="navbar-toggle-collapse" is-nav class="w-100 overflow-auto" style="max-width: 150px;" visible>
    <div class="w-100 overflow-auto">
      <ul class="w-100">
        <li v-for="(menu, menuIndex) in menus" :key="menuIndex">
          <router-link :to="menu.to" v-slot="{href, navigate, isActive, isExactActive}">
            <a :href="href" @click="navigate" :class="{'active': isExactActive}">
              {{ menu.label }}
            </a>
          </router-link>
        </li>
      </ul>
    </div>
  </b-collapse>
</template>

<script>
import 'vue-router'
import {bus} from '../main'
import L from 'leaflet'
import {mapFields} from 'vuex-map-fields';

export default {
  name: "ToolTabs",
  components: {},

  data() {
    return {
      tabIndex: 0,
      navbar: true,
      toolbar: true,
      toggleButton: null,

      menus: [
        {to: "maptools", label: "Map tools"},
        {to: "uavsar", label: "UAVSAR"},
        {to: "gnss", label: "GNSS"},
        {to: "seismicity", label: "Seismicity"},
        {to: "momentmagnitude", label: "Magnitude"},
        {to: "disloc", label: "Disloc"},
        {to: "specialstudies", label: "Studies"},
        {to: "3dimaging", label: "3D imaging"},
        {to: "ckfusion", label: "CK Fusion"},
        {to: "report", label: "Report"},
        {to: "help", label: "Help"}
      ]
    }
  },

  created() {
    this.directUrl(this.tabUrl);
  },
  mounted() {
    bus.$on('ToggleNav', () =>
        this.navbar = true);

  },
  watch: {
    tabIndex: function (val) {
      bus.$emit('ToPage', val);
      bus.$emit('OpenBar');
    },
    tabUrl: function (val) {
      this.directUrl(val);
    }
  },
  computed: {
    tabUrl: function () {
      return this.$route.fullPath;
    },
    ...mapFields(['map.globalMap', 'map.layers'])
  },
  methods: {

    addToggle() {
      let vm = this;
      if (!vm.toolbar && !vm.navbar) {
        if (vm.toggleButton == null) {
          vm.toggleButton = L.control({position: 'topleft'});
          vm.toggleButton.onAdd = function () {

            var btn = L.DomUtil.create('button', 'toggle');
            btn.id = "toggleButton";
            btn.setAttribute("style", "text-align: center;  padding: 10px; border-radius: 5px; background: #FFFFFF;");
            btn.innerHTML = '<i class="fa-lg fas fa-bars" style="color: #2F7CF6;"></i>';
            btn.addEventListener("click",
                function () {
                  vm.globalMap.removeControl(vm.toggleButton);

                  vm.toggleButton = null;
                  vm.navbar = true;
                },
                false);
            return btn;

          }
          this.toggleButton.addTo(this.globalMap);
        }
      }
    },
    removeToggle() {
      this.navbar = true;
      bus.$emit("ToggleNav");
    },
    closeNav() {
      this.navbar = false;
      this.addToggle();
    },


    closeBar() {
      bus.$emit('CloseBar');
      this.toolbar = false;
      this.addToggle();
    },
    openBar() {
      bus.$emit('OpenBar');
      this.toolbar = true;
    },
    directUrl(page) {
      var index = null;
      this.toolbar = true;
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
          //case "/nowcast":
          //    index = 4;
          //    break;
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
        case "/ckfusion":
          index = 8;
          break;
        case "/report":
          index = 9;
          break;
        case "/help":
          index = 10;
          break;
      }
      if (this.tabIndex != index) {
        this.tabIndex = index;
      }
    },
  }
}
</script>

<style scoped lang="scss">
// Bootstrap and its default variables
@import '~bootstrap/scss/bootstrap';
// BootstrapVue and its default variables
@import '~bootstrap-vue/src/index.scss';

ul {
  list-style: none;
  padding: 0px;
}

ul li a {
  text-align: left;
  letter-spacing: 0px;
  color: $secondary;
  background-color: $white;
  padding: 10px 15px;
  border-left: 4px solid $white;
  border-right: 2px solid lighten($secondary, 48%);
  font-size: 1rem;
  font-weight: 500;
  display: block;
}

ul li a:hover {
  color: $primary;
}

ul li a.active {
  color: $primary;
  background-color: $light;
  border-left: 4px solid $primary;
  border-right: 2px solid $light;
}


//#sidebar {
//  overflow-y: scroll;
//  float: left;
//  background-color: #FFFFFF;
//  -webkit-transition: none;
//  transition: none;
//}
//
//.nav {
//  background-color: #FFFFFF;
//}
//
//#tabs {
//  min-height: 100vh;
//  background-color: #FFFFFF;
//
//}
//
//.tab-text {
//  width: auto;
//  position: relative;
//  align-content: center;
//  height: 100%;
//  overflow: auto;
//
//}
//
//
//h3 {
//  font-size: 20px !important;
//}
//
//.nav-pills .nav-link.active {
//  background-color: #343a40;
//
//}
//
//.nav-link.tab {
//  color: #343a40;
//}
//
//label {
//  color: #343a40;
//}
//
//p {
//  color: #343a40;
//}
//
//.bar-toggle {
//  pointer-events: auto;
//  color: #2F7CF6;
//  background: transparent;
//  border: none;
//  height: 80vh;
//}
//
//.nav-toggle {
//  color: #2F7CF6;
//  background: #FFFFFF;
//}
//
//.icon-btn {
//  background: transparent;
//  border: none;
//  color: #2F7CF6
//}
//
//button:active {
//  outline: none;
//  border: none;
//  box-shadow: none;
//}
//
//button:focus {
//  outline: none;
//  border: none;
//  box-shadow: none !important;
//}

</style>
