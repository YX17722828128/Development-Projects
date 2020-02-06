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

//允许上传的视频后缀
    $allowedExts = array("flv", "rmvb", "mp4", "avi", "wmv","mkv","swf","mov","mpg","3gp","webm","ogg","3gpp");
    $temp = explode(".", $_FILES["file"]["name"]);
    $extension = end($temp);     // 获取文件后缀名
    if (in_array($extension, $allowedExts))
    {
        if ($_FILES["file"]["error"] > 0)
        {
            echo "错误：: " . $_FILES["file"]["error"] . "<br>";
        }
        else
        {
            
        // 判断当期目录下的 upload 目录是否存在该文件
        // 如果没有 upload 目录，你需要创建它，upload 目录权限为 777
        $_FILES["file"]["name"] = str_replace(" ","-",$_FILES["file"]["name"]);
        $_FILES["file"]["name"] = str_replace('&','',$_FILES["file"]["name"]);
        if (file_exists("static/video/" . $_FILES["file"]["name"]))
        {
            echo $_FILES["file"]["name"] . " 文件已经存在。 ";
        }
        else
        {
            $video_src = $_FILES["file"]["name"];
            $size = round(($_FILES["file"]["size"] / (1024*1024)),2);
            $file_size =  $size. " MB";
            $upload_time = date("Y/m/d h:i:s");
            $image_point = $_POST["image_point"];
            $gif_point = $_POST["gif_point"];
            
            $name = $_FILES["file"]["name"];
            $extension = ".".$extension;
            $name = str_replace($extension, "", $name);
            $image_src = $name.".jpg";
            $gif_src = $name.".gif";

            /*$sql = "INSERT INTO my_upload (video_src,image_src,gif_src,file_size,upload_time)
                    VALUES ('".$video_src."', '".$image_src."', '".$gif_src."', '".$file_size."', '".$upload_time."')";
            if($mysqli->query($sql) === TRUE) {
                echo "上传文件名: " . $_FILES["file"]["name"] . "<br>";
                echo "文件类型: " . $_FILES["file"]["type"] . "<br>";
                echo "文件大小: " . $file_size . "<br>";
            } else {
                echo "Error: " . $sql . "<br>" . $mysqli->error;
            }*/

            // 如果 upload 目录不存在该文件则将文件上传到 upload/video/ 目录下
            move_uploaded_file($_FILES["file"]["tmp_name"], "static/video/" . $_FILES["file"]["name"]);
            echo "文件存储在: " . "static/video/" . $_FILES["file"]["name"];

            //格式转换
            /*if($extension!=".mp4"||$extension!=".webm"||$extension!=".ogg"){             
                $from = "C:/xampp/htdocs/static/video/" . $_FILES["file"]["name"];
                $str = "ffmpeg -i ".$from." -ab 56000 -ar 22050 -b:a 500000 -r 29.97 -s 320x240 C:/xampp/htdocs/static/video/".$name.".mp4";
                system($str);
                echo "视频格式被转换<br>";
            }*/
            //gif_part
            $from = "C:/xampp/htdocs/static/video/" . $_FILES["file"]["name"];
            $str = "ffmpeg -i ".$from." -ss ".$gif_point." -s 480x360 -vframes 60 -y -f gif C:/Users/Dean/Desktop/".$name.".gif";
            system($str);

            //image_part
            $from = "C:/xampp/htdocs/static/video/" . $_FILES["file"]["name"];
            $str = "ffmpeg -i ".$from." -y -f image2 -ss ".$image_point." -t 0.001 -s 480x360 C:/Users/Dean/Desktop/".$name.".jpg";
            system($str);
                }
            }
        }
    else
    {
        echo "非法的文件格式";
    }
    $mysqli->close();
?>