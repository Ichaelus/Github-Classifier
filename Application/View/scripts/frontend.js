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
			isActive: "active",
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
						vstring +="<div class='row'><div class='col-xs-6'>"+key+"</div><div class='col-xs-6'>"+this.data[key]+"</div></div>"	
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
			isActive: "",
			html: '',
			handleData: function() { return this.html}
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
