<?php
require_once '../util/functions.php';
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../css/screen.css" type="text/css" media="screen" title="default"/>
    <title>价格监控</title>
</head>
<body>
<div id="page-top-outer">
    <!-- Start: page-top -->
    <div id="page-top">
        <!-- start logo -->
        <div id="logo">
            <a href="http://monitor.usau-buy.me/"><h1 style="color: #fff; font-size: 35px">欢迎使用，<?php session_start();
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
            <a href="../index.html" id="logout"><img src="../images/shared/nav/nav_logout.gif" width="64"
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
                    <li><a href="../php/price.php"><b>价格监控</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>

                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="../php/product/addProduct.php"><b>添加商品</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="../php/user/userinfo.php"><b>个人信息</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <div class="nav-divider">&nbsp;</div>
                <ul class="select">
                    <li><a href="../php/about/about.php"><b>关于</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <?php
                $user_id = $_SESSION['id'];
                if ($user_id == 1 || $user_id == 2) {
                    echo '<div class="nav-divider">&nbsp;</div>
                    <ul class="select">
                        <li><a href="allusers.php"><b>后台管理</b><!--[if IE 7]><!--></a><!--<![endif]-->
                            <!--[if lte IE 6]>
                            <table>
                                <tr>
                                    <td><![endif]-->
                            <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                        </li>
                    </ul>';
                }
                ?>
                <div class="nav-divider">&nbsp;</div>
                <div class="clear"></div>
            </div>
            <div class="clear"></div>
        </div>
    </div>
    <div class="clear"></div>
    <!--  start nav-outer -->
</div>
<div id="content-outer">
    <!-- start content -->
    <div id="content">
        <h1 style="color: #1a1a1a; padding: 10px 0 20px 20px; font-size: 25px">价格监控（新添加商品的名称与价格会延迟显示，不影响监控）</h1>
        <table border="0" width="100%" cellpadding="0" cellspacing="0" id="content-table">
            <tr>
                <td></td>
            </tr>
            <tr>
                <th rowspan="3" class="sized"><img src="../images/shared/side_shadowleft.jpg" width="20"
                                                   height="300"
                                                   alt=""/></th>
                <th class="topleft"></th>
                <td id="tbl-border-top">&nbsp;</td>
                <th class="topright"></th>
                <th rowspan="3" class="sized"><img src="../images/shared/side_shadowright.jpg" width="20"
                                                   height="300"
                                                   alt=""/></th>
            </tr>
            <tr>
                <td id="tbl-border-left"></td>
                <td>
                    <div id="content-table-inner">
                        <!--  start table-content  -->
                        <div id="table-content">
                            <!--  start product-table ..................................................................................... -->
                            <form id="mainform" action="">
                                <table border="0" width="100%" cellpadding="0" cellspacing="0" id="product-table">
                                    <tr>
                                        <th class="table-header-repeat line-left minwidth-1">商品ID</th>
                                        <th class="table-header-repeat line-left minwidth-1">商品名称</th>
                                        <th class="table-header-repeat line-left minwidth-1">商城名称</th>
                                        <th class="table-header-repeat line-left minwidth-1">商品价格</th>
                                        <th class="table-header-repeat line-left minwidth-1">预期价格</th>
                                        <th class="table-header-repeat line-left minwidth-1">监控状态</th>
                                        <th class="table-header-repeat line-left minwidth-1">监控管理</th>
                                        <th class="table-header-repeat line-left minwidth-1">备注</th>
                                        <th class="table-header-repeat line-left minwidth-1">监控开关</th>
                                    </tr>
                                    <?php
                                    connectDB();
                                    $result = mysql_query("SELECT * FROM monitor where user_id = $user_id");
                                    $data_count = mysql_num_rows($result);
                                    for ($i = 0; $i < $data_count; $i++) {
                                        $result_arr = mysql_fetch_assoc($result);
                                        $id = $result_arr['id'];
                                        $item_id = $result_arr['item_id'];
                                        $item_name = $result_arr['item_name'];
                                        $mall_name = $result_arr['mall_name'];
                                        $item_price = $result_arr['item_price'];
                                        $user_id = $result_arr['user_id'];
                                        $status = $result_arr['status'];
                                        $note = $result_arr['note'];
                                        $status == 0?($statusCode =  '<span style="color: red">尚未监控</span>'):($statusCode = '<span style="color: green">正在监控</span>');
                                        $user_price = $result_arr['user_price'];
                                        echo "<tr><td>$item_id</td><td><a href='https://item.jd.com/$item_id.html'style="text-decoration: none;">$item_name</a></td><td>$mall_name</td><td>$item_price</td><td>$user_price</td><td>$statusCode</td>
                                              <td><a href='editProduct.php?id=$id'>修改</a>
                                              |<a href='deleteProduct.php?id=$id'>删除</a></td><td>$note</td>
                                              <td><a href=\"switch.php?status=1&&id=$id\" class=\"icon-5 info-tooltip\"></a><a href=\"switch.php?status=0&&id=$id\" class=\"icon-2 info-tooltip\"></a></td></tr>";
                                    }
                                    ?>
                                </table>
                                <!--  end product-table................................... -->
                            </form>
                        </div>
                        <!--  end content-table  -->
                </td>
                <td id="tbl-border-right"></td>
            </tr>
            <tr>
                <th class="sized bottomleft"></th>
                <td id="tbl-border-bottom">&nbsp;</td>
                <th class="sized bottomright"></th>
            </tr>
        </table>
        <div class="clear"></div>

    </div>
    <!--  end content-table-inner ............................................END  -->
    </td>
    <tr>
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
</div>
<!--  end content-outer........................................................END -->
<!-- start footer -->
<div id="footer">
    <!--  start footer-left -->
    <div id="footer-left">
        &copy; Copyright By ShaTong, Zhendong Yang. <span id="spanYear"></span> <a href="http://monitor.usau-buy.me/"></a> All rights
        reserved.
    </div>
    <!--  end footer-left -->
    <div class="clear">&nbsp;</div>
</div>
</body>
</html>
