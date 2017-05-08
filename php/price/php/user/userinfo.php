<?php
require_once '../../util/functions.php';
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../css/screen.css" type="text/css" media="screen" title="default"/>
    <title>添加监控商品</title>
</head>
<body>
<div id="page-top-outer">

    <!-- Start: page-top -->
    <div id="page-top">

        <!-- start logo -->
        <div id="logo">
            <h1 style="color: #fff; font-size: 35px">欢迎您！<?php session_start();
                    echo $_SESSION['name'] ?></h1>
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
            <table border="0" width="100%" cellpadding="0" cellspacing="0" id="content-table">
                <tr>
                    <th rowspan="3" class="sized"><img src="../../images/shared/side_shadowleft.jpg" width="20"
                                                       height="300"
                                                       alt=""/></th>
                    <th class="topleft"></th>
                    <td id="tbl-border-top">&nbsp;</td>
                    <th class="topright"></th>
                    <th rowspan="3" class="sized"><img src="../../images/shared/side_shadowright.jpg" width="20"
                                                       height="300"
                                                       alt=""/></th>
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
                                            <div class="step-dark-left"><a href="">个人信息</a></div>
                                            <div class="clear"></div>
                                        </div>
                                        <!--  end step-holder -->
                                        <!-- start id-form -->
                                        <?php
                                        $id1 = $_SESSION['id'];
                                        connectDB();
                                        $result = mysql_query("SELECT * FROM user WHERE user_id = $id1;");
                                        $result_arr = mysql_fetch_assoc($result);
                                        $id = $result_arr['user_id'];
                                        $name = $result_arr['user_name'];
                                        $pw = $result_arr['user_pwd'];
                                        $email = $result_arr['user_email'];
                                        ?>
                                        <table border="0" cellpadding="0" cellspacing="0" id="id-form">
                                            <tr>
                                                <th valign="top">ID:</th>
                                                <td><?php echo $id; ?></td>
                                                <td>

                                                </td>
                                            </tr>
                                            <tr>
                                                <th valign="top">用户名:</th>
                                                <td><?php echo $name; ?></td>
                                                <td>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th valign="top">密码:</th>
                                                <td><?php echo $pw; ?></td>
                                                <td></td>
                                            </tr>

                                            <tr>
                                                <th valign="top">邮箱:</th>
                                                <td><?php echo $email; ?></td>
                                                <td></td>
                                            </tr>
                                            <tr>              
												 <th valign="top"></th>
												<td>
													<input type="button"  class="form-edit" onclick="location.href='edituser.php?id=<?php echo $id;?>'"/>
                                            </tr>
                                        </table>
                                        <!-- end id-form  -->
                                    </td>
                                    <td>
                                        <!--  start related-activities -->
                                        <div id="related-activities">
                                            <!--  start related-act-top -->
                                            <div id="related-act-top">
                                                <img src="../../images/forms/header_related_act.gif" width="271"
                                                     height="43"
                                                     alt=""/>
                                            </div>
                                            <!-- end related-act-top -->
                                            <!--  start related-act-bottom -->
                                            <div id="related-act-bottom">
                                                <!--  start related-act-inner -->
                                                <div id="related-act-inner">

                                                    <div class="lines-dotted-short"></div>
                                                    <div class="left"><a href=""><img
                                                                    src="../../images/forms/icon_edit.gif"
                                                                    width="21" height="21" alt=""/></a>
                                                    </div>
                                                    <div class="right">
                                                        <h4>备注</h4>
                                                        <div style="height: 15px"></div>
                                                        请填写正确的邮箱地址，防止收不到提醒邮件！
                                                        <ul class="greyarrow">
                                                            <li><a href=""></a></li>
                                                        </ul>
                                                    </div>
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
        &copy Copyright By ShaTong, Zhendong Yang <span id="spanYear"></span>. All rights
        reserved.
    </div>
    <!--  end footer-left -->
    <div class="clear">&nbsp;</div>
</div>
</body>
</html>

