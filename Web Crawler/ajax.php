    <?php
    require('mysqli_class.php');
    require("GitHandler.class.php");

    $db = new MYSQL();
    if(!$db->init()){ throw new Exception("Could not connect to the database");}

    $apihandler = new GitHandler();

    $header = 'Content-Type: text/html; charset=utf-8; Access-Control-Allow-Origin: *';
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
            if($getkey != "")
                handleGET($getkey);
        }
        if(isset($_POST['key'])){
            // Handle POST Requests based on the `key` value
            $postkey = post_attr('key');
            if($postkey != "")
                handlePOST($postkey);
        }
        report(false, "This is not a valid API call."); // this report() call will only be shown if no previous report() was made.
    }catch(Exception $e){
        report(false, "Exception catched: " . $e->getMessage());
    }

    header($header);
    ob_end_flush();

    function handleGET($getkey){
        global $apihandler, $db;
        $table = get_attr("table") != "" ? get_attr("table") : "train";
        $attrs = "`class`, `api_calls`, `api_url`, `author`, `avg_commit_length`, `branch_count`, `commit_count`, `commit_interval_avg`, `commit_interval_max`, `contributors_count`, `description`, `file_count`, `files`, `folders`, `folder_count`, `forks`, `hasDownloads`, `hasWiki`, `isFork`, `open_issues_count`, `language_main`, `language_array`, `name`, `readme`, `stars`, `tagger`, `treeArray`, `treeDepth`, `url`, `watches`";
        switch ($getkey) {
            case "api:old":
                // To be removed: returns the content of the old train set.
                $filter = generate_filter("(class != 'SKIPPED'  AND class != 'UNSURE') AND");
                $limitation = getLimitation();
                $data = $db->select("SELECT * FROM `_depr_samples` $filter $limitation");
                reportIf($data !== false, $data, "Database error.");
                break;
            case "api:all":
                // Return every sample of <table>
                $filter = generate_filter("(class != 'SKIPPED'  AND class != 'UNSURE') AND");
                $limitation = getLimitation();
                $data = $db->select("SELECT * FROM `$table` $filter $limitation");
                reportIf($data !== false, $data, "Database error.");
                break;
            case "api:train":
            case "api:test":
            case "api:unlabeled":
            case "api:to_classify":
            case "api:semi_supervised":
            case "api:standard_train_samples":
            case "api:standard_test_samples":
                // Returns a list of train samples
                $filter = generate_filter("(class != 'SKIPPED'  AND class != 'UNSURE') AND");
                $t = substr($getkey, 4);
                $limitation = getLimitation();
                $data = $db->select("SELECT * FROM `$t` $filter $limitation");
               // print "SELECT * FROM `train` $filter";
                reportIf($data !== false, $data, "Database error.");
                break;

            case "api:single":
                // Returns a random sample of the given <table>
                $data = $db->select("SELECT * FROM `$table` WHERE class != 'SKIPPED'  AND class != 'UNSURE'  ORDER BY RAND() LIMIT 0, 1");
                reportIf($data !== false && count($data) > 0, $data[0], "There is no classified sample.");
                break;
            case "api:equal":
                // Returns an equal amount of samples based on the class count of the given <table>
                $mdata = $db->select("SELECT COUNT(*) AS minimum FROM `$table` GROUP BY class ORDER BY minimum LIMIT 0, 1");
                if($mdata !== false && count($mdata) == 1){
                    $minimum = $mdata[0]["minimum"];
                    $class_equal_query = "SELECT
                                          `$table`.*
                                        FROM
                                          `$table` INNER JOIN (
                                            SELECT
                                              class,
                                              GROUP_CONCAT(id ORDER BY id DESC) grouped_id
                                            FROM
                                              `$table`
                                            GROUP BY class) group_max
                                          ON `$table`.class = group_max.class
                                             AND FIND_IN_SET(id, grouped_id) BETWEEN 1 AND $minimum
                                        ORDER BY
                                          `$table`.class DESC";
                    $data = $db->select($class_equal_query);
                    reportIf($data !== false, $data, "Database error");
                }else
                    report(false, "Table empty or database error");
                break;
            case "api:class":
                // Returns all samples of the given class <name>
                $class = get_attr("name");
                $data = $db->select("SELECT * FROM `$table` WHERE `class` = '$class'");
                reportIf($data !== false, $data, "Database error");
                break;
            case "api:count":
                // Returns the amount of data affected by <table> and <filter>
                $filter = generate_filter();
                $data = $db->select("SELECT COUNT(*) AS count FROM `$table` $filter");
                reportIf($data !== false && count($data) == 1, $data[0]["count"], "Result empty or database error");
                break;
            case "api:class-count":
                // Returns the a class-based count
                $filter = generate_filter();
                $data = $db->select("SELECT class, COUNT(*) AS count FROM `$table` $filter GROUP BY `class`");
                reportIf($data !== false, $data, "Database error");
                break;
            case "api:tagger-class-count":
                // Returns the a class-based count based on the <tagger> attribute
                $additional = "";
                if(get_attr("tagger") != "")
                    $additional .= "WHERE `tagger` = '".get_attr("tagger")."'";
                $data = $db->select("SELECT class, COUNT(*) AS count FROM `$table` $additional GROUP BY `class`");
                reportIf($data !== false, $data, "Database error");
                break;
            case "api:generate_sample_url":
                $credentials = $apihandler->getAPItoken(get_attr("client_id"), get_attr("client_secret"));
                // Either use passed credentials or rotate through the list
                reportIf($credentials !== false, generateSampleUrl(), "API token missing.");
                break;
            case "api:generate_sample":
                $credentials = $apihandler->getAPItoken(get_attr("client_id"), get_attr("client_secret"));
                // Either use passed credentials or rotate through the list
                if($credentials == false){
                    report(false, "API token missing.");
                }else{
                    $url = trim(get_attr("api_url")) == "" ?  generateSampleUrl() : get_attr("api_url");
                    $class = strtoupper(trim(get_attr("class")));
                    if(!isValidApiUrl($url))
                        throw new Exception("Invalid API url");
                    // Generate new sample url
                    $vector = generateRepoVector($url);
                    if(isValidLabel($class))
                        // Set class if given
                        $vector["class"] = $class;
                    if($vector["url"] == "")
                        throw new Exception("Something went wrong");
                    saveVector($vector);
                    reportIf(count($vector) > 0, $vector, "Vector seems to be broken");
                }
                break;
            case "api:move":
                // Move a repo, taken from the pool <from_table> to the pool <table2>. If <label> is set, overwrite label
                $t1 = strtolower(get_attr("from_table")); $t2 = strtolower(get_attr("to_table")); $l = strtoupper(get_attr("label")); $api_url = get_attr("api_url");
                if(isValidTable($t1) && isValidTable($t2) && isValidApiUrl($api_url)){
                    $qID = $db->select("SELECT id FROM `$t1` WHERE `api_url` = '$api_url'");
                    if(count($qID) != 0 && $t1 != "train"){
                        if($l != ""){ // Update label
                            if(!isValidLabel($l))
                                throw new Exception("Invalid lable");
                            $db->query("UPDATE `$t1` SET `class` = '$l' WHERE `api_url` = '$api_url'");
                        }
                        $iid = $db->insert("INSERT INTO `$t2` ($attrs) SELECT $attrs FROM `$t1` WHERE `api_url` = '$api_url'");
                        if($iid){
                            $db->query("DELETE FROM `$t1` WHERE `api_url` = '$api_url'");
                            $data = $db->select("SELECT * FROM `$t2` WHERE `api_url` = '$api_url'");
                            reportIf($data !== false && count($data) > 0, $data[0], "Database error");
                        }else
                            throw new Exception("Error moving row");
                    }else
                        throw new Exception("Sample not generated");
                }else
                    throw new Exception("Invalid Parameters");
                break;
                
            case "api:to-reclassify":
                // Single classified repo, that is present in `standard_train_samples` but not in `train`
                $data = $db->select("SELECT s.url, s.class FROM `standard_train_samples` s LEFT JOIN `train` r ON s.url = r.url WHERE r.id IS NULL AND s.class != 'UNLABELED' AND s.class != 'SKIPPED'  AND s.class != 'UNSURE'  ORDER BY s.id DESC LIMIT 0, 1");
                reportIf(count($data) == 1, $data[0], "There is no old classified sample.");
                break;
            case "api:patchwork":
                // Add missing data to the table <table>
                //$api_url = get_attr("api_url");
                if(isValidTable($table)){
                    $data = $db->select("SELECT api_url FROM `$table` WHERE `patchworked` = false LIMIT 0, 1");
                    if($data && count($data) > 0){
                        $api_url = $data[0]['api_url'];
                        $repo = $apihandler->getJSON($api_url . "?" . $apihandler->getAPItoken(), false);
                        if(isEmptyRepo($repo)){
                            $db->query("DELETE FROM `$table` WHERE `api_url` = '$api_url'");
                            throw new Exception("Repository is empty.");
                        }
                        $git_refs = getGitRefs($repo);
                        $treeObj = getTreeObj($repo, $git_refs);
                        $filesAndFolders = getFilesAndFolders($treeObj);
                        $folders = $filesAndFolders["folders"];
                        $db->query("UPDATE `$table` SET `folders` = '$folders', `patchworked` = true WHERE `api_url` = '$api_url'");
                        report(true, "Sample patchworked.");
                    }else{
                        report(false, "There is no sample that needs to be patchworked");
                    }
                }else
                    report(false, "Invalid table");
                break;
            case "api:stats":
                // Gets a list of per <table> statistics
                if(get_attr("string_based") === ""){
                    $numerical_attrs = array("api_calls", "avg_commit_length", "branch_count", "commit_count", "commit_interval_avg", "commit_interval_max", "contributors_count", "file_count", "folder_count", "forks", "open_issues_count", "stars", "treeDepth", "watches");
                    $selector = "";
                    foreach ($numerical_attrs as $na)
                        $selector .= " ROUND(SUM($na)), ROUND(AVG($na)), ROUND(MIN($na)), ROUND(MAX($na)),";
                    $selector = trim($selector, ",");
                    $data = $db->select("SELECT $selector FROM `$table`");
                    reportIf($data !== false && count($data) == 1, $data[0], "Error while generating numerical stats for < $table >");
                }else{
                    $string_attrs = array("class", "api_url", "author", "description", "files", "folders", "language_main", "language_array", "name", "readme", "tagger", "treeArray", "url");
                    $selector = "";
                    foreach ($string_attrs as $sa)
                        $selector .= "  ROUND(AVG(CHAR_LENGTH($sa))),";
                    $selector = trim($selector, ",");
                    $data = $db->select("SELECT $selector FROM `$table`");
                    reportIf($data !== false && count($data) == 1, $data[0], "Error while generating string stats for < $table >");
                }
                break;

            default:
                report(false, "Nothing in here.");
                break;

        }//switch
    }

    function handlePOST($postkey){
        global $apihandler, $db;
        $table = post_attr("table") != "" ? post_attr("table") : "train";
        switch ($postkey) {
            case "unclassified":
                // Add repo link only, to be classified
                $iid = $db -> insert("INSERT INTO `todo` (url) VALUES ('".post_attr('api_url')."')");
                reportIf(is_numeric($iid), "Insertion succeeded","Failed inserting row");
                break;
            case "skip":
                // Remove repo link
                $db->query("UPDATE `train` SET `class` = 'SKIPPED' WHERE `id` = '".post_attr('id')."'");
                report(true, "Sample skipped");
                break;
            case "classify":
                // Classify a generated repo, taken from the pool <table>
                $qID = $db->select("SELECT id FROM `$table` WHERE `id` = '".post_attr('id')."'");
                if($qID !== false && count($qID) != 0 && $table != "train"){
                    $db->query("UPDATE `$table` SET `class` = '".post_attr('class')."', `tagger` = '".post_attr('tagger')."' WHERE `id` = '".post_attr('id')."'");
                    $iid = $db->insert("INSERT INTO `train` ($attrs) SELECT $attrs FROM `$table` WHERE `api_url` = '$api_url'");
                    if($iid){
                        $db->query("DELETE FROM `<1tab></1tab>le` WHERE `api_url` = '$api_url'");
                        report(true,"Repository classified.");
                    }else
                        report(false, "Error moving row");
                }else
                    report(false, "Sample not generated");
                break;
            default:
                report(false, "Nothing in here.");
                break;
        }//switch
    }

    function reportIf($condition, $data, $error_message){
        // If condition is true, return data. If not, display error message
        if($condition === false)
            report(false, $error_message);
        else
            report(true, $data);
    }

    $reported = false;
    function report($succes, $data){
        // Report the call status, only once per call
        //var_dump($data);
        global $reported;
        if(!$reported){
            if($succes)
                $response = json_encode(array("success" => true, "data" => $data));
            else
                $response = json_encode(array("success" => false, "message" => $data));
            if($response === false){
                //var_dump($data);
                throw new Exception("JSON could not be generated.");
            }else
                print($response);
            $reported = true;
        }
    }

    function isValidTable($t){
        return in_array($t, array("train", "test", "unlabeled", "to_classify", "semi_supervised", "_old_train")) == true;
    }

    function isValidLabel($l){
        return in_array($l, array("DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER", "UNSURE", "UNLABELED")) == true;
    }

    function isValidApiUrl($url){
        return !(strpos($url, "https://api.github.com/repos/") === false);
    }

    function generate_filter($filterbasis = ""){
        # Adds potential filters to the sql query
        # Also, check if the equal-class-amount flag is set
        # filterbasis must either be empty, or like '() AND'
        global $db;
        $operators = array("=","<","<=",">=",">");
        $attributes = array("id","class","api_calls","api_url","author","avg_commit_length","branch_count","commit_count","commit_interval_avg","commit_interval_max","contributors_count","description","file_count","files","folders","folder_count","forks","hasDownloads","hasWiki","isFork","open_issues_count","language_main","language_array","name","readme","stars","tagger","treeArray","treeDepth","url","watches");
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
                    foreach ($ORs as $value) 
                        $attrfilter .= "`$attrname` $operator '".$db->check($value)."' OR ";

                    $attrfilter = rtrim($attrfilter, " OR ");
                    if(in_array($attrname, $attributes))
                        $filter .= " ( " . $attrfilter . " ) AND ";
                    
                }
            }
        }
        $filter = $filterbasis . $filter;
        $filter = rtrim($filter, " AND "); // if filter is empty, cut AND from filterbasis. If not, cut it from filter
        $filter = strlen($filter) > 0 ? "WHERE $filter" : "";
        // Add other conditions
        /*
        $additional = "";
        if(get_attr("tagger") != "")
            $additional .= "AND `tagger` = '".get_attr("tagger")."'";
        $filter = strlen($filter) > 0 ? "$filter $additional " : "WHERE TRUE $additional";*/
        return $filter;
    }

    function getLimitation(){
        $limit = get_attr("limit");
        if($limit != "")
            return " ORDER BY RAND() LIMIT 0, $limit";
        return "";
    }

    function generateSampleUrl(){
        // Get the API Url for a random Github repository
        global $apihandler, $db;
        $url = "https://api.github.com/repositories?since=" . rand(0, 5*pow(10, 7)) . "&" . $apihandler->getAPItoken();
        $repos = $apihandler -> getJSON($url);
        if(count($repos) == 0) throw new Exception("failed generating sample url.");
        return $repos[rand(0, count($repos) - 1)]["url"];
    }

    function generateRepoVector($api_url){
        // Use the input-(api)-URL to generate a feature vector for the selected repository
        global $apihandler, $db;
        try{
            $repo = $apihandler->getJSON($api_url . "?" . $apihandler->getAPItoken(), false);
            if(isEmptyRepo($repo))
                throw new Exception("Repository is empty.");
            $commits = getCommits($repo);
            $commitStats = getCommitStats($commits);
            $git_refs = getGitRefs($repo);
            $treeObj = getTreeObj($repo, $git_refs);
            $languages = getLanguages($repo);
            $filesAndFolders = getFilesAndFolders($treeObj);
            $treeData = calcTree($treeObj); 
            $vector = array(
              "api_calls" => $apihandler->getCount(),
              "api_url" =>  $db->check($repo["url"]),
              "author" =>  $db->check($repo["owner"]["login"]),
              "avg_commit_length" => $commitStats["avg_commit_length"],
              "branch_count" =>  count($git_refs),
              "class" => "UNLABELED",
              "commit_count" => count($commits),
              "commit_interval_avg"  => $commitStats["commit_interval_avg"],
              "commit_interval_max" => $commitStats["commit_interval_max"],
              "contributors_count" =>  getContributorsCount($repo),
              "description" =>  $repo["description"] != null ? $db->check($repo["description"]) : "",
              "files" => $filesAndFolders["files"],// String representation
              "file_count" => $treeData["file_count"],
              "folders" => $filesAndFolders["folders"],// String representation
              "folder_count" => $treeData["folder_count"],
              "forks" =>  $repo["forks_count"],
              "hasDownloads" => $repo["has_downloads"],
              "hasWiki" => $repo["has_wiki"],
              "isFork" => $repo["fork"],
              "open_issues_count" => $repo["open_issues_count"],
              "language_main" => $languages["main"],
              "language_array" =>  $languages["string_array"],
              "name" =>  $db->check($repo["name"]),
              "readme" =>  $db->check(getReadme($repo)),
              "stars" =>  $repo["watchers_count"],
              "treeArray" =>  $treeData["array"], // String representation
              "treeDepth" =>  $treeData["depth"],
              "url" =>  $repo["html_url"],
              "watches" =>  $repo["subscribers_count"]
            );
           return $vector;
        }catch(Exception $ex){
            //var_dump($ex);
            throw new Exception("Error while generating sample vector ($api_url): ". $ex->getMessage());
        }
    }

    function calcTree($tree){
      // Get relevant information out of a tree of file and folder nodes
      global $apihandler, $db;
      $tree_result = array("depth" =>  0, "array" => array(), "file_count" => 0, "folder_count" => 0);
      if($tree != null)
          recTree($tree, $tree_result, "", 0);
      $tree_result["array"] = join(" ", $tree_result["array"]);
      return $tree_result;
    }

    function recTree($node, &$tree_result, $path, $depth){
      // Use every node as root, save paths (without filenames) in array
      global $apihandler, $db;
      $tree_result["array"][] = $db->check($path);
      $tree_result["depth"] = $depth > $tree_result["depth"] ? $depth : $tree_result["depth"];
      for($i = 0; $i < count($node); $i++){
        // Accumulate nodeArray + set depth
        if ($node[$i]["type"] == "tree"){
          $tree_result["folder_count"]++;
          if($tree_result["folder_count"] < 50){
              // don't exceed API limit
              $subtree = $apihandler -> getJSON($node[$i]["url"]  . "?" . $apihandler->getAPItoken(), false);
              if(isset($subtree["tree"]))
                recTree($subtree["tree"],$tree_result, $path . '\\'. $node[$i]["path"], $depth + 1);
            }
        }else
          $tree_result["file_count"]++;
      }
    }

    function getGitRefs($repo){
        // Returns the git repos or an empty array
        global $apihandler;
        $ref_url_base = explode("{", $repo["git_refs_url"]);
        $git_refs = $apihandler -> getJSON($ref_url_base[0] . "?" . $apihandler->getAPItoken(), false);
        return (isset($git_refs["documentation_url"]) && isset($git_refs["message"])) ? array() : $git_refs;
    }

    function getFilesAndFolders($treeObj){
        // Returns an array of top level files and folders
        global $db;
        $folders = array(); $files = array();
        //$readme_exists = false;
        for($i = 0; $i < count($treeObj); $i++){
            //$readme_exists = $readme_exists || (strpos(strtolower($treeObj[$i]["path"]), "readme") >= 0);
            if($treeObj[$i]["type"] == "blob"){
                $files[] = $db->check($treeObj[$i]["path"]);
            }else{ // folder or commit
                $folders[] = $db->check($treeObj[$i]["path"]);
            }
        }
        return array("folders" => join(" ", $folders), "files" => join(" ", $files));
    }

    function getTreeObj($repo, $git_refs){
        // Returns the file and folder three array or null.
        global $apihandler;
        $ref_url = "";
        for($i = 0; $i < count($git_refs); $i++){
          if(strpos($git_refs[$i]["ref"], $repo["default_branch"]) >= 0){
            $ref_url = $git_refs[$i]["object"]["url"];
            break;
          }
        }
        if(trim($ref_url) == "" && count($git_refs) > 0)
          // Default branch is not available
          $ref_url = $git_refs[0]["object"]["url"];
        if($ref_url == "") return null;
        $branch =  $apihandler -> getJSON($ref_url . "?" . $apihandler->getAPItoken(), false);
        if(!isset($branch["tree"]["url"])) return null;
        $treeObj = $apihandler -> getJSON($branch["tree"]["url"] . "?" . $apihandler->getAPItoken(), false);
        return (isset($treeObj["tree"])) ? $treeObj["tree"] : null;
    }

    function getLanguages($repo) {
        // Returns the string representation of the language array and the main language
        global $db, $apihandler;
        $languages = array("main" => "", "string_array" => "");
        $data = $apihandler -> getJSON($repo["languages_url"]. "?" . $apihandler->getAPItoken(), false);
        $l = !isset($data["documentation_url"]) && !isset($data["message"]) ? array_keys($data) : null;
        $l = $l == null ? array() : $l;
        $languages["string_array"] = join(" ", $l);
        $languages["main"] = $repo["language"] != null ? $db->check($repo["language"]) : (count($l) == 0 ? "" : $db->check($l[0]));
        return $languages;
    }

    function getCommitStats($commits){
        // Calculates Commit statistics such as avg length and intervals
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
        $avg_length = round($avg_length / max(1, count($commits)));   
        return array("avg_commit_length" => $avg_length, "commit_interval_avg" => round(array_sum($commit_intervals) / count($commit_intervals)), "commit_interval_max" => max($commit_intervals));
    }

    function getContributorsCount($repo){
        // returns the amount of contributors
        global $apihandler;
        $data = $apihandler -> getJSON($repo["contributors_url"] . "?" . $apihandler->getAPItoken(), false);
        return !isset($data["documentation_url"]) && !isset($data["message"]) ? count($data) : 0;
    }

    function getCommits($repo){
        // Get a list of commits
        global $apihandler;
        $commit_url_base = explode("{", $repo["commits_url"]);
        $i = 1;
        $commits = array(); $commit_page = array(); // page = temporary variable
        do{
            $commit_page = $apihandler -> getJSON($commit_url_base[0] . "?page=".$i."&" . $apihandler->getAPItoken(), false);
            if(isset($commit_page["documentation_url"]))
                break;
            $commits = array_merge($commits, $commit_page);
            $i++;
        }while(count($commit_page)>0  && $i < 50);
        return $commits;
    }

    function getReadme($repo){
        global $apihandler;
        $readme_data = $apihandler -> getJSON($repo["url"] . "/readme?" . $apihandler->getAPItoken(), false);
        if(isset($readme_data["content"]) && isset($readme_data["encoding"]))
            return $readme_data["content"];
        return "";
    }

    function isEmptyRepo($repo){
        if(isset($repo["documentation_url"]) && isset($repo["message"]))
            if($repo["message"] == "Moved Permanently" || $repo["message"] == "Git Repository is empty." || $repo["message"] == "Not Found")
                return true;
        return false;
    }

    function saveVector(&$vector){
        // Save the feature vector as a new repository in the database
        global $db;
        $table = strtolower($vector['class']) != 'unlabeled' ? 'train' : 'unlabeled';

        $data = $db->select("SELECT * FROM `$table` WHERE `url` = '".$vector['url']."'");
        if($data !== false && count($data) == 0){
            $keys =  "`" . join("`, `", array_keys($vector)) . "`";
            $values = "'" . join("', '", $vector) . "'";
            $query = "INSERT INTO `$table` ( $keys ) VALUES ( $values )";
            $iid = $db->insert($query);
            return $iid;
        }/*else
            throw new Exception("Duplicate Vector");*/
    }

    ?>