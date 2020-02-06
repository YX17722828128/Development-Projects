<?php
	Session_start();
	//connect to database
	$mysql_conf = array(
    'host'    => '127.0.0.1:3306', 
    'db'      => 'website', 
    'db_user' => 'xxx',
    'db_pwd'  => 'xxx',
    );

	$mysqli = @new mysqli($mysql_conf['host'], $mysql_conf['db_user'], $mysql_conf['db_pwd']);
	if($mysqli->connect_errno) {
	    die("could not connect to the database:\n" . $mysqli->connect_error);//诊断连接错误
	}
	$mysqli->query("set names 'utf8';");//编码转化
	$select_db = $mysqli->select_db($mysql_conf['db']);
	if(!$select_db) {
	    die("could not connect to the db:\n" .  $mysqli->error);
	}
	//update_data
	if(isset($_SESSION["account"]) && isset($_SESSION["psd"])){
		if(isset($_POST["nickname"]) || isset($_POST["gender"]) || isset($_POST["tel_email"]) || isset($_POST["base64"])){
	    		if(!empty($_POST["nickname"]))
	    			$temp = $temp.",nickname = '".$_POST["nickname"]."'";
	    		if(!empty($_POST["gender"]))
	    			$temp = $temp.",gender = '".$_POST["gender"]."'";
	    		if(!empty($_POST["tel/email"]))
	    			$temp = $temp.",tel/email = '".$_POST["tel_email"]."'";
	    		if(!empty($_POST["base64"]))
	    			$temp = $temp.",base64 = '".$_POST["base64"]."'";
	    		if($temp!=""){
	    			$temp = substr_replace($temp,"",0,1);
					$sql = "UPDATE user SET ".$temp." WHERE account = '".$_SESSION["account"]."'";
					if($mysqli->query($sql) === TRUE){
				    	echo "update data successfully";
					}
					else{
					    echo "Error: " . $sql . "<br>" . $mysqli->error;
					}
	    		}
	    		else{
	    			echo "you haven't choose one";
	    		}
			}
			else{
				echo "error";
			}
	    }
	else{
		echo "sign in first";
	} 
	$mysqli->close();
?> 