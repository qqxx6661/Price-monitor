<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/12
 * Time: 14:28
 */
date_default_timezone_set('Asia/Shanghai');
header("Content-type: text/html; charset=utf-8");
$name = $_POST['name'];
$password = $_POST['password'];
$email = $_POST['email'];
$register_date = date('Y-m-d H:i:s');
if (empty($name)) {
    echo "<script> alert(\"用户名不能为空哦！\")</script>";
    $url="register.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
if (empty($password)) {
    echo "<script> alert(\"密码不能为空哦！\")</script>";
    $url="register.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
if (empty($email)) {
    echo "<script> alert(\"邮箱不能为空哦！\")</script>";
    $url="register.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
require_once '../../util/functions.php';
connectDB();
$user_name_count = mysql_num_rows(mysql_query("select * from user where user_name='$name'"));
if($user_name_count>0){
	echo"<script> alert(\"用户名已存在，请重新输入！\")</script>";
	$url="register.php";
	echo "<script language=\"javascript\">";
	echo "location.href=\"$url\"";
	echo "</script>";
}else{
	mysql_query("INSERT INTO user (user_name,user_pwd,user_email,register_date) VALUES ('$name','$password','$email','$register_date')");
	if (mysql_errno()) {
		echo mysql_error();
	} else {
		session_start();
		$_SESSION['user_name'] = $name;
		header("Location:registerSuccess.php");
	}
}