<?php
	$video_src = $_POST["video_src"];
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
	$sql = "SELECT * FROM comment_data WHERE relate_movie = '".$video_src."' ORDER BY likes";
	$result = mysqli_query($mysqli, $sql);
	if (mysqli_num_rows($result) > 0) {
	    $final_result = "";
	    while($row = mysqli_fetch_assoc($result)) {
	    	$arr = array($row["replies_numbers"],$row["comment_user"],$row["comment_time"],$row["comment_content"],$row["likes"]);
	        $regId=implode("*",$arr);
	        $final_result = $regId . "@" . $final_result;
	    }
	    $final_result = substr($final_result, 0, -1);
	    echo "$final_result";
	}
	else {
	    echo "没有评论";
	}

	$mysqli->close();
?>
<!-- SELECT * FROM comment_data WHERE relate_movie = "10-CRAZIEST-Animal-Fights-Caught-On-Camera.mp4" ORDER BY likes -->

<!-- UPDATE comment_data SET relate_movie = "5-Cool-Technology-GADGETS-in-REAL-You-Can-Buy-On-Amazon-Under-Rs250-NEW-TECHNOLOGY.mp4" WHERE comment_data.relate_movie = "5-Cool-Technology-GADGETS-in-REAL-✅-You-Can-Buy-On-Amazon-Under-Rs250---NEW-TECHNOLOGY.mp4";
UPDATE mytube_video SET video_src = "5-Cool-Technology-GADGETS-in-REAL-You-Can-Buy-On-Amazon-Under-Rs250-NEW-TECHNOLOGY.mp4" WHERE comment_data.relate_movie = "5-Cool-Technology-GADGETS-in-REAL-✅-You-Can-Buy-On-Amazon-Under-Rs250---NEW-TECHNOLOGY.mp4";
UPDATE mytube_video SET image_src = "5-Cool-Technology-GADGETS-in-REAL-You-Can-Buy-On-Amazon-Under-Rs250-NEW-TECHNOLOGY.jpg" WHERE comment_data.relate_movie = "5-Cool-Technology-GADGETS-in-REAL-✅-You-Can-Buy-On-Amazon-Under-Rs250---NEW-TECHNOLOGY.jpg";
UPDATE mytube_video SET gif_src = "5-Cool-Technology-GADGETS-in-REAL-You-Can-Buy-On-Amazon-Under-Rs250-NEW-TECHNOLOGY.gif" WHERE comment_data.relate_movie = "5-Cool-Technology-GADGETS-in-REAL-✅-You-Can-Buy-On-Amazon-Under-Rs250---NEW-TECHNOLOGY.gif"; -->