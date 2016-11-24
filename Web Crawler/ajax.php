<?php
require('mysqli_class.php');
require("GitHandler.class.php");

$db = new MYSQL();
if(!$db->init()){ throw new Exception("Could not connect to the database");}

$apihandler = new GitHandler();

$header = 'Content-Type: text/html; charset=utf-8';
session_start();
ob_start();

function get_attr($name){
    // Returns an escaped GET attribute, if present
    global $db;
    if(isset($_GET[$name])){
        return $db->check($_GET[$name]);
    }else{
        return "";
    }
}

function post_attr($name){
    // Returns an escaped POST attribute, if present
    global $db;
    if(isset($_POST[$name])){
        return $db->check($_POST[$name]);
    }else{
        return "";
    }
}
try{
    // Handle GET Requests based on the `key` value
    if(isset($_GET['key'])){
        $getkey = $db->check($_GET['key']);
        if($getkey != ""){
            switch ($getkey) {
                case "todolist":
                    $todos = $db->select("SELECT `url` from `todo`");
                    print("[");
                    for ($i=0; $i < count($todos); $i++) { 
                        print('"'.$todos[$i]["url"] . '"'. ($i + 1 < count($todos) ? ", " : ""));
                    }
                    print("]");
                    break;
                case "api:all":
                    $filter = generate_filter();
                    $data = $db->select("SELECT * FROM `repositories` $filter");
                    print(json_encode($data));
                    break;
                case "api:old":
                    $filter = generate_filter();
                    $data = $db->select("SELECT * FROM `samples` $filter");
                    print(json_encode($data));
                    break;
                case "api:unlabeled":
                    $filter = generate_filter();
                    $data = $db->select("SELECT * FROM `repositories` WHERE `class` = 'UNLABELED'");
                    print(json_encode($data));
                    break;
                case "api:single":
                    $data = $db->select("SELECT * FROM `repositories` WHERE class != 'UNLABELED' AND class != 'SKIPPED'  AND class != 'UNSURE'  ORDER BY RAND() LIMIT 0, 1");
                    if(count($data) == 0)
                        throw new Exception("There is no classified sample.");
                    print(json_encode($data[0]));
                    break;
                case "api:single-unlabeled":
                case "api:single-unclassified":
                    $data = $db->select("SELECT * FROM `repositories` WHERE class = 'UNLABELED' LIMIT 0, 1");
                    if(count($data) == 0)
                        throw new Exception("There is no unclassified sample.");
                    print(json_encode($data[0]));
                    break;
                case "api:to-reclassify":
                    // Single classified repo, that is present in `samples` but not in `repositories`
                    $data = $db->select("SELECT s.url, s.class FROM `samples` s LEFT JOIN `repositories` r ON s.url = r.url WHERE r.id IS NULL AND s.class != 'UNLABELED' AND s.class != 'SKIPPED'  AND s.class != 'UNSURE' AND s.tagger != ''  ORDER BY s.id DESC LIMIT 0, 1");
                    if(count($data) == 0)
                        throw new Exception("There is no old classified sample.");
                    print(json_encode($data[0]));
                    break;
                case "api:equal":
                    $mdata = $db->select("SELECT COUNT(*) AS minimum FROM repositories GROUP BY class ORDER BY minimum LIMIT 0, 1");
                    $minimum = $mdata[0]["minimum"];
                    $class_equal_query = "SELECT
                                          repositories.*
                                        FROM
                                          repositories INNER JOIN (
                                            SELECT
                                              class,
                                              GROUP_CONCAT(id ORDER BY id DESC) grouped_id
                                            FROM
                                              repositories
                                            GROUP BY class) group_max
                                          ON repositories.class = group_max.class
                                             AND FIND_IN_SET(id, grouped_id) BETWEEN 1 AND $minimum
                                        ORDER BY
                                          repositories.class DESC";
                    $data = $db->select($class_equal_query);
                    print(json_encode($data));
                    break;
                case "api:class":
                    $class = get_attr("name");
                    $data = $db->select("SELECT * FROM `repositories` WHERE `class` = '$class'");
                    print(json_encode($data));
                    break;
                case "api:count":
                    $filter = generate_filter();
                    $data = $db->select("SELECT COUNT(*) AS count FROM `repositories` $filter");
                    print($data[0]["count"]);
                    break;
                case "api:class-count":
                    $data = $db->select("SELECT class, COUNT(*) AS count FROM `repositories` GROUP BY `class`");
                    print(json_encode($data));
                    break;
                case "api:tagger-class-count":
                    $additional = "";
                    if(get_attr("tagger") != "")
                        $additional .= "WHERE `tagger` = '".get_attr("tagger")."'";
                    $data = $db->select("SELECT class, COUNT(*) AS count FROM `repositories` $additional GROUP BY `class`");
                    print(json_encode($data));
                    break;
                case "api:generate_sample_url":
                    $credentials = $apihandler->getAPItoken(get_attr("client_id"), get_attr("client_secret"));
                    // Either use passed credentials or rotate through the list
                    if($credentials == false){
                        throw new Exception("API token missing.");
                    }else{
                        print generateSampleUrl();
                    }
                    break;
                case "api:generate_sample":
                    $credentials = $apihandler->getAPItoken(get_attr("client_id"), get_attr("client_secret"));
                    // Either use passed credentials or rotate through the list
                    if($credentials == false){
                        throw new Exception("API token missing.");
                    }else{
                        $url = trim(get_attr("api-url")) == "" ?  generateSampleUrl() : get_attr("api-url");
                        // Generate new sample url
                        $vector = generateRepoVector($url);
                        if(trim(get_attr("class")) != ""){
                            $vector["class"] = strtoupper(trim(get_attr("class")));
                        }
                        if($vector["url"] == ""){
                            throw new Exception("Something went wrong");
                        }
                        saveVector($vector);
                        $enc = json_encode($vector);
                        if($enc == false){
                            var_dump($vector);
                            throw new Exception("JSON could not be generated.");
                        }else{
                            print($enc);
                        }

                    }
                    break;
                default:
                    throw new Exception("Nothing in here.");
                    break;
            }//switch
        }
    }

    if(isset($_POST['key'])){
        // Handle POST Requests based on the `key` value
        $postkey = post_attr('key');
        if($postkey != ""){
            switch ($postkey) {
                case "unclassified":
                    // Add repo link only, to be classified
                    $iid = $db -> insert("INSERT INTO `todo` (url) VALUES ('".post_attr('api_url')."')");
                    print(is_numeric($iid) ? "success" : "error");
                    break;
                case "skip":
                    // Remove repo link
                    $db->query("UPDATE `repositories` SET `class` = 'SKIPPED' WHERE `id` = '".post_attr('id')."'");
                    break;
                case "classify":
                    // Classify a generated repo
                    $qID = $db->select("SELECT id FROM `repositories` WHERE `id` = '".post_attr('id')."'");
                    if(count($qID) != 0){
                        $query = "UPDATE `repositories` SET `class` = '".post_attr('class')."', `tagger` = '".post_attr('tagger')."' WHERE `id` = '".post_attr('id')."'";
                        $db->query($query);
                        print "Repository classified.";
                    }else{
                        print("error: sample not generated");
                    }
                    break;
                default:
                    print("Nothing in here.");
                    break;
            }//switch
        }
    }
}catch(Exception $e){
    print(json_encode(array("Error" => $e->getMessage())));
}

header($header);
ob_end_flush();

function generate_filter(){
    # Adds potential filters to the sql query
    # Also, check if the equal-class-amount flag is set
    global $db;
    $filter = "";
    $operators = array("=","<","<=",">=",">");
    $attributes = array("author","class","description","forks","id","languages","name","readme","stars","tree","url","watches");
    $q = base64_decode(get_attr("filter"));
    #print($q . "\n");
    if(strlen($q) > 0){
        $ANDs = explode(",",$q);
        foreach ($ANDs as $expr) {
            $operator = "";
            #print("EXPR" . "$expr\n");
            foreach ($operators as $op) {
                if(strpos($expr, $op) > 0){
                    $operator = $op;// Valid operation
                    break; // inner loop
                 }
            }
            #print("OP $operator\n");
            $tokens = explode($operator, $expr);
            // $tokens = ["className", "value1|value2"]
            if(count($tokens) == 2){
                $attrname = $tokens[0];
                $ORs = explode("|", $tokens[1]);
                $attrfilter = "";
                foreach ($ORs as $value) {
                    $attrfilter .= "`$attrname` $operator '".$db->check($value)."' OR ";
                }
                $attrfilter = rtrim($attrfilter, " OR ");
                if(in_array($attrname, $attributes)){
                    $filter .= " ( " . $attrfilter . " ) AND ";
                }
            }
        }
        $filter = rtrim($filter, " AND ");
        $filter = strlen($filter) > 0 ? "WHERE $filter" : "";
    }
    // Add other conditions
    /*
    $additional = "";
    if(get_attr("tagger") != "")
        $additional .= "AND `tagger` = '".get_attr("tagger")."'";
    $filter = strlen($filter) > 0 ? "$filter $additional " : "WHERE TRUE $additional";*/
    return $filter;
}

function generateSampleUrl(){
    // Get the API Url for a random Github repository
    global $apihandler, $db;
    $url = "https://api.github.com/repositories?since=" . rand(0, 5*pow(10, 7)) . "&" . $apihandler->getAPItoken();
    $repos = $apihandler -> getJSON($url);
    
    return $repos[rand(0, count($repos) - 1)]["url"];
}

function generateRepoVector($url){
    // Use the input-(api)-URL to generate a feature vector for the selected repository
    global $apihandler, $db;
    $repo = $apihandler->getJSON($url . "?" . $apihandler->getAPItoken());
    $ref_url_base = explode("{", $repo["git_refs_url"]);
    $commit_url_base = explode("{", $repo["commits_url"]);
    $git_refs = $apihandler -> getJSON($ref_url_base[0] . "?" . $apihandler->getAPItoken());
    $commmit_count = 0; $i = 1;
    $commits = array(); $commit_page = array(); // page = temporary variable
    do{
        $commit_page = $apihandler -> getJSON($commit_url_base[0] . "?page=".$i."&" . $apihandler->getAPItoken());
        $commit_count += count($commit_page);
        $commits = array_merge($commits, $commit_page);
        $i++;
    }while(count($commit_page)>0  && $i < 50);

    $avg_length = 1;
    $date_tuple = array();
    $commit_intervals = array(0);
    foreach ($commits as $c) {
        $avg_length += strlen($c["commit"]["message"]);
        $date_tuple[] = $c["commit"]["committer"]["date"];
        if(count($date_tuple) == 2){
            // Compare two commit dates and remove the oldest
            $d1 = new DateTime(array_shift($date_tuple));
            $d2 = new DateTime($date_tuple[0]);
            $commit_intervals[] = intval($d1->diff($d2)->format("%d")); // Subtract older (d1) from newer (d1) commit
        }

    }
    $avg_length = round($avg_length / count($commits));
    $ref_url = "";
    for($i = 0; $i < count($git_refs); $i++){
      if(strpos($git_refs[$i]["ref"], $repo["default_branch"]) >= 0){
        $ref_url = $git_refs[$i]["object"]["url"];
        break;
      }
    }
    if(trim($ref_url) == "")
      // Default branch is not available
      $ref_url = $git_refs[0]["object"]["url"];
    $branch =  $apihandler -> getJSON($ref_url . "?" . $apihandler->getAPItoken());
    $treeObj = $apihandler -> getJSON($branch["tree"]["url"] . "?" . $apihandler->getAPItoken());
    $languages = array_keys($apihandler -> getJSON($repo["languages_url"]. "?" . $apihandler->getAPItoken()));
    if($languages == null)
        $languages = array();
    $readme_exists = false;
    $folders = array(); $files = array();
    for($i = 0; $i < count($treeObj["tree"]); $i++){
        $readme_exists = $readme_exists || (strpos(strtolower($treeObj["tree"][$i]["path"]), "readme") >= 0);
        if($treeObj["tree"][$i]["type"] == "blob"){
            $files[] = $db->check($treeObj["tree"][$i]["path"]);
        }else{ // folder or commit
            $folders[] = $db->check(treeObj["tree"][$i]["path"]);
        }
    }

    $treeData = calcTree(isset($treeObj["tree"]) ? $treeObj["tree"] : null , $apihandler->getAPItoken());
    $readme = array("content"=> "", "encoding" => "none");
    if($readme_exists)
      $readme = $apihandler -> getJSON($repo["url"] . "/readme?" . $apihandler->getAPItoken());
    $contributors = $apihandler -> getJSON($repo["contributors_url"] . "?" . $apihandler->getAPItoken());
    $vector = array(
      "api_calls" => $apihandler->getCount(),
      "api_url" =>  $repo["url"],
      "author" =>  $db->check($repo["owner"]["login"]),
      "avg_commit_length" => $avg_length,
      "branch_count" =>  count($git_refs),
      "class" => "UNLABELED",
      "commit_count" => $commit_count,
      "commit_interval_avg"  => round(array_sum($commit_intervals) / count($commit_intervals)),
      "commit_interval_max" => max($commit_intervals),
      "contributors_count" =>  count($contributors),
      "description" =>  $repo["description"] != null ? $db->check($repo["description"]) : "",
      "files" => join(" ", $files),
      "file_count" => $treeData["file_count"],
      "folders" => join(" ", $folders),
      "folder_count" => $treeData["folder_count"],
      "forks" =>  $repo["forks_count"],
      "hasDownloads" => $repo["has_downloads"],
      "hasWiki" => $repo["has_wiki"],
      "isFork" => $repo["fork"],
      "open_issues_count" => $repo["open_issues_count"],
      "language_main" => $repo["language"] != null ? $db->check(repo["language"]) : (count($languages) == 0 ? "" : $db->check($languages[0])),
      "language_array" =>  join(" ", $languages),
      "name" =>  $db->check($repo["name"]),
      "readme" =>  $db->check($readme["content"]),
      "stars" =>  $repo["watchers_count"],
      "treeArray" =>  join(" ", $treeData["array"]), // String representation
      "treeDepth" =>  $treeData["depth"],
      "url" =>  $repo["html_url"],
      "watches" =>  $repo["subscribers_count"]

      // avg wortunterschied 
    );
    return $vector;
}

function calcTree($tree){
  // Get relevant information out of a tree of file and folder nodes
  global $apihandler, $db;
  $tree_result = array("depth" =>  0, "array" => array(), "file_count" => 0, "folder_count" => 0);
  if($tree != null)
      recTree($tree, $tree_result, "", 0, $apihandler->getAPItoken());
  return $tree_result;
}
function recTree($node, &$tree_result, $path, $depth){
  // Use every node as root, save paths (without filenames) in array
  global $apihandler, $db;
  $tree_result["array"][] = $db->check($path);
  $tree_result["depth"] = $depth > $tree_result["depth"] ? $depth : $tree_result["depth"];
  for($i = 0; $i < count($node); $i++){
    // Accumulate nodeArray + set depth
    if ($node[$i]["type"] != "blob"){
      $tree_result["folder_count"]++;
      if($tree_result["folder_count"] < 50){
          // don't exceed API limit
          $subtree = $apihandler -> getJSON($node[$i]["url"]  . "?" . $apihandler->getAPItoken());
          if(isset($subtree["tree"]))
            recTree($subtree["tree"],$tree_result, $path . '\\'. $node[$i]["path"], $depth + 1, $apihandler->getAPItoken());
        }
    }else{
      $tree_result["file_count"]++;
    }
  }
}

function saveVector(&$vector){
    // Save the feature vector as a new repository in the database
    global $db;
    if(count($db->select("SELECT * FROM `repositories` WHERE `url` = '".$vector['url']."'")) == 0){
        $keys =  "`" . join("`, `", array_keys($vector)) . "`";
        $values = "'" . join("', '", $vector) . "'";
        $query = "INSERT INTO `repositories` ( $keys ) VALUES ( $values )";
        //print $query;
        $iid = $db->insert($query);
        return $iid;
        //print(is_numeric($iid) ? "success" : "error");
    }else{
        throw new Exception("error: duplicate");
    }
}

?>