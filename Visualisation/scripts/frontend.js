console.log("Frontend started..");
let stateView;
/*
$.ajax({
  type: "GET",
  url: "../post/test",
}).done(function(res) {
   alert(res);
});*/

let stateData = {
	modules: []
}

initVue();
updateVue({modules: [
		{
			title: "Chose sample source",
			classes: "input",
			isActive: "",
			html: '<div class="left notchosen"><h4>Sample Generator</h4><span>With Active Learning</span></div>\
              <div class="right notchosen"><h4>User Input</h4><span>Specific Repository</span></div>'
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
  </div>'
		},
		{
			title: "Sample Extractor",
			classes: "input",
			isActive: "active",
			html: '<div style="text-align: center;">\
			<img src="http://bestanimations.com/Science/Gears/loadinggears/gear-animation-5.gif">\
			<!--<img src="https://darkiemindyou.files.wordpress.com/2015/04/loading6_230x230-cooler.gif?w=682" style="position: absolute;margin-left: -89px;width: 60px;margin-top: 115px;">\
			</div>'
		},
		{
			title: "Feature Vector",
			classes: "input",
			isActive: "",
			html: ''
		},
		{
			title: "Ensemble Learner",
			classes: "input",
			isActive: "",
			html: ''
		},
		{
			title: "Probability Diagram",
			classes: "input",
			isActive: "",
			html: ''
		},
		{
			title: "Result",
			classes: "input",
			isActive: "",
			html: ''
		},
		{
			title: "New sample pool",
			classes: "input",
			isActive: "",
			html: ''
		}
	]});


function initVue(){
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
  for(let key in data)
    stateData[key] = data[key];

  document.getElementById("modules").style.width = data.modules.length * 900 + "px";
  updateFocus();
/*
  $("#loading").fadeOut('fast', function() {
    $("#githubContent").fadeIn('fast');
  });*/
}


function updateFocus(){
	// Set focus to selected module
  for(let i = 0; i < stateData.modules.length; i++)
	if(stateData.modules[i].isActive == "active")
  		document.getElementById("modules").style.margin = "0 0 0 calc( (100% - 900px) / 2 - "+i+" * 900px)";
}
