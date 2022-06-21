<template>
  <div class="w-100 p-2 bg-light text-left">

    <h3>User Resources</h3>
    <!--
    <a href="https://archive.geo-gateway.org:3000/main.html" target="_blank"> <i>Visit the archived Geo-Gateway</i></a>
   -->
    <div class="tool-content">
      <a target="_blank"
         href="https://github.com/GeoGateway/GeoGatewayStaticResources/raw/master/documents/GeoGateway_User_Guide.pdf"><strong>User
        Guide (pdf)</strong></a>
      <br/>
      <a target="_blank" href="https://www.youtube.com/channel/UC0_bNEBxRWH2qBULDl6cB7Q/featured"><strong>Tutorial
        Videos</strong></a>
      <br/>
      <a target="_blank"
         href="https://github.com/GeoGateway/GeoGatewayStaticResources/raw/master/documents/GeoGateway_Exercises.pdf"><strong>Exercises
        (pdf)</strong></a>
      <br/><br/>
      <!--
         <strong>Recent Publications</strong>
         <div align="left" style="width:300px;">
         <b-list-group>
             <b-list-group-item v-for="item in papers" :key="item.year">
                 <a target="_blank" :href= "item.doiurl">{{ item.title }}</a>
              </b-list-group-item>
         </b-list-group>
         </div>
         <br/> -->
      <h3>More</h3>
      <a target="_blank" href="https://earthdata.nasa.gov/learn/articles/getting-started-with-sar"><strong>GSA 2020
        Workshop</strong></a>
      <br/><a target="_blank"
              href="https://cdn.earthdata.nasa.gov/conduit/upload/15244/GSA__2020_GeoGateway_updated_October_14.pdf"><strong>GSA
      2020 Workshop (slides)</strong></a>
      <br/><a target="_blank" href="https://youtu.be/Dz2JPgCpd-k"><strong>GSA 2020 Workshop (video)</strong></a>
      <br/>
      <a target="_blank"
         href="https://github.com/GeoGateway/GeoGatewayStaticResources/raw/master/documents/GeoGateway_SSA_Workshop.pdf"><strong>SSA
        2019 GeoGateway Workshop (slides)</strong></a>
    </div>
  </div>
</template>

<script>
export default {
  name: "help",
  data() {
    return {
      papers: [
        {
          title: 'Donnellan, A., Parker, J., Heflin, M. et al. Improving access to geodetic imaging crustal deformation data using GeoGateway. Earth Science Informatics, (2021).',
          doiurl: 'https://doi.org/10.1007/s12145-020-00561-7',
          year: 2021
        },
        {
          title: 'Heflin, M., Donnellan, A., Parker, J. et al. Automated Estimation and Tools to Extract Positions, Velocities, Breaks, and Seasonal Terms From Daily GNSS Measurements: Illuminating Nonlinear Salton Trough Deformation. Earth and Space Science, (2020).',
          doiurl: 'https://doi.org/10.1029/2019EA000644',
          year: 2020
        },
        {
          title: 'Parker, J., Bilham, R., Donnellan, A. et al. Buried Aseismic Slip and Off‐Fault Deformation on the Southernmost San Andreas Fault triggered by the 2010 El Mayor Cucapah Earthquake revealed by UAVSAR. Earth and Space Science, (2021).',
          doiurl: 'https://doi.org/10.1002/essoar.10506047.1',
          year: 2021
        },
      ],
    }
  },
}
</script>

<style scoped>

</style>
