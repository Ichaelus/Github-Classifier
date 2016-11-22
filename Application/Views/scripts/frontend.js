console.log("Frontend started..");
let stateView, inputView, classificatorView, outputView,
	stateData = {
		mode: "stream",
		isSemiSupervised: false,
		trainInstantly: false,
		formula: "",
		formulas: []
	},
	inputData = {},
	classificatorData = {},
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

    	}
    }
  });

  classificatorView = new Vue({
    el: '#classificators',
    data: classificatorData,
    methods:{
    	showInfo: function(id){

    	},
    	switchState: function(id){

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