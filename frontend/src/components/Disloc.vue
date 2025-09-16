<template>
  <div class="w-100 p-2 bg-light text-left">
    <b-alert :show="true">
      <b-link @click="disclocInfo=true" href="#">
        <b-icon icon="info-circle-fill"/>
      </b-link>&ensp;
      About Discloc
    </b-alert>

    <hr/>

    <div id="upload-container">
      <!--
      <h5><b>Input File Upload &nbsp;&nbsp;</b>
        <b-icon icon="question-circle-fill" v-b-modal.modal-2></b-icon></h5>
      <b-modal id="modal-2" title="Input File Format" button-size="sm" ok-only>

          Use this form to upload one or more faults that are already in Disloc input file format. The following example shows formatting:
          <hr/>
          <ul>
            <li>Line 1: 32.904255 -115.526449 1 (this is the lat, lon of the origin; and "1" signifies use of a grid).</li>
            <li>Line 2: -75 1 151 -40 1 41 (the grid: x0, x_delta, x_number, y0, y_delta, y_number).</li>
            <li>Line 3: 20.489759271 -80.624111128 355.0 (first fault patch: x, y (km) from origin and strike (degrees).</li>
            <li>Line 4: 0 1.21 45.0 1.0 1.0 -0.0 -0.0 0.0 3.0 3.0 (fault_type 0 for point dislocation, depth, dip (degrees), lambda, mu,u1,u2,u3, length, width).</li>
            <li>Repeat the formats for Lines 3 and 4 for each additional fault.</li>
          </ul>

      </b-modal>
      <label>
        <input  type="file" id="file" ref="file" @change="handleFileUpload"/>
      </label>
      <div>
        <strong>Synthetic Interferograms Parameters:</strong>
        <b-input-group prepend="Elevation (Deg)">
            <b-form-input v-model="Elevation" name="Elevation"></b-form-input>
        </b-input-group>
        <b-input-group prepend="Azimuth (Deg)">
            <b-form-input v-model="Azimuth" name="Azimuth"></b-form-input>
        </b-input-group>
        <b-input-group prepend="Radar Frequency (GHz)">
            <b-form-input v-model="RadarFrequency" name="RadarFrequency"></b-form-input>
        </b-input-group>
      </div><br>
      <button @click="submitFile()">Submit</button>
      <div class="container" v-html="fileInfo">
      </div>
      <br>
      -->
      <!--
          <div v-if="jobActive" class="center">
              <b-spinner type="grow" label="Job executing..."></b-spinner>
             <br />
         </div>
      -->

      <b-button @click="loadExperiments()">
        <div v-if="results.length !== 0">
          Refresh Experiments
        </div>
        <div v-else>
          Load Experiments
        </div>
      </b-button>


      <div v-for="entry in results" :key="entry.exp.name" class="collapsed">

        <div>
          <div @click="extendEntry(entry)" v-bind:style="{backgroundColor: entry.activeBackground}"
               class="clickableName">
            {{ entry.exp.name }}
          </div>
          <div v-if="entry.extended">
            <b>Experiment Status:</b> {{ entry.exp.experimentStatus.name }}
            <br/>
            <div v-if="entry.exp.experimentStatus.name === 'COMPLETED'">
              <input type="checkbox" v-model="entry.active" @change="showHideLayers(entry)">Show Synthetic
              Interferograms
              <br/>
              <a :href="entry.result2.url">Download CSV</a>&ensp;
              <a :href="entry.result.url">Download KMZ</a>
            </div>

          </div>
        </div>
        <!--&lt;!&ndash;          {{entry.exp}}&ndash;&gt;-->
      </div>
      <br>
    </div>

    <!-- info  popup -->
    <b-modal
        v-model="disclocInfo"
        title="Discloc">
      <p class="my-4">
        Elastic dislocation models are commonly used to analyze inversion on faults
        following the event of an earthquake (Chen et al., 2020). In 1985, Yoshimitsu
        Okada (Ph.D.) proposed a formula which calculated displacement in an isotropic,
        uniform elastic half space. The formula can calculate coseismic deformation
        caused by any fault within the elastic half space (Okada, 1985). Okada’s dislocation
        theory, which is the most commonly used dislocation theory, is often used with
        InSAR. InSAR monitors the surface coseismic deformation field, and subsequently, Okada’s theory is used to
        conduct
        fault slip inversion, calculating the coseismic strain stress field (Chen et al., 2020).
        deformation of an elastic medium due to slip from active faults (Avouac, n.d.).
      </p>
      <div slot="modal-footer" class="w-100">
      </div>
    </b-modal>

  </div>
</template>

<script>
import axios from "axios";
import {bus} from '../main';
import 'leaflet-kmz';
import 'axios'


axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'
import {mapFields} from '../utils/mapFields';
import L from "leaflet";

export default {

  name: "Disloc",
  data() {
    return {
      disclocInfo: false,

    }
  },
  computed: {
    // file: null,
    // fileInfo: null,
    // Elevation: 60,
    // Azimuth: 0,
    // jobActive: false,
    // jobCompleted: false,
    // experiment: null,
    // app_id: null,
    // models: null,
    // services: null,
    // session: null,
    // utils: null,
    // expData: null,
    // results: [],
    ...mapFields([
      'disloc.file',
      'disloc.fileInfo',
      'disloc.Elevation',
      'disloc.Azimuth',
      'disloc.RadarFrequency',
      'disloc.jobActive',
      'disloc.jobCompleted',
      'disloc.experiment',
      'disloc.app_id',
      'disloc.models',
      'disloc.services',
      'disloc.session',
      'disloc.utils',
      'disloc.expData',
      'disloc.results',
      'disloc.showFullExp',
      'disloc.hostname',

      //map
      'map.globalMap',
    ])
  },

  mounted() {
    bus.on('updateDisloc', (html) =>
        this.fileInfo = html);


  },
  beforeUnmount() {
    bus.off('updateDisloc');
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    extendEntry(entry) {
      if (!entry.fullRetrieved) {
        if (entry.exp.experimentStatus.name === "COMPLETED") {
          this.loadFullExperiment(entry);
        } else {
          entry.extended = true;
          //entry.extended ? entry.activeBackground = '#8494a3' : entry.activeBackground = '#7ee04c';
          entry.activeBackground = '#8494a3';
        }
      }

    },
    showHideLayers(entry) {
      let vm = this;
      // let name = entry.exp.name
      if (entry.active) {
        entry.layer = L.kmzLayer(entry.result.url);
        vm.globalMap.addLayer(entry.layer);

        // });
      } else {
        this.globalMap.removeLayer(entry.layer);
      }

    },
    submitFile() {
      let vm = this;
      var uploadUrl = '/geogateway_django_app/disloc/';
      let formData = new FormData();
      formData.append('file', this.file);
      axios.post(uploadUrl, formData
      ).then(function (response) {
        var dislocArgs = response.data;
        vm.case_submitexperiment(dislocArgs);
      })
          .catch(function (response) {
            console.log(response)
          });
    },
    case_submitexperiment(dislocArgs) {
      this.jobActive = true;
      dislocArgs["Elevation"] = this.Elevation;
      dislocArgs["Azimuth"] = this.Azimuth;
      dislocArgs["Radar Frequency"] = this.RadarFrequency;
      let vm = this;
      this.app_id = dislocArgs["app_id"];


      // Load the application interface for the application module with id app_id
      const loadAppInterface = this.services.ApplicationModuleService.getApplicationInterface({
        lookup: this.app_id,
      });
      // Find the compute resource id for the 'this.hostname'
      const loadComputeResourceIds = this.services.ComputeResourceService.names()
          .then((computeResourceIds) => {
            for (const computeResourceId in computeResourceIds) {
              if (computeResourceIds[computeResourceId] === this.hostname) {
                return computeResourceId;
              }
            }
            throw new Error("Couldn't find a compute resource for host " + this.hostname);
          });
      // Find a group resource profile that can run an experiment on 'this.hostname'
      // Also, find the default queue configuration for the application deployment on that 'this.hostname'
      const loadResourceProfiles = this.services.GroupResourceProfileService.list()
      const loadGroupResourceProfileAndQueue = Promise.all([loadComputeResourceIds, loadResourceProfiles])
          .then(([computeResourceId, groupResourceProfiles]) => {

            const groupResourceProfile = groupResourceProfiles.find(grp => {
              for (const computePref of grp.computePreferences) {
                if (computePref.computeResourceId === computeResourceId) {
                  return true;
                }
              }
              return false;
            });
            if (!groupResourceProfile) {
              throw new Error("Couldn't find a group resource profile for host " + this.hostname);
            }
            const loadDeployments = this.services.ApplicationDeploymentService.list({
              appModuleId: this.app_id,
              groupResourceProfileId: groupResourceProfile.groupResourceProfileId,
            })
                .then(deployments => {
                  const deployment = deployments.find(d => d.computeHostId === computeResourceId);
                  if (!deployment) {
                    throw new Error("Couldn't find a deployment for host " + this.hostname);
                  }
                  return this.services.ApplicationDeploymentService.getQueues({
                    lookup: deployment.appDeploymentId
                  })
                      .then(queues => {
                        const queue = queues.find(q => q.isDefaultQueue);
                        if (!queue) {
                          throw new Error("Couldn't find a default queue for host " + this.hostname);
                        }
                        return queue;
                      });
                });
            return Promise.all([computeResourceId, groupResourceProfile, loadDeployments]);
          });
      // Load user's workspace prefs to find the id of most recently used project; experiment must be added to a project
      const loadWorkspacePrefs = this.services.WorkspacePreferencesService.get();
      Promise.all([loadAppInterface, loadGroupResourceProfileAndQueue, loadWorkspacePrefs])
          .then(([appInterface, [computeResourceId, groupResourceProfile, defaultQueue], workspacePrefs]) => {
            const experiment = appInterface.createExperiment();
            experiment.experimentName = "Disloc on " + new Date().toLocaleString();
            experiment.projectId = workspacePrefs.most_recent_project_id;
            // Copy groupResourceProfileId and queue defaults to experiment configuration
            experiment.userConfigurationData.groupResourceProfileId = groupResourceProfile.groupResourceProfileId;
            experiment.userConfigurationData.computationalResourceScheduling.resourceHostId = computeResourceId;
            experiment.userConfigurationData.computationalResourceScheduling.totalCPUCount = defaultQueue.defaultCPUCount;
            experiment.userConfigurationData.computationalResourceScheduling.nodeCount = defaultQueue.defaultNodeCount;
            experiment.userConfigurationData.computationalResourceScheduling.wallTimeLimit = defaultQueue.defaultWalltime;
            experiment.userConfigurationData.computationalResourceScheduling.queueName = defaultQueue.queueName;
            // Copy input values from Maptool.cplexInputValues to experimentInputs
            for (let input of experiment.experimentInputs) {
              if (input.name in dislocArgs) {
                input.value = dislocArgs[input.name];
              }
            }
            return this.services.ExperimentService.create({data: experiment});
          })
          .then(experiment => {
            vm.experiment = experiment;
            return this.services.ExperimentService.launch({
              lookup: experiment.experimentId
            }).then(() => {
              vm.loadExperiments();

            });
          });
    },
    loadExperiments() {
      //check if user is logged in
      let vm = this;
      return this.services.ExperimentSearchService.list({
        limit: 5,
        [this.models.ExperimentSearchFields.USER_NAME.name]:
        this.session.Session.username,
        //when I add the app_id no results are returned
      }).then((data) => {
        let prev = vm.results;

        vm.results = [];
        data.results.forEach((exp, index) => {
          let entry = {exp: exp, result: null, active: false, layer: null, extended: false, fullRetrieved: false};
          let currStatus = exp.experimentStatus.name;
          if (prev.length !== 0) {
            let prevStatus = prev[index].exp.experimentStatus.name;
            if (prevStatus !== currStatus) {
              vm.extendEntry(entry);
            }
          }

          if (currStatus !== "COMPLETED") {
            vm.extendEntry(entry);
          } else {
            entry.activeBackground = '#7ee04c'
          }
          vm.results.push(entry);
          // vm.loadFullExperiment(exp, index)
          //sort list
        });

      });
    },
    loadFullExperiment(entry) {
      let exp = entry.exp;
      if (exp.experimentStatus === this.models.ExperimentState.COMPLETED) {
        this.services.FullExperimentService.retrieve({
          lookup: exp.experimentId,
        })
            .then((fullDetails) => {
              const kmz = fullDetails.experiment.experimentOutputs.find(
                  (o) => o.name === "KMZ Output File"
              ).value;
              const stdoutDataProduct = fullDetails.outputDataProducts.find(
                  (dp) => dp.productUri === kmz
              );
              const csv = fullDetails.experiment.experimentOutputs.find(
                  (o) => o.name === "Disloc Output"
              ).value;
              const csvDataProduct = fullDetails.outputDataProducts.find(
                  (dp) => dp.productUri === csv
              );

              if (
                  stdoutDataProduct &&
                  stdoutDataProduct.downloadURL
              ) {
                Promise.all([fetch(stdoutDataProduct.downloadURL, {credentials: "same-origin",}),
                  fetch(csvDataProduct.downloadURL, {credentials: "same-origin",})
                ]).then(([result, result2]) => {
                  entry.result = result;
                  entry.result2 = result2;
                  entry.fullRetrieved = true;
                  entry.extended = !entry.extended;
                  //entry.extended ? entry.activeBackground = '#7ee04c' : entry.activeBackground = '#7ee04c';
                  entry.activeBackground = '#7ee04c';
                });
              }

            })
      }
    }

  }
}
</script>

<style scoped>
#upload-container {
  float: left;
  text-align: left;
}

.collapsed {
  width: auto;
  height: auto;
  border: 2px solid #e6e6ff;
  box-sizing: border-box;
  border-radius: 8px;
  overflow-y: auto;
  background-color: #A5B9CC;
  /*A5B9CC*/
}

.clickableName {
  cursor: pointer;
}

</style>
