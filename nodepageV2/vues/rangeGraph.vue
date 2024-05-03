
<script>

  
  export default {
    props: {
      inputData: Object,
      upperRange: Number,
      lowerRange: Number,
    },
    data() {
      return {
        seconds: 0,
        chart: null,
        timeout: null,

        options: {
          labelFontColor: "transparent",
          backgroundColor: "transparent",
          axisX: {
            labelFontColor: "transparent",
            tickColor: "transparent",
            lineThickness: 0,
	          tickThickness: 0
          },
          axisY: {
            tickColor: "transparent",
            labelFontColor: "transparent",
            stripLines: [],
            lineThickness: 0,
            gridThickness: 0,
            tickLength: 0,
            minimum: -5,
            maximum: 6,
          },
          data: [{lineColor: '#982E2E',
                  color: '#462225',
                  type:"area",
                  axisYType: "primary",
                  name: "Range",
                  markerSize: 5,
                  yValueFormatString: "#",
                  dataPoints: [],
                }]
        },
        styleOptions: {
          'width': '45vw', 
          'height': '20vh',
        }

      }
    },
    mounted(){
      setInterval(this.updateData, 500);
    },
    methods: {
      updateData() {
        let boilerColor, deltaY, yVal;

        // for (let i = 0; i < this.chart.options.data.length; i++){
        //   let currentData = this.chart.options.data[i];
        //   let channel = currentData.name


        //   if (Object.keys(this.inputData).includes(channel)){
        //     this.chart.options.data[i].dataPoints = [];

        //     for (let j = 0; j < this.inputData[channel].length; j++){
        //       this.chart.options.data[i].dataPoints.push({'x': j * 100, 'y': this.inputData[channel][j], "channel": channel});
        //     }

            
    
        //   }
          
        // }

  
        let [x, y, z] = [this.inputData["x"], this.inputData["y"], this.inputData["z"]];


        if (x != 0 || y != 0){
          this.seconds += 1;
        }else{
          this.seconds = 0;
        }

        this.chart.data[0].dataPoints.push({"x": new Date().getTime(), 'y': this.seconds})
        
        if (this.chart.data[0].dataPoints.length > 10){
          this.chart.data[0].dataPoints.splice(0, 1);
        }

        this.chart.render();
 
      },
      chartInstance(chart) {
        this.chart = chart;
        this.updateData();
      }
    },
    unmounted() {
      clearTimeout(this.timeout);
    }

  }
</script>
  
<template>
  <div id="display-tab-graph-container">
    <CanvasJSChart :options="options" :style="styleOptions" @chart-ref="chartInstance" id="canvas-chart"/>
  </div>
</template> 

<style>

#canvas-chart{
  position: relative;
  top: 3vh;
  left: 5vw;
}


</style>