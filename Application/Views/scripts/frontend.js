console.log("Frontend started..");
let stateView, inputView, classificatorView, outputView, wrapperView,
	stateData = {
		action: "halt",
		mode: "stream",
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
		classificatorData.classificators = yield jQGetPromise("/get/classificators", "json");
		initVue();
	});
}catch(ex){
	console.log(ex);
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
		singleStep: function(){
			stateData.action = "singleStep";
			console.log("Single step");
		},
		halt: function(){
			stateData.action = "halt";
			console.log("Halting");
		},
		loop: function(){
			stateData.action = "loop";
			console.log("Looping");
		}
    }
  });
  stateView.getFormulas();


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
    			inputData.poolSize = result;
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
    		wrapperData.id = classificatorData.classificators[i].id;
    		wrapperData.name = classificatorData.classificators[i].name;
    		wrapperData.description = classificatorData.classificators[i].description;
    	},
		retrain: function(){
			console.log("Wrapper: retraining.");
		},
		retrain_semi: function(){
			console.log("Wrapper: semi retraining.");
		},
		save: function(){
			console.log("Wrapper: saving.");
		},
		load: function(){
			console.log("Wrapper: loading.");
		},
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