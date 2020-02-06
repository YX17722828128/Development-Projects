<?php
    if(isset($_REQUEST['code'])){
         session_start();
        if($_REQUEST['code']==$_SESSION['code']){
            echo "正确";
        }else{
            echo "错误";
        }
    }
?>