<script>

export default {
    props: {data: {type: Number},
        size: {type: Number}, lowerRange: {type: Number}, upperRange: {type: Number},
        label: {type: String, default: ""}}
}

</script>

<template>
    <div class="container">
        <div class="temperature-gauge" :style="{width: `${size/2.4}vw`, height: `${size/2}vh`}">
            

            <div class="circle-border" 
            :style="{ 
                background: `linear-gradient(to right, #E25065 0%, #E25065 ${20}%, #E9B837 ${20}%, #E9B837 ${80}%, #7FB57B ${80}%, #7FB57B 100%)`,
                width: `${size/20*8}vw`,
                height: `${size/20*15}vh`,
                left: `${size/20*-2.4}vw`}">
                
                
                <div class="circle"
                    :style="{ 
                        top: `${size/20*0.5}vh`,
                        left: `${size/20*0.5}vw`,
                        width: `${size/20*7}vw`,
                        height: `${size/20*15}vh`}">
                </div>

                
            </div>

            
            <div class="display-bar" :style="{ 
                background: `linear-gradient(to right, ${data <= lowerRange ? '#E25065' : data < upperRange ? '#E9B837' : '#7FB57B'} 0%, ${data <= lowerRange ? '#E25065' : data < upperRange ? '#E9B837' : '#7FB57B'} ${20 + 0.6 * ((data - lowerRange) / (upperRange - lowerRange))*100}%, #2F2F31 ${20 + 0.6 * ((data - lowerRange) / (upperRange - lowerRange))*100}%, #2F2F31 100%)`,
                        top: `${size/20*-13.75}vh`,
                        left: `${size/20+5-5}vw`,
                        width: `${size/20*6.25}vw`,
                        height: `${size/20*13.5}vh`,}">

                <div class="circle"
                    :style="{ 
                        top: `${size/20*2}vh`,
                        left: `${size/20*0.6}vw`,
                        width: `${size/20*5}vw`,
                        height: `${size/20*14}vh`}">
                </div>

            </div>

            

        </div>

        <h3 class="temperature-display" :style="{
                                                 'font-size': `${size/30*1.25}vw`,
                                                 'left': `${size/30*5}vw`,
                                                 'top': `${size/30*-3}vw`}">{{label == "" ? "&nbsp;" : label}}</h3>

        <h3 class="temperature-display" :style="{color: `${data < lowerRange ? '#E25065' : data < upperRange ? '#E9B837' : '#7FB57B'}`,
                                                 'font-size': `${size/30*1.5}vw`,
                                                 'left': `${size/30*4.5}vw`,
                                                 'top': `${size/30*-3}vw`}">{{Math.floor(data)}}</h3>
   
    </div>
</template>

<style>

.temperature-display{
    position: relative;
    margin: 0;
}

.display-bar{
  position: relative;
  text-align: center;

  border-radius: 100%;
  background-color: #E9B837;
  border: none;
  clip-path: inset(0 0 29% 0);
}

.circle {
  position: relative;
  text-align: center;
  border-radius: 100%;
  background-color: #181B1F;
  border: none;
}

.circle-border {
  position: relative;
  text-align: center;
  margin-left: 30%;
  border-radius: 50%;
  background-color: #E53B3B;
  border: none;
  /* background: linear-gradient(to right,
        #E9B837 0%,
        #E9B837 v-bind("lowerPercentage")%,
        #7FB57B 33.33%,
        #7FB57B 66.66%,
        #E25065 66.66%,
        #E25065 100%
      ); */
  clip-path: inset(0 0 30% 0); /* Adjusted the clip-path */
}

</style>