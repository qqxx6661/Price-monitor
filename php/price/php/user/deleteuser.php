<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/12
 * Time: 9:07
 */
header("Content-type: text/html; charset=utf-8");
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
echo "<script> comfirm(\"你确定要删除吗？\")</script>";
mysql_query("DELETE FROM user WHERE user_id = $id");

if (mysql_errno()){
    echo "<script> alert(\"当前用户存在监控的商品，无法删除！\")</script>";
    $url="allusers.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}else{
    header("Location:allusers.php");
}