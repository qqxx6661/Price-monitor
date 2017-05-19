<?php
require_once '../../util/functions.php';
session_start();
$user_id = $_SESSION['id'];
connectDB();
        $result_all = mysql_query("SELECT * FROM monitor where user_id = $user_id");
		$result_onMonitor = mysql_query("SELECT * FROM monitor where user_id = $user_id and status = 1");
		$result_offMonitor = mysql_query("SELECT * FROM monitor where user_id = $user_id and status = 0");
        $data_count = mysql_num_rows($result_all);
		$onMonitor_count = mysql_num_rows($result_onMonitor);
		$offMonitor_count = mysql_num_rows($result_offMonitor);
		?>
			
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../css/screen.css" type="text/css" media="screen" title="default"/>
	<script type="text/javascript" src="../../js/jquery-1.4.4.js"></script>
	<script type="text/javascript" src="../../js/pagePlay.js"></script>
    <title>价格监控</title>
</head>
<body>
<div id="page-top-outer">
    <!-- Start: page-top -->
    <div id="page-top">
        <!-- start logo -->
        <div id="logo">
            <a href="http://monitor.usau-buy.me/"><h1 style="color: #fff; font-size: 35px">欢迎使用,<?php 
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
                <ul class="select">
                    <li><a href="../other/other.php"><b>友情链接</b><!--[if IE 7]><!--></a><!--<![endif]-->
                        <!--[if lte IE 6]>
                        <table>
                            <tr>
                                <td><![endif]-->
                        <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                    </li>
                </ul>
                <?php
                if ($user_id == 1 || $user_id == 2) {
                    echo '<div class="nav-divider">&nbsp;</div>
                    <ul class="select">
                        <li><a href="../user/allusers.php"><b>用户管理</b><!--[if IE 7]><!--></a><!--<![endif]-->
                            <!--[if lte IE 6]>
                            <table>
                                <tr>
                                    <td><![endif]-->
                            <!--[if lte IE 6]></td></tr></table></a><![endif]-->
                        </li>
                    </ul>
                    <div class="nav-divider">&nbsp;</div>
                    <ul class="select">
                        <li><a href="../product/allproducts.php"><b>商品管理</b><!--[if IE 7]><!--></a><!--<![endif]-->
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
        <h1 style="color: #1a1a1a; padding: 10px 0 20px 20px; font-size: 25px">友情链接</h1>
		<h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如有版权问题，请联系作者删除！</h3>
        <table border="0" width="100%" cellpadding="0" cellspacing="0" id="content-table">
            <tr>
                <td></td>
            </tr>
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
                    <div id="content-table-inner">
                        <!--  start table-content  -->
                        <div id="table-content">
                            <!--  start product-table ..................................................................................... -->
                            <form id="mainform" action="">
                                <table border="0" width="100%" cellpadding="0" cellspacing="0" id="product-table">
                                    <tr>
                                        <td><a href="">图</a></td>
										<td><a href="">片</a></td>
										<td><a href="">待</a></td>
										<td><a href="">加</a></td>										
                                    </tr>
									<tr>
                                        <td><a href="">谢</a></td>
										<td><a href="">谢</a></td>
										<td><a href="">合</a></td>
										<td><a href="">作</a></td>										
                                    </tr>
									<tr>
                                        <td><a href=""></a></td>
										<td><a href=""></a></td>
										<td><a href=""></a></td>
										<td><a href=""></a></td>										
                                    </tr>
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
