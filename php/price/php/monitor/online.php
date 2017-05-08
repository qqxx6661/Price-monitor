<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2017/5/3
 * Time: 22:28
 */
function onlineUsers()
{
    session_start();
    $session = session_id();
    $time = time();
    $time_check = $time - 300;     //5分钟删除session id
    $tbl_name = 'online_users';
    connectDB();
    $sql = "SELECT * FROM $tbl_name WHERE session='$session'";
    $result = mysql_query($sql);
    $count = mysql_num_rows($result);

    if ($count == "0") {
        $sql1 = "INSERT INTO $tbl_name(session, time)VALUES('$session', '$time')";
        $result1 = mysql_query($sql1);
    } else {
        $sql2 = "UPDATE $tbl_name SET time='$time' WHERE session = '$session'";
        $result2 = mysql_query($sql2);
    }
    $sql3 = "SELECT * FROM $tbl_name";
    $result3 = mysql_query($sql3);
    $count_user_online = mysql_num_rows($result3);
    $sql4 = "DELETE FROM $tbl_name WHERE time<$time_check";
    $result4 = mysql_query($sql4);
    return $count_user_online;
}

function monitorProducts(){
    connectDB();
    $product_num = mysql_num_rows(mysql_query("SELECT * FROM monitor where status = '1'"));
    return $product_num;
}
