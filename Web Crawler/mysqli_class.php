<?php
class MYSQL{
	var $CONN = "";
	var $USER = "u51019db1";
	var $PASS = "c99t6%3NSjte7eaub8iw7y1a!";
	var $SERVER = "localhost";
	
	var $TRAIL = array();
	var $HITS = array();
	var $AUTOAPPROVE = true;

	function error($text){
		$no= mysqli_errno();
		$msg = mysqli_error();
		echo "[$text] ( $no : $msg )</br>\n";
		exit;
	}
	function init($dbase="u51019db1"){
		$user= $this->USER;
		$pass = $this->PASS;
		$server = $this->SERVER;
		$conn = mysqli_connect($server,$user,$pass);
		if(!$conn){
			$this->error("No connection!");
		}
		if(!mysqli_select_db($conn,$dbase)){
			$this->error("No database!");
		}
		$this->CONN = $conn;
		return true;
	}
	function query($sql=""){
		if(empty($sql)){ return false;}
		if(empty($this->CONN)){return false;}
		$conn= $this->CONN;
		$results= mysqli_query($conn,$sql);
		return($results);
	}
	function select($sql=""){
		if(empty($sql)){ return false;}
		if(!preg_match("/^select/i",$sql)){ // Case insensitive
			echo "<h2>Wrong command!</h2>\n";
			return false;
		}
		if(empty($this->CONN)){return false;}
		$conn= $this->CONN;
		$results= mysqli_query($conn,$sql);
		if((!$results) or (empty($results)) ) {
			mysqli_free_result($results);
			return false;
		}
		$data = array();
		while($row = mysqli_fetch_array($results, $resulttype = MYSQLI_ASSOC)){
			$data[]=$row;
		}
		mysqli_free_result($results);
		return $data;
	}
	function insert($sql=""){
		if(empty($sql)){ return false;}
		if(!preg_match("/^insert/i",$sql)){ // Case insensitive
			echo "<h2>Wrong command!</h2>\n";
			return false;
		}
		if(empty($this->CONN)){return false;}
		$conn= $this->CONN;
		$results = mysqli_query($conn,$sql);
		if(!$results){return false;}
		$results= mysqli_insert_id($conn);
		return $results;
	}
	function check($statement){
		if(empty($this->CONN)){return false;}
		$conn= $this->CONN;
		$statement = mysqli_real_escape_string($conn, $statement);
		return $statement;
	}
	function getinfo($sql=""){
		if(empty($sql)){ return false;}
		if(empty($this->CONN)){return false;}
		$conn= $this->CONN;
		$result= mysqli_query($conn,$sql);
		$results=array();
		while($finfo = mysqli_fetch_field($result)){
			$results[]=$finfo->name;
		}
		return($results);
	}
	function gettables(){
		if(empty($this->CONN)){return false;}
		$conn= $this->CONN;
		$result= mysqli_query($conn,"SHOW TABLES");
		$tableList=array();
		while($cRow = mysqli_fetch_array($result)){
	    	$tableList[] = $cRow[0];
		}
		return($tableList);
	}
	function getdbs(){
		if(empty($this->CONN)){return false;}
		$conn= $this->CONN;
		$result= mysqli_query($conn,"SHOW DATABASES");
		$dbs=array();
		while($cRow = mysqli_fetch_array($result)){
	    	$dbs[] = $cRow[0];
		}
		return($dbs);
	}
}
?>