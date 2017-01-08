/*
  Author: Michael Leimstädtner
  JQuery has to be accessible
  */
console.log("Repocrawler started");
 
 // Global variables
 var qS = (query) => document.querySelector(query),
     converter = new showdown.Converter(), // display markdown
     liveView, buttons, // vue objects
     postData, goodRepos = [], oAuth = get_auth_tag(), // fetching objects + stacks
     initialized = false,
     min_feedback = 1,// # watches + stars + forks
     max_id = 5 * Math.pow(10, 7), // GitHub's current repo amount -1 * 10**7, older repos are more likely to be complete
     repoData = {
      author: "",
      user_url: "",
      name: "",
      url: "",
      stars: "",
      watchers: "",
      forks: "",
      language: "",
      description: "",
      commit_author: "",
      commit_msg: "",
      files: "",
      readme: "",
      tagger: get_name_tag()
    };

initButtons();
initVue();
getRepos();

function getRepos(){
  // Goes through a random list of repos and, if it fits our needs, adds them to a list
  console.log("Getting repos..");

  console.log(oAuth);
  tryNextIteration();

  runGenerator(function *main(){
    if(!initialized){
      // Add pending repos to list
      let todoList = yield jQGetPromise('ajax.php?key=todolist', "json");
      console.log(todoList);
      for(let i = 0; i < todoList.length; i++)
        yield addRepoByUrl(todoList[i]);
      initialized = true;
    }
    while(goodRepos.length < 3){
      // Buffering a few more
      let repoList = yield jQGetPromise('https://api.github.com/repositories?since=' + Math.floor(Math.random() * max_id) + "&" + oAuth, "json");
      console.log(repoList);
      let repo_urls = repoList.map(function(elem, i){
        return jQGetPromise(elem.url + "?" + oAuth, "json");
      });
      // Check each of the 100 Repos, filter out those who give an 453 or similar error
      let repos = yield Promise.all(repo_urls.map(p => p.catch(e => e)));
      for(let i = 0; i < repos.length; i++){
        if(parseInt(repos[i].subscribers_count) + parseInt(repos[i].watchers_count) + parseInt(repos[i].forks_count) >= min_feedback){
          console.log("Found a new repo ("+repos[i].url+")");
          goodRepos.push(repos[i]);
          $.post("ajax.php", {key: "unclassified", api_url : repos[i].url});
          // Remove following line to add > 1 per fetch. 
          // break prevents multiple repos of one author to be present
          break;
        }
      }
    }
    console.log("'good' repos: ");
    console.log(goodRepos);
  });
}
function addRepoByUrl(url){
  console.log("Adding single url to list: " + url);
  return new Promise(function(resolve, reject){
    runGenerator(function *main(){
      goodRepos.push(yield jQGetPromise(url + "?" + oAuth, "json"));
      resolve();
    });
  });
}
function tryNextIteration(){
  // If a preloaded repo is ready, remove it from the list and visualize it
  if(goodRepos.length > 0){
    runGenerator(function *main(){
      let repo = goodRepos.shift(), git_refs, ref_url = "", commit, treeObj;
      console.log("Iteration started with repo:");
      console.log(repo);
      try{
        git_refs = yield jQGetPromise(repo.git_refs_url.split("{")[0] + "?" + oAuth);

        for(let i = 0; i < git_refs.length; i++){
          if(git_refs[i].ref.indexOf(repo.default_branch) >= 0){
            ref_url = git_refs[i].object.url;
            break;
          }
        }
        if(ref_url == "")
          // Default branch is not available
          ref_url = git_refs[0].object.url;

        commit =  yield jQGetPromise(ref_url + "?" + oAuth);
        treeObj = yield jQGetPromise(commit.tree.url + "?" + oAuth);

        //repo["language"] // languages_url
        let readme_exists = false;
        let folderstring = "", fileString = "";
        for(let i = 0; i < treeObj.tree.length; i++){
          readme_exists = readme_exists || (treeObj.tree[i].path.toLowerCase().indexOf("readme") >= 0);
          let tmp = 
            '<div title="'+treeObj.tree[i].type+'" class="col-xs-12 '+treeObj.tree[i].type+'">\
                <div class="col-xs-12">'+treeObj.tree[i].path+'</div>\
                <div class="col-xs-0"></div>\
                <div class="col-xs-0"></div>\
            </div>';
            if(treeObj.tree[i].type == "blob")
              fileString += tmp;
            else // folder or commit
              folderstring += tmp;
        }
        treeData = yield* calcTree(treeObj.tree);

        let readme = {content: "", encoding : "none"};
        if(readme_exists)
          readme = yield jQGetPromise(repo.url + "/readme?" + oAuth);

        let contributors = yield jQGetPromise(repo.contributors_url + "?" + oAuth, "json"),
            contributors_count = contributors.length;

        // Update Page
        repoData = {
          author: repo.owner.login,
          user_url: repo.html_url.split(repo.name)[0],
          name: repo.name,
          url: repo.html_url,
          stars: repo.watchers_count,
          watchers: repo.subscribers_count,
          forks: repo.forks_count,
          language: repo.language,
          description: repo.description,
          commit_author: commit.committer.name,
          commit_msg: commit.message,
          files: folderstring + fileString,
          readme: readme.encoding == "base64" ?  converter.makeHtml(atob(readme.content)) : readme.content,
          tagger: repoData.tagger
        };
        postData = {
          api_url: repo.url,
          author: repoData.author,
          commit_count: git_refs.length,
          contributors_count: contributors_count,
          description: repoData.description,
          forks: repoData.forks,
          languages: repoData.language,
          name: repoData.name,
          readme: readme.content,
          stars: repoData.stars,
          tagger: repoData.tagger,
          //tree: JSON.stringify(treeObj.tree),
          treeArray: treeData.array.join(" "), // String representation
          treeDepth: treeData.depth,
          url: repoData.url,
          watches: repoData.watchers
        }

        updateVue();
      }catch(ex){
        // Error while fetching url
       /* skipRepo(repo.url);
        setTimeout(tryNextIteration, 50);*/
        console.log("iteration halted:" + ex);
      }
    });
  }else{
    console.log("No repository fits our needs.");
    setTimeout(tryNextIteration, 50);
  }
}

function* calcTree(tree){
  console.log("Calculating file tree");
  let r = { depth: 0, array: []}
  yield* recTree(tree, r, "", 0);
  console.log("File tree result");
  console.log(r);
  return r;
}
// Use every node as root, save paths (without filenames) in array
// r: return object
function* recTree(node, r, path, depth){
  r.array.push(path);
  r.depth = Math.max(r.depth, depth);
  for(let i = 0; i < node.length; i++){
    // Accumulate nodeArray + set depth
    if (node[i].type != "blob"){
      let subtree = yield jQGetPromise(node[i].url  + "?" + oAuth, "json");
      if(typeof subtree.tree != "undefined")
        yield* recTree(subtree.tree, r, path + "\\"+ node[i].path, depth + 1);
    }
  }
}


function initVue(){
  initButtons();
  liveView = new Vue({
    el: '#githubContent',
    data: repoData
  });
}
function updateVue(){
  // Update/Rerender every vue property
  for(let key in repoData)
    liveView[key] =repoData[key];
  $("#loading").fadeOut('fast', function() {
    $("#githubContent").fadeIn('fast');
  });
}
/* Following: Button handling functions */
function handleButton(btn) {
  if(Object.keys(repoData).length > 0){
    $("#githubContent").fadeOut('fast', function() {
      $("#loading").fadeIn('fast');
    });
    if($(btn).data("type") == "classify")
      classify($(btn).data("label"));
    else
      skipRepo();
  }else{
    notify("Status", "No repository is selected.")
  }
}
function classify(label){
    postData.key = "classify";
    postData.class = label;
    console.log(postData);
    $.post("/ajax.php", postData).then(
      function(result){
        if(result.indexOf("success") >= 0){
          notify("Status", "Classification submitted.");
        }else{
          notify("Status", "There was an error while trying to submit ("+result+").");
        }
        // Keep at least three repos buffered + get next liveView
        getRepos();
    });
}
function skipRepo(url = ""){
    if(url == "")
      url = postData.api_url;
    $.post("/ajax.php", {key: "skip", api_url: url}).then(
      function(result){
        notify("Status", "Classification skipped.");
        // Keep at least three repos buffered + get next liveView
        getRepos();
    });
}
function initButtons(){
   buttons = new Vue({
    el: '#buttons',
    components: {
      'cbutton': {
        props: ['vclick', 'vtitle', 'vname'],
        template: '<div><a v-bind:data-label="vname" v-bind:data-type="vclick" onClick="handleButton(this)" :title="vtitle">{{ vname }} <span class="badge">{{ count }}</span></a></div>',
        methods: {
        },
        data: function(){
          return {
            count: getCount(this.vname)
          };
        }
      }
    }
  });
}

function getCount(className){
  if(className.toLowerCase() == "skip")
    return "";
  let timestamp = localStorage.getItem("count_timestamp"),
      counts = localStorage.getItem("class_count");
  if(timestamp == null || parseInt(timestamp) + 1000 * 10 < $.now()){
    localStorage.setItem("count_timestamp", $.now());
    jQGetPromise("ajax.php?key=api:class-count&tagger="+repoData.tagger, "json").then(function(result){
      localStorage.setItem("class_count", JSON.stringify(result));
    });
  }
  if(counts != null){
    counts = JSON.parse(counts);
    for(let i = 0; i < counts.length; i++)
      if(counts[i]["class"] == className)
        return counts[i]["count"];
  }
  return 0;
}

function get_auth_tag(){
  let client_id = localStorage.getItem("client_id"),
      client_secret = localStorage.getItem("client_secret");
  if(client_id == null || client_secret == null){
    client_id = String.trim(prompt("Please insert your client id"));
    client_secret = String.trim(prompt("Please insert your client secret"));
    localStorage.setItem("client_id", client_id);
    localStorage.setItem("client_secret", client_secret);
  }
  oAuth = "client_id="+ client_id + "&client_secret=" + client_secret;
  return oAuth;
}

function get_name_tag(){
  let name_tag = localStorage.getItem("name_tag");
  if(name_tag == null){
    name_tag = String.trim(prompt("Please insert your name tag")).toLowerCase();
    localStorage.setItem("name_tag", name_tag);
  }
  return name_tag;
}
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
