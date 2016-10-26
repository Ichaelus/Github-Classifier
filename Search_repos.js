/*
  Author: Michael Leimstädtner
  */

let max_id = 5 * Math.pow(10, 7), // GitHub's current repo amount -1 * 10**7, older repos are more likely to be complete
    id = Math.random(max_id);

function getRepos(){
  runGenerator(function *main(){
      //yield Promise.all(actions);
     let repoList = yield jQGetPromise('https://api.github.com/repositories?since=' + id, "json");
      alert("yay");
     console.log(repoList);
  });
}


/*
  A simple ES6 runGenerator, handling tasks
 */
function runGenerator(g) {
  var it = g(), ret;
  var result = it.next();
  // asynchronously iterate over generator
  (function iterate(val){
    //result = it.next( val );
    if (!result.done) {
      // poor man's "is it a promise?" test
      if ("then" in result.value) {                
        // resolve to a promise to make it easy
        let promise = Promise.resolve(result.value);
        promise.then(function(value) {
          result = it.next(value);
          iterate();
        }).catch(function(error) {
          result = it.throw(error);
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
    $.get(url, function(data){resolve(data)},datatype);
  }).then(function(data){
    return data;
  });
}

