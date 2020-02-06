<?php
	Session_start();
	//connect to database
	$mysql_conf = array(
    'host'    => '127.0.0.1:3306', 
    'db'      => 'emp', 
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
	//login in and set the session
	if(isset($_POST["login_account"]) && isset($_POST["login_password"])){
		$sql = "SELECT * FROM user WHERE account = '".$_POST["login_account"]."' AND password = '".$_POST["login_password"]."'";
		$result = mysqli_query($mysqli, $sql);
		if(mysqli_num_rows($result) > 0){
		    $_SESSION["account"] = $_POST["login_account"];
		    $_SESSION["password"] = $_POST["login_password"];
		    echo "successfully login in";
		}
		else{
		    echo "login in failure";
		}
	}
	//search data
	if(isset($_POST["search_content"])){
		$sql = "SELECT * FROM employee WHERE emp_id = '".$_POST["search_content"]."' OR emp_name = '".$_POST["search_content"]."' OR dept_no = '".$_POST["search_content"]."'";
		$result = mysqli_query($mysqli, $sql);
		if(mysqli_num_rows($result) > 0){
		    $final_result = "";
		    while($row = mysqli_fetch_assoc($result)) {
		    	$arr = array($row["emp_id"],$row["emp_name"],$row["dept_no"],$row["salary"],$row["authority"]);
		        $regId=implode(",",$arr);
		        $final_result = $regId . "@" . $final_result;
		    }
		    $final_result = substr($final_result, 0, -1);
		    echo $final_result;
		} 
		else{
		    echo "NULL";
		}
    }
    //create data
    if(isset($_POST["add_id"]) && isset($_POST["add_name"]) && isset($_POST["add_no"]) && isset($_POST["add_salary"]) && isset($_POST["add_authority"])){
    	if(!empty($_POST["add_id"]) && !empty($_POST["add_name"]) && !empty($_POST["add_no"]) && !empty($_POST["add_salary"]) && !empty($_POST["add_authority"])){
    		$sql = "INSERT INTO employee (emp_id,emp_name,dept_no,salary,authority) VALUES ('".$_POST["add_id"]."','".$_POST["add_name"]."','".$_POST["add_no"]."','".$_POST["add_salary"]."','".$_POST["add_authority"]."')";
			if($mysqli->query($sql) === TRUE){
		    	echo "add data successfully";
			}
			else{
			    echo "Error: " . $sql . "<br>" . $mysqli->error;
			}
    	}
		else{
			echo "you should input all choices.";
		}
    }
    // echo "sign in account: ".$_SESSION["account"]."sign in password:".$_SESSION["password"];
    //delete data
    if(isset($_POST["delete_id"])){
    	//check current user's authority
    	$sql_1 = "SELECT authority FROM employee WHERE emp_id = '".$_SESSION["password"]."'";
    	$result_1 = mysqli_query($mysqli, $sql_1);
    	$row_1 = mysqli_fetch_assoc($result_1);
    	//check delete employee's authority
    	$sql_2 = "SELECT authority FROM employee WHERE emp_id = '".$_POST["delete_id"]."'";
    	$result_2 = mysqli_query($mysqli, $sql_2);
    	$row_2 = mysqli_fetch_assoc($result_2);
    	if(mysqli_num_rows($result_2) > 0){
    		if($row_1["authority"]>$row_2["authority"]){
	    		$sql = "DELETE FROM employee WHERE emp_id = '".$_POST["delete_id"]."'";
				if($mysqli->query($sql) === TRUE){
			    	echo "delete data successfully";
				}
				else{
				    echo "Error: " . $sql . "<br>" . $mysqli->error;
				}
	    	}
			else{
				echo "Lack of authority\ndetails:your authority is ".$row_1["authority"].",authority of the one you are trying to delete is ".$row_2["authority"];
			}
    	}
    	else{
    		echo "empty search result";
    	}
    }
    //choose_update_id
    if(isset($_POST["update_id"])){
    	//check current user's authority
    	$sql_1 = "SELECT authority FROM employee WHERE emp_id = '".$_SESSION["password"]."'";
    	$result_1 = mysqli_query($mysqli, $sql_1);
    	$row_1 = mysqli_fetch_assoc($result_1);
    	//check delete employee's authority
    	$sql_2 = "SELECT authority FROM employee WHERE emp_id = '".$_POST["update_id"]."'";
    	$result_2 = mysqli_query($mysqli, $sql_2);
    	$row_2 = mysqli_fetch_assoc($result_2);
    	if(mysqli_num_rows($result_2) > 0){
    		if($row_1["authority"]>$row_2["authority"]){
	    		//update_data
			    if(isset($_POST["update_name"]) || isset($_POST["update_no"]) || isset($_POST["update_salary"]) || isset($_POST["update_authority"])){
			    	$sql = "SELECT authority FROM employee WHERE emp_id = '".$_POST["update_id"]."'";
			    	$result = mysqli_query($mysqli, $sql);
			    	$row = mysqli_fetch_assoc($result);
			    	if($_POST["update_authority"]<=$row["authority"]){
			    		$temp = "";
			    		if(!empty($_POST["update_name"]))
			    			$temp = $temp.",emp_name = '".$_POST["update_name"]."'";
			    		if(!empty($_POST["update_no"]))
			    			$temp = $temp.",dept_no = '".$_POST["update_no"]."'";
			    		if(!empty($_POST["update_salary"]))
			    			$temp = $temp.",salary = '".$_POST["update_salary"]."'";
			    		if(!empty($_POST["update_authority"]))
			    			$temp = $temp.",authority = '".$_POST["update_authority"]."'";
			    		if($temp!=""){
			    			$temp = substr_replace($temp,"",0,1);
							$sql = "UPDATE employee SET ".$temp." WHERE emp_id = '".$_POST["update_id"]."'";
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
						echo "you can not make the authority greater than current's";
					}
			    }
	    	}
			else{
				echo "Lack of authority\ndetails:your authority is ".$row_1["authority"]." but authority of the one you are trying to update is ".$row_2["authority"];
			}
    	}
    	else{
    		echo "empty search result";
    	}
    }
    
    if(isset($_POST["annual"])){
    	$sql = "SELECT dept_no,AVG(salary) FROM employee GROUP BY dept_no";
    	$result = mysqli_query($mysqli, $sql);
    	echo mysqli_num_rows($result);
		if (mysqli_num_rows($result) > 0) {
		    $final_result = "";
		    while($row = mysqli_fetch_assoc($result)) {
		    	$arr = array($row["AVG(salary)"],$row["dept_no"]);
		        $regId=implode(",",$arr);
		        $final_result = $regId . "@" . $final_result;
		    }
		    $final_result = substr($final_result, 0, -1);
		    echo $final_result;
		} else {
		    echo "null";
		}
    }

    if(isset($_POST["monthly"])){
    	$sql = "SELECT dept_no,AVG(salary)/12 FROM employee GROUP BY dept_no";
    	$result = mysqli_query($mysqli, $sql);
    	echo mysqli_num_rows($result);
		if (mysqli_num_rows($result) > 0) {
		    $final_result = "";
		    while($row = mysqli_fetch_assoc($result)) {
		    	$arr = array($row["AVG(salary)/12"],$row["dept_no"]);
		        $regId=implode(",",$arr);
		        $final_result = $regId . "@" . $final_result;
		    }
		    $final_result = substr($final_result, 0, -1);
		    echo $final_result;
		} else {
		    echo "null";
		}
    }
	$mysqli->close();
?> 