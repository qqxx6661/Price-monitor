<?php
require_once '../../util/functions.php';
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../css/screen.css" type="text/css" media="screen" title="default"/>
    <script type="text/javascript" src="../../js/jquery-1.4.4.js"></script>
    <script type="text/javascript" src="../../js/user.js"></script>
    <title>修改用户信息</title>
</head>
<?php
if (!empty($_GET['id'])) {
    connectDB();
    $id = $_GET['id'];
    $result = mysql_query("SELECT * FROM user WHERE user_id = $id");
    $arr = mysql_fetch_assoc($result);
    $name = $arr['user_name'];
    $password = $arr['user_pwd'];
    $email = $arr['user_email'];
} else {
    echo "<script> alert(\"ID不能为空哦！\")</script>";
    $url="userinfo.php";
    echo "<script language=\"javascript\">";
    echo "location.href=\"$url\"";
    echo "</script>";
}
?>
<body>
<div id="page-top-outer">
    <!-- Start: page-top -->
    <div id="page-top">
        <!-- start logo -->
        <div id="logo">
            <a href="http://jd.usau-buy.me/"><h1 style="color: #fff; font-size: 35px">欢迎您！<?php session_start();
                    echo $_SESSION['name'] ?></h1></a>
        </div>
        <div class="clear"></div>
    </div>
    <!-- End: page-top -->
</div>
<div class="nav-outer-repeat">
    <!--  start nav-outer -->
    <div class="nav-outer">
        <!-- start nav-right -->
        <div id="nav-right">
            <div class="nav-divider">&nbsp;</div>
            <a href="../../index.php" id="logout"><img src="../../images/shared/nav/nav_logout.gif" width="64" height="14"
                                                       alt=""/></a>
            <div class="nav-divider">&nbsp;</div>
            <div class="clear">&nbsp;</div>
        </div>
        <!-- end nav-right -->
        <div class="nav">
            <div class="table">
                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="../monitor/price.php"><b>价格监控</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>

                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="../product/addProduct.php"><b>添加商品</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="userinfo.php"><b>个人信息</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="../about/about.php"><b>关于</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <div class="nav-divider">&nbsp;</div>
                <div class="clear"></div>
            </div>
            <div class="clear"></div>
        </div>
    </div>
    <div class="clear"></div>
    <!--  start nav-outer -->
</div>
<!-- start content-outer -->
<div id="content-outer">
    <!-- start content -->
    <div id="content">
        <form action="edituser_server.php" method="GET" name="formEdit" >
            <table border="0" width="100%" cellpadding="0" cellspacing="0" id="content-table">
                <tr>
                    <th rowspan="3" class="sized"><img src="../../images/shared/side_shadowleft.jpg" width="20" height="300" alt="" /></th>
                    <th class="topleft"></th>
                    <td id="tbl-border-top">&nbsp;</td>
                    <th class="topright"></th>
                    <th rowspan="3" class="sized"><img src="../../images/shared/side_shadowright.jpg" width="20" height="300" alt="" /></th>
                </tr>
                <tr>
                    <td id="tbl-border-left"></td>
                    <td>
                        <!--  start content-table-inner -->
                        <div id="content-table-inner">
                            <table border="0" width="100%" cellpadding="0" cellspacing="0">
                                <tr valign="top">
                                    <td>
                                        <!--  start step-holder -->
                                        <div id="step-holder">
                                            <div class="step-no">★</div>
                                            <div class="step-dark-left"><a href="">修改用户信息</a></div>
                                            <div class="clear"></div>
                                        </div>
                                        <!--  end step-holder -->
                                        <!-- start id-form -->
                                        <?php $id = $_GET['id'];
                                        connectDB();
                                        $result = mysql_query("SELECT * FROM monitor where id = $id");
                                        $data_count = mysql_num_rows($result);
                                        for ($i = 0; $i < $data_count; $i++) {
                                            $result_arr = mysql_fetch_assoc($result);
                                            $id = $result_arr['id'];
                                            $item_id = $result_arr['item_id'];
                                            $item_name = $result_arr['item_name'];
                                            $mall_name = $result_arr['mall_name'];
                                            $item_price = $result_arr['item_price'];
                                            $user_id = $result_arr['user_id'];
                                            $user_price = $result_arr['user_price'];
                                        }
                                        ?>
                                        <table border="0" cellpadding="0" cellspacing="0"  id="id-form">
                                            <tr>
                                                <th valign="top">ID:</th>
                                                <td><input type="text" class="inp-form" name="id" value="<?php echo $id ?>" readonly></td>

                                            </tr>
                                            <tr>
                                                <th valign="top">用户名:</th>
                                                <td><input type="text" class="inp-form" name="username" id="name" value="<?php echo $name ?>"></td>
                                                <td>
                                                    <input type="hidden"  name="id" value="<?php echo $id;?>"/>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th valign="top">密码:</th>
                                                <td><input type="text" class="inp-form" name="password" id="password" value="<?php echo $password ?>"></td>
                                                <td></td>
                                            </tr>

                                            <tr>
                                                <th valign="top">邮箱:</th>
                                                <td><input type="text" class="inp-form" name="email" id="email" value="<?php echo $email ?>"></td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                                <th>&nbsp;</th>
                                                <td valign="top">
                                                    <input type="button" value="" class="form-submit" onclick="document.formEdit.submit();"/>
                                                    <input type="reset" value="" class="form-reset"  />
                                                </td>
                                                <td></td>
                                            </tr>
                                        </table>
                                        <!-- end id-form  -->
                                    </td>
                                    <td>
                                        <!--  start related-activities -->
                                        <div id="related-activities">
                                            <!--  start related-act-top -->
                                            <div id="related-act-top">
                                                <img src="../../images/forms/header_related_act.gif" width="271" height="43" alt="" />
                                            </div>
                                            <!-- end related-act-top -->
                                            <!--  start related-act-bottom -->
                                            <div id="related-act-bottom">
                                                <!--  start related-act-inner -->
                                                <div id="related-act-inner">
                                                    <div class="lines-dotted-short"></div>
                                                    <div class="left"><a href=""><img src="../../images/forms/icon_edit.gif" width="21" height="21" alt="" /></a></div>
                                                    <div class="right">
                                                        <h5>个人信息修改</h5>
                                                        此页面修改你的个人信息，用户名和密码都不少于6位数哦！
                                                        <ul class="greyarrow">

                                                        </ul>
                                                    </div>
                                                    <div class="clear"></div>
                                                </div>
                                                <!-- end related-act-inner -->
                                                <div class="clear"></div>
                                            </div>
                                            <!-- end related-act-bottom -->
                                        </div>
                                        <!-- end related-activities -->
                                    </td>
                                </tr>
                            </table>
                            <div class="clear"></div>
                        </div>
                        <!--  end content-table-inner  -->
                    </td>
                    <td id="tbl-border-right"></td>
                </tr>
                <tr>
                    <th class="sized bottomleft"></th>
                    <td id="tbl-border-bottom">&nbsp;</td>
                    <th class="sized bottomright"></th>
                </tr>
            </table>
            <div class="clear">&nbsp;</div>

    </div>
    <!--  end content -->
    <div class="clear">&nbsp;</div>
</div>
<!--  end content-outer -->

<!-- start footer -->
<div id="footer">
    <!--  start footer-left -->
    <div id="footer-left">
        &copy; Copyright BY ShaTong. <span id="spanYear"></span> <a href="http://jd.usau-buy.me/"></a>. All rights
        reserved.
    </div>
    <!--  end footer-left -->
    <div class="clear">&nbsp;</div>
</div>
</body>
</html>