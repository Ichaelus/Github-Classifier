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
		poolSize: 0
	},
	classificatorData = {
    isPrediction: true,
		classificators: []
	},
	outputData = {},
	wrapperData = {
		name: "",
		description: "",
		id: 0
	};

try{
	runGenerator(function *main(){
		let initData = yield jQGetPromise("/get/classificators", "json");
    classificatorData.classificators = initData.classificators;
    inputData.repoName = initData.repoName;
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
    		assert(isNotEmpty(f), "Formula should not be empty");
    		stateData.formula = f;
    	},
      switchMode: function(){
        classificatorData.isPrediction = stateData.mode == 'test';
      },
		  singleStep: function(){
  			stateData.action = "singleStep";
  			console.log("Single step");
        runGenerator(function *main(){
          // Fetch sample, display
          inputData.repoName = "Searching..";
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
  			runGenerator(function *main(){
  				// Fetch sample, display then repeat until stateData has changed
  				while(stateData.action == "loop"){
            inputData.repoName = "Searching..";
  					results = yield jQGetPromise("/get/doSingleStep"+getStateQuery(), "json");
  					stateView.updateResults(results);
  					// To remove
  					stateData.action = "halt";
  				}
  			});
  		},
  		updateResults: function(results){
        assert(results != null && typeof(results.repoName) != "undefined" && typeof(results.classificatorResults) != "undefined", "Result is not well-formatted.");
        inputData.repoName = results.repoName;
  			for(let cid in results.classificatorResults){
  				for(let c in classificatorData.classificators)
  					if(classificatorData.classificators[c].id == cid)
  						classificatorData.classificators[c].result = results.classificatorResults[cid];
  			}
  		},
      predictSingle: function(){
        let repoLink = prompt("Please insert the link to a repository you wish to classify.");
        if(repoLink){
          runGenerator(function *main(){
            // Fetch sample, display
            results = yield jQGetPromise("/get/PredictSingleSample?repoLink="+repoLink, "json");
            stateView.updateResults(results);
          });
        }
      },
      startTest: function(){
        runGenerator(function *main(){
          // Fetch sample, display
          results = yield jQGetPromise("/get/startTest", "json");
          stateView.updateResults(results);
        });
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
      }
    }
  });
  inputView.getPoolsize();


  classificatorView = new Vue({
    el: '#classificators',
    data: classificatorData,
    methods:{
    	showInfo: function(id){
    		wrapperView.setData(id);
    		$('.overlay_blur').fadeIn();
    		$('#overlay_wrapper').fadeIn();
    	},
    	switchState: function(id){
    		classificatorData.classificators[id].active = !classificatorData.classificators[id].active;
    	},
    	getMax: function(id){
    		let max = 0;
    		for(let i = 0; i < classificatorData.classificators[id].result.length; i ++){
    			max = Math.max(max, classificatorData.classificators[id].result[i].val);
    		}
    		return max;
    	}
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
    		wrapperData.name = classificatorData.classificators[i].name;
    		wrapperData.description = classificatorData.classificators[i].description;
    	},
  		retrain: function(){
  			console.log("Wrapper: "+wrapperData.name+" retraining.");
        runGenerator(function *main(){
          results = yield jQGetPromise("/get/retrain?name="+wrapperData.name, "json");
        });
  		},
  		retrain_semi: function(){
  			console.log("Wrapper: "+wrapperData.name+" semi retraining.");
        runGenerator(function *main(){
          results = yield jQGetPromise("/get/retrainSemiSupervised?name="+wrapperData.name, "json");
        });
  		},
  		save: function(){
  			console.log("Wrapper: "+wrapperData.name+" saving.");
        runGenerator(function *main(){
          results = yield jQGetPromise("/get/save?name="+wrapperData.name, "json");
        });
  		},
  		load: function(){
  			console.log("Wrapper: "+wrapperData.name+" loading.");
        runGenerator(function *main(){
          results = yield jQGetPromise("/get/load?name="+wrapperData.name, "json");
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
      // immediate value: just send right back in
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