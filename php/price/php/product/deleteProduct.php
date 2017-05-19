<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/12
 * Time: 9:07
 */
header("Content-type: text/html; charset=utf-8");
if(empty($_GET['id'])){
    echo "<script> alert(\"ID不能为空！\")</script>";
    $url="../monitor/price.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
    $delete_auth = $_GET['delete_auth'];
require_once '../../util/functions.php';

connectDB();

$id = intval($_GET['id']);
echo "<script> confirm(\"您确定要删除吗?\")</script>";
mysql_query("DELETE FROM monitor WHERE id = $id");

if (mysql_errno()){
    echo "<script> alert(\"删除失败！\")</script>";
    $url="../monitor/price.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}else{

    echo "<script> alert(\"删除成功！\")</script>";
    if($delete_auth == 1&&$delete_auth!=null){
        $url="allproducts.php";
    }else{
        $url="../monitor/price.php";
    }
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}