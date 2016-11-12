<?php
require('mysqli_class.php');
$db = new MYSQL();
if(!$db->init()){ throw new Exception("Could not connect to the database");}

$header = 'Content-Type: text/html; charset=utf-8';
session_start();
ob_start();

function get_attr($name){
    global $db;
    if(isset($_GET[$name])){
        return $db->check($_GET[$name]);
    }else{
        return "";
    }
}

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
                $data = $db->select("SELECT * FROM `samples` $filter");
                print(json_encode($data));
                break;
            case "api:equal":
                $mdata = $db->select("SELECT COUNT(*) AS minimum FROM samples GROUP BY class ORDER BY minimum LIMIT 0, 1");
                $minimum = $mdata[0]["minimum"];
                $class_equal_query = "SELECT
                                      samples.*
                                    FROM
                                      samples INNER JOIN (
                                        SELECT
                                          class,
                                          GROUP_CONCAT(id ORDER BY id DESC) grouped_id
                                        FROM
                                          samples
                                        GROUP BY class) group_max
                                      ON samples.class = group_max.class
                                         AND FIND_IN_SET(id, grouped_id) BETWEEN 1 AND $minimum
                                    ORDER BY
                                      samples.class DESC";
                $data = $db->select($class_equal_query);
                print(json_encode($data));
                break;
            case "api:class":
                $class = get_attr("name");
                $data = $db->select("SELECT * FROM `samples` WHERE `class` = '$class'");
                print(json_encode($data));
                break;
            case "api:count":
                $filter = generate_filter();
                $data = $db->select("SELECT COUNT(*) AS count FROM `samples` $filter");
                print($data[0]["count"]);
                break;
            case "api:class-count":
                $additional = "";
                if(get_attr("tagger") != "")
                    $additional .= "WHERE `tagger` = '".get_attr("tagger")."'";
                $data = $db->select("SELECT class, COUNT(*) AS count FROM `samples` $additional GROUP BY `class`");
                print(json_encode($data));
                break;
            default:
                print("Nothing in here.");
                break;
        }//switch
    }
}

function post_attr($name){
    global $db;
    if(isset($_POST[$name])){
        return $db->check($_POST[$name]);
    }else{
        return "";
    }
}

if(isset($_POST['key'])){
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
                $db->query("DELETE FROM `todo` WHERE `url` = '".post_attr('api_url')."'");
                break;
            case "classify":
                // Add repo to list
                if(count($db->select("SELECT * FROM `samples` WHERE `url` = '".post_attr('url')."'")) == 0){
                    $query = "INSERT INTO `samples` ( class, author, name, description,
                                                        url, watches, stars, forks, languages,
                                                        readme, tree, tagger) VALUES
                                ('".post_attr('class')."', '".post_attr('author')."', '".post_attr('name')."', '".post_attr('description')."',
                                '".post_attr('url')."', '".post_attr('watches')."', '".post_attr('stars')."', '".post_attr('forks')."', '".post_attr('languages')."',
                                '".post_attr('readme')."', '".post_attr('tree')."', '".post_attr('tagger')."')";
                    $iid = $db->insert($query);
                    $db->query("DELETE FROM `todo` WHERE `url` = '".post_attr('api_url')."'");
                    print(is_numeric($iid) ? "success" : "error");
                }else{
                    print("error: duplicate");
                }
                break;
            default:
                print("Nothing in here.");
                break;
        }//switch
    }
}
header($header);
ob_end_flush();

?>