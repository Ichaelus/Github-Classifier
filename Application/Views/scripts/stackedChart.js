function StackedChart(id, data, options){
  var cfg = {
     w: 400,        //Width of the circle
     h: 400,        //Height of the circle
     margin: {top: 100, right: 100, bottom: 100, left: 100}, //The margins of the SVG
     levels: 5,       //How many levels or inner circles should there be drawn
     maxValue: 0,       //What is the value that the biggest circle will represent
     labelFactor: 1.25,   //How much farther than the radius of the outer circle should the labels be placed
     wrapWidth: 60,     //The number of pixels after which a label needs to be given a new line
     opacityArea: 0.35,   //The opacity of the area of the blob
     dotRadius: 4,      //The size of the colored circles of each blog
     opacityCircles: 0.1,   //The opacity of the circles of each blob
     strokeWidth: 2,    //The width of the stroke around each blob
     roundStrokes: true,  //If true the area and stroke will follow a round path (cardinal-closed)
     color: d3.scale.category10() //Color function
    };
    
  //Put all of the options into a variable called cfg
  if('undefined' !== typeof options){
    for(var i in options){
    if('undefined' !== typeof options[i]){ cfg[i] = options[i]; }
    }//for i
  }//if
  //Remove whatever chart with the same id/class was present before
  d3.select(id).select("svg").remove();
  
  //Initiate the radar chart SVG
  var svg = d3.select(id).append("svg")
      .attr("width",  cfg.w + cfg.margin.left + cfg.margin.right)
      .attr("height", cfg.h + cfg.margin.top + cfg.margin.bottom)
      .attr("class", "radar"+id);
      /*
  var svg = d3.select("svg"),
      margin = {top: 20, right: 20, bottom: 30, left: 40},
      width = +svg.attr("width") - margin.left - margin.right,
      height = +svg.attr("height") - margin.top - margin.bottom,
      g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
*/
  var x = d3.scaleBand()
      .rangeRound([0, cfg.w])
      .padding(0.1)
      .align(0.1);

  var y = d3.scaleLinear()
      .rangeRound([cfg.h, 0]);

  var z = d3.scaleOrdinal()
      .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

  var stack = d3.stack();

  /* 
    data scructure:
    [
      {
        "name": "HW",
        "accuracy": []
      }
    ]
  

  */



  data.sort(function(a, b) { return b.accuracy - a.accuracy; });

  x.domain(data.map(function(d) { return d.class; }));  // Label names
  y.domain([0, d3.max(data, function(d) { return d.accuracy; })]).nice(); // Accuracy
  z.domain(data.columns.slice(1));

  g.selectAll(".serie")
    .data(stack.keys(data.columns.slice(1))(data))
    .enter().append("g")
      .attr("class", "serie")
      .attr("fill", function(d) { return z(d.key); })
    .selectAll("rect")
    .data(function(d) { return d; })
    .enter().append("rect")
      .attr("x", function(d) { return x(d.data.State); })
      .attr("y", function(d) { return y(d[1]); })
      .attr("height", function(d) { return y(d[0]) - y(d[1]); })
      .attr("width", x.bandwidth());

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y).ticks(10, "s"))
    .append("text")
      .attr("x", 2)
      .attr("y", y(y.ticks(10).pop()))
      .attr("dy", "0.35em")
      .attr("text-anchor", "start")
      .attr("fill", "#000")
      .text("Population");

  var legend = g.selectAll(".legend")
    .data(data.columns.slice(1).reverse())
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; })
      .style("font", "10px sans-serif");

  legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .attr("fill", z);

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .text(function(d) { return d; });

  function type(d, i, columns) {
    for (i = 1, t = 0; i < columns.length; ++i) t += d[columns[i]] = +d[columns[i]];
    d.total = t;
    return d;
  }
}