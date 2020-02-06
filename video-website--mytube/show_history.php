<?php
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

	$sql = "SELECT * FROM mytube_video WHERE video_src = ANY(SELECT video_src FROM history)";
	$result = mysqli_query($mysqli, $sql);
	if (mysqli_num_rows($result) > 0) {
	    $total_arr = array();
	    while($row = mysqli_fetch_assoc($result)) {
	    	$arr = array("author" => utf8_encode($row["author"]), "video_src" => utf8_encode($row["video_src"]), "image_src" => utf8_encode($row["image_src"]), "gif_src" => utf8_encode($row["gif_src"]), "views" => utf8_encode($row["views"]));
	    	array_push($total_arr, $arr);
	    }
	    echo json_encode($total_arr);
	}
	else {
	    echo json_encode("登录失败");
	}
	$mysqli->close();
?>
