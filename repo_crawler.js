/*
  Author: Michael Leimstädtner
  JQuery has to be accessible (like on stackoverflow)
  */
getRepos();

var client_id = prompt("Please insert your client id"),
    client_secret = prompt("Please insert your client secret"),
    oAuth = "client_id="+ client_id + "&client_secret=" + client_secret,
    min_feedback = 100; // # watches + stars + forks

function getRepos(){
  // Goes through a random list of repos and, if it fits our needs, adds them to a list
  console.log("Repocrawler started..");
  let max_id = 5 * Math.pow(10, 7), // GitHub's current repo amount -1 * 10**7, older repos are more likely to be complete
    id = Math.floor(Math.random() * max_id);
  
  runGenerator(function *main(){
     
      //yield Promise.all(actions);
     let repoList = yield jQGetPromise('https://api.github.com/repositories?since=' + id + "&" + oAuth, "json");
      console.log(repoList);
    let repo_urls = repoList.map(function(elem, i){
      return jQGetPromise(elem.url + "?" + oAuth, "json");
    });
    let repos = yield Promise.all(repo_urls);
    console.log(repos);
    let result = [],
        resultstring = "";
    for(let i = 0; i < repos.length; i++){
      if(parseInt(repos[i].stargazers_count) + parseInt(repos[i].watchers_count) + parseInt(repos[i].forks_count) >= min_feedback){
        result.push(repos[i]);
        resultstring += repos[i].html_url + "\n";
      }
    }
    console.log(result);
    alert(resultstring);
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

