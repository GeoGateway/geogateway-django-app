<template>
    <div ref="draggableContainer" id="draggable-container">
        <div id="draggable-header" @mousedown="dragMouseDown">
            <b-icon-x @click="hidePlot()" id="close-button"></b-icon-x>
                <slot name="header" id="plot-header"></slot>



        </div>
        <slot name="main"></slot>
        <slot name="footer"></slot>
    </div>
</template>

<script>
    import {bus} from "../main";

    export default {
        name: 'DraggableDiv',
        data: function () {
            return {
                positions: {
                    clientX: undefined,
                    clientY: undefined,
                    movementX: 0,
                    movementY: 0
                }
            }
        },
        methods: {
            hidePlot(){
                bus.$emit('hidePlot');
            },
            dragMouseDown: function (event) {
                event.preventDefault()
                // get the mouse cursor position at startup:
                this.positions.clientX = event.clientX
                this.positions.clientY = event.clientY
                document.onmousemove = this.elementDrag
                document.onmouseup = this.closeDragElement
            },
            elementDrag: function (event) {
                event.preventDefault()
                this.positions.movementX = this.positions.clientX - event.clientX
                this.positions.movementY = this.positions.clientY - event.clientY
                this.positions.clientX = event.clientX
                this.positions.clientY = event.clientY
                // set the element's new position:
                this.$refs.draggableContainer.style.top = (this.$refs.draggableContainer.offsetTop - this.positions.movementY) + 'px'
                this.$refs.draggableContainer.style.left = (this.$refs.draggableContainer.offsetLeft - this.positions.movementX) + 'px'
            },
            closeDragElement () {
                document.onmouseup = null
                document.onmousemove = null
            }
        }
    }
</script>

<style>
    #draggable-container {
        position: absolute;
        z-index: 9;

    }
    #draggable-header {
        z-index: 10;
        /*background-color: #343a40;*/
        align-content: center;
        cursor: move;
        /*border-radius: 15px;*/
    }
    #close-button {
        height: 25px;
        width: 25px;
        float: right;
        color: #000000;
        cursor: pointer;

    }
    #plot-header {
        margin-left: 125px;
    }
</style>

