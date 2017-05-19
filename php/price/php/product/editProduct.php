<?php
require_once '../../util/functions.php';
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../css/screen.css" type="text/css" media="screen" title="default"/>
    <title>编辑监控商品</title>
</head>
<body>
<div id="page-top-outer">

    <!-- Start: page-top -->
    <div id="page-top">

        <!-- start logo -->
        <div id="logo">
            <h1 style="color: #fff; font-size: 35px">欢迎您！<?php session_start();
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
            <a href="../../index.php" id="logout"><img src="../../images/shared/nav/nav_logout.gif" width="64"
                                                       height="14"
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
                    <li><a href="addProduct.php"><b>添加商品</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="../user/userinfo.php"><b>个人信息</b><!--[if IE 7]><!--></a><!--<![endif]-->
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
        <form method="get" action="editProduct_server.php" name="editProduct">
            <table border="0" width="100%" cellpadding="0" cellspacing="0" id="content-table">
                <tr>
                    <th rowspan="3" class="sized"><img src="../../images/shared/side_shadowleft.jpg" width="20"
                                                       height="300" alt=""/></th>
                    <th class="topleft"></th>
                    <td id="tbl-border-top">&nbsp;</td>
                    <th class="topright"></th>
                    <th rowspan="3" class="sized"><img src="../../images/shared/side_shadowright.jpg" width="20"
                                                       height="300" alt=""/></th>
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
                                            <div class="step-dark-left"><a href="">编辑监控商品</a></div>
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
                                            $status = $result_arr['status'];
                                        }
                                        ?>
                                        <table border="0" cellpadding="0" cellspacing="0" id="id-form">
                                            <tr>
                                                <th valign="top">商品ID:</th>
                                                <td><input type="text" class="inp-form" name="item_id"
                                                           value="<?php echo $item_id; ?>"/></td>
                                                <td><input type="hidden" class="inp-form" name="user_id"
                                                           value="<?php echo $user_id; ?>"/>
                                                    <input type="hidden" class="inp-form" name="id"
                                                           value="<?php echo $id; ?>"/>
                                                    <input type="hidden" class="inp-form" name="status"
                                                           value="<?php echo $status; ?>"/></td>
                                            </tr>

                                            <tr>
                                                <th valign="top">商城名称:</th>
                                                <td><select class="inp-form" name="mall_name">
                                                        <option value="<?php echo $mall_name; ?>">
                                                            <?php
                                                            if ($mall_name == 'jd') {
                                                                $mall_name_ven = '京东';
                                                            } elseif ($mall_name == 'tb') {
                                                                $mall_name_ven = '淘宝';
                                                            } elseif ($mall_name == 'tm') {
                                                                $mall_name_ven = '天猫';
                                                            } else {
                                                                $mall_name_ven = $mall_name;
                                                            }
                                                            echo $mall_name_ven; ?></option>
                                                        <?php
                                                        if ($mall_name == 'jd') {
                                                            echo '<option value="tb">淘宝</option>
                                                    <option value="tm">天猫</option>';
                                                        } elseif ($mall_name == 'tb') {
                                                            echo '<option value="tm">天猫</option>
					                                 <option value="jd">京东</option>';
                                                        } elseif ($mall_name == 'tm') {
                                                            echo ' <option value="tb">淘宝</option>
                                                                 <option value="jd">京东</option>';
                                                        } else {
                                                            echo '<option value="tb">淘宝</option>
                                                    <option value="tm">天猫</option>
					                                 <option value="jd">京东</option>';
                                                        }
                                                        ?>
                                                    </select></td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                                <th valign="top">预期价格:</th>
                                                <td><input type="text" class="inp-form" name="user_price"
                                                           value="<?php echo $user_price; ?>"/></td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                            <tr>
                                                <th>&nbsp;</th>
                                                <td valign="top">
                                                    <input type="button" value="" class="form-submit"
                                                           onclick="document.editProduct.submit();"/>
                                                    <input type="reset" value="" class="form-reset"/>
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
                                                <img src="../../images/forms/header_related_act.gif" width="271"
                                                     height="43" alt=""/>
                                            </div>
                                            <!-- end related-act-top -->

                                            <!--  start related-act-bottom -->
                                            <div id="related-act-bottom">

                                                <!--  start related-act-inner -->
                                                <div id="related-act-inner">

                                                    <div class="left"><a href=""><img
                                                                    src="../../images/forms/icon_plus.gif" width="21"
                                                                    height="21" alt=""/></a></div>
                                                    <div class="right">
                                                        <h5>添加监控商品</h5>
                                                        Lorem ipsum dolor sit amet consectetur
                                                        adipisicing elitsed do eiusmod tempor.
                                                        <ul class="greyarrow">
                                                            <li><a href="">点此继续添加</a></li>
                                                        </ul>
                                                    </div>

                                                    <div class="clear"></div>
                                                    <div class="lines-dotted-short"></div>

                                                    <div class="left"><a href=""><img
                                                                    src="../../images/forms/icon_minus.gif" width="21"
                                                                    height="21" alt=""/></a></div>
                                                    <div class="right">
                                                        <h5>删除监控商品</h5>
                                                        Lorem ipsum dolor sit amet consectetur
                                                        adipisicing elitsed do eiusmod tempor.
                                                        <ul class="greyarrow">
                                                            <li><a href="">点此删除商品</a></li>
                                                        </ul>
                                                    </div>
                                                    <div class="clear"></div>
                                                    <div class="lines-dotted-short"></div>
                                                    <div class="left"><a href=""><img
                                                                    src="../../images/forms/icon_edit.gif" width="21"
                                                                    height="21" alt=""/></a></div>
                                                    <div class="right">
                                                        <h5>编辑监控商品</h5>
                                                        Lorem ipsum dolor sit amet consectetur
                                                        adipisicing elitsed do eiusmod tempor.
                                                        <ul class="greyarrow">
                                                            <li><a href="">点此编辑商品</a></li>
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
        &copy; Copyright BY ShaTong. <span id="spanYear"></span>All rights
        reserved.
    </div>
    <!--  end footer-left -->
    <div class="clear">&nbsp;</div>
</div>
</body>
</html>