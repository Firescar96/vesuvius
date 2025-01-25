<template>
  <main>
      <svg ref="svg" :width="tableWidth + margin.left + margin.right" :height="tableHeight + margin.top + margin.bottom">

        <text
          fill="white"
          :x="margin.left + tableWidth / 2"
          :y="tableHeight + margin.top + margin.bottom - 20"
          text-anchor="middle"
          font-size="12px"
        >
          Time (Months)
        </text>

        <text fill="white" transform="rotate(-90)" :x="-(margin.top + tableHeight / 2)" :y="20" text-anchor="middle" font-size="12px">Monthly Rent</text>
        <text fill="white" :x="tableWidth" :y="40" text-anchor="middle" font-size="12px">Days on the market</text>

        <g :transform="`translate(${margin.left}, ${margin.top})`">
          <rect :x="tableWidth + 20" y="50" width="20" height="400" fill="url(#gradient)" />

          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%" />
          </defs>
        </g>
      </svg>


    <div
      v-if="selectedDwelling || dwellingLegendLock"
     :ref="selectedLegend" 
     class="absolute bg-stone-900 border border-solid border-stone-300 border-radius-2 p-2 flex flex-col"
     :class="[!selectedDwelling && 'opacity-0']">
      
      <span>{{selectedDwelling.addressLine1}}</span>
      <br/>
      <strong>Days on Market:</strong> {{selectedDwelling.daysOnMarket}}

      <a class="text-blue-400" :href="`https://app.rentcast.io/app?address=${selectedDwelling.formattedAddress}`" target="_blank">Rentcast search</a>
      <a class="text-blue-400" :href="`https://www.zillow.com/homes/${/(\d+ \w[a-zA-Z]? .*)/.exec(selectedDwelling.formattedAddress)[1]}`" target="_blank">Zillow search</a>
    </div>
  </main>
</template>


<script setup lang="ts">
import * as d3 from 'd3';
import {rentalListingsInactive} from '@/chartData';
import {useTemplateRef, watch, ref} from 'vue'
import dayjs from 'dayjs'

const svgRef = useTemplateRef<HTMLOrSVGElement>('svg');

// set the dimensions and margins of the graph
const margin = {top: 10, right: 70, bottom: 50, left: 60};
const tableWidth = 1080 - margin.left - margin.right;
const tableHeight = 720 - margin.top - margin.bottom;

const selectedDwelling = ref(null);
const dwellingLegendLock = ref(false);

watch(svgRef, () => {
  const data = rentalListingsInactive
    // .filter(x => x.bedrooms === 3)
    .filter(x => x.daysOnMarket)
    .filter(x => ['Multi-Family', 'Apartment'].includes(x.propertyType))
    .map(x => ({...x, removedDate: new Date(x.removedDate)}))
    // this sort makes the smaller dots, with less days on the market, appear on top
    .sort((a, b) => dayjs(a.removedDate).diff(dayjs(b.removedDate)));

  // append the svg object to the body of the page
  const svg = d3.select(svgRef.value)
    .select('g')

  // Add X axis
  // Get the minimum and maximum dates using d3.extent
  const dateDomain = d3.extent(data, d => d.removedDate);
  const x = d3.scaleTime()
    .domain(dateDomain)
    .range([ 0, tableWidth ]);
    svg.append("g")
    .attr("transform", `translate(0, ${tableHeight})`)
    .call(d3.axisBottom(x).ticks(20));

  // Add Y axis
  const maxPrice = d3.max(data, x => x.price);
  const y = d3.scaleLinear()
    .domain([0, maxPrice])
    .range([ tableHeight, 0]);
    svg.append("g")
    .call(d3.axisLeft(y).ticks(20));


  // Create a log scale
  const colorScale = d3.scaleLog()
    .domain(d3.extent(data, d => d.daysOnMarket))
    .range([0, 1]);

  // Apply the color scale
  const colorInterpolator = d3.interpolateHcl("#00ff00", "#aa0044");
  const getColor = (value: number) => colorInterpolator(colorScale(value));



  svg.append('g')
    .selectAll("dot")
    .data(data)
    .join("circle")
        .attr("cx", function (d) { return x(d.removedDate); } )
        .attr("cy", function (d) { return y(d.price); } )
        .attr("r", d => Math.log(d.daysOnMarket + 10) / Math.log(2))
        .style("fill", d => getColor(d.daysOnMarket))
        .on("mouseover", (_, d) => {
          if(dwellingLegendLock.value) return;
          selectedDwelling.value = d;
        })
        .on("mouseout", () => {
          if(dwellingLegendLock.value) return;
          selectedDwelling.value = null;
        })
        .on('click', async (_, d) => {
          if(selectedDwelling.value?.addressLine1 === d.addressLine1) {
            dwellingLegendLock.value = !dwellingLegendLock.value;
          } else dwellingLegendLock.value = true;
          selectedDwelling.value = d;
        });


  const legendScale = d3.scaleLog()
  .domain(d3.extent(data, d => d.daysOnMarket))
  .range([0, 400]); // Height of the legend


// Add a vertical gradient
const linearGradient = svg.select("linearGradient");

// Add color stops to the gradient
linearGradient.selectAll("stop")
  .data(colorScale.ticks(10).map((t, i, arr) => ({
    offset: `${(i / (arr.length - 1)) * 100}%`,
    color: getColor(t)
  })))
  .join("stop")
  .attr("offset", d => d.offset)
  .attr("stop-color", d => d.color);

// Add the axis
svg.append("g")
  .attr("transform", `translate(${tableWidth + 40}, 49)`) // Position the axis next to the gradient
  .call(d3.axisRight(legendScale)); // Add ticks to match the legend scale
})

</script>
