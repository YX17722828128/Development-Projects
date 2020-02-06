<?php
    Session_start();
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

	$sql = "SELECT * FROM my_upload WHERE user = '".$_SESSION["account"]."' ";
	$result = mysqli_query($mysqli, $sql);
	if (mysqli_num_rows($result) > 0) {
	    // 输出数据
	    $final_result = "";
	    while($row = mysqli_fetch_assoc($result)) {
	    	$row["video_src"] = "upload/video/".$row["video_src"];
	    	$row["image_src"] = "upload/image/".$row["image_src"];
	    	$row["gif_src"] = "upload/gif/".$row["gif_src"];
	    	$arr = array($row["video_src"],$row["image_src"],$row["gif_src"],$row["file_size"],$row["upload_time"]);
	        $regId=implode(",",$arr);
	        $final_result = $regId . "@" . $final_result;
	    }
	    $final_result = substr($final_result, 0, -1);
	    echo $final_result;
	} else {
	    echo "没有匹配的信息";
	}
	$mysqli->close();
?>