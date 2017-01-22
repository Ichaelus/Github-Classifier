
//########################################
//# GUI rendering and interaction engine #
//########################################

console.log("Frontend started..");
$.ajaxSetup({timeout: 14400000}); // Client waits for up to 4 hours for responses - retraining may take a while
// Initialize state and view objects
let stateView, inputView, classifierView, outputView, wrapperView, footerView,
	stateData = {
		action: "halt",
    flag: "",
		formula: "",
		formulas: [],
    isSemiSupervised: false,
    mode: "test", // stream, pool, test, single
    poolSize: 0,
    predictionHandling: "predict", // predict | feedback
    retrainAllState: "Retrain all classifers",
    saveAllState: "Save all classifers",
    trainInstantly: false,
    useExtendedTestSet: true
	},
  inoutData = {
    classifiers: {}, //{name : {active, description, isTrained, uncertainty, confusionMatrix: {matrix:[[],..], order: [class1,..n]},precision: [{class, val},..], probability : [{class, val},..]}, ...}
    classifierAsking: "",
    classifiersUnsure: false,
    isPrediction: true,
    manualClass: "?",
    repo: {repoName: "",repoAPILink: "",author: "",description: "",file_count: 0,folder_count: 0,commit_count: 0, language: ""},
    semisupervised: {"SemiSupervisedSureEnough" : true, "SemiSupervisedLabel": "None"},
    selectedMeasure: "",
    state: "empty", // empty, xy, showResult
    TestDistribution: [] // same as above, but fixed to test
  },
  wrapperData = {
    // Data used by the wrapper shown when displaying the detailed page
    activeMember: "andreas",
    currentName: "",
    current: {description: "", active: false, uncertainty: 0, confusionMatrix: {}, precision: {}, probability: {}},
    distribution: "Test", // Test, Train
    distributionArray: [], // [{class, count},..]
    documentationContent: "",
    documentations: [], // ["filename1",..]
    expression: "neutral",
    exprState: "",
    id: 0,
    loadstate: "Load version",
    numStats: {},
    thinking: false,
    retrainstate: "Retrain from scratch",
    semiretrainstate: "Retrain with semi-supervised data",
    savePoints: {}, // fileName: {precision: [{class, val}, ..]}
    savestate: "Save current image",
    selectedDocumentation: "Chose documentation",
    selectedPoint: "Version",
    selectedTable: 'unlabeled',
    strStats: {},
    tableList: ["semi_supervised", "standard_test_samples", "standard_train_samples", "test", "to_classify", "train", "unlabeled"]
  },
  footerData = {
    andreas: {
      degree: "Computer Science and Multimedia Computing BSC",
      //expertise: "",
      name: "Andreas Grafberger",
      term: "3."
    },
    martin: {
      degree: "Computer Science BSC",
      //expertise: "",
      name: "Martin Keßler",
      term: "5."
    },
    michael: {
      degree: "Computer Science and Multimedia Computing BSC",
      //expertise: "Web stack, Frontend development and server maintenance",
      name: "Michael Leimstädtner",
      term: "5."
    },
    stefan:{
      degree: "Computer Science BSC",
      //expertise: "",
      name: "Stefan Grafberger",
      term: "5."
    }

  };

// Kickstarting methods. Load classifiers and startup View

try{
	runGenerator(function *main(){
		let initData = yield jQGetPromise("/get/classifiers", "json");
    Vue.set(inoutData, "classifiers", initData.classifiers);
    if(Object.keys(initData.classifiers).length > 0)
      Vue.set(wrapperData, "current", initData.classifiers[Object.keys(initData.classifiers)[0]]); // Set "current" to dummy variables
    setInititalProbability();
		initVue();
    $("#page").fadeIn();
    $('[data-toggle="tooltip"]').tooltip();
	});
}catch(ex){
	console.log(ex);
}

function setInititalProbability(){
  // Fill classifier probabilities with according values or zeros
  let cd = inoutData.classifiers;
  for(let c in cd){
    assert(typeof(cd[c].precision) != "undefined", "Object missing");
    cd[c].probability = [];
    for(let j = 0; j < cd[c].precision.length; j++){
      cd[c].probability[j] = {class : cd[c].precision[j].class, val : 0.0};
    }
  }
}

function getStateQuery(){
  // Converts the stateData object to a query string to be passed <as it is> to the Python backend
	let query = "?";
	var keys = Object.keys(stateData);
	for(var i = 0; i < keys.length; i++){
	  if(typeof(stateData[keys[i]]) == "string" || typeof(stateData[keys[i]]) == "boolean")
	  	query += keys[i] + "=" + encodeURIComponent(stateData[keys[i]]) + "&";
	}
	return query;
}

function initVue(){
  // Init Vue components (state, title, input, classifiers, output, wrapper, footer)
  assert(typeof(Vue) != "undefined", "Vue script missing");
  stateView = new Vue({
    // Methods regarding the heading / controlling section
    el: '#header',
    data: stateData,
    methods:{
    	getFormulas: function(){
        // Refreshes list of available formulas
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
        // Choses formula <f> to be selected
    		assert(isNotEmpty(f) && stateData.formulas.indexOf(f) >= 0, "Formula should not be empty");
    		Vue.set(stateData, "formula", f);
    	},
      switchMode: function(){
        // Reacts on a basic mode change
        stateView.resetView();
        Vue.set(inoutData, "isPrediction", stateData.mode == 'test');
        outputView.switchMode(stateData.mode);
        Vue.set(inoutData, "state", "empty");
        if(stateData.mode == 'test')
          wrapperView.getDistributionArray();
      },
		  singleStep: function(){
        // Proceeds a single step (play button) action.
  			console.log("Proceeding single step");
        stateView.loop("single");
  		},
  		halt: function(){
        // Prevents the AL loop from continuing
  			Vue.set(stateData, "action", "halt");
  			console.log("Halting");
  		},
  		loop: function(type){
        // Performs single AL steps until halted
  			Vue.set(stateData, "action", "loop");
  			console.log("Looping");
        stateView.resetView();
  			runGenerator(function *main(){
  				// Fetch sample, display then repeat until stateData has changed
          let skipped = 0;
          Vue.set(inoutData, "state", "Searching..");
          while(stateData.action == "loop"){
            skipped++;
  					results = yield jQGetPromise("/get/doSingleStep"+getStateQuery(), "json");
  					stateView.updateResults(results);
            if(results.classifiersUnsure){
              if(type == "single")
                Vue.set(stateData, "action", "halt"); // Halt and do not loop again
              else
                Vue.set(stateData, "action", "halt_loop"); // Halt until classified
            }else
              Vue.set(inoutData, "state", "Skipped " + skipped + " samples.");
  				}
  			});
  		},
  		updateResults: function(results){
        // Apply returned changes to the internal GUI state
        // classifiers: { moduleName => {attr_changed: val_changed,..},...}
        assert(results != null, "Result is not well-formatted.");

        if(typeof(results.repo) != "undefined"){
          Vue.set(inoutData, "repo", results.repo);
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

        if(typeof(results.classifiers != "undefined"))
          stateView.updateClassifiers(results.classifiers);
        Vue.set(inoutData, "state", "showResult");
  		},
      updateClassifiers: function(data){
        console.log("updating classifiers");
        // Update data regarding classifiers
        for(let c in inoutData.classifiers){ // c => classifier name
          if(typeof(data[c] != "undefined")){
            // classifier is not muted, update it's results
            for(let newkey in data[c])
              Vue.set(inoutData.classifiers[c], newkey, data[c][newkey]);
          }
        }
      },
      predictSingle: function(repoLink){
        // Predict a single sample identified by <repoLink>
        if(repoLink == "")
          repoLink = prompt("Please insert the link to a repository you wish to classify.");
        if(repoLink){
          try{
            resetOutput();
            repoLink = convertToApiLink(repoLink);
            runGenerator(function *main(){
              // Fetch sample, display
              results = yield jQGetPromise("/get/PredictSingleSample?repoLink="+repoLink, "json");
              if(typeof(results.error) !== 'undefined')
                notify("Error predicting sample", results.error, 2500);
              stateView.updateResults(results);
            });
          }catch(ex){
            notify("Error predicting sample", ex, 2500);
          }
        }
      },
      showListPrediction: function(){
        // Fades in the List prediction wrapper
        showWrapper("#predictionList_wrapper");
      },
      startTest: function(){
        // Tests each classifier on the predefined <testset>. This will take a while
        Vue.set(inoutData, "state", "Testing..");
        notify("Testing", "Every module is being tested on the selected test set. This may take a while.", 3000);
        runGenerator(function *main(){
          // Fetch sample, display
          results = yield jQGetPromise("/get/startTest?useExtendedTestSet="+stateData.useExtendedTestSet, "json");
          stateView.updateResults(results);
          notify("Testing", "Test results are available now.", 3000);
          Vue.set(inoutData, "state", "showResult");
        });
      },
      resetView: function(){
        // Reset classifiers, but keep precision
        for(let c in inoutData.classifiers){ // c => classifier name
            cf = inoutData.classifiers[c];
            for(let i in cf.probability)
              Vue.set(cf.probability[i], "val", 0.0);
            Vue.set(cf, "uncertainty", 0);
        }
        Vue.set(inoutData, "classifiersUnsure", false);
      },
      retrainAll: function(){
        // Retrains <ands saves> <every|untrained> classification modules.
        let all = !confirm("Would you like to retrain only untrained classifiers?");
        let save = confirm("Would you like to save the retrained classifiers to the disk?");
        notify("Retrain all classifers", "Retraining many classifiers. This may take a couple of minutes; you may keep an eye on the console output.");
        for(let c in inoutData.classifiers)
          if(all || !inoutData.classifiers[c].isTrained)
            wrapperView.retrain(c, save);
      },
      saveAll: function(){
        // Saves every classification module
        notify("Saving all classifiers", "Every classifier is being saved to disk.");
        for(let c in inoutData.classifiers)
          wrapperView.save(c);
      },
      getStats: function(callback){
        // Updates statistics for the <selectedTable> and runs <callback> on success
        runGenerator(function *main(){
          numStats = yield jQGetPromise("/get/stats?table="+wrapperData.selectedTable+"&string_attrs=false", "json");
          strStats = yield jQGetPromise("/get/stats?table="+wrapperData.selectedTable+"&string_attrs=true", "json");
          Vue.set(wrapperData, "numStats", numStats);
          Vue.set(wrapperData, "strStats", strStats);
          callback();
        });
      },
      showStats: function(){
        // Displays the statistics wrapper when loaded
        stateView.getStats(function(){
          showWrapper('#stats_wrapper');
        });
      },
      showDocumentationWrapper: function(){
        // Fades in the documentation wrapper
        wrapperView.changeDocumentation("Documentation.md");
        showWrapper('#docs_wrapper');
      },
      changeExtendedSet: function(){
        // updates the sample distribution array depending on <useExtendedTestSet>
        Vue.set(wrapperData, "distribution","Test");
        wrapperView.getDistributionArray();
      }
    }
  });/* stateView */
  stateView.getFormulas();

  titleView = new Vue({
    // A controller for methods regarding actions in the title section
    el: '#titles',
    data: stateData,
    methods: {
      getQuote: function(){
        // Returns the quote displayed on top of the page depending on the <mode>
        switch(stateData.mode){
          case "pool":
            return "<strong>Pool Based Active Learning</strong> selects the sample with the highest uncertainty out of a pool of unlabeled data as input. The uncertainty is being calculated (in turns) by a single classifier, marked in blue. There are currently <strong>"+stateData.poolSize+"</strong> samples in this pool.";
            break;
          case "test":
            return "The <strong>testing option</strong> runs each classifier against a predefined set of test samples, thus updating the confusion matrix and precision per class.";
            break;
          case "single":
            return "The <strong>single sample prediction</strong> method is used to test the outcome of the classifiers for a specified repository (identified by its URL).";
            break;
          default:
          case "stream": 
            return "<strong>Stream Based Active Learning</strong> selects a random sample out of a pool of unlabeled data as input. There are currently <strong>"+stateData.poolSize+"</strong> samples in this pool.";
            break;
        }
      },
      getPoolsize: function(){
        // Fetches the amount of samples located in the table <unlabeled>
        $.get("/get/poolSize", function(data){
          if(isNaN(data))
            throw new Error("Invalid server response");
          Vue.set(stateData, "poolSize", parseInt(data));
        });
      },
      checkAPICalls: function(){
        // Checks if the burned API calls reach a certain cap (4000). If yes, warn the user
        $.get("/get/getAPICalls", function(data){
          let calls = parseInt(data["calls"]);
          if(!isNaN(calls) && calls > 4000)
            Vue.set(stateData, "flag", "During the last hour, more than <b>"+calls+"</b> of GitHub's limited API calls have been used. You may not be able to classify userdefined repositories.");
          else
            Vue.set(stateData, "flag", "");
        }, "json");
      }
    }
  }); /* titleView */
  titleView.getPoolsize();
  titleView.checkAPICalls();
  setInterval(titleView.checkAPICalls, 120000);

  inputView = new Vue({
    // Methods and values regarding the input section
    el: '#input',
    data: inoutData,
    methods:{
      getClassifierAmount: function(){
        // Returns the amount of classifiers
        return Object.keys(inoutData.classifiers).length;
      }
    },
    computed:{
      shortDesc: function(){
        // Returns the short description of the input repo, limited to 200 signs
        return add3Dots(inoutData.repo.description, 200);
      },
      mode: function(){
        // Returns the <mode>
        return stateData.mode;
      }
    }
  });/* inputView */

  classifierView = new Vue({
    // Methods regarding the classifier section
    el: '#classifier_wrapper',
    data: inoutData,
    methods:{
      showInfo: function(name){
        // Display the information wrapper for the classifier <name>
        wrapperView.setData(name);
        wrapperView.getSavePoints();
        wrapperView.setSavePoint("Version");
        //RadarChart("#class_accuarcy_chart", [precisionToGraphData(wrapperData.current.precision)], getRadarConfig(700));
        showWrapper('#details_wrapper');
      },
      switchState: function(name){
        // Enables or disables classifier <name>
        let c = inoutData.classifiers[name];
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
        // Returns the maximum value for a class <either precision or probability>
        let max = 0;
        array = stateData.mode == "test" ? "precision" : "probability";
        if(typeof(inoutData.classifiers[id][array]) != "undefined")
          for(let i = 0; i < inoutData.classifiers[id][array].length; i ++)
            max = Math.max(max, inoutData.classifiers[id][array][i].val);
        return max;
      },
      isAsking: function(name){
        // Checks if the classifier <name> should be marked blue
        return stateData.mode == "pool" && inoutData.classifierAsking == name;
      },
      changeMeasure: function(measure){
        // Sets the <measure> to be selected
        Vue.set(inoutData, "selectedMeasure", measure);
      },
      getMeasureName: function(){
        // Returns the name of the selected measure
        return inoutData.selectedMeasure == "Preordered" ? "Fscore M" : inoutData.selectedMeasure;
      },
      getMeasure: function(c){
        // Returns the value of the current measure for classifier <c>
        return Math.round(c.confusionMatrix.measures[this.getMeasureName()] * 100);
      },
      getMeasureDescription: function(measure){
        // Returns a description for <measure>
        let descriptions = {"Preordered": "Internal order not sorted by any measure",
                            "Precision mu": "Agreement of the data class labels with those of a classifiers if calculated from sums of per-sample decisions",
                            "Fscore mu": "Relations between data’s positive labels and those given by a classifier based on sums of per-sample decisions (β = 0.5)",
                            "Error Rate": "The average per-class classification error",
                            "Recall M": "An average per-class effectiveness of a classifier to identify class labels",
                            "Average Accuracy": "The average per-class effectiveness of a classifier",
                            "Recall mu": "Effectiveness of a classifier to identify class labels if calculated from sums of per-sample decisions",
                            "Fscore M": "Relations between data’s positive labels and those given by a classifier based on a per-class average (β = 0.5)",
                            "Precision M": "An average per-class agreement of the data class labels with those of a classifiers"};
        if(typeof(descriptions[measure]) !== "undefined")
          return descriptions[measure];
        return "";
      }
    },
    computed:{
      orderedClassifiers: function(){
        // Returns an ordered list of classifiers [dict -> array]
        let ordered = inoutData.classifiers;
        // This is actualy not a copy but a reference, though no hurt is being done by adding stuff.
        for(let c in inoutData.classifiers)
          ordered[c].name = c;
        if(inoutData.selectedMeasure == "Preordered")
          // Don't change order
          return _.values(ordered);
        else
          return _.orderBy(ordered, function(o){
            return o.confusionMatrix.measures[inoutData.selectedMeasure];
          }, "desc");
        },
      measures: function(){
        // Returns a list of measures available
        let _measures = ["Preordered"];
        _measures = _measures.concat(['Precision M','Recall M','Fscore M','Average Accuracy','Error Rate','Precision mu','Recall mu','Fscore mu']); // Hardcoded but with proper order
        /*if(Object.keys(inoutData.classifiers).length > 0)
          _measures = _measures.concat(Object.keys(inoutData.classifiers[Object.keys(inoutData.classifiers)[0]].confusionMatrix.measures));*/
        return _measures;
      },
      mode: function(){
        // Returns the current <mode>
        return stateData.mode;
      }
    }
  });/* classifierView */
  classifierView.changeMeasure(classifierView.measures[0]);

  outputView = new Vue({
    // Methods used in the output section
    el: '#output',
    data: inoutData,
    methods:{
      switchMode: function(mode){
        /* This would display an overlapped radar chart of classifier accuracies
          if(mode == "test"){
          let data = [];
          for(let c in inoutData.classifiers){
            data.push(precisionToGraphData(inoutData.classifiers[c].precision));
          }
          if(data.length > 0)
            RadarChart("#testOuputChart", data, getRadarConfig(350));
        }*/
      },
      getClassifierAmount: function(){return inputView.getClassifierAmount();},
      manualClassification: function(){
        // Opens a new window in order to let the user classify a sample manually
        if(inoutData.manualClass == '?')
          (function(window, undefined){
              var win = window.open("/user_classification.html?popup=true&api_url="+inoutData.repo.repoAPILink, '_blank');
              win.focus();
          })(window);
      },
      mapDistribution: function(data){
        // Maps each classifier to its best predicted class
        let maxProbs = _.values(_.mapValues(inoutData.classifiers,function(c){
          // Returns only the maximum key value pair
          return getClassifierMaximumClass(c[data]);
        }));
        let output = {}, total = 0;
        for(let p in maxProbs){
          if(typeof(output[maxProbs[p]]) == "undefined")
            output[maxProbs[p]] = {count: 0, percentage: 0, name: maxProbs[p]};
          output[maxProbs[p]].count ++;
          total++;
        }
        for(let i in output)
          output[i].percentage = total > 0 ? 100 * output[i].count / total : 0;
        return _.orderBy(output, "count", "desc");
      },
      getOutputClass: function(){
        // Returns the actual output predicted class
       return getClassifierMaximumClass(classifierView.orderedClassifiers[0].probability);
      },
      getMeasureDescription: function(m){ return classifierView.getMeasureDescription(m);}
    },
    computed: {
      predictionDistribution: function(){
        return this.mapDistribution("probability");
      },
      precisionDistribution: function(){
        return this.mapDistribution("precision");
      },
      outputMeasures: function(){
        return classifierView.orderedClassifiers[0].confusionMatrix.measures;
      },
      topMostName: function(){
        return classifierView.orderedClassifiers[0].name;
      },
      predictionHandling: function(){
        return stateView.predictionHandling;
      },
      mode: function(){
        return stateData.mode;
      }
    }
  });/* outputView */
  outputView.switchMode(stateView.mode);

  wrapperView = new Vue({
    // Methods used and triggered in one of the wrapper views
    el: '#wrappers',
    data: wrapperData,
    methods:{
      setData: function(classifierName){
        // Sets <classifierName> to be currently selected
        Vue.set(wrapperData, "current", inoutData.classifiers[classifierName]);
        Vue.set(wrapperData, "currentName", classifierName);
      },
      getSavePoints: function(){
        // Refreshes the list of savepoints for the currently selected classifier and displays its performace graph
        $.get("/get/savePoints?name="+wrapperData.currentName, function(resp){
          if(resp != ""){
            resp = JSON.parse(resp);
            if(resp === false)
              throw new Error("Invalid server response");
            Vue.set(wrapperData, "savePoints", resp.savepoints);
            let data = [];
            for(let sp in wrapperData.savePoints){
              data.push(precisionToGraphData(wrapperData.savePoints[sp].precision));
            }
            if(data.length > 0){
              RadarChart("#version_precision_chart", data, getRadarConfig(500));
              document.getElementById('version_chart_header').style.display = "block";
            }else
              document.getElementById("version_precision_chart").style.display = "none";
              document.getElementById("version_chart_header").style.display = "none";
            $('[data-toggle="tooltip"]').tooltip();
          }
        });
      },
      setSavePoint: function(fileName){
        // Confirm and remember savePoint selection by the user
        Vue.set(wrapperData, "selectedPoint", fileName);
      },
      retrain: function(name, save){
        // Retrain classifier <name> and <save> it optionally.
        console.log("Wrapper: "+name+" retraining.");
        Vue.set(wrapperData, "retrainstate", "Retraining..");
        notify("Retraining", "The classifier: "+name+" started retraining. This could take a while.", 2500);
        runGenerator(function *main(){
          let data = yield jQGetPromise("/get/retrain?name="+name + "&useExtendedTestSet="+stateData.useExtendedTestSet);
          if(JSON.parse(data) != false){
            data = JSON.parse(data);
            stateView.updateClassifiers(data.classifiers);
            notify("Retrained successfull", "The classifier: "+name+" finished retraining", 2500);
            if(save)
              wrapperView.save(name);
          }else{
            notify("Error while retraining", data, 2500);
          }
          Vue.set(wrapperData, "retrainstate", "Retrain from scratch");
        });
      },
      retrain_semi: function(name){
        // Retrain classifier <name> with semi supervised data
        console.log("Wrapper: "+name+" semi retraining.");
        Vue.set(wrapperData, "semiretrainstate", "Retraining..");
        runGenerator(function *main(){
          notify("Retrained", yield jQGetPromise("/get/retrainSemiSupervised?name="+name + "&useExtendedTestSet="+stateData.useExtendedTestSet.currentName), 2500);
          Vue.set(wrapperData, "semiretrainstate", "Retraining with semi-supervised data");
        });
      },
      save: function(name){
        // Save classifier <name> to disk
        console.log("Wrapper: "+name+" saving.");
        Vue.set(wrapperData, "savestate", "Saving..");
        runGenerator(function *main(){
          notify("Saved", yield jQGetPromise("/get/save?name="+name), 2500);
          wrapperView.getSavePoints();
          Vue.set(wrapperData, "savestate", "Save current image");
        });
      },
      load: function(){
        // Loads a selected savePoint for the current classifier
        console.log("Wrapper: "+wrapperData.currentName+" loading.");
        Vue.set(wrapperData, "loadstate", "Loading..");
        runGenerator(function *main(){
          data = yield jQGetPromise("/get/load?name="+wrapperData.currentName + "&savepoint="+wrapperData.selectedPoint + "&useExtendedTestSet="+stateData.useExtendedTestSet, "json");
          // data contains a name of the selected classifier and an precision array
          if(typeof(data.Error) != "undefined"){
            notify("Error", data.Error, 2500);
           }else{ 
            stateView.updateClassifiers(data.classifiers);
            notify("Loaded", "The classifier "+wrapperData.currentName+" has been loaded.", 2500);
          }
          Vue.set(wrapperData, "loadstate", "Load version");
        });
      },
      getMatrixDiag: function(matrix){
        // Returns the elements on the diagonal of the confusion matrix
        if(typeof(matrix) !== "undefined")
          return matrix.map(function(val, rowInd) {return val.filter( function(cell, colInd) {return rowInd == colInd})[0];});
      },
      arrayRowSum: function(array){
        // Returns an array containing the row based sum of <array>
        if(typeof(array) !== "undefined")
          return array.reduce(function(pv, cv) { return parseInt(pv) + parseInt(cv); }, 0);
      },
      arrayColSum: function(array, i){
        // Returns an array containing the col based sum of <array>
        if(typeof(array) !== "undefined")
          return array.reduce(function(prevRow, actRow, actIndex) { 
            return prevRow == 0 ? actRow[i] : parseInt(prevRow[i]) + parseInt(actRow[i]);
          }, 0);
      },
      formatStats: function(stats){
        // Format statistic attribute names and values. 
        let attrs = {};
        for(let i in stats){
          let attrName = i.substr(10, i.length - 12);//ROUND(AVG(attrName))
          if(typeof(attrs[attrName]) === "undefined")
            attrs[attrName] = {};
          attrs[attrName][i.substr(6, 3)] = stats[i]; 
        }
        return attrs;
      },
      predictList: function(){
        // Predicts every repository listed in the <inputList> and displays its output line per line on the right side
        let list = document.querySelector("#inputList").value.split("\n");
        let to_append = "\n";
        document.querySelector("#outputList").value = "";
        runGenerator(function *main(){
          notify("List prediction", "List prediction started. Results will soon show up.")
          for (var i = 0; i < list.length; i++) {
            if(list[i].length > 0){
              Vue.set(wrapperData, "exprState", "Processing " + list[i]);
              try{
                Vue.set(wrapperData, "expression", "neutral");
                Vue.set(wrapperData, "thinking", true);
                wrapperView.keepThinking();
                repoLink = convertToApiLink(list[i]);
                results = yield jQGetPromise("/get/PredictSingleSample?repoLink="+repoLink, "json");

                if(typeof(results.error) !== 'undefined'){
                  notify("Error predicting sample", results.error, 2500);
                  throw new Error(results.error);
                }else{
                  stateView.updateResults(results);
                  Vue.set(wrapperData, "thinking", false);
                  to_append = list[i] + " " + outputView.getOutputClass() + "\n";
                  Vue.set(wrapperData, "expression", "found");
                }
              }catch(err){
                Vue.set(wrapperData, "expression", "error");
                Vue.set(wrapperData, "thinking", false);
                to_append = "Invalid repository url or internal error\n";
                console.log(err);
              };
              document.querySelector("#outputList").value += to_append;
              yield wait_async(1000);
            }
          };
          Vue.set(wrapperData, "expression", "neutral");
          Vue.set(wrapperData, "exprState", "Finished processing list.");
        });
      },
      keepThinking: function(){
        // Switch between thinking images
        let i = 0;
        let interval = setInterval(
          function(){
            i++;
            if(!wrapperData.thinking)
              clearInterval(interval);
            else
              Vue.set(wrapperData, "expression", "thinking"+i%3)
        }, 1000);
      },
      getDistributionArray: function(){
        // Updates the distribution array for the test or train set
        $.get("/get/distributionArray?table="+wrapperData.distribution + "&useExtendedTestSet="+stateData.useExtendedTestSet, function(data){
          Vue.set(wrapperData, "distributionArray", _.sortBy(data, "class"));
          if(wrapperData.distribution == "Test")
            // Special variable because of permanent visibility in test mode
            Vue.set(inoutData, "TestDistribution", _.sortBy(data, "class"));
        }, "json");
      },
      changeDistribution: function(dist){
        // Switches between train and test set
        Vue.set(wrapperData, "distribution", dist);
        wrapperView.getDistributionArray();
      },
      changeDocumentation: function(docName){
        // Displays the file specified in <docName> 
        Vue.set(wrapperData, "selectedDocumentation", docName);
        $.get("/docs/"+docName, function(data){
          let converter = new showdown.Converter();
          Vue.set(wrapperData, "documentationContent", converter.makeHtml(data).replace(/<table>/g, "<table class='table table-bordered table-striped'>"));
        });
      },
      getDocumentationNames: function(){
        // Updates the list of documentation files available
        $.get("/get/documentationNames", function(data){
          Vue.set(wrapperData, "documentations", JSON.parse(data));
        });
      },
      getMeasureDescription: function(m){ return classifierView.getMeasureDescription(m);},
      showTeam: function(member){footerView.showTeam(member);},
      getMeasureName: function(){return classifierView.getMeasureName();},
      getMeasure: function(c){return classifierView.getMeasure(c);},
      formatFileName: function(fn){
        // Transforms filenames into a better readable format
        if(fn == "Version")
          return fn;
        try{
          // "2017-01-09T192504.535000.pkl" => "2017-01-09T19:25:04"
          let d = new Date(fn.substr(0, 13) + ":" + fn.substr(13, 2) + ":" + fn.substr(15, 2));
          return d.toLocaleString();
        }catch(ex){
          return fn;
        }
      },
      selectTable: function(table){
        // Switches to select <table>
        Vue.set(wrapperData, "selectedTable", table);
        stateView.getStats(function(){});
      }
    },
    computed: {
      topMostName: function(){
        return classifierView.orderedClassifiers[0].name;
      },
      mode: function(){
        return stateData.mode;
      },
      degree: function() { return footerData[wrapperData.activeMember].degree;},
      //expertise: function() { return footerData[wrapperData.activeMember].expertise;},
      name: function() { return footerData[wrapperData.activeMember].name;},
      term: function() { return footerData[wrapperData.activeMember].term;}
    }
  });/* wrapperView */
  
  footerView = new Vue({
    // Methods used in the footer of the page
    el: 'footer',
    data: footerData,
    methods: {
      showTeam: function(member){
        // Shows the team wrapper with focus on <member>
        Vue.set(wrapperData, "activeMember", member);
        showWrapper('#team_wrapper');
      }
    },
    computed:{
    }
  });/* footerView */
  
  wrapperView.getDistributionArray();
  wrapperView.getDocumentationNames();
}

function getClassifierMaximumClass(c){
  // Gets the class that being best predicted by classifier <c>
  return _.values(_.pick(_.maxBy(c, "val"), "class"))[0];
}

function wait_async(time){
  // Wait <time> milliseconds before continuing
  return new Promise(function(resolve, reject){
    setTimeout(function(){
      resolve();
    }, time);
  });
}

function hideInfo(){
  // Hide any visible popup
  $('.overlay_wrapper').fadeOut();
	$('.overlay_blur').fadeOut();
}

function showWrapper(elem){
  // Fades in the selected overlay
  if(document.querySelector('.overlay_blur').style.display == "none"){
    $('.overlay_blur').fadeIn();
    $(elem).css("margin-top", window.scrollY - 50);
    $(elem).fadeIn();
  }
}

function formatMeasure(m){
  // 0.03 => 3.0 %)
  return Math.round(m * 1000)/10 + "%";
}

function HandlePopupResult(result) {
  // If the sample has been labeled, update view
  console.log("result of popup is: ");
  console.log(result);
  setTimeout(function(){Vue.set(inoutData, "manualClass", result.label);}, 250);
  if(!result.skipped)
    $.get("/get/ALclassification"+getStateQuery()+"api_url="+result["api_url"]+"&label="+result.label, function(data){
      console.log(data);
    });
  setTimeout(function(){
    if(stateData.action == "halt_loop")
      stateView.loop();
  }, 1000);
}

function convertToApiLink(repoLink){
  // Converts a repo link an to api link. E.g. https://github.com/Ichaelus/Githubclassifier/ -> https://api.github.com/repos/Ichaelus/Githubclassifier/
  if(repoLink.indexOf("https://github.com/") >= 0){
    return trimRight(repoLink.replace("https://github.com/", "https://api.github.com/repos/", "/").trim(), "/");
  }else{
    throw new Error("RepoLink invalid");
  }
}

function originalMeasureName(m){
  // Transform "mu" to be an actual μ
  return m.replace(" mu", " μ");
}

function orderMeasures(measures){
  // Returns an ordered list of <measurs> 
  let ordered = [], _o = classifierView.measures;
  for(let i = 0; i < _o.length; i++)
    if(_o[i] != "Preordered")
      ordered.push([_o[i], measures[_o[i]]]);
  return ordered;
}

function resetOutput(){
  // Resets the output after a prediciton
  Vue.set(inoutData, "manualClass", "?");
}

function precisionToGraphData(res){
  // Converts a result array to a radar data array
  assert(typeof(res) == "object" && res.length > 0, "Invalid input data");
  let data = [];
  for(let i = 0; i < res.length; i++)
    data.push({axis: res[i].class, value: res[i].val});
  return data;
}

function getRadarConfig(size){
  // Defines the standard configuration of radar graphs
  let radarChartOptions = {
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
      notify("Internal exception", "Error getting data from url " + url, 3000);
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
function add3Dots(string, limit){
  // Transforms string to stri...
  var dots = "...";
  if(string.length > limit)  {
    // you can also use substr instead of substring
    string = string.substring(0,limit) + dots;
  }
  return string;
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


function trimRight(str, charlist) {
  // Trims specific chars from the right side of a string
  if (charlist === undefined)
    charlist = "\s";
  return str.replace(new RegExp("[" + charlist + "]+$"), "");
};