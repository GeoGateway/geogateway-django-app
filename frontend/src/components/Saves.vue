<template>
    <div class="tab-window">
        <q-btn color="positive" @click="saveState">Save Current State</q-btn>
        <br/> <br>

        <div v-for="save in saves" :key="save.date">
            <input type="checkbox" :value="save.active" v-model="save.active" @change="showHideLayers(save)"> <span class="checkbox-label">{{save.date}}</span> <br>
            <hr/>
        </div>

    </div>
</template>

<script>
    import {bus} from '../main'
    import {mapFields} from '../utils/mapFields'
    export default {
        name: "Saves",
        data(){
            return {

            }
        },
      computed: {
          ...mapFields(['mapSaves.saves', 'map.layers'])
      },
        methods:{
            saveState(){
                console.log('test')

            },
            storeSave(layers){
                var today = new Date();
                var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate() + ' | ' + today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
                console.log(date);
                let copiedLayers = Object.assign({}, layers);
                this.saves.push({data: copiedLayers, date: date, active: false})
            },
            showHideLayers(layers){
                if(layers.active){
                    bus.emit('displaySave', layers.data);
                }
                else {
                    bus.emit('clearSaveLayer', layers.data)
                }
            }
        },
        mounted() {
            bus.on('saved', (layers) =>
                this.storeSave(layers));
        },
        beforeUnmount() {
            bus.off('saved');
        }
    }
</script>

<style scoped>

</style>