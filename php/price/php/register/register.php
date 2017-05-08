<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>注册</title>
    <link rel="stylesheet" href="../../css/register.css" type="text/css" media="screen" title="default" />
    <script type="text/javascript" src="../../js/jquery-1.4.4.js"></script>
    <script type="text/javascript" src="../../js/user.js"></script>
</head>
<body id="login-bg">

<!-- Start: login-holder -->
<div id="login-holder">

    <!-- start logo -->
    <div id="logo-login">
        <h1 style="font-size: 25px;color: #fff;">用户注册</h1>
    </div>
    <!-- end logo -->

    <div class="clear"></div>
    <!--  start loginbox ................................................................................. -->
    <div id="loginbox">
        <!--  start login-inner -->
        <div id="login-inner">
            <form method="post" action="register_server.php" id="formRegister">
                <table border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <th>用户名</th>
                        <td colspan="2"><input type="text" name="name" id="name" class="login-inp" /></td>
                    </tr>
                    <tr>
                        <th>密 &nbsp;&nbsp;码</th>
                        <td colspan="2"><input type="password" name="password" id="password" class="login-inp"/></td>
                    </tr>
                    <tr>
                        <th>邮 &nbsp;&nbsp;箱</th>
                        <td colspan="2"><input type="text" name="email" id="email" class="login-inp" /></td>
                    </tr>
                    <tr>
                        <th></th>
                        <td><input type="button" id="send" class="submit-reg"/>
                            <input type="button"  id="res" class="reset-login"/></td>
                    </tr>
                </table>
            </form>
        </div>
        <!--  end login-inner -->
        <div class="clear"></div>
        <a href="../../index.php" class="forgot-pwd">已有帐号?</a>
    </div>
    <!--  end loginbox -->
</div>
<!-- End: login-holder -->
</body>
</html>