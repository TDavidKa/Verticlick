
<script>

  
  export default {
    props: {
      inputData: Object,
      upperRange: Number,
      lowerRange: Number,
    },
    data() {
      return {
        chart: null,
        timeout: null,
        options: {
          labelFontColor: "white",
          backgroundColor: "transparent",
          toolTip: {
            contentFormatter: function (e) {
              // customize tooltip content
              return "Label: Movement" + "<br>Value: " + e.entries[0].dataPoint.y + "";
            },
            backgroundColor: "lightyellow", 
            borderColor: "orange", 
          },
          axisX: {
            labelFontColor: "white",
            tickColor: "white",
          },
          axisY: {
            tickColor: "white",
            labelFontColor: "white",

            suffix: "",
            minimum: -500,
            maximum: 500,
            stripLines:[]

          },
          data: [{
                  type:"line",
                  axisYType: "primary",
                  name: "X",
                  showInLegend: true,
                  markerSize: 0,
                  yValueFormatString: "#,##0",
                  dataPoints: [],
                },{
                  type:"line",
                  axisYType: "primary",
                  name: "Y",
                  showInLegend: true,
                  markerSize: 0,
                  yValueFormatString: "#,##0 °C",
                  dataPoints: []
                },{
                  type:"line",
                  axisYType: "primary",
                  name: "Z",
                  showInLegend: true,
                  markerSize: 0,
                  yValueFormatString: "#,##0 °C",
                  dataPoints: []
                },]
        },
        styleOptions: {
          'width': '55vw', 
          'height': '50vh',
        }

      }
    },
    mounted(){
      setInterval(this.updateData, 500);
    },
    methods: {
      updateData() {
        let boilerColor, deltaY, yVal;

        let [x, y, z] = [this.inputData["x"], this.inputData["y"], this.inputData["z"]];


        

        if (!isNaN(x)){
          this.options.data[0].dataPoints.push({"x": new Date().getTime(), "y": x});
          this.options.data[0].dataPoints = this.options.data[0].dataPoints.slice(-60);
        }
        
        if (!isNaN(y)){
          this.options.data[1].dataPoints.push({"x": new Date().getTime(), "y": y});
          this.options.data[1].dataPoints = this.options.data[1].dataPoints.slice(-60);
        }

        if (!isNaN(z)){
          this.options.data[2].dataPoints.push({"x": new Date().getTime(), "y": z});
          this.options.data[2].dataPoints = this.options.data[2].dataPoints.slice(-60);
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
    <CanvasJSChart :options="options" :style="styleOptions" @chart-ref="chartInstance"/>
  </div>
</template> 

<style>

#display-tab-graph-container{
  width: 55vw;
  height: 20vh;
  color: white;
}



</style>