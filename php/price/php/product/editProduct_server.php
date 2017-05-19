<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/04/26
 * Time: 14:28
 */

$id = $_GET['id'];
$user_id =  $_GET['user_id'];
$item_id = $_GET['item_id'];
$mall_name = $_GET['mall_name'];
$status = $_GET['status'];
$user_price = $_GET['user_price'];
if (empty($item_id)) {
    echo "<script> alert(\"商品ID不能为空！\")</script>";
    $url="../product/editProduct.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
require_once '../../util/functions.php';
connectDB();

mysql_query("UPDATE monitor SET item_id = '$item_id',mall_name = '$mall_name',user_price = '$user_price',STATUS = $status,user_id = '$user_id' WHERE id = $id");
if (mysql_errno()) {
    echo mysql_error();
} else {
    session_start();
    $_SESSION['user_id'] = $user_id;
        header("Location:../monitor/price.php");
}