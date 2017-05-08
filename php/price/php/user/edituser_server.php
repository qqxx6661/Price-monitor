<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/11
 * Time: 17:20
 */

if (!isset($_GET['username'])){
    echo "<script> alert(\"用户名不能为空哦！\")</script>";
    $url="userinfo.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
if (!isset($_GET['password'])){
    echo "<script> alert(\"密码不能为空哦！\")</script>";
    $url="userinfo.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
$id = $_GET['id'];
$username = $_GET['username'];
$password = $_GET['password'];
$email = $_GET['email'];
$personal = $_GET['personal'];

if (empty($username)){
    echo "<script> alert(\"用户名不能为空哦！\")</script>";
    $url="userinfo.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
if (empty($password)){
    echo "<script> alert(\"密码不能为空哦！\")</script>";
    $url="userinfo.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
if (empty($email)){
    echo "<script> alert(\"邮箱不能为空哦！\")</script>";
    $url="userinfo.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}

require_once '../../util/functions.php';

connectDB();

mysql_query("UPDATE user set user_name ='$username',user_pwd ='$password',user_email='$email' 
            WHERE user_id = $id" );
if (mysql_errno()){
    echo mysql_error();
}else{
        header("Location:userinfo.php");
}
