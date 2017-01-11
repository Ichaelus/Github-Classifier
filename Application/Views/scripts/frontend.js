
//########################################
//# GUI rendering and interaction engine #
//########################################

console.log("Frontend started..");
let stateView, inputView, classifierView, outputView, wrapperView, footerView,
	stateData = {
		action: "halt",
		formula: "",
		formulas: [],
    isSemiSupervised: false,
    mode: "test", // stream, pool, test, single
    poolSize: 0,
    predictionHandling: "predict", // predict | feedback
    trainInstantly: false,
    useExtendedTestSet: false
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
    thinking: false,
    savePoints: {}, // fileName: {precision: [{class, val}, ..]}
    selectedDocumentation: "Chose documentation",
    selectedPoint: "Version",
    selectedTable: 'unlabeled',
    tableList: ["semi_supervised", "standard_test_samples", "standard_train_samples", "test", "to_classify", "train", "unlabeled"],
    numStats: {},
    strStats: {},
    id: 0
  },
  footerData = {
    andreas: {
      degree: "Computer Science and Multimedia Computing BSC",
      expertise: "",
      name: "Andreas Grafberger",
      term: "3."
    },
    martin: {
      degree: "Computer Science and Mathematics BSC",
      expertise: "",
      name: "Martin Keßler",
      term: "5."
    },
    michael: {
      degree: "Computer Science and Multimedia Computing BSC",
      expertise: "Web stack, Frontend development and server maintenance",
      name: "Michael Leimstädtner",
      term: "5."
    },
    stefan:{
      degree: "Computer Science and Mathematics BSC",
      expertise: "",
      name: "Stefan Grafberger",
      term: "5."
    }

  };

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
	let query = "?";
	var keys = Object.keys(stateData);
	for(var i = 0; i < keys.length; i++){
	  if(typeof(stateData[keys[i]]) == "string" || typeof(stateData[keys[i]]) == "boolean")
	  	query += keys[i] + "=" + encodeURIComponent(stateData[keys[i]]) + "&";
	}
	return query;
}

function initVue(){
  // Init Vue components (state, input, classifiers, output)
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
        Vue.set(inoutData, "state", "empty");
        if(stateData.mode == 'test')
          wrapperView.getDistributionArray();
      },
		  singleStep: function(){
  			Vue.set(stateData, "action", "singleStep");
  			console.log("Proceeding single step");
        stateView.resetView();
        runGenerator(function *main(){
          // Fetch sample, display
          Vue.set(inoutData, "state", "Searching..");
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
          let skipped = 0;
          Vue.set(inoutData, "state", "Searching..");
          while(stateData.action == "loop"){
            skipped++;
  					results = yield jQGetPromise("/get/doSingleStep"+getStateQuery(), "json");
  					stateView.updateResults(results);
            if(results.classifiersUnsure)
              Vue.set(stateData, "action", "halt_loop");
            else
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
        if(repoLink == "")
          repoLink = prompt("Please insert the link to a repository you wish to classify.");
        if(repoLink){
          try{
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
        showWrapper("#predictionList_wrapper");
      },
      startTest: function(){
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
        let all = !confirm("Would you like to retrain only untrained classifiers?");
        let save = confirm("Would you like to save the retrained classifiers to the disk?");

        notify("Retrain all classifers", "Retraining many classifiers. This may take a couple of minutes; you may keep an eye on the console output.");
        for(let c in inoutData.classifiers)
          if(all || !inoutData.classifiers[c].isTrained)
            wrapperView.retrain(c, save);
      },
      saveAll: function(){
        notify("Saving all classifiers", "Every classifier is being saved to disk.");
        for(let c in inoutData.classifiers)
          wrapperView.save(c);
      },
      getStats: function(callback){
        runGenerator(function *main(){
          numStats = yield jQGetPromise("/get/stats?table="+wrapperData.selectedTable+"&string_attrs=false", "json");
          strStats = yield jQGetPromise("/get/stats?table="+wrapperData.selectedTable+"&string_attrs=true", "json");
          Vue.set(wrapperData, "numStats", numStats);
          Vue.set(wrapperData, "strStats", strStats);
          callback();
        });
      },
      showStats: function(){
        // Fetch sample, display
        stateView.getStats(function(){
          showWrapper('#stats_wrapper');
        });
      },
      showDocumentationWrapper: function(){
        showWrapper('#docs_wrapper');
      },
      changeExtendedSet: function(){
        Vue.set(wrapperData, "distribution","Test");
        wrapperView.getDistributionArray();
      }
    }
  });/* stateView */
  stateView.getFormulas();

  titleView = new Vue({
    el: '#titles',
    data: stateData,
    methods: {
      getQuote: function(){
        switch(stateData.mode){
          case "pool":
            return "<strong>Pool Based Active Learning</strong> selects the sample with the highest uncertainty out of a pool of unlabeled data as input. The uncertainty is being calculated (in turns) by a single classifier, marked in blue. There are currently <strong>"+stateData.poolSize+"</strong> samples in this pool.";
            break;
          case "test":
            return "The <strong>testing option</strong> runs each classifier against a predefined set of test samples, thus updating the confusion matrix and precision per class.";
            break;
          case "single":
            return "The <strong>single sample prediction</strong> method is used to test the outcome of the classifiers for specified a repository (identified by its URL).";
            break;
          default:
          case "stream": 
            return "<strong>Stream Based Active Learning</strong> selects a random sample out of a pool of unlabeled data as input. There are currently <strong>"+stateData.poolSize+"</strong> samples in this pool.";
            break;
        }
      },
      getPoolsize: function(){
        $.get("/get/poolSize", function(data){
          if(isNaN(data))
            throw new Error("Invalid server response");
          Vue.set(stateData, "poolSize", parseInt(data));
        });
      }
    }
  }); /* titleView */
  titleView.getPoolsize();

  inputView = new Vue({
    el: '#input',
    data: inoutData,
    methods:{
      getClassifierAmount: function(){
        return Object.keys(inoutData.classifiers).length;
      }
    },
    computed:{
      shortDesc: function(){
        return add3Dots(inoutData.repo.description, 200);
      },
      mode: function(){
        return stateData.mode;
      }
    }
  });/* inputView */

  classifierView = new Vue({
    el: '#classifier_wrapper',
    data: inoutData,
    methods:{
      showInfo: function(name){
        wrapperView.setData(name);
        wrapperView.getSavePoints();
        //RadarChart("#class_accuarcy_chart", [precisionToGraphData(wrapperData.current.precision)], getRadarConfig(700));
        showWrapper('#details_wrapper');
      },
      switchState: function(name){
        let c= inoutData.classifiers[name];
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
        array = stateData.mode == "test" ? "precision" : "probability";
        if(typeof(inoutData.classifiers[id][array]) != "undefined")
          for(let i = 0; i < inoutData.classifiers[id][array].length; i ++)
            max = Math.max(max, inoutData.classifiers[id][array][i].val);
        return max;
      },
      isAsking: function(name){
        return stateData.mode == "pool" && inoutData.classifierAsking == name;
      },
      changeMeasure: function(measure){
        Vue.set(inoutData, "selectedMeasure", measure);
      },
      getMeasureName: function(){
        return inoutData.selectedMeasure == "Preordered" ? "Precision mu" : inoutData.selectedMeasure;
      },
      getMeasure: function(c){
        return Math.round(c.confusionMatrix.measures[this.getMeasureName()] * 100);
      },
      getMeasureDescription: function(measure){
        let descriptions = {"Preordered": "Internal order not sorted by any measure",
                            "Precision mu": "Agreement of the data class labels with those of a classifiers if calculated from sums of per-text decisions",
                            "Fscore mu": "Relations between data’s positive labels and those given by a classifier based on sums of per-text decisions",
                            "Error Rate": "The average per-class classification error",
                            "Recall M": "An average per-class effectiveness of a classifier to identify class labels",
                            "Average Accuracy": "The average per-class effectiveness of a classifier",
                            "Recall mu": "Effectiveness of a classifier to identify class labels if calculated from sums of per-text decisions",
                            "Fscore M": "Relations between data’s positive labels and those given by a classifier based on a per-class average",
                            "Precision M": "An average per-class agreement of the data class labels with those of a classifiers"};
        if(typeof(descriptions[measure]) !== "undefined")
          return descriptions[measure];
        return "";
      }
    },
    computed:{
      orderedClassifiers: function(){
        let ordered = inoutData.classifiers;
        // This is actualy not a copy but a referency, though no hurt is being done but adding stuff.
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
        let _measures = ["Preordered"];
        if(Object.keys(inoutData.classifiers).length > 0)
          _measures = _measures.concat(Object.keys(inoutData.classifiers[Object.keys(inoutData.classifiers)[0]].confusionMatrix.measures));
        return _measures;
      },
      mode: function(){
        return stateData.mode;
      }
    }
  });/* classifierView */
  classifierView.changeMeasure(classifierView.measures[0]);

  outputView = new Vue({
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
      getClassifierAmount: function(type){
        return Object.keys(inoutData.classifiers).length;
      },
      manualClassification: function(){
        if(inoutData.manualClass == '?')
          (function(window, undefined){
              var win = window.open("/user_classification.html?popup=true&api_url="+inoutData.repo.repoAPILink, '_blank');
              win.focus();
          })(window);
      },
      mapDistribution: function(data){
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

  function getClassifierMaximumClass(c){
    return _.values(_.pick(_.maxBy(c, "val"), "class"))[0];
  }
  outputView.switchMode(stateView.mode);

  wrapperView = new Vue({
    el: '#wrappers',
    data: wrapperData,
    methods:{
      setData: function(i){
        Vue.set(wrapperData, "current", inoutData.classifiers[i]);
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
              data.push(precisionToGraphData(wrapperData.savePoints[sp].precision));
            }
            if(data.length > 0){
              RadarChart("#version_precision_chart", data, getRadarConfig(600));
              document.getElementById('version_chart_header').style.display = "block";
            }else
              document.getElementById("version_precision_chart").style.display = "none";
              document.getElementById("version_chart_header").style.display = "none";
            $('[data-toggle="tooltip"]').tooltip();
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
        });
      },
      retrain_semi: function(){
        console.log("Wrapper: "+wrapperData.currentName+" semi retraining.");
        runGenerator(function *main(){
          notify("Retrained", yield jQGetPromise("/get/retrainSemiSupervised?name="+wrapperData + "&useExtendedTestSet="+stateData.useExtendedTestSet.currentName), 2500);
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
          data = yield jQGetPromise("/get/load?name="+wrapperData.currentName + "&savepoint="+wrapperData.selectedPoint + "=useExtendedTestSet="+stateData.useExtendedTestSet, "json");
          // data contains a name of the selected classifier and an precision array
          if(typeof(data.Error) != "undefined"){
            notify("Error", data.Error, 2500);
           }else{ 
            stateView.updateClassifiers(data.classifiers);
            notify("Loaded", "The classifier "+wrapperData.currentName+" has been loaded.", 2500);
          }
        });
      },
      getMatrixDiag: function(matrix){
        // Returns the elements on the diagonal of the confusion matrix
        if(typeof(matrix) !== "undefined")
          return matrix.map(function(val, rowInd) {return val.filter( function(cell, colInd) {return rowInd == colInd})[0];});
      },
      arrayRowSum: function(array){
        if(typeof(array) !== "undefined")
          return array.reduce(function(pv, cv) { return parseInt(pv) + parseInt(cv); }, 0);
      },
      arrayColSum: function(array, i){
        if(typeof(array) !== "undefined")
          return array.reduce(function(prevRow, actRow, actIndex) { 
            return prevRow == 0 ? actRow[i] : parseInt(prevRow[i]) + parseInt(actRow[i]);
          }, 0);
      },
      formatStats: function(stats){
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
          $.get("/get/distributionArray?table="+wrapperData.distribution + "&useExtendedTestSet="+stateData.useExtendedTestSet, function(data){
            Vue.set(wrapperData, "distributionArray", _.sortBy(data, "class"));
            if(wrapperData.distribution == "Test")
              // Special variable because of permanent visibility in test mode
              Vue.set(inoutData, "TestDistribution", _.sortBy(data, "class"));
          }, "json");
      },
      changeDistribution: function(dist){
        Vue.set(wrapperData, "distribution", dist);
        wrapperView.getDistributionArray();
      },
      changeDocumentation: function(docName){
        Vue.set(wrapperData, "selectedDocumentation", docName);
        $.get("/docs/"+docName, function(data){
          let converter = new showdown.Converter();
          Vue.set(wrapperData, "documentationContent", converter.makeHtml(data).replace(/<table>/g, "<table class='table'>"));
        });
      },
      getDocumentationNames: function(){
        $.get("/get/documentationNames", function(data){
          Vue.set(wrapperData, "documentations", JSON.parse(data));
          console.log(JSON.parse(data));
        });
      },
      getMeasureDescription: function(m){ return classifierView.getMeasureDescription(m);},
      showTeam: function(member){footerView.showTeam(member);},
      getMeasureName: function(){return classifierView.getMeasureName();},
      getMeasure: function(c){return classifierView.getMeasure(c);},
      formatFileName: function(fn){
        try{
          // "2017-01-09T192504.535000.pkl" => "2017-01-09T19:25:04"
          let d = new Date(fn.substr(0, 13) + ":" + fn.substr(13, 2) + ":" + fn.substr(15, 2));
          return d.toLocaleString();
        }catch(ex){
          return fn;
        }
      },
      selectTable: function(t){
        Vue.set(wrapperData, "selectedTable", t);
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
      expertise: function() { return footerData[wrapperData.activeMember].expertise;},
      name: function() { return footerData[wrapperData.activeMember].name;},
      term: function() { return footerData[wrapperData.activeMember].term;}
    }
  });/* outputView */
  
  footerView = new Vue({
    el: 'footer',
    data: footerData,
    methods: {
      showTeam: function(member){
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
  setTimeout(function(){Vue.set(inoutData, "manualClass", result.label)}, 250);
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
  // Converts a repo link to an api link. E.g. https://github.com/Ichaelus/Githubclassifier/ -> https://api.github.com/repos/Ichaelus/Githubclassifier/
  if(repoLink.indexOf("https://github.com/") >= 0){
    return trimRight(repoLink.replace("https://github.com/", "https://api.github.com/repos/", "/").trim(), "/");
  }else{
    throw new Error("RepoLink invalid");
  }
}

function originalMeasureName(m){
  return m.replace(" mu", " μ");
}

function precisionToGraphData(res){
  // Converts a result array to a radar data array
  assert(typeof(res) == "object" && res.length > 0, "Invalid input data");
  let data = [];
  for(let i = 0; i < res.length; i++)
    data.push({axis: res[i].class, value: res[i].val});
  return data;
}
1
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