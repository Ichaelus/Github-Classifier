console.log("Frontend started..");
let stateView, inputView, classificatorView, outputView, wrapperView,
	stateData = {
		action: "halt",
		mode: "stream", // pool, test, single
		isSemiSupervised: false,
		trainInstantly: false,
		formula: "",
		formulas: []
	},
	inputData = {
		type: stateData.mode,
		repoName: "Repository Name",
    repoAPILink: "",
    classifiersUnsure: false,
    semisupervised: {"SemiSupervisedSureEnough" : true, "SemiSupervisedLabel": "None"},
    classifierAsking: "",
		poolSize: 0
	},
	classificatorData = {
    isPrediction: true,
		classificators: {} // name : {description, yield, active, uncertainty, result : [{class, val},..]}
	},
	outputData = {},
	wrapperData = {
    // Data used by the wrapper shown when displaying the detailed page
    currentName: "",
		current: {description: "", yield: 0, active: false, uncertainty: 0, result: {}},
    savePoints: {}, // fileName: {yield, result: [{class, val}, ..]}
    selectedPoint: "",
		id: 0
  },
  radarChartOptions = {
    // Defines the standard configuration of radar graphs
    margin: {top: 100, right: 100, bottom: 100, left: 100},
    maxValue: 0.5,
    levels: 5,
    roundStrokes: true,
    color: d3.scale.ordinal().range(["#EDC951","#CC333F","#00A0B0"]),
    init: function(){
      this.w =  Math.min(700, window.innerWidth - 10) - this.margin.left - this.margin.right,
      this.h = Math.min(this.w, window.innerHeight - this.margin.top - this.margin.bottom - 20)
    }
  }.init();

try{
	runGenerator(function *main(){
		let initData = yield jQGetPromise("/get/classificators", "json");
    classificatorData.classificators = initData.classificators;
		initVue();
	});
}catch(ex){
	console.log(ex);
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
    		$.get("/get/formulas", function(result){
    			result = JSON.parse(result);
    			if(result === false)
    				throw new Error("Invalid server response");
    			stateData.formulas = result;
    			if(result.length > 0)
    				stateData.formula = result[0];
    		});
    	},
    	setFormula: function(f){
    		assert(isNotEmpty(f) && stateData.formulas.indexOf(f) >= 0, "Formula should not be empty");
    		stateData.formula = f;
    	},
      switchMode: function(){
        stateView.resetView();
        classificatorData.isPrediction = stateData.mode == 'test';
      },
		  singleStep: function(){
  			stateData.action = "singleStep";
  			console.log("Proceeding single step");
        stateView.resetView();
        runGenerator(function *main(){
          // Fetch sample, display
          Vue.set(inputData, "repoName", "Searching..");
          results = yield jQGetPromise("/get/doSingleStep"+getStateQuery(), "json");
          stateView.updateResults(results);
        });
  		},
  		halt: function(){
  			stateData.action = "halt";
  			console.log("Halting");
        state.action = "halt";
  		},
  		loop: function(){
  			stateData.action = "loop";
  			console.log("Looping");
        stateView.resetView();
  			runGenerator(function *main(){
  				// Fetch sample, display then repeat until stateData has changed
  				while(stateData.action == "loop"){
            Vue.set(inputData, "repoName", "Searching..");
  					results = yield jQGetPromise("/get/doSingleStep"+getStateQuery(), "json");
  					stateView.updateResults(results);
            if(results.classifiersUnsure)
              stateData.action = "halt_loop";
  				}
  			});
  		},
  		updateResults: function(results){
        // Apply returned changes to the internal GUI state
        // classificators: { moduleName => {attr_changed: val_changed,..},...}
        assert(results != null, "Result is not well-formatted.");

        if(typeof(results.repo) != "undefined"){
          inputData.repoName = results.repo.repoName;
          inputData.repoAPILink = results.repo.repoAPILink;
        }
        if(stateData.mode == "stream"){
          inputData.classifiersUnsure = results.classifiersUnsure;
          inputData.semisupervised = results.semisupervised;
          if(results.classifiersUnsure)
            window.open("/user_classification.html?popup=true&api_url="+results.repo.repoAPILink, "User decision", "channelmode=yes");
        }else if(stateData.mode == "pool"){
          inputData.classifierAsking = results.classifierAsking;
        }

        if(typeof(results.classificators != "undefined"))
          stateView.updateClassificators(results.classificators);
  		},
      updateClassificators: function(data){
        // Update data regarding classificators
        for(let c in classificatorData.classificators){ // c => classificator name
          if(typeof(data[c] != "undefined")){
            // Classificator is not muted, update it's results
            for(let newkey in data[c])
              classificatorData.classificators[c][newkey] = data[c][newkey];
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
        Vue.set(inputData, "repoName", "Testing..");
        runGenerator(function *main(){
          // Fetch sample, display
          results = yield jQGetPromise("/get/startTest", "json");
          stateView.updateResults(results);
          Vue.set(inputData, "repoName", "Test result");
        });
      },
      resetView: function(){
        // Reset classificators
        for(let c in classificatorData.classificators){ // c => classificator name
            cf = classificatorData.classificators[c];
            for(let i in cf.result)
              Vue.set(cf.result[i], "val", 0.0);
            Vue.set(cf, "uncertainty", 0);
            console.log(cf);
        }
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
    data: inputData,
    methods:{
      switchMode: function(type){

      },
      getPoolsize: function(){
        $.get("/get/poolSize", function(result){
          if(isNaN(result))
            throw new Error("Invalid server response");
          inputData.poolSize = parseInt(result);
        });
      },
      getClassifierAmount: function(){
        return Object.keys(classificatorData.classificators).length;
      }
    }
  });
  inputView.getPoolsize();


  classificatorView = new Vue({
    el: '#classificators',
    data: classificatorData,
    methods:{
    	showInfo: function(name){
    		wrapperView.setData(name);
        wrapperView.getSavePoints();
        RadarChart("#class_accuarcy_chart", [resultToGraphData(wrapperData.current.result)], radarChartOptions);
    		$('.overlay_blur').fadeIn();
    		$('#overlay_wrapper').fadeIn();
    	},
    	switchState: function(name){
        let c= classificatorData.classificators[name];
        c.active = !c.active;
        if(!c.active){
          $.get("/get/mute?name="+name, function(result){
            if(result != "success")
                throw new Error("Invalid server response");
          });
        }else{
          $.get("/get/unmute?name="+name, function(result){
            if(result != "success")
                throw new Error("Invalid server response");
          });
        }
    	},
    	getMax: function(id){
    		let max = 0;
    		for(let i = 0; i < classificatorData.classificators[id].result.length; i ++){
    			max = Math.max(max, classificatorData.classificators[id].result[i].val);
    		}
    		return max;
    	},
      isAsking: function(name){
        return stateData.mode == "pool" && inputData.classifierAsking == name;
      }
      /*,
      updateSaveState: function(name, yield, classificatorResults){
        for(let i in classificatorData.classificators){
          if(i == name){
            let c = classificatorData.classificators[i];
            c.yield = yield <= 1 ? yield : yield/100;
            c.result = classificatorResults;
          }
        }
      }*/
    }
  });

  outputView = new Vue({
    el: '#output',
    data: outputData,
    methods:{
  		switchMode: function(type){

  		}
    }
  });

  wrapperView = new Vue({
    el: '#overlay_wrapper',
    data: wrapperData,
    methods:{
    	setData: function(i){
    		wrapperData.current = classificatorData.classificators[i];
        wrapperData.currentName = i;
    	},
      getSavePoints: function(){
        $.get("/get/savePoints?name="+wrapperData.currentName, function(result){
          if(result != ""){
            result = JSON.parse(result);
            if(result === false)
              throw new Error("Invalid server response");
            wrapperData.savePoints = result.savepoints;
            let data = [];
            for(let sp in wrapperData.savePoints){
              data.push(resultToGraphData(wrapperData.savePoints[sp].result));
            }
            if(data.length > 0)
              RadarChart("#version_accuarcy_chart", data, radarChartOptions);
          }
        });
      },
      setSavePoint: function(fileName){
        wrapperData.selectedPoint = fileName;
      },
  		retrain: function(){
  			console.log("Wrapper: "+wrapperData.currentName+" retraining.");
        notify("Retraining", "The classifier: "+wrapperData.currentName+" started retraining. This could take a while.", 2500);
        runGenerator(function *main(){
          let data = yield jQGetPromise("/get/retrain?name="+wrapperData.currentName);
          if(JSON.parse(data) != false){
            data = JSON.parse(data);
            stateView.updateClassificators(data.classificators);
            notify("Retrained successfull", "The classifier: "+wrapperData.currentName+" finished retraining", 2500);
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
  		save: function(){
  			console.log("Wrapper: "+wrapperData.currentName+" saving.");
        runGenerator(function *main(){
          notify("Saved", yield jQGetPromise("/get/save?name="+wrapperData.currentName), 2500);
          wrapperView.getSavePoints();
        });
  		},
  		load: function(){
  			console.log("Wrapper: "+wrapperData.currentName+" loading.");
        runGenerator(function *main(){
          result = yield jQGetPromise("/get/load?name="+wrapperData.currentName + "&savepoint="+wrapperData.selectedPoint, "json");
          // result contains a name of the selected classificator and an accuracy array
          if(typeof(result.Error) != "undefined"){
            notify("Error", result.Error, 2500);
           }else{ 
            stateView.updateClassificators(result.classificators);
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
  $.get("/get/ALclassification"+getStateQuery()+"api_url="+result["api_url"]+"&label="+result.label, function(result){
    console.log(result);
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

function resultToGraphData(res){
  // Converts a result array to a radar data array
  assert(typeof(res) == "object" && res.length > 0, "Invalid input data");
  let data = [];
  for(let i = 0; i < res.length; i++)
    data.push({axis: res[i].class, value: res[i].val});
  return data;
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
