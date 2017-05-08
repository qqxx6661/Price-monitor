<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/04/26
 * Time: 14:28
 */
session_start();
$user_id =  $_SESSION['id'];
$item_id = $_GET['item_id'];
$item_name = $_GET['item_name'];
$mall_name = $_GET['mall_name'];
$item_price = $_GET['item_price'];
$user_price = $_GET['user_price'];

if (empty($item_id)) {
    echo "<script> alert(\"商品ID不能为空哦！\")</script>";
    $url="addProduct.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
require_once '../../util/functions.php';
connectDB();

mysql_query("INSERT INTO monitor (item_id,item_name,mall_name,item_price,user_price,status,user_id) 
VALUES ('$item_id','$item_name','$mall_name','$item_price','$user_price','1','$user_id')");
if (mysql_errno()) {
    echo mysql_error();
} else {
    $_SESSION['user_id'] = $user_id;
    header("Location:../monitor/price.php");
}