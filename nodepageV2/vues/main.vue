<script>

import FakeGraph from "./FakeGraph.vue"
import temperatureGauge from "./temperatureGauge.vue"
import RangeGraph from "./rangeGraph.vue"

export default {
  components: {FakeGraph, temperatureGauge, RangeGraph},
  data() {
    return {
      nodeName: "Thermocouple",
      currentTab: "graph",
      data: {},
      dataHistory: {},
      timestamps: [],
      hottestTemperature: 100,
      averageTemperature: 0,
      lowerRange: -500,
      upperRange: 500,
      tempOutOfRange: 0,
      highestMovement: 0,
      totalMovement: 0,
      seconds : 0,
      leftClick: 0,
      rightClick: 0,
      
    }
  },
  mounted(){
    fetch("../get_node_name")
      .then(response => {
        return response.json()
      }).then(json => {
        this.nodeName = json[0];
      })

    // Fetch new data from sensor every 500 milliseconds
    setInterval(this.fetchData, 500);
    this.fetchData();
  },
  methods: {
    fetchData(){
      let data = fetch("../get_frame_data").then(response => {
          return response.json();
      }).then(json => {


          let [x, y, z] = [json["x"], json["y"], json["z"]];
          this.data["x"] = x;
          this.data["y"] = y;
          this.data["z"] = z;

          this.highestMovement = Math.max(Math.abs(x), Math.abs(y), Math.abs(z));
          this.totalMovement = x + y + z;

          if (x != 0 || y != 0){
            this.seconds += 1;
          }else{
            this.seconds = 0;
          }

          let [leftClick, rightClick] = [json["leftClick"], json["rightClick"]];
          this.leftClick = leftClick;
          this.rightClick = rightClick;

        });

    },
    
    
                
  }
}
</script>

<template>
  <div id="site-container"> 
    <div id="site-header">
      <h1 id="node-name-header"> ☰ NMD 342 → Mouse Analytics → <span id="node-name-header-grey">Performance Graphs</span></h1>
    </div>
 
    <div id="site-content">
      <div id="site-content-left">
        <div id="channel-temperatures">
          <h2> Accelerometers</h2>

          <div id="temperature-gauge-container">
          <temperatureGauge label='X' id="temperatureGauge" :size="30" :data="data['x']" :lowerRange="lowerRange" :upperRange="upperRange"> </temperatureGauge>
          <temperatureGauge label='Y' id="temperatureGauge" :size="30" :data="data['y']" :lowerRange="lowerRange" :upperRange="upperRange"> </temperatureGauge>
          <temperatureGauge label='Z' id="temperatureGauge" :size="30" :data="data['z']" :lowerRange="lowerRange" :upperRange="upperRange"> </temperatureGauge>
         
          </div>
        </div>

        <div id="channel-temperature-graph">
          <h2> Graph </h2>

          <div id="graph-container">
            <FakeGraph :inputData="data" :lowerRange="lowerRange" :upperRange="upperRange"></FakeGraph>
          </div>

        </div>
      </div>

      <div id="site-content-right">
        <div id="site-content-right-top">
          <div id="average-temperature">
            <h2> Highest Movement </h2>
             <temperatureGauge id="temperatureGauge" :size="30" :data="highestMovement" lowerRange="0" upperRange="1000"> </temperatureGauge>
          </div>

          <div id="hottest-temperature">
            <h2> Total Movement </h2>
          
            <temperatureGauge id="temperatureGauge" :size="30" :data="totalMovement" lowerRange="-1500" upperRange="1500"> </temperatureGauge>
            
        
          </div>
        </div>

        <div id="temperature-outside-of-range-graph">
          <h2> Seconds of Continuous Movement </h2>

          <div>
            <h3 id="tempOutsideOfRange"> {{seconds}}</h3>
            <RangeGraph :inputData="data" :lowerRange="lowerRange" :upperRange="upperRange"></RangeGraph>
          </div>
        
        </div>

        <div id="temperature-range">
          <h2 id="mouse-clicks-title" > Buttons Pressed</h2>

          <div id="temperature-range-selector">
            <div id="temperature-lower-range-selector">
                <h2> {{this.leftClick}} </h2>
            </div>

            <div id="temperature-upper-range-selector">
                <h2> {{this.rightClick}} </h2>
                
            </div>
          </div>


        </div>
      </div> 
      
    </div>
  </div>

</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Azeret+Mono&display=swap');

#tempOutsideOfRange{
  color: #982E2E;
  font-size: 2vw;

  position: relative;

  top: 5vh;
  left: 26vw;
}

#graph-container{
  display: flex;
  justify-content: center;
  align-items: center;

  width: 58vw;
  height: 20vh;
}

#temperature-upper-range-selector h2,
#temperature-lower-range-selector h2{
  font-size: 3vw !important;
}

#temperature-upper-range-selector input,
#temperature-lower-range-selector input{
  width: 10vw;
  height: 5vh;

  background: #222224;
  border: 1px solid #515151;
  border-radius: 5px;

  text-align: center;

  color: white;
}

#mouse-clicks-title{
  font-size: 2vw;
}

#temperature-range{
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;

}

#temperature-range-selector{
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  width: 30vw;
  height: 10vh;
}

#temperature-gauge-container{
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex-wrap: wrap;

  width: 58vw;
  height: 20vh;
}

#site-content-left h2{
  font-size: 1vw;
  width: 100%;

  text-align: left;
  padding-left: 2vw;
}

#site-content-right h2{
  font-size: 0.9vw;
  width: 100%;

  text-align: center;
}

#average-temperature,
#hottest-temperature{
  width: 17vw;
  height: 30vh;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex-direction: column;
}

#temperature-outside-of-range-graph,
#temperature-range{
  width: 35vw;
  height: 28vh;
}

#site-content-right-top{
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  width: 38vw;
}

#site-content-right{
  height: 95vh;
  width: 38vw;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;

  padding-left: 0;
  margin-left: 0;

}

#site-content-left{
  width: 60vw;
  height: 95vh;

  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;

  padding-right: 0;
  margin-right: 0;
}

#temperature-outside-of-range-graph{
  overflow-y: hidden;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

#channel-temperatures,
#channel-temperature-graph,
#average-temperature,
#hottest-temperature,
#temperature-outside-of-range-graph,
#temperature-range{
  background: #181B1F;
  border: solid #282A2F 2px;
  border-radius: 5px;
  font-size: 0.75vw;
}

#channel-temperature-graph{
  width: 58vw;
  height: 58vh;

  background: #181B1F;
  border: solid #282A2F 2px;
  border-radius: 5px;
}

#channel-temperatures{
  width: 58vw;
  height: 30vh;
}


#site-content-right{
  width: 38vw;
}

#node-name-header-grey{
  color: grey;
}

#site-container{
  position: absolute;
  top: 0;
  left: 0;

  width: 100vw;
  height: 100%;

  padding: 0;
  margin: 0;
  font-family: 'Azeret Mono', monospace;
  color: lightgrey;

  overflow-y: hidden;
  overflow-x: hidden;
}

#site-header{
  position: absolute;
  top: 0;
  left: 0;

  display: flex;
  justify-content: space-between;

  width: 100vw;
  height: 5vh;

  margin: 0;
  padding: 0;

  font-size: 0.5vw;

  border-bottom: black solid 2px;


  background-color: #181B1F; 
  color: lightgrey;

}

#tab-selector{
  display: flex;
  width: 30vw;
}
  
#tab-selector h1{
  width: 15vw;
  height: 100%;
  
  margin: 0;

  display: flex;
  justify-content: center;
  align-items: center;

  border-left: black solid 2px;
}

.selectedTab{
  background-color: #252F4A;
}


#tab-selector h1:hover{
  background-color: #333d57;
}


#node-name-header{
  margin-left: 2vw;
}

#site-content{
  height: 95%;
  padding-top: 5vh;
  background-color: #101116;

  display: flex;
  align-items: center;
  justify-content: center;
}

</style>