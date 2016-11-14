<?php
	class GitHandler{
		
		var $tokenList = array(
				array("786e167cb4599083c50f", "7b5c5422ab50aa15c15f6b32297b1c92a6745855"), // Michi
				array("4e290575e9eef794e3b3", "cfe75b4a0e3e4bd5c38138d07da1e189e762f39b") // Andi
			);

		var $currentIndex = 0;
		var $token = "";
		var $count = 0;

		function __construct(){
			$this->ch = curl_init();
		}

		function __destruct(){
		    // Closing
		    curl_close($this->ch);
		}

		function getAPItoken($id = "", $secret = ""){
		  if($this->token == ""){
		  	  if($id == "" || $secret == ""){
		  	  	// use credential rotation
				$id = $this->tokenList[$this->currentIndex][0];
				$secret = $this->tokenList[$this->currentIndex][1];
			  }
			  $this->token = "client_id=".$id."&client_secret=".$secret;
			}
			//if($this-> allExpired()) return false;
			return $this->token;
		}

		function nextToken(){
			if($this->currentIndex < count($tokenList) -1){
				$this->currentIndex ++;
			  	$this->token = "client_id=".$this->tokenList[$this->currentIndex][0]."&client_secret=".$this->tokenList[$this->currentIndex][1];
			}else{
				throw new Exception("API limit reached.");
			}
		}

		function count(){
			$this->count++;
		}

		function getCount(){
			return $this->count;
		}

		function HandleHeaderLine( $curl, $header_line ) {
		    $pos = strpos($header_line, "X-RateLimit-Remaining: ");
		    if($pos === 0){
		        $this->count();
		        // get remaining calls, if neccessary use next credentials
		        $calls = intval(substr($header_line, 22));
		        if($calls <= 10)
		            $this->nextToken();
		    }
		    return strlen($header_line);
		}

		function getJSON($url){
		    // global $_APICALLS;
		    // $_APICALLS++;
		    // print($_APICALLS);
		    //  Initiate curl
		    curl_setopt($this->ch, CURLOPT_USERAGENT, "Awesome crawler");//'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13');
		    // Disable SSL verification
		    curl_setopt($this->ch, CURLOPT_SSL_VERIFYPEER, false);
		    // Will return the response, if false it print the response
		    curl_setopt($this->ch, CURLOPT_RETURNTRANSFER, true);
		    // Set the url
		    curl_setopt($this->ch, CURLOPT_URL,$url);
		    // Check remaining git api calls
		    curl_setopt($this->ch, CURLOPT_HEADERFUNCTION, array($this, "HandleHeaderLine"));
		    // Execute
		    $result=curl_exec($this->ch);
		    
		    return json_decode($result, true);
		}

	}
?>