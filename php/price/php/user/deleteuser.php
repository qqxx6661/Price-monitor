<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/12
 * Time: 9:07
 */

if(empty($_GET['id'])){
    echo "<script> alert(\"ID不能为空哦！\")</script>";
    $url="allusers.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}

require_once '../../util/functions.php';

connectDB();

$id = intval($_GET['id']);

mysql_query("DELETE FROM user WHERE user_id = $id");

if (mysql_errno()){
    die("delete failed");
}else{
    header("Location:allusers.php");
}