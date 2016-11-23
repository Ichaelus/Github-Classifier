console.log("Frontend started..");
let stateView, inputView, classificatorView, outputView,
	stateData = {
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
		classificators: [
			{
				name: "Neural network",
				accuracy: "81",
				active: true,
				result: [
					{class: "DEV", val : 0.04},
					{class: "HW", val : 0.13},
					{class: "EDU", val : 0.11},
					{class: "DOCS", val : 0.24},
					{class: "WEB", val : 0.59},
					{class: "DATA", val : 0.02},
					{class: "OTHER", val : 0.04}
				]
			},
			{
				name: "Neural network",
				accuracy: "55",
				active: false,
				result: [
					{class: "DEV", val : 0.94},
					{class: "HW", val : 0.03},
					{class: "EDU", val : 0.01},
					{class: "DOCS", val : 0.04},
					{class: "WEB", val : 0.09},
					{class: "DATA", val : 0.02},
					{class: "OTHER", val : 0.04}
				]
			},
			{
				name: "Neural network",
				accuracy: "90",
				active: true,
				result: [
					{class: "DEV", val : 0.94},
					{class: "HW", val : 0.03},
					{class: "EDU", val : 0.01},
					{class: "DOCS", val : 0.04},
					{class: "WEB", val : 0.09},
					{class: "DATA", val : 0.02},
					{class: "OTHER", val : 0.04}
				]
			}
		]
	},
	outputData = {};

try{
	initVue();
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
			console.log("Single step");
		},
		halt: function(){
			console.log("Halting");
		},
		loop: function(){
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
    		$('.overlay_blur').fadeIn();
    		$('.overlay_wrapper').fadeIn();
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
}

function hideInfo(){
	// Hide any visible popup
	$('.overlay_wrapper').fadeOut();
	$('.overlay_blur').fadeOut();
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