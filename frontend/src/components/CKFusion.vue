<template>
  <div class="w-100 p-2 bg-light text-left">
    <b-alert :show="true">
      <b-link @click="ckfusionInfo=true" href="#">
        <b-icon icon="info-circle-fill"/>
      </b-link>&ensp;
      About CK Fusion
    </b-alert>
    
    <!-- info  popup -->
    <b-modal
        v-model=ckfusionInfo
        title="CK Fusion">
        CK Fusion software uses the clustered kriging fusion method to combine earth surface displacement observations from two sources: GNSS and UAVSAR.
        <br><br>
        There are three stand alone components to software each of which can be run separately as a python executable.
        <ul>
        <li><b>get_uavsar_displacements</b>: Retrieves GNSS displacements over an InSAR epoch defined by the input UAVSAR annotation file.</li> 
        <li><b>clusterKrigeVelocities</b>: A stand alone implementation of the clustered kriging algorithm that uses only the GNSS observations to generate an estimated field.</li>
        <li><b>CK_Fusion_GNSS_InSAR</b>: Implements the full clustered kriging fusion method for GNSS and UAVSAR displacement observations.</li>
        </ul>
      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>
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
