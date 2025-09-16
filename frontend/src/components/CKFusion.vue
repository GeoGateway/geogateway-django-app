<template>
  <div class="w-100 p-2 bg-light text-left">
    <q-banner class="bg-info text-white q-mb-md">
      <q-btn 
        flat 
        dense 
        @click="ckfusionInfo=true" 
        icon="info" 
        color="white"
        class="q-mr-sm"
      />
      About CK Fusion
    </q-banner>
    <div class="tool-content">
      <a target="_blank"
         href="https://github.com/GeoGateway/GeoGatewayStaticResources/raw/master/documents/CK_Fusion_Software_User_Guide.pdf"><strong>CK Fusion User
        Guide</strong></a>
    </div>
    <br>
    We are working on CK fusion as a cloud service.
    <br><br>
    <a target="_blank" href="https://data.geo-gateway.org/stage/Salton_Sea_Fusion_Results/">Salton Sea Fusion Examples</a>
    <!--
    <b-button>Create New Experiment</b-button><br><br>
    <b-button>Load Experiments</b-button>
    -->

    <!-- info  popup -->
    <q-dialog v-model="ckfusionInfo">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">CK Fusion</div>
        </q-card-section>
        
        <q-card-section class="q-pt-none">
          <p>
            CK Fusion software uses the clustered kriging fusion method to combine earth surface displacement observations from two sources: GNSS and UAVSAR.
          </p>
          <p>
            There are three stand alone components to software each of which can be run separately as a python executable.
          </p>
          <ul>
            <li><strong>get_uavsar_displacements</strong>: Retrieves GNSS displacements over an InSAR epoch defined by the input UAVSAR annotation file.</li> 
            <li><strong>clusterKrigeVelocities</strong>: A stand alone implementation of the clustered kriging algorithm that uses only the GNSS observations to generate an estimated field.</li>
            <li><strong>CK_Fusion_GNSS_InSAR</strong>: Implements the full clustered kriging fusion method for GNSS and UAVSAR displacement observations.</li>
          </ul>
        </q-card-section>
        
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>

</template>

<script>
export default {
  name: "CKFusion",
  data() {
    return {
      ckfusionInfo: false,
    }
  },
}
</script>

<style scoped>

</style>
