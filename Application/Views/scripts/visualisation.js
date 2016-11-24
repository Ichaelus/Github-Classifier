console.log("Frontend started..");
// Global variables
let stateView,
	stateData = {
		modules: []
	};
// Startup
try{
	initVue();
	updateVue({modules: [
			{
				title: "Chose sample source",
				classes: "input",
				isActive: "",
				html: '<div class="left notchosen"><h4>Sample Generator</h4><span>With Active Learning</span></div>\
	              <div class="right notchosen"><h4>User Input</h4><span>Specific Repository</span></div>',
	              handleData: function() { return this.html}
			},
			{
				title: "Active Learning",
				classes: "input",
				isActive: "",
				html: '<div class="max100">\
				<ol class="al_list">\
	  <li class="notchosen">\
	    <span>Ruby Koans</span> ... <span>DATA</span>\
	  </li>\
	  <li class="notchosen">\
	    <span>TSMessages</span> ... <span>DEV</span>\
	  </li>\
	  <li class="chosen">\
	    <span>Ionic</span> ... <span>?</span>\
	  </li>\
	  </ul>\
	  </div>',
	  handleData: function() { return this.html}
			},
			{
				title: "Sample Extractor",
				classes: "input",
				isActive: "",
				html: '<div class="center">	<p class="general_desc">Fetching data for <span class="highlighted">Ionic</span>...</p>		<div class="row"><div class="col-xs-4 col-xs-offset-1">\
	  <div class="gitprev">\
	    <span>github.com/SeraphimSerapis/Ionic/</span>\
	    <div class="gitcontent"><h4>Ionic</h4>\
	  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.<br> At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.<br><br> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. </div>\
	  </div>\
	</div><div class="col-xs-6"><img src="http://bestanimations.com/Science/Gears/loadinggears/gear-animation-5.gif"></div>\
	</div>			<!--<img src="https://darkiemindyou.files.wordpress.com/2015/04/loading6_230x230-cooler.gif?w=682" style="position: absolute;margin-left: -89px;width: 60px;margin-top: 115px;">			</div>--></div>',
	handleData: function() { return this.html}
			},
			{
				title: "Feature Vector",
				classes: "input",
				isActive: "",
				html: '',
				data: {"api_calls":54,"api_url":"https:\/\/api.github.com\/repos\/ilonaa\/Robotti","author":"ilonaa","avg_commit_length":2,"branch_count":2,"class":"UNLABELED","commit_count":98,"commit_interval_avg":0,"commit_interval_max":0,"contributors_count":0,"description":"","files":"","file_count":0,"folders":"","folder_count":0,"forks":0,"hasDownloads":true,"hasWiki":true,"isFork":false,"open_issues_count":0,"language_main":"","language_array":"","name":"Robotti","readme":"","stars":0,"treeArray":"","treeDepth":0,"url":"https:\/\/github.com\/ilonaa\/Robotti","watches":0},
				handleData: function(){
					if(this.html == ""){
						vstring = "";
						for (let key in this.data) {
							vstring +="<div class='row'><div class='col-xs-4' style='font-weight:bold;'>"+key+"</div><div class='content col-xs-8'>"+this.data[key]+"</div></div>"	
						};
						this.html = '<p class="general_desc center">Following data has been extracted from <span class="highlighted">Ionic</span>:</p><div class="vector">'+vstring+'</div>';
					}
					return this.html;
				}
			},
			{
				title: "Ensemble Learner",
				classes: "input",
				isActive: "",
				html: '',
				handleData: function() { return this.html}
			},
			{
				title: "Probability Diagram",
				classes: "input",
				isActive: "active",
				html: '',
				data: [

					{ class: "DEV",		probability: .18167},
					{ class: "HW",		probability: .01492},
					{ class: "EDU",		probability: .22780},
					{ class: "DOCS",	probability: .04253},
					{ class: "WEB",		probability: .12702},
					{ class: "DATA",	probability: .05288},
					{ class: "OTHER",	probability: .02022}
				],
				handleData: function() { 
					// http://bl.ocks.org/mbostock/3885705
					if(this.html == ""){
						var d = this.data;
						this.html = "<div id='chart'></div>";
						setTimeout(function(){this.html = drawChart(d)}, 100);
					}
					return this.html
				}

			},
			{
				title: "Result",
				classes: "input",
				isActive: "",
				html: '',
				handleData: function() { return this.html}
			},
			{
				title: "New sample pool",
				classes: "input",
				isActive: "",
				html: '',
				handleData: function() { return this.html}
			}
		]});
}catch(er){
	console.log(er);
}

function initVue(){
  // Init Vue for the module wrapper
  assert(typeof(Vue) != "undefined", "Vue script missing");
  stateView = new Vue({
    el: '#module_wrapper',
    data: stateData,
    methods:{
		setFocus: function(index){
			for(let i = 0; i < stateData.modules.length; i++)
				stateData.modules[i].isActive = "";
			stateData.modules[index].isActive = "active"
			updateFocus();
		}
    }
  });
}

function updateVue(data){
  // Update/Rerender every vue property
  assert(Object.keys(data).length == Object.keys(stateData).length, "Data object does not match stateData");
  for(let key in data)
    stateData[key] = data[key];

  document.getElementById("modules").style.width = data.modules.length * 900 + "px";
  updateFocus();
}

function updateFocus(){
	// Set focus to selected module
  for(let i = 0; i < stateData.modules.length; i++)
	if(stateData.modules[i].isActive == "active")
  		document.getElementById("modules").style.margin = "0 0 0 calc( (100% - 900px) / 2 - "+i+" * 900px)";
}

function drawChart(data){
	// Draw Charts to visualise the classification distribution
	var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 800 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

	var formatPercent = d3.format(".0%");

	var x = d3.scale.ordinal()
	    .rangeRoundBands([0, width], .1, 1);

	var y = d3.scale.linear()
	    .range([0, height]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .tickFormat(formatPercent);

	var svg = d3.select("#chart").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	  x.domain(data.map(function(d) { return d.class; }));
	  y.domain(data.map(function(d)  { return d.probability; }));

	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis);

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("Probability");

	  svg.selectAll(".bar")
	      .data(data)
	    .enter().append("rect")
	      .attr("class", "bar")
	      .attr("x", function(d) { return x(d.class); })
	      .attr("width", x.rangeBand())
	      .attr("y", function(d) { return y(d.probability); })
	      .attr("height", function(d) { return height - y(d.probability); });

	  var sortTimeout = setTimeout(function() {
	    change(x, data, svg, xAxis);
	  }, 1000);

	  return document.querySelector("#chart").innerHTML;
}


function change(x, data, svg, xAxis) {
	// Copy-on-write since tweens are evaluated after a delay.
	var x0 = x.domain(data.sort(function(a, b) { return b.probability - a.probability; })
	    .map(function(d) { return d.class; }))
	    .copy();

	svg.selectAll(".bar")
	    .sort(function(a, b) { return x0(a.class) - x0(b.class); });

	var transition = svg.transition().duration(750),
	    delay = function(d, i) { return i * 50; };

	transition.selectAll(".bar")
	    .delay(delay)
	    .attr("x", function(d) { return x0(d.class); });

	transition.select(".x.axis")
	    .call(xAxis)
	  .selectAll("g")
      .delay(delay);

     setTimeout(function(){
	    svg.select(".bar")
	    	.attr("class", "bar chosen")
	    	delay(delay);      	
      }, 600);
}


function assert(condition, message) {
  // Throw error if condition is not true  
  if (!condition) {
      message = message || "Assertion failed";
      if (typeof Error !== "undefined") {
          throw new Error(message);
      }
      throw message; // Fallback
  }
}

function isNotEmpty(str){
  // Checks if str is not empty and not null
  return !isEmpty(str);
}

function isEmpty(str) {
  // Checks if str is empty or null
  return (!str || 0 === str.length);
}