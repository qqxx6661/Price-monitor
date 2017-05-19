<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/04/26
 * Time: 14:28
 */
header("Content-type: text/html; charset=utf-8");
session_start();
$user_id =  $_SESSION['id'];
$item_id = $_GET['item_id'];
$item_name = "商品名和当前商品价格正在抓取，请稍等...";
$mall_name = $_GET['mall_name'];
$user_price = $_GET['user_price'];
require_once '../../util/functions.php';
connectDB();
if($item_id!=''){
    if ($user_price!=''){
        mysql_query("INSERT INTO monitor (item_id,item_name,mall_name,user_price,status,user_id)VALUES ('$item_id','$item_name','$mall_name','$user_price','1','$user_id')");
        $_SESSION['user_id'] = $user_id;
        header("Location:../monitor/price.php");
    }else{
        echo "<script> alert(\"请设置您预期的价格哦！\")</script>";
        $url="addProduct.php";
        echo "<script language=\"javascript\">";
        echo "location.href=\"$url\"";
        echo "</script>";
    }
}else{
    echo "<script> alert(\"商品ID不能为空哦！\")</script>";
    $url="addProduct.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
if (mysql_errno()) {
    echo "<script> alert(\"添加失败！\")</script>";
    $url="addProduct.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}