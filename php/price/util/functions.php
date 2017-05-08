<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/13
 * Time: 15:10
 */
require_once 'config.php';

function connectDB()
{
    $conn = mysql_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PW);
    if (!$conn) {
        die('<span style="color:red">数据库连接失败！</span>');
    } else {
        mysql_select_db('pricemonitor');
        mysql_query("set character set 'utf8'");//读库
        mysql_query("set names 'utf8'");//写库
        return $conn;
    }
}