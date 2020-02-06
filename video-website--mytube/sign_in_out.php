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
	//sign in and set the session
	if(isset($_POST["account"]) && isset($_POST["step1"])){
		$sql = "SELECT * FROM user WHERE account = '".$_POST["account"]."'";
		$result = mysqli_query($mysqli, $sql);
		if(mysqli_num_rows($result) > 0){
		    echo "sign in";
		}
		else{
		    echo "sign up";
		}
	} 
	if(isset($_POST["account"]) && isset($_POST["psd"]) && isset($_POST["step2"])){
        if($_POST["step2"] == "sign in"){
            $sql = "SELECT * FROM user WHERE account = '".$_POST["account"]."' AND psd = '".$_POST["psd"]."'";
            $result = mysqli_query($mysqli, $sql);
            if(mysqli_num_rows($result) > 0){
                $_SESSION["account"] = $_POST["account"];
                $_SESSION["psd"] = $_POST["psd"];
                echo "sign in";
            }
            else{
                echo "sign in failure";
            }
        }
        else{
            if(isset($_POST["account"]) && isset($_POST["psd"])){
                $sql = "SELECT * FROM user WHERE account = '".$_POST["account"]."'";
                $result = mysqli_query($mysqli, $sql);
                if(mysqli_num_rows($result) > 0){
                    $_SESSION["account"] = $_POST["account"];
                    $_SESSION["psd"] = $_POST["psd"];
                    echo "sign in";
                }
                else{
                    $sql =  "INSERT INTO user (account,psd) VALUES ('".$_POST["account"]."','".$_POST["psd"]."')";
                    if($mysqli->query($sql) === TRUE){
                        $_SESSION["account"] = $_POST["account"];
                        $_SESSION["psd"] = $_POST["psd"];
                        echo "Sign up successfully!<br>Username: ".$_POST["account"]."<br>Password: ".$_POST["psd"];
                    }
                    else{
                        echo "Error: " . $sql . "<br>" . $mysqli->error;
                    }
                }

            }
        }
	}

	$mysqli->close();
?> 