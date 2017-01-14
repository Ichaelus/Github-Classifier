/*
  Author: Michael Leimstädtner
  JQuery has to be accessible
  */
console.log("Repocrawler started");
 
 // Global variables
 var qS = (query) => document.querySelector(query),
     backend = "ajax.php",
     liveView,
     initialized = false,
     min_feedback = 1,// # watches + stars + forks
     max_id = 5 * Math.pow(10, 7), // GitHub's current repo amount -1 * 10**7, older repos are more likely to be complete
     data = {
      minedAmount: 0
      };
function initVue(){
  liveView = new Vue({
    el: '#main',
    data: data
  });
}
function sampleMining(){
  // Requests the server to generate a random unlabeled sample. Once finished, request the next until no more API calls are available
  console.log("Mining unlabeled sample");
  $.get(backend+"?key=api:generate_sample").then(function(result){
    if( result != ""){
      result = JSON.parse(result);
      // Maybe out of old classifications
      if(result === false || !result.success){
        console.log(result);
        // Keep mining, but wait 5 minutes (API calls may be over)
        setTimeout(sampleMining, 300000);
      }else{
        Vue.set(data, "minedAmount", data.minedAmount + 1);
        setTimeout(sampleMining, 1000);
      }
    }else{
      setTimeout(sampleMining, 1000);
    }
  });
}

initVue();
sampleMining();

/*
  Prompts a browser notification and/or requests permission to do
 */
function notify(title, note){
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
      setTimeout(notification.close.bind(notification), 1000); 
  }
}
/*
  A simple ES6 runGenerator, handling tasks
 */
function runGenerator(g) {
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

/*
    Converts a function into a simple Promise
   */
function generalPromise(f, ...params){
  return new Promise( function(resolve, reject){
    let fnc = params.length > 0 ? f.bind(f, params, resolve) : f.bind(f, resolve);
    fnc();
  }).then(function(text=""){
    return text;
  });
}
  

/*
    $.get Promise
   */
function jQGetPromise(url, datatype = ""){
  return new Promise(function(resolve, reject){
    $.get(url, function(data){resolve(data)},datatype)
    .fail(function(data){
      reject("Error getting data from url " + url);
    });
  }).then(function(data){
    return data;
  });
}
