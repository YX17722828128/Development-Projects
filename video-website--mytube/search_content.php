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
	//search
	if(isset($_POST["search_content"])){
		$sql = "SELECT * FROM mytube_video WHERE author LIKE \"%".$_POST["search_content"]."%\" OR video_src LIKE \"%".$_POST["search_content"]."%\"";
		$result = mysqli_query($mysqli, $sql);
		if(mysqli_num_rows($result) > 0){
		    $final_result = "";
		    while($row = mysqli_fetch_assoc($result)) {
		    	$regId = $row["video_src"];
		        $final_result = $regId . "@" . $final_result;
		    }
		    $final_result = substr($final_result, 0, -1);
		    echo $final_result;
		} 
		else{
		    echo "NULL";
		}
	}
	else{
		echo "no content";
	} 
	$mysqli->close();
?> 