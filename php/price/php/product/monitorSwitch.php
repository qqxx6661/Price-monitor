<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/12
 * Time: 10:23
 */

require_once '../../util/functions.php';
header("Content-type: text/html; charset=utf-8");

if (empty($_GET['id'])) {
    echo "<script> alert(\"商品ID有误！\")</script>";
    $url="../monitor/price.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
$status = $_GET['status'];
$id = $_GET['id'];
connectDB();
$result = mysql_query("SELECT * FROM monitor WHERE id =$id  ");
$arr = mysql_fetch_assoc($result);
$result_count = mysql_num_rows($result);

if ($result_count != 0) {
        mysql_query("update monitor set status = $status WHERE id =$id  ");
        if ($_GET['auth']==1){
            header("Location:allproducts.php");
        }else{
            header("Location:../monitor/price.php");
        }
} else {
    echo "<script> alert(\"开启监控商品失败！\")</script>";
    $url="../monitor/price.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}



