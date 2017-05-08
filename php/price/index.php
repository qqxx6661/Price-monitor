<?php
require_once 'util/functions.php';
require_once 'php/monitor/online.php';
?>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>电商价格监控系统</title>
    <link rel="stylesheet" href="css/screen.css" type="text/css" media="screen" title="default"/>
    <script type="text/javascript" src="js/user.js"></script>
</head>
<body id="login-bg" onload="getLangDate()">
<div id="online_users">
    <h1 style="font-size: 15px;color: #fff;">&nbsp;</h1>
</div>
<div>
    <h1 id="online_users"><?php echo '当前在线人数：' . onlineUsers(); ?></h1>
</div>
<div>
    <h1 id="products"><?php echo '当前监控商品：' . monitorProducts(); ?></h1>
</div>
<div>
    <h1 id="dateStr">时间载入中...</h1>
</div>

<!-- Start: login-holder -->
<div id="login-holder">

    <!-- start logo -->
    <div id="logo-login">
        <h1 style="font-size: 25px;color: #fff;">电商价格监控系统</h1>

    </div>
    <!-- end logo -->

    <div class="clear"></div>

    <!--  start loginbox ................................................................................. -->
    <div id="loginbox">

        <!--  start login-inner -->
        <div id="login-inner">
            <form name="formLogin" action="php/login/login.php" method="post">
                <table border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <th>用户名</th>
                        <td colspan="2"><input type="text" class="login-inp" name="username"/></td>
                    </tr>
                    <tr>
                        <th>密 &nbsp;&nbsp;码</th>
                        <td colspan="2"><input type="password" class="login-inp" name="password"/></td>
                    </tr>
                    <tr>
                        <th></th>
                        <td valign="top" colspan="2"><input type="checkbox" class="checkbox-size"
                                                            id="login-check"/><label for="login-check">记住我</label></td>
                    </tr>
                    <tr>
                        <th></th>
                        <td><input type="button" class="submit-login" onclick="document.formLogin.submit();"/></td>
                        <td><a href="php/register/register.php"><input type="button" class="submit-reg"/></a></td>
                    </tr>
                </table>
            </form>
        </div>
        <!--  end login-inner -->
        <div class="clear"></div>
        <a href="php/forgetPwd/forgetPwd.php" class="forgot-pwd">忘记密码?</a>
    </div>
    <!--  end loginbox -->
</div>
<!-- End: login-holder -->
</body>
</html>