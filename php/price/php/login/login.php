<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/05/04
 * Time: 10:23
 */

require_once '../../util/functions.php';
header("Content-type: text/html; charset=utf-8");
if (empty($_POST['username'])) {
	echo'<script> alert("用户名不能为空哦！"); </script>';
	$url="../../index.php";
	echo "<script language=\"javascript\">";
	echo "location.href=\"$url\"";
	echo "</script>";
}
if (empty($_POST['password'])) {
   echo'<script> alert("密码不能为空哦！"); </script>';
	$url="../../index.php";
	echo "<script language=\"javascript\">";
	echo "location.href=\"$url\"";
	echo "</script>";

}

$name = $_POST['username'];
$password = $_POST['password'];

connectDB();

$result = mysql_query("SELECT * FROM user WHERE user_name = '$name' && user_pwd = '$password'");
$arr = mysql_fetch_assoc($result);
$result_count = mysql_num_rows($result);

if ($result_count != 0) {
    session_start();
    $_SESSION['id'] = $arr['user_id'];
    $_SESSION['name'] = $arr['user_name'];
    header("Location:../monitor/price.php");
} else {
    echo'<script> alert("用户名或密码错误！"); </script>';
	$url="../../index.php";
	echo "<script language=\"javascript\">";
	echo "location.href=\"$url\"";
	echo "</script>";
}


