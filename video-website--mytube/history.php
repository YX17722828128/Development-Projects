<?php
	$video_src = $_POST["video_src"];
	$view_time = date("Y/m/d h:i:s");
	$mysql_conf = array(
    'host'    => '127.0.0.1:3306', 
    'db'      => 'website', 
    'db_user' => 'xxx',
    'db_pwd'  => 'xxx',
    );

	$mysqli = @new mysqli($mysql_conf['host'], $mysql_conf['db_user'], $mysql_conf['db_pwd']);
	if ($mysqli->connect_errno) {
	    die("could not connect to the database:\n" . $mysqli->connect_error);//诊断连接错误
	}
	$mysqli->query("set names 'utf8';");//编码转化
	$select_db = $mysqli->select_db($mysql_conf['db']);
	if (!$select_db) {
	    die("could not connect to the db:\n" .  $mysqli->error);
	}

	$sql = "DELETE FROM history WHERE video_src = '".$video_src."'";
	if($mysqli->query($sql) === TRUE) {
    	echo "原记录删除";
	}
	else{
	    echo "Error: " . $sql . "<br>" . $mysqli->error;
	}
	
	$sql = "INSERT INTO history (video_src,view_time)
			VALUES ('".$video_src."', '".$view_time."')";
	if($mysqli->query($sql) === TRUE) {
    	echo "新记录插入成功";
	}
	else{
	    echo "Error: " . $sql . "<br>" . $mysqli->error;
	}
	$mysqli->close();
?>