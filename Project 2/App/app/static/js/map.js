d3.json("/API/most_recent").then( data => {
	let plotData = [{
		type: 'choropleth',
		locationmode: 'country names',
		locations: data.map(c => c.country),
		z: data.map(c => c.Cases),
		text: data.map(c => c.Cases),
		autocolorscale: true
	}];

	var layout = {
	  title: 'COVID-19',
	  geo: {
		scope: "world",
		projection: {
			type: 'natural earth'
		},
		oceancolor: '#3399ff',
		showcountries: true,
	  }
	};

	Plotly.newPlot("map-container", plotData, layout, {showLink: false});

	}

)








// function getCountry(region){
// 	countryData = null;
// 	d3.json(`/records/`).then( data => {
// 		if (region !== "World") {
// 			countryData = data.filter(record => record.iso3===region)
// 		}else{
// 			countryData=data
// 		}
// 		console.log(countryData)
// 	}
// 	)
	
// 	return countryData
// };

// function buildMap(mapData) {

// 	let plotData = [{
// 		type: 'choropleth',
// 		locationmode: 'ISO-3',
// 		locations: mapData.map(c => c.iso3),
// 		z: mapData.map(c => c.confirmed),
// 		text: mapData.map(c => c.confirmed),
// 		// text: mapData.map(c => {c.confirmed, c.deaths, c.recovered}),
// 		autocolorscale: true
// 	}];

// 	var layout = {
// 	  title: 'COVID-19',
// 	  geo: {
// 		  projection: {
// 			  type: 'robinson'
// 		  }
// 	  }
// 	};

// 	Plotly.newPlot("map-container", plotData, layout, {showLink: false});
	  
// }

// const handleDateChange = (data) => {
// 	let lookupDate = d3.select('p#value-time').property("value");
// 	console.log(lookupDate)
// 	let filteredData = data.filter(
// 		dataRow => dataRow.date === lookupDate
// 	);
	
// 	buildMap(filteredData);
	
// };



// dateData = d3.json(`/records/`).then( data => {
// 	dataTime = data.map(e=>{
// 		return new Date(e.date)
// 	})
// 	console.log(`dataTime: ${dataTime}`)
// 	console.log(`min dataTime: ${d3.min(dataTime)}`)
// 	console.log(`max dataTime: ${d3.max(dataTime)}`)

// 	let sliderTime = d3
// 	.sliderBottom()
// 	.min(d3.min(dataTime)) 
// 	.max(d3.max(dataTime)) 
// 	.step(1000 * 60 * 60 * 24) // Daily Step
// 	.width(600) //Adjust to appropriate size @Josh
// 	.tickFormat(d3.timeFormat('%Y-%m-%d'))
// 	.default(d3.max(dataTime))
// 	.on('onchange', val => {
// 		d3.select('p#value-time').text(d3.timeFormat('%Y-%m-%d')(val));
// 	});

// 	let gTime = d3
// 		.select('div#slider-time')
// 		.append('svg')
// 		.attr('width', 700) //Adjust to appropriate size @Josh
// 		.attr('height', 100) //Adjust to appropriate size @Josh
// 		.append('g')
// 		.attr('transform', 'translate(30,30)'); //Adjust to appropriate size @Josh
	
// 	gTime.call(sliderTime);

// 	d3.select('p#value-time').text(d3.timeFormat('%Y.%m.%d')(sliderTime.value()));

// 	return data;
// })




	
// mapPlot = dateData.then( data => {
// 	d3.select('p#value-time').on("onchange", handleDateChange(data))
// });


// ---------------------------------------------------------------------------------------------------

















// Plotly.d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/2010_alcohol_consumption_by_country.csv', function(err, rows){
//       function unpack(rows, key) {
//           return rows.map(function(row) { return row[key]; });
//       }

//     let data = [{
//         type: 'choropleth',
//         locations: unpack(rows, 'location'),
//         z: unpack(rows, 'alcohol'),
//         text: unpack(rows, 'location'),
//         autocolorscale: true
//     }];

//     var layout = {
//       title: 'Pure alcohol consumption<br>among adults (age 15+) in 2010',
//       geo: {
//           projection: {
//               type: 'robinson'
//           }
//       }
//     };

//     Plotly.newPlot("map-container", data, layout, {showLink: false});

// });







// // World Map
// import {legend} from "@d3/color-legend";
// d3 = require("d3@5");
// width  = 1500;
// height = 750;
// projection = d3.geoEqualEarth();
// path = d3.geoPath(projection);
// outline = ({type: "Sphere"});
// world = FileAttachment("countries-50m.json").json(); // replace with our data
// countries = topojson.feature(world, world.objects.countries); // replace with our data
// topojson = require("topojson-client@3");





// let svg = d3.create("svg").style("display", "block").attr("viewBox", [0, 0, width, height]);
  
// defs = svg.append("defs");
// defs.append("path")
// 	.attr("id", "outline")
// 	.attr("d", path(outline));
  
// defs.append("clipPath")
// 	.attr("id", "clip")
//   	.append("use")
// 	.attr("xlink:href", new URL("#outline", location));
  
// let g = svg.append("g")
// 	.attr("clip-path", `url(${new URL("#clip", location)})`); 

// g.append("use")
// 	.attr("xlink:href", new URL("#outline", location))
// 	.attr("fill", "white");
  
// g.append("g")
// 	.selectAll("path")
// 	.data(countries.features) // replace with our data
// 	.join("path")
// 	.attr("fill", d => color(data.get(d.properties.name))) // replace with our data
// 	.attr("d", path)
// 	.append("title")
// 	.text(d => `${d.properties.name}${data.has(d.properties.name) ? data.get(d.properties.name) : "N/A"}`); // replace with our data
  
// g.append("path")
// 	.datum(topojson.mesh(world, world.objects.countries, (a, b) => a !== b)) // replace with our data
// 	.attr("fill", "none")
// 	.attr("stroke", "white")
// 	.attr("stroke-linejoin", "round")
// 	.attr("d", path);
  
// svg.append("use")
// 	.attr("xlink:href", new URL("#outline", location))
// 	.attr("fill", "none")
// 	.attr("stroke", "black");
