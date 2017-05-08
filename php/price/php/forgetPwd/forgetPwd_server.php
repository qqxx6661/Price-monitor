<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2017/5/4
 * Time: 22:02
 */
header("Content-type: text/html; charset=utf-8");
$name = $_POST['name'];
$email = $_POST['email'];

if (empty($name)) {
    echo "<script> alert(\"用户名不能为空哦！\")</script>";
    $url="forgetPwd.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}

if (empty($email)) {
    echo "<script> alert(\"邮箱不能为空哦！\")</script>";
    $url="forgetPwd.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
require_once '../../util/functions.php';
connectDB();
$forget_result=mysql_query("select * from user where user_name='$name' AND user_email = '$email'");
$forget_result_count = mysql_num_rows($forget_result);
$forget_arr = mysql_fetch_assoc($forget_result);
if($forget_result_count>0){
    $url="forgetPwd.php";
    session_start();
    $_SESSION['user_pwd'] = $forget_arr['user_pwd'];
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\";";
    echo "</script>";
//    echo "<script>document.getElementById(\"forget_Message\").innerHTML(\"您的密码是:$user_pwd\");</script>";

}else{
    echo "<script> alert(\"你输入的用户名和密码不匹配！如果有疑问，请联系网站管理员！QQ：862681898 OR 404013419\")</script>";
    $url="forgetPwd.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}