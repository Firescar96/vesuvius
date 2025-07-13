<template>
  <main class="flex flex-col h-full">
    <h1>Geographic Rents</h1>
    <HouseFilters class="my-2" v-model="searchFilters" @submit="search" />
    <div class="flex-1 flex relative">
      <div id="map" class="w-[1200px] h-[675px]"></div>
      <svg class="absolute top-0 left-0 w-[1200px] h-[675px] pointer-events-none" ref="svg">
        <g id="houseDots"></g>
      </svg>
    </div>
    <div
      v-if="selectedDwelling || dwellingLegendLock"
     class="absolute bg-stone-900 border border-solid border-stone-300 border-radius-2 p-2 flex flex-col"
     :class="[!selectedDwelling && 'opacity-0']">
      
      <span>{{selectedDwelling.addressLine1}}</span>
      <span>Latitude: {{ selectedDwelling.latitude }}</span>
      <span>Longitude: {{ selectedDwelling.longitude }}</span>
      <br/>

      <a class="text-blue-400" :href="`https://app.rentcast.io/app?address=${selectedDwelling.formattedAddress}`" target="_blank">Rentcast search</a>
      <a class="text-blue-400" :href="zillowAddress" target="_blank">Zillow search</a>
    </div>
  </main>
</template>

<script setup lang="ts">
import * as d3 from 'd3';
import HouseFilters from "@/components/HouseFilters.vue";
import { Loader } from "@googlemaps/js-api-loader";
import { useTemplateRef, ref, computed } from "vue";
import VersuviusService from '@/services';


// TODO embed street view of the area
// show the last price rented and when
// keep filtering to only bedroom and bath matches
// sort by the most a property was rented by and show the ten top
// only show sold prices that are within the past 6 months

// Rentability
// nearby attractions, grocery, restaurants, bars

const svgRef = useTemplateRef<HTMLOrSVGElement>('svg');
const searchFilters = ref({ address: "", bedrooms: 0 });

const minLatitude = ref(0);
const maxLatitude = ref(0);
const minLongitude = ref(0);
const maxLongitude = ref(0);

const map = ref(null);

const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
const loader = new Loader({
  apiKey, // Use your env variable
  version: "weekly", // Specify version (e.g., "weekly" or a specific version)
});

const selectedDwelling = ref(null);
const dwellingLegendLock = ref(false);
const properties = ref([]);

const zillowAddress = computed(() => {
  if(!selectedDwelling.value) return '';

  const partialAddressMatch = /(\d+ \w[a-zA-Z]? .*)/.exec(selectedDwelling.value.formattedAddress);
  if(partialAddressMatch?.length > 1) {
    return `https://www.zillow.com/homes/${partialAddressMatch[1]}`;
  }
  return `https://www.zillow.com/homes/${selectedDwelling.value.formattedAddress}`;
})

const initMap = async () => {
  await loader.load()

  console.log("Google Maps API loaded", google.maps);
  map.value = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.7749, lng: -122.4194 }, // Replace with your desired coordinates
    zoom: 100,
    disableDefaultUI: true, // Hides default controls
    mapTypeId: 'roadmap', // Change to 'satellite', 'terrain', or 'hybrid' if needed
  });
  window.map = map.value;

  google.maps.event.addListener(map.value, "bounds_changed", () => {
    drawProperties();
  });
}
initMap();


const drawProperties = () => {  const southWestCoordinate = map.value.getBounds().getSouthWest();
  const northEastCoordinate = map.value.getBounds().getNorthEast();

  // Add X axis
  const x = d3.scaleLinear()
  .domain([southWestCoordinate.lng(), northEastCoordinate.lng()])
    .range([ 0, 1200]);

  // Add Y axis
  const y = d3.scaleLinear()
    .domain([northEastCoordinate.lat()-0, southWestCoordinate.lat()])
    .range([ 0, 675 ]);

  const minimumSalePrice = d3.min(properties.value, d => d.lastSalePrice);
  d3.select(svgRef.value)
    .select('g#houseDots')
    .selectAll("circle")
    .data(properties.value)
    .join("circle")
        .attr("cx", function (d) { return x(d.longitude); } )
        .attr("cy", function (d) { return y(d.latitude); } )
        .attr("r", d => Math.log(d.lastSalePrice || minimumSalePrice) / Math.log(20))
        .attr('class', 'pointer-events-auto cursor-pointer')
        .style("fill", 'red')
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
} 

const search = async () => {
  console.log("Searching for", searchFilters.value);
  properties.value = await VersuviusService.property.getProperties();

  if (!properties.value) {
    return;
  }

  minLatitude.value = properties.value[0].latitude;
  maxLatitude.value = properties.value[0].latitude;
  minLongitude.value = properties.value[0].longitude;
  maxLongitude.value = properties.value[0].longitude;

  properties.value.forEach((property) => {
    if (property.latitude < minLatitude.value) {
      minLatitude.value = property.latitude;
    }
    if (property.latitude > maxLatitude.value) {
      maxLatitude.value = property.latitude;
    }
    if (property.longitude < minLongitude.value) {
      minLongitude.value = property.longitude;
    }
    if (property.longitude > maxLongitude.value) {
      maxLongitude.value = property.longitude;
    }
  });

  console.log("Properties", properties.value);
  map.value.setCenter({
    lat: (minLatitude.value + maxLatitude.value) / 2,
    lng: (minLongitude.value + maxLongitude.value) / 2,
  });

  const bounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(minLatitude.value, minLongitude.value), // Southwest corner
    new google.maps.LatLng(maxLatitude.value, maxLongitude.value)  // Northeast corner
  );
  map.value.fitBounds(bounds);

  drawProperties();
};
</script>

