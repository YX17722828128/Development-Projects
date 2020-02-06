<?php
	$account = $_POST["account"];
	$psd = $_POST["psd"];
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

	// $sql = "INSERT INTO user (account,psd)
	// 		VALUES ('".$account."', '".$psd."')";
	// if($mysqli->query($sql) === TRUE) {
 //    echo "新记录插入成功";
	// } else {
	//     echo "Error: " . $sql . "<br>" . $mysqli->error;
	// }

	$sql = "SELECT * FROM user WHERE account = '".$account."' AND psd = '".$psd."'";
	$result = mysqli_query($mysqli, $sql);
	if (mysqli_num_rows($result) > 0) {
	    // 输出数据
	    $final_result = "";
	    while($row = mysqli_fetch_assoc($result)) {
	    	$arr = array($row["account"],$row["psd"]);
	        $regId=implode(",",$arr);
	        $final_result = $regId . "@" . $final_result;
	    }
	    $final_result = substr($final_result, 0, -1);
	    echo $final_result;
	} else {
	    echo "登录失败";
	}
	$mysqli->close();
?> 