<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>注册成功</title>
    <link rel="stylesheet" href="../../css/screen.css" type="text/css" media="screen" title="default" />
</head>
<body id="login-bg">

<!-- Start: login-holder -->
<div id="login-holder">

    <!-- start logo -->
    <div id="logo-login">
        <h1 style="font-size: 25px;color: #fff;">注 册 成 功</h1>
    </div>
    <!-- end logo -->

    <div class="clear"></div>
    <div id="loginbox">
        <div id="login-inner">
            <table border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <th style="height: 40px;font-size: 20px;color: white">恭喜您！</th>
                    <td colspan="2"><span style="color: red;font-size: 20px"><?php session_start();
                        echo $_SESSION['user_name'] ?></span>，<span style="color: white;font-size: 20px">注册成功！ </td>
                </tr>
                <tr>
                    <th style="height: 50px;font-size: 15px;color: white">现在去登录</th>
                    <td>
                    <a href="../../index.php"
                           class="sbm_btn"">GO</a></td>
                </tr>
            </table>
        </div>
        <!--  end login-inner -->
        <div class="clear"></div>
    </div>
    <!--  end loginbox -->
</div>
<!-- End: login-holder -->
</body>
</html>