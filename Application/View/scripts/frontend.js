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
			title: "Input handler",
			classes: "input",
			isActive: ""
		},
		{
			title: "Input handler2",
			classes: "input",
			isActive: "active"
		},
		{
			title: "Input handler3",
			classes: "input",
			isActive: ""
		},
		{
			title: "Input handler4",
			classes: "input",
			isActive: ""
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
