console.log("Frontend started..");
let stateView, inputView, classificatorView, outputView, wrapperView,
	stateData = {
		action: "halt",
		mode: "test", // stream, pool, test, single
		isSemiSupervised: false,
		trainInstantly: false,
		formula: "",
		formulas: []
	},
	inoutData = {
    classifierAsking: "",
    classifiersUnsure: false,
    manualClass: "?",
		poolSize: 0,
    repoAPILink: "",
    repoName: "Repository Name",
    semisupervised: {"SemiSupervisedSureEnough" : true, "SemiSupervisedLabel": "None"},
    isPrediction: true,
		classificators: {} // name : {description, yield, active, uncertainty, accuracy: [{class, val},..], probability : [{class, val},..]}
	},
	wrapperData = {
    // Data used by the wrapper shown when displaying the detailed page
    currentName: "",
		current: {description: "", yield: 0, active: false, uncertainty: 0, accuracy: {}, probability: {}},
    savePoints: {}, // fileName: {yield, accuracy: [{class, val}, ..]}
    selectedPoint: "",
		id: 0
  };

try{
	runGenerator(function *main(){
		let initData = yield jQGetPromise("/get/classificators", "json");
    Vue.set(inoutData, "classificators", initData.classificators);
    setInititalProbability();
		initVue();
    $("#page").fadeIn();
	});
}catch(ex){
	console.log(ex);
}

function setInititalProbability(){
  let cd = inoutData.classificators;
  for(let c in cd){
    assert(typeof(cd[c].accuracy) != "undefined", "Object missing");
    cd[c].probability = [];
    for(let j = 0; j < cd[c].accuracy.length; j++){
      cd[c].probability[j] = {class : cd[c].accuracy[j].class, val : 0.0};
    }
  }
}

function getStateQuery(){
	let query = "?";
	var keys = Object.keys(stateData);
	for(var i = 0; i < keys.length; i++){
	  if(typeof(stateData[keys[i]]) == "string" || typeof(stateData[keys[i]]) == "boolean")
	  	query += keys[i] + "=" + encodeURIComponent(stateData[keys[i]]) + "&";
	}
	return query;
}

function initVue(){
  // Init Vue components (state, input, classificators, output)
  assert(typeof(Vue) != "undefined", "Vue script missing");
  stateView = new Vue({
    el: '#header',
    data: stateData,
    methods:{
    	getFormulas: function(){
    		$.get("/get/formulas", function(data){
    			data = JSON.parse(data);
    			if(data === false)
    				throw new Error("Invalid server response");
    			Vue.set(stateData, "formulas", data);
    			if(data.length > 0)
    				Vue.set(stateData, "formula", data[0]);
    		});
    	},
    	setFormula: function(f){
    		assert(isNotEmpty(f) && stateData.formulas.indexOf(f) >= 0, "Formula should not be empty");
    		Vue.set(stateData, "formula", f);
    	},
      switchMode: function(){
        stateView.resetView();
        Vue.set(inoutData, "isPrediction", stateData.mode == 'test');
        outputView.switchMode(stateData.mode);
      },
		  singleStep: function(){
  			Vue.set(stateData, "action", "singleStep");
  			console.log("Proceeding single step");
        stateView.resetView();
        runGenerator(function *main(){
          // Fetch sample, display
          Vue.set(inoutData, "repoName", "Searching..");
          results = yield jQGetPromise("/get/doSingleStep"+getStateQuery(), "json");
          stateView.updateResults(results);
        });
  		},
  		halt: function(){
  			Vue.set(stateData, "action", "halt");
  			console.log("Halting");
  		},
  		loop: function(){
  			Vue.set(stateData, "action", "loop");
  			console.log("Looping");
        stateView.resetView();
  			runGenerator(function *main(){
  				// Fetch sample, display then repeat until stateData has changed
  				while(stateData.action == "loop"){
            Vue.set(inoutData, "repoName", "Searching..");
  					results = yield jQGetPromise("/get/doSingleStep"+getStateQuery(), "json");
  					stateView.updateResults(results);
            if(results.classifiersUnsure)
              Vue.set(stateData, "action", "halt_loop");
  				}
  			});
  		},
  		updateResults: function(results){
        // Apply returned changes to the internal GUI state
        // classificators: { moduleName => {attr_changed: val_changed,..},...}
        assert(results != null, "Result is not well-formatted.");

        if(typeof(results.repo) != "undefined"){
          Vue.set(inoutData, "repoName", results.repo.repoName);
          Vue.set(inoutData, "repoAPILink", results.repo.repoAPILink);
        }
        for(let key in {"classifiersUnsure" : 0, "semisupervised" : 0, "classifierAsking": 0}){
          // Adjust state variables
          if(typeof(results[key]) != "undefined")
            Vue.set(inoutData, key, results[key]);
        }

        if(stateData.mode == "stream" || stateData.mode == "pool"){
          // Set output ?
          if(results.classifiersUnsure){
            Vue.set(inoutData, "manualClass", "?");
          }
        }

        if(typeof(results.classificators != "undefined"))
          stateView.updateClassificators(results.classificators);
  		},
      updateClassificators: function(data){
        console.log("updating classificators");
        // Update data regarding classificators
        for(let c in inoutData.classificators){ // c => classificator name
          if(typeof(data[c] != "undefined")){
            // Classificator is not muted, update it's results
            for(let newkey in data[c])
              Vue.set(inoutData.classificators[c], newkey, data[c][newkey]);
          }
        }
      },
      predictSingle: function(){
        let repoLink = prompt("Please insert the link to a repository you wish to classify.");
        if(repoLink){
          try{
            repoLink = convertToApiLink(repoLink);
            runGenerator(function *main(){
              // Fetch sample, display
              results = yield jQGetPromise("/get/PredictSingleSample?repoLink="+repoLink, "json");
              stateView.updateResults(results);
            });
          }catch(ex){
            notify("Error predicting sample", ex, 2500);
          }
        }
      },
      startTest: function(){
        Vue.set(inoutData, "repoName", "Testing..");
        runGenerator(function *main(){
          // Fetch sample, display
          results = yield jQGetPromise("/get/startTest", "json");
          stateView.updateResults(results);
          Vue.set(inoutData, "repoName", "Test result");
        });
      },
      resetView: function(){
        // Reset classificators, but keep accuracy
        for(let c in inoutData.classificators){ // c => classificator name
            cf = inoutData.classificators[c];
            for(let i in cf.probability)
              Vue.set(cf.probability[i], "val", 0.0);
            Vue.set(cf, "uncertainty", 0);
        }
        Vue.set(inoutData, "classifiersUnsure", false);
      },
      retrainAll: function(){
        notify("Retrain all", "Training every untrained classificator. This may take a couple of minutes");
        for(let c in inoutData.classificators)
          if(inoutData.classificators[c].yield <= 0)
            wrapperView.retrain(c, true);
      }
    }
  });
  stateView.getFormulas();

  titleView = new Vue({
    el: '#titles',
    data: stateData
  });

  inputView = new Vue({
    el: '#input',
    data: inoutData,
    methods:{
      switchMode: function(type){

      },
      getPoolsize: function(){
        $.get("/get/poolSize", function(data){
          if(isNaN(data))
            throw new Error("Invalid server response");
          inoutData.poolSize = parseInt(data);
        });
      },
      getClassifierAmount: function(){
        return Object.keys(inoutData.classificators).length;
      }
    }
  });
  inputView.getPoolsize();


  classificatorView = new Vue({
    el: '#classificators',
    data: inoutData,
    methods:{
      getMode: function(){
        return stateData.mode;
      },
    	showInfo: function(name){
    		wrapperView.setData(name);
        wrapperView.getSavePoints();
        //RadarChart("#class_accuarcy_chart", [accuracyToGraphData(wrapperData.current.accuracy)], getRadarConfig(700));
    		$('.overlay_blur').fadeIn();
    		$('#overlay_wrapper').fadeIn();
    	},
    	switchState: function(name){
        let c= inoutData.classificators[name];
        c.active = !c.active;
        if(!c.active){
          $.get("/get/mute?name="+name, function(data){
            if(data != "success")
                throw new Error("Invalid server response");
          });
        }else{
          $.get("/get/unmute?name="+name, function(data){
            if(data != "success")
                throw new Error("Invalid server response");
          });
        }
    	},
    	getMax: function(id){
    		let max = 0;
        array = stateData.mode == "test" ? "accuracy" : "probability";
        if(typeof(inoutData.classificators[id][array]) != "undefined")
          for(let i = 0; i < inoutData.classificators[id][array].length; i ++)
      			max = Math.max(max, inoutData.classificators[id][array][i].val);
    		return max;
    	},
      isAsking: function(name){
        return stateData.mode == "pool" && inoutData.classifierAsking == name;
      }
    }
  });

  outputView = new Vue({
    el: '#output',
    data: inoutData,
    methods:{
  		switchMode: function(mode){
        if(mode == "test"){
          let data = [];
          for(let c in inoutData.classificators){
            data.push(accuracyToGraphData(inoutData.classificators[c].accuracy));
          }
          if(data.length > 0)
            RadarChart("#testOuputChart", data, getRadarConfig(350));
        }
  		},
      getClassifierAmount: function(type){
        return Object.keys(inoutData.classificators).length;
      },
      getMode: function(){
        return stateData.mode;
      },
      manualClassification: function(){
        if(inoutData.manualClass == '?')
          window.open("/user_classification.html?popup=true&api_url="+inoutData.repoAPILink, "User decision", "channelmode=yes");
      }
    }
  });
  outputView.switchMode(stateView.mode);

  wrapperView = new Vue({
    el: '#overlay_wrapper',
    data: wrapperData,
    methods:{
    	setData: function(i){
    		Vue.set(wrapperData, "current", inoutData.classificators[i]);
        Vue.set(wrapperData, "currentName", i);
    	},
      getSavePoints: function(){
        $.get("/get/savePoints?name="+wrapperData.currentName, function(resp){
          if(resp != ""){
            resp = JSON.parse(resp);
            if(resp === false)
              throw new Error("Invalid server response");
            Vue.set(wrapperData, "savePoints", resp.savepoints);
            let data = [];
            for(let sp in wrapperData.savePoints){
              data.push(accuracyToGraphData(wrapperData.savePoints[sp].accuracy));
            }
            if(data.length > 0)
              RadarChart("#version_accuarcy_chart", data, getRadarConfig(700));
            else
              document.getElementById("version_accuarcy_chart").style.display = "none";
          }
        });
      },
      setSavePoint: function(fileName){
        Vue.set(wrapperData, "selectedPoint", fileName);
      },
  		retrain: function(name, save){
  			console.log("Wrapper: "+name+" retraining.");
        notify("Retraining", "The classifier: "+name+" started retraining. This could take a while.", 2500);
        runGenerator(function *main(){
          let data = yield jQGetPromise("/get/retrain?name="+name);
          if(JSON.parse(data) != false){
            data = JSON.parse(data);
            stateView.updateClassificators(data.classificators);
            notify("Retrained successfull", "The classifier: "+name+" finished retraining", 2500);
            if(save)
              wrapperView.save(name);
          }else{
            notify("Error while retraining", data, 2500);
          }
        });
  		},
  		retrain_semi: function(){
  			console.log("Wrapper: "+wrapperData.currentName+" semi retraining.");
        runGenerator(function *main(){
          notify("Retrained", yield jQGetPromise("/get/retrainSemiSupervised?name="+wrapperData.currentName), 2500);
        });
  		},
  		save: function(name){
  			console.log("Wrapper: "+name+" saving.");
        runGenerator(function *main(){
          notify("Saved", yield jQGetPromise("/get/save?name="+name), 2500);
          wrapperView.getSavePoints();
        });
  		},
  		load: function(){
  			console.log("Wrapper: "+wrapperData.currentName+" loading.");
        runGenerator(function *main(){
          data = yield jQGetPromise("/get/load?name="+wrapperData.currentName + "&savepoint="+wrapperData.selectedPoint, "json");
          // data contains a name of the selected classificator and an accuracy array
          if(typeof(data.Error) != "undefined"){
            notify("Error", data.Error, 2500);
           }else{ 
            stateView.updateClassificators(data.classificators);
            notify("Loaded", "The classifier "+wrapperData.currentName+" has been loaded.", 2500);
          }
        });
  		}
    }
  });
}
function hideInfo(){
	// Hide any visible popup
	$('#overlay_wrapper').fadeOut();
	$('.overlay_blur').fadeOut();
}

function HandlePopupResult(result) {
  // If the sample has been labeled, update view
  console.log("result of popup is: ");
  console.log(result);
  setTimeout(function(){Vue.set(inoutData, "manualClass", result.label)}, 250);
  $.get("/get/ALclassification"+getStateQuery()+"api_url="+result["api_url"]+"&label="+result.label, function(data){
    console.log(data);
    if(stateData.action == "halt_loop")
      stateView.loop();
  });
}
function convertToApiLink(repoLink){
  // Converts a repo link to an api link. E.g. https://github.com/Ichaelus/GithubClassificator/ -> https://api.github.com/repos/Ichaelus/GithubClassificator/
  if(repoLink.indexOf("https://github.com/") >= 0){
    return repoLink.replace("https://github.com/", "https://api.github.com/repos/");
  }else{
    throw new Error("RepoLink invalid");
  }
}

function accuracyToGraphData(res){
  // Converts a result array to a radar data array
  assert(typeof(res) == "object" && res.length > 0, "Invalid input data");
  let data = [];
  for(let i = 0; i < res.length; i++)
    data.push({axis: res[i].class, value: res[i].val});
  return data;
}

function getRadarConfig(size){
  let radarChartOptions = {
    // Defines the standard configuration of radar graphs
    margin: {top: 25, right: 25, bottom: 25, left: 25},
    maxValue: 0.5,
    levels: 5,
    roundStrokes: true,
    color: d3.scale.ordinal().range(["#EDC951","#CC333F","#00A0B0"])
  };
  radarChartOptions.w =  Math.min(size, window.innerWidth - 10) - radarChartOptions.margin.left - radarChartOptions.margin.right;
  radarChartOptions.h = Math.min(radarChartOptions.w, window.innerHeight - radarChartOptions.margin.top - radarChartOptions.margin.bottom - 20);
  return radarChartOptions;
}

function jQGetPromise(url, datatype = ""){
  // Promise for $.get 
  assert(isNotEmpty(url), "URL missing");
  return new Promise(function(resolve, reject){
    $.get(url, function(data){resolve(data)},datatype)
    .fail(function(data){
      reject("Error getting data from url " + url);
    });
  }).then(function(data){
    return data;
  });
}

function runGenerator(g) {
  //A simple ES6 runGenerator, handling tasks
  var it = g(), ret;
  var result = it.next();
  // asynchronously iterate over generator
  (function iterate(val){
    if (!result.done) {
      // poor man's "is it a promise?" test
      if ("then" in result.value) {                
        // resolve to a promise to make it easy
        let promise = Promise.resolve(result.value);
        promise.then(function(value) {
          result = it.next(value);
          iterate();
        }).catch(function(error) {
          console.log("Generator caught an error: " + error);
          result = it.next(null);//it.throw("Generator caught an error: " + error);
          iterate();
        });
      }
      // immediate value: just send right bk in
      else {
        // avoid synchronous recursion
        setTimeout( function(){
          iterate( result.value );
        }, 0 );
      }
    }
  })();
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

function notify(title, note, duration = 1000){
  //Prompts a browser notification and/or requests permission to do
  var got_permission = false;
  if ("Notification" in window) {
    if (Notification.permission === "granted") {
      got_permission = true;
    } else if (Notification.permission !== 'denied') {
      Notification.requestPermission((permission) => {
        if (permission === "granted")
          got_permission = true;
      });
    }
  }
  if(got_permission){
      title = title === "" ? getString('notif_title') : title;
      let options = {
          body: note,
          icon: '/images/sheep_logo.png',
      };
      let notification = new Notification(title, options);
      setTimeout(notification.close.bind(notification), duration); 
  }
}
