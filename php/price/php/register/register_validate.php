<?php
/**
 * Created by PhpStorm.
 * User: shatong
 * Date: 2017/01/12
 * Time: 14:12
 */
// 定义变量并设置为空值
$nameErr = $emailErr = $passwordErr =   "";
$name = $email = $password = $comment =  "";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    if (empty($_GET["name"])) {
        $nameErr = "帐号是必填的";
    } else {
        $name = test_input($_GET["name"]);
        // 检查姓名是否包含字母和空白字符
        if (!preg_match("/^[a-zA-Z ]*$/", $name)) {
            $nameErr = "只允许字母和空格";
        }
    }
    if (empty($_GET["password"])) {
        $passwordErr = "密码是必填的";
    } else {
        $password = test_input($_GET["password"]);
        // 检查密码是否包含字母和空白字符
        if (!preg_match("/^[a-zA-Z ]*$/", $password)) {
            $passwordErr = "只允许字母和空格";
        }
    }

    if (empty($_GET["email"])) {
        $emailErr = "邮箱是必填的";
    } else {
        $email = test_input($_GET["email"]);
        // 检查电子邮件地址语法是否有效
        if (!preg_match("/([\w\-]+\@[\w\-]+\.[\w\-]+)/", $email)) {
            $emailErr = "无效的 email 格式";
            die();
        }
    }
    /*
        if (empty($_GET["website"])) {
            $website = "";
        } else {
            $website = test_input($_GET["website"]);
            // 检查 URL 地址语法是否有效（正则表达式也允许 URL 中的斜杠）
            if (!preg_match("/\b(?:(?:https?|ftp):\/\/|www\.)[-a-z0-9+&@#\/%?=~_|!:,.;]*[-a-z0-9+&@#\/%=~_|]/i",$website)) {
                $websiteErr = "无效的 URL";
            }
        }*/

    if (empty($_GET["comment"])) {
        $comment = "";
    } else {
        $comment = test_input($_GET["comment"]);
    }
}

function test_input($data)
{
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

?>