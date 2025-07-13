<template>
  <div class="profit-projections">
    <h1>2603 N. Richards Street - Profit Projections</h1>
    
    <!-- User Input Controls -->
    <div class="controls">
      <div class="input-group">
        <label for="monthlyIncome">Monthly Income ($):</label>
        <input 
          id="monthlyIncome"
          v-model.number="monthlyIncome" 
          type="number" 
          min="0" 
          step="100"
          class="income-input"
        />
      </div>
      
      <div class="slider-group">
        <label>Monthly Income Slider: ${{ monthlyIncome.toLocaleString() }}</label>
        <input 
          v-model.number="monthlyIncome" 
          type="range" 
          min="0" 
          max="10000" 
          step="100"
          class="income-slider"
        />
      </div>
    </div>

    <!-- Fee Information -->
    <div class="fee-info">
      <h3>Fee Structure:</h3>
      <ul>
        <li><strong>Maintenance Fee:</strong> 5% of monthly income</li>
        <li><strong>Yearly Turnover Fee:</strong> $1,000 per year</li>
      </ul>
      <p class="formula">
        <strong>Net Monthly Income = Monthly Income - (Monthly Income × 0.05)</strong><br>
        <strong>Net Yearly Income = (Net Monthly Income × 12) - $1,000</strong>
      </p>
    </div>

    <!-- Chart Container -->
    <div class="chart-container">
      <div id="chart" ref="chartRef"></div>
    </div>

    <!-- Data Table -->
    <div class="data-section">
      <h3>Historical Data and Scenarios</h3>
      <table v-if="tableData.length">
        <thead>
          <tr>
            <th v-for="(col, index) in tableData[0]" :key="index">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in tableData.slice(1)" :key="rowIndex">
            <td v-for="(cell, colIndex) in row" :key="colIndex">{{ cell }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else>Loading data...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import * as d3 from 'd3';

interface TableRow {
  [key: string]: string | number;
}

const tableData = ref<TableRow[]>([]);
const monthlyIncome = ref(3000);
const chartRef = ref<HTMLElement>();

const loadGoogleSheet = async () => {
  const sheetId = "1cFI_hwJq9N5Dn4lfm7Eht-NYH1QSUtHmgPqC9SYH9Bs";
  const sheetName = "Projections";
  const query = encodeURIComponent("SELECT *");
  const url = `https://docs.google.com/spreadsheets/d/${sheetId}/gviz/tq?sheet=${sheetName}&tq=${query}`;

  try {
    const res = await fetch(url);
    const text = await res.text();
    const json = JSON.parse(text.substring(47, text.length - 2));
    const cols = json.table.cols.map((col: { label: string }) => col.label);
    const rows = json.table.rows.map((row: { c: Array<{ v: string | number } | null> }) =>
      row.c.map((cell) => (cell ? cell.v : ""))
    );
    tableData.value = [cols, ...rows];
  } catch (err) {
    console.error("Failed to load sheet:", err);
  }
};

const createChart = () => {
  if (!chartRef.value || !tableData.value.length) return;

  // Clear existing chart
  d3.select(chartRef.value).selectAll("*").remove();

  // Parse historical data and calculate cumulative net
  interface HistoricalDataPoint {
    year: number;
    cumulativeNet: number;
  }
  
  const historicalData: HistoricalDataPoint[] = [];
  let historicalCumulativeNet = 0;
  
  tableData.value.slice(1).forEach((row: TableRow) => {
    const year = parseInt(String(row[0]));
    const expenses = parseFloat(String(row[1]).replace(/,/g, '')) || 0;
    historicalCumulativeNet -= expenses; // Subtract expenses (negative cumulative)
    
    historicalData.push({
      year: year,
      cumulativeNet: historicalCumulativeNet
    });
  });

  // Get current year and month
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();
  const currentMonth = currentDate.getMonth();

  // Generate future data at year/month granularity with cumulative net
  interface FutureDataPoint {
    year: number;
    month: number;
    cumulativeNet: number;
  }
  
  const futureData: FutureDataPoint[] = [];
  let futureCumulativeNet = historicalCumulativeNet; // Start from historical cumulative
  
  // Start from current month
  for (let year = currentYear; year <= currentYear + 15; year++) {
    const startMonth = year === currentYear ? currentMonth : 0;
    const endMonth = year === currentYear + 15 ? 11 : 11;
    
    for (let month = startMonth; month <= endMonth; month++) {
      const monthlyNet = monthlyIncome.value * 0.95; // 5% maintenance fee
      futureCumulativeNet += monthlyNet;
      
      // Apply yearly turnover fee
      if (month === 11) { // December
        futureCumulativeNet -= 1000;
      }
      
      futureData.push({
        year: year,
        month: month,
        cumulativeNet: futureCumulativeNet
      });
    }
  }

  console.log('historicalData', historicalData);
  console.log('futureData', futureData);

  // Combine historical and future data using a dictionary to allow overwriting
  const yearDataMap = new Map<number, { value: number; type: string }>();
  
  // Add historical data points
  for (const historicalPoint of historicalData) {
    yearDataMap.set(historicalPoint.year, {
      value: historicalPoint.cumulativeNet,
      type: 'historical'
    });
  }
  
  // Add future data points - this will overwrite historical data for overlapping years
  const futureByYear = new Map();
  for (const dataPoint of futureData) {
    const year = dataPoint.year;
    if (!futureByYear.has(year)) {
      futureByYear.set(year, []);
    }
    futureByYear.get(year).push(dataPoint);
  }
  
  for (const [year, yearData] of futureByYear) {
    // Use the last month of each year for the marker
    const lastMonthData = yearData[yearData.length - 1];
    yearDataMap.set(year, {
      value: lastMonthData.cumulativeNet,
      type: 'future'
    });
  }
  
  // Convert map to sorted arrays for chart display
  const chartData = Array.from(yearDataMap.entries())
    .map(([year, data]) => ({
      year: year,
      value: data.value,
      type: data.type
    }))
    .sort((a, b) => a.year - b.year);
  
  const displayMarkers = [...chartData]; // Same data for display markers
  

  // Set up dimensions
  const margin = { top: 20, right: 30, bottom: 60, left: 80 };
  const width = 800 - margin.left - margin.right;
  const height = 400 - margin.top - margin.bottom;

  // Create SVG
  const svg = d3.select(chartRef.value)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Scales
  const xScale = d3.scaleLinear()
    .domain(d3.extent(chartData, d => d.year) as [number, number])
    .range([0, width]);

  const yScale = d3.scaleLinear()
    .domain([
      d3.min(chartData, d => d.value) as number,
      d3.max(chartData, d => d.value) as number
    ])
    .range([height, 0]);

  // Line generator
  const line = d3.line<{year: number, value: number}>()
    .x(d => xScale(d.year))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);

  // Add the line path
  svg.append("path")
    .datum(chartData)
    .attr("fill", "none")
    .attr("stroke", "#60a5fa")
    .attr("stroke-width", 3)
    .attr("d", line);

  // Add data points (year-level markers)
  svg.selectAll(".dot")
    .data(displayMarkers)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("cx", d => xScale(d.year))
    .attr("cy", d => yScale(d.value))
    .attr("r", 4)
    .attr("fill", d => d.type === 'historical' ? "#f87171" : "#4ade80")
    .attr("stroke", "#1f2937")
    .attr("stroke-width", 2);

  // Add axes
  const xAxis = d3.axisBottom(xScale).tickFormat(d3.format("d"));
  const yAxis = d3.axisLeft(yScale).tickFormat(d => `$${d3.format(",")(d)}`);

  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(xAxis)
    .style("color", "#d1d5db");

  svg.append("g")
    .call(yAxis)
    .style("color", "#d1d5db");

  // Add axis labels
  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", width / 2)
    .attr("y", height + margin.bottom - 10)
    .text("Year")
    .style("fill", "#d1d5db");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", -margin.left + 20)
    .text("Profit/Loss ($)")
    .style("fill", "#d1d5db");

  // Add zero line
  svg.append("line")
    .attr("x1", 0)
    .attr("x2", width)
    .attr("y1", yScale(0))
    .attr("y2", yScale(0))
    .attr("stroke", "#6b7280")
    .attr("stroke-width", 1)
    .attr("stroke-dasharray", "5,5");

  // Add tooltips
  const tooltip = d3.select(chartRef.value)
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0)
    .style("position", "absolute")
    .style("background", "#1f2937")
    .style("border", "1px solid #374151")
    .style("padding", "8px")
    .style("border-radius", "4px")
    .style("pointer-events", "none")
    .style("color", "#d1d5db");

  svg.selectAll(".dot")
    .on("mouseover", function(event, d: unknown) {
      const dataPoint = d as { type: string; year: number; value: number };
      tooltip.transition()
        .duration(200)
        .style("opacity", .9);
      tooltip.html(`
        <strong>${dataPoint.type === 'historical' ? 'Historical' : 'Future'}</strong><br/>
        Year: ${dataPoint.year}<br/>
        Cumulative Net: $${d3.format(",")(dataPoint.value)}
      `)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseout", function() {
      tooltip.transition()
        .duration(500)
        .style("opacity", 0);
    });

  // Find break-even point
  const breakEvenPoint = chartData.find(d => d.value >= 0);
  if (breakEvenPoint) {
    svg.append("circle")
      .attr("cx", xScale(breakEvenPoint.year))
      .attr("cy", yScale(breakEvenPoint.value))
      .attr("r", 8)
      .attr("fill", "none")
      .attr("stroke", "#fbbf24")
      .attr("stroke-width", 3);

    svg.append("text")
      .attr("x", xScale(breakEvenPoint.year) + 15)
      .attr("y", yScale(breakEvenPoint.value) - 10)
      .text("Break-even")
      .attr("font-size", "12px")
      .attr("fill", "#fbbf24");
  }
};

// Watch for changes and update chart
watch([monthlyIncome, tableData], () => {
  nextTick(() => {
    createChart();
  });
}, { deep: true });

onMounted(() => {
  loadGoogleSheet();
});
</script>

<style scoped>
.profit-projections {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #111827;
  color: #d1d5db;
  min-height: 100vh;
}

h1 {
  text-align: center;
  color: #f9fafb;
  margin-bottom: 30px;
}

.controls {
  display: flex;
  gap: 40px;
  margin-bottom: 30px;
  padding: 20px;
  background: #1f2937;
  border-radius: 8px;
  align-items: center;
  border: 1px solid #374151;
}

.input-group, .slider-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label, .slider-group label {
  font-weight: bold;
  color: #e5e7eb;
}

.income-input {
  padding: 8px 12px;
  border: 2px solid #4b5563;
  border-radius: 6px;
  font-size: 16px;
  width: 150px;
  background-color: #374151;
  color: #d1d5db;
}

.income-input:focus {
  outline: none;
  border-color: #60a5fa;
}

.income-slider {
  width: 200px;
  background: #374151;
}

.income-slider::-webkit-slider-thumb {
  background: #60a5fa;
}

.income-slider::-moz-range-thumb {
  background: #60a5fa;
}

.fee-info {
  background: #451a03;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border-left: 4px solid #fbbf24;
}

.fee-info h3 {
  margin-top: 0;
  color: #fbbf24;
}

.fee-info ul {
  margin: 10px 0;
  padding-left: 20px;
}

.fee-info li {
  margin: 5px 0;
  color: #fef3c7;
}

.formula {
  background: #374151;
  padding: 15px;
  border-radius: 6px;
  margin-top: 15px;
  font-family: monospace;
  line-height: 1.6;
  color: #d1d5db;
}

.chart-container {
  margin: 30px 0;
  text-align: center;
}

#chart {
  display: inline-block;
  border: 1px solid #374151;
  border-radius: 8px;
  padding: 20px;
  background: #1f2937;
}

.data-section {
  margin-top: 40px;
}

.data-section h3 {
  color: #f9fafb;
  margin-bottom: 15px;
}

table {
  border-collapse: collapse;
  width: 100%;
  background: #1f2937;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  border: 1px solid #374151;
}

th, td {
  border: 1px solid #374151;
  padding: 12px;
  text-align: left;
}

th {
  background: #374151;
  font-weight: bold;
  color: #f9fafb;
}

tr:nth-child(even) {
  background: #374151;
}

tr:nth-child(odd) {
  background: #1f2937;
}

.tooltip {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  font-size: 12px;
  z-index: 1000;
}
</style>
