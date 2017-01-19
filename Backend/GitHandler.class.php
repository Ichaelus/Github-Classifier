<?php
	################################################
	# The interface between PHP and the GitHub API #
	################################################

	class GitHandler{
		var $tokenList = array(
				# This list is being used to access the GitHub API
				# Even though using more than one id:secret pair, the server is limited to 5000 API calls per minute per IP
				# If more than one backend instance is running, this list will be useful
				array("786e167cb4599083c50f", "7b5c5422ab50aa15c15f6b32297b1c92a6745855"), // Michi
				array("4e290575e9eef794e3b3", "cfe75b4a0e3e4bd5c38138d07da1e189e762f39b"), // Andi
				array("076b012762c504c5ae11", "cb9242a96a092be66eeb241cce6b0b343e320b22"), // Stefan
				array("6ad3502f8120b8d5fc18", "3c0500b4942fa1ca7499d82ebcc48cab36bb8760"), // Leo
				array("172526aa59ac8f917e46", "6a8a8b218f73925f4f849c09ba656a89af3055a1") // Martin
			);

		var $currentIndex = 0;
		var $token = "";
		var $count = 0;

		function __construct(){
			// Init CURL handler
			$this->ch = curl_init();
		}

		function __destruct(){
		    // Close CURL handler
		    curl_close($this->ch);
		}

		function getAPItoken($id = "", $secret = ""){
		  // Return one of the tokens listed on top of this class
		  if($this->token == ""){
		  	  if($id == "" || $secret == ""){
		  	  	// use credential rotation
				$id = $this->tokenList[$this->currentIndex][0];
				$secret = $this->tokenList[$this->currentIndex][1];
			  }
			  $this->token = "client_id=".$id."&client_secret=".$secret;
			}
			return $this->token;
		}

		function nextToken(){
			// If the 5000 call limit is reached, use the next pair
			if($this->currentIndex < count($this->tokenList) -1){
				$this->currentIndex ++;
			  	$this->token = "client_id=".$this->tokenList[$this->currentIndex][0]."&client_secret=".$this->tokenList[$this->currentIndex][1];
			}else{
				throw new Exception("API limit reached. ". $this->tokenList[$this->currentIndex][0]);
			}
		}

		function count(){
			// Note each API call
			$this->count++;
		}

		function getCount(){
			// Return the API calls for this session
			return $this->count;
		}

		function HandleHeaderLine( $curl, $header_line ) {
			// get remaining calls, if neccessary use next credentials
		    $pos = strpos($header_line, "X-RateLimit-Remaining: ");
		    if($pos === 0){
		        $this->count();
		        $calls = intval(substr($header_line, 22));
		        if($calls <= 10)
		            $this->nextToken();
		    }
		    return strlen($header_line);
		}

		function getJSON($url, $throw = true){
			if( trim($url, "?") == $this->getAPItoken())
				throw new Exception("Url empty!");
			// Get the ressources from a $url and return the decoded JSON content
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
		    if($result == null && $throw)
		        throw new Exception("$url: Result empty or out of API calls");
		    $res = json_decode($result, true);
		    if(isset($res["documentation_url"], $res["message"])){
		    	//if($res["message"] == "Moved Permanently")
		    		//return getJSON($res["url"]);
		    	if($throw || strpos($res["message"], "API rate limit exceeded for") !== false )
	    			throw new Exception($res["message"]);
	    		else
	    			return $res;
	    		//var_dump($res);
	    		//throw new Exception($res["message"]. " | $url");
		    }

		    return $res;
		}
	}
?>