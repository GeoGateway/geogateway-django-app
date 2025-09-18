<template>
  <div class="full-width q-pa-sm bg-grey-2 text-left">
    <q-banner class="bg-info text-white q-mb-md">
      <q-btn 
        flat 
        dense 
        @click="threedInfo=true" 
        icon="info" 
        color="white"
        class="q-mr-sm"
      />
      About 3D Imaging
    </q-banner>

    <div align="left">
      <q-checkbox
        v-model="ridgecrest"
        @update:model-value="loadridgecrest"
        class="text-weight-bold q-mb-sm"
      >
        <span class="text-caption text-weight-bold">Postseismic Products of Ridgecrest Earthquake</span>
      </q-checkbox>
      <div id="ridgecrest_div" v-show="this.ridgecrest">
        <p>High-Resolution Targeted 3D imaging Postseismic Products of the Ridgecrest M6.4 (July 4, 2019) and M7.1 (July
          5, 2019) Earthquake Sequence.
          Collected by Andrea Donnellan and Gregory Lyzenga<a
              href="https://appliedsciences.nasa.gov/our-impact/news/nasa-geogateway-team-uses-drones-map-3d-2019-california-earthquakes-ruptures"
              target=_>&nbsp;more</a>
          <br/>The point clouds (in LAZ format) are released with <a target=_ href="https://doi.org/10.1785/0220190274">research
            article</a>. If using these products, please cite: Donnellan, A., Lyzenga, G., Wang, J., Pierce, Ma.,
          Goulet, C., 2019, High-resolution Targeted 3D Imaging Postseismic Products of the Ridgecrest M6.4 and M7.1
          Earthquake Sequence, DOI: 10.5967/5sq2-rs60. <a target=_ href="http://hdl.handle.net/2022/23341">Full
            record</a>
        </p>
        <div class="q-pl-md">
          <q-checkbox 
            :model-value="ridgecrest_checkbox.includes('0')" 
            @update:model-value="updateridgecrest('0')"
            class="q-mb-sm"
          >
            <span class="q-ml-sm">
              <a target="_blank" download href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_2019_M6.4.kml">
                Inferred Rupture Traces M6.4
              </a>
            </span>
          </q-checkbox>
          <q-checkbox 
            :model-value="ridgecrest_checkbox.includes('1')" 
            @update:model-value="updateridgecrest('1')"
            class="q-mb-sm"
          >
            <span class="q-ml-sm">
              <a target="_blank" download href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_RC20190709_orthomosaic_preview.kml">
                Overview of orthomosaic image M6.4
              </a>
            </span>
          </q-checkbox>
          <q-checkbox 
            :model-value="ridgecrest_checkbox.includes('2')" 
            @update:model-value="updateridgecrest('2')"
            class="q-mb-sm"
          >
            <span class="q-ml-sm">
              <a target="_blank" download href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_2019_M7.1.kml">
                Inferred Rupture Traces M7.1
              </a>
            </span>
          </q-checkbox>
          <q-checkbox 
            :model-value="ridgecrest_checkbox.includes('3')" 
            @update:model-value="updateridgecrest('3')"
            class="q-mb-sm"
          >
            <span class="q-ml-sm">
              <a target="_blank" download href="https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_SV20190715_orthomosaic_preview.kml">
                Overview of orthomosaic image M7.1
              </a>
            </span>
          </q-checkbox>
        </div>
        <br>
        <center><strong>M 6.4 products</strong></center>
        <table class="uavsar-table">
          <tbody>
          <tr class="uavar-tr">
            <td>2019/07/09</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190709C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190709/RC20190709_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190709C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!--
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190709/RC20190709_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190709C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/07/11</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190711C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190711/RC20190711_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190711C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!--
              <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190711_dsm.tif">GeoTiff</a></td> -->

            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190711C_report.pdf"
                   target=_>Report</a></td>
          </tr>
          <tr class="uavar-tr">
            <td>2019/07/15</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190715C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190715/RC20190715_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190715C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190715/RC20190715_dsm.tif">GeoTiff</a></td> -->

            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190715C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/07/22</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190722C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190722/RC20190722_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190722C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190722/RC20190722_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190722C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/08/08</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190808C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190722/RC20190722_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190808C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190722/RC20190722_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190808C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/09/27</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190927C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190722/RC20190722_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190927C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M64_20190722/RC20190722_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/RC20190927C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td colspan=2><a target=_
                             href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/KMLOverview/M64_products_overview.kmz">Products
              overview (kmz)</a></td>
            <td colspan=2><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/pointcloudviewer/RC20190709.html"><strong>View
              Point Clouds</strong></a></td>
          </tr>
          </tbody>
        </table>

        <br>
        <center><strong>M 7.1 products</strong></center>
        <table class="uavsar-table">
          <tbody>
          <tr class="uavar-tr">
            <td>2019/07/09</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SVRL20190709C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190709/SVRL20190709_transparent_mosaic_group1.tif">GeoTiff</a></td>-->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SVRL20190709C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190709/SVRL20190709_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SVRL20190709C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/07/11</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190711C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190711/SV20190711_transparent_mosaic_group1.tif">GeoTiff</a></td>-->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190711C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!-- <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190711/SV20190711_dsm.tif">GeoTiff</a></td>-->

            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190711C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/07/15</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190715C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190715C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190715C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/07/22</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190722C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190722C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190722C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/08/08</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190808C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190808C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190808C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td>2019/09/27</td>
            <td><a target=_
                   href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190927C_group1_densified_point_cloud.laz">Point
              Cloud</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_transparent_mosaic_group1.tif">GeoTiff</a></td> -->
            <td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190927C_dsm_2cm.laz">2cm
              DSM</a></td>
            <!--<td><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/M71_20190715/SV20190715_dsm.tif">GeoTiff</a></td> -->
            <td><a href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/data/SV20190927C_report.pdf"
                   target=_>Report</a></td>
          </tr>

          <tr class="uavar-tr">
            <td colspan=2><a target=_
                             href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/KMLOverview/M71_products_overview.kmz">Products
              overview (kmz)</a></td>
            <td colspan=2><a target=_ href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/pointcloudviewer/SV20190711.html"><strong>View
              Point Clouds</strong></a></td>
          </tr>
          </tbody>
        </table>
        <a target="_blank" href="https://data.geo-gateway.org/3dimaging/Ridgecrest_2019/animation/M7.1RAB4v2.gif"><strong>View
          Animated Gif</strong></a> <br>

      </div>

    </div>

    <!-- info  popup -->
    <q-dialog v-model="threedInfo">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">3D Imaging</div>
        </q-card-section>
        
        <q-card-section class="q-pt-none">
          <p class="my-4">
            Users can locate postseismic products of the Ridgecrest Earthquake
            (M6.4 (July 4, 2019) and M7.1 (July 5, 2019)) by navigating to the "3D
            Imaging" tab and clicking on the box labeled "Postseismic Products of
            Ridgecrest Earthquake." The data was collected by Andrea Donnellan and
            Gregory Lyzenga.
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
import {bus} from '../main'
import {mapFields} from '../utils/mapFields';
import axios from "axios";

axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  name: "ThreeDImaging",
  data: function () {
    return {
      threedInfo: false,
      ridgecrest: false,
      ridgecrest_checkbox: [],
      ridgecresturls: ["https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_2019_M6.4.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_RC20190709_orthomosaic_preview.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_2019_M7.1.kml",
        "https://raw.githubusercontent.com/GeoGateway/GeoGatewayStaticResources/master/kmz/Ridgecrest_SV20190715_orthomosaic_preview.kml"],
    }
  },
  computed: {
    ...mapFields([
      'map.globalMap',
    ])
  },
  methods: {

    loadridgecrest() {
      if (this.ridgecrest) {
        this.globalMap.setView([35.64378, -117.51143], 14);
      } else {
        var i = this.ridgecrest_checkbox.length;
        while (i--) {
          var code = this.ridgecrest_checkbox[i];
          this.ridgecrest_checkbox.splice(i, 1);
          this.updateridgecrest(code);
        }
      }
    },

    // update ridgecrest
    updateridgecrest(val) {
      var vp = parseInt(val);
      var rlayerName = 'ridge' + val + "L";
      if (this.ridgecrest_checkbox.includes(val)) {
        bus.emit('UrlAddLayer', this.ridgecresturls[vp], rlayerName);
      } else bus.emit('RemoveLayer', rlayerName);
    },

  }
}
</script>

<style scoped>
label {
  padding: 5px;
}

p {
  font-size: 15px;
}

table {
  border-collapse: collapse;
  border: 1px solid black;
  width: 100%;
}

td {
  padding-top: 0px;
  padding-bottom: 0px;
  height: 0px
}
</style>
