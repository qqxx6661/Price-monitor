<?php
require_once '../../util/functions.php';
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../css/screen.css" type="text/css" media="screen" title="default"/>
    <script type="text/javascript" src="../../js/jquery-1.4.4.js"></script>
	    <script type="text/javascript" src="../../js/pagePlay.js"></script>
    <title>所有商品信息</title>
</head>
<body>
<div id="page-top-outer">

    <!-- Start: page-top -->
    <div id="page-top">

        <!-- start logo -->
        <div id="logo">
            <a href="http://monitor.usau-buy.me/"><h1 style="color: #fff; font-size: 35px">欢迎您！<?php session_start();
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
        <h1 style="color: #1a1a1a; padding: 10px 0 20px 20px; font-size: 25px">所有商品信息</h1><h3><?php $user_id_admin=$_SESSION['id'];
            if ($user_id_admin==1||$user_id_admin==2){ echo '<a href="deleteAllProduct.php">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;删除所有商品（谨慎操作！）</a>';} ?></h3>
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
                                        <th class="table-header-repeat line-left minwidth-1">商品ID</th>
                                        <th class="table-header-repeat line-left minwidth-1">商品名称</th>
                                        <th class="table-header-repeat line-left minwidth-1">商城名称</th>
                                        <th class="table-header-repeat line-left minwidth-1">商品价格</th>
                                        <th class="table-header-repeat line-left minwidth-1">预期价格</th>
                                        <th class="table-header-repeat line-left minwidth-1">监控状态</th>
                                        <th class="table-header-repeat line-left minwidth-1">监控用户</th>
                                        <th class="table-header-repeat line-left minwidth-1">添加时间</th>
                                        <th class="table-header-repeat line-left minwidth-1">监控管理</th>
                                        <th class="table-header-repeat line-left minwidth-1">监控开关</th>
                                    </tr>
                                    <?php
                                    if ($user_id_admin==1||$user_id_admin==2){
                                        connectDB();
                                        $result = mysql_query("SELECT * FROM monitor ");
                                        $data_count = mysql_num_rows($result);
                                        for ($i = 0; $i < $data_count; $i++) {
                                            $result_arr = mysql_fetch_assoc($result);
                                            $id = $result_arr['id'];
                                            $item_id = $result_arr['item_id'];
                                            $item_name = $result_arr['item_name'];
                                            $mall_name = $result_arr['mall_name'];
                                            if ($mall_name=='jd'){
                                                $mall_name_ven='京东';
                                            }elseif ($mall_name=='tb'){
                                                $mall_name_ven='淘宝';
                                            }elseif($mall_name=='tm'){
                                                $mall_name_ven='天猫';
                                            }else{
                                                $mall_name_ven=$mall_name;
                                            }
                                            $item_price = $result_arr['item_price'];
                                            $user_id = $result_arr['user_id'];
                                            $add_date = $result_arr['add_date'];
                                            $user_result = mysql_query("SELECT * FROM user WHERE user_id = $user_id");
                                            $user_result_arr = mysql_fetch_assoc($user_result);
                                            $user_name = $user_result_arr['user_name'];
                                            $status = $result_arr['status'];
                                            $note = $result_arr['note'];
                                            $status == 0 ? ($statusCode = '<span style="color: red">尚未监控</span>') : ($statusCode = '<span style="color: green">正在监控</span>');
                                            $user_price = $result_arr['user_price'];
                                            echo "<tr><td>$item_id</td><td><a href='https://item.jd.com/$item_id.html'>$item_name</a></td><td>$mall_name_ven</td><td>$item_price</td><td>$user_price</td><td>$statusCode</td>
                                              <td>$user_name</td><td>$add_date</td><td><a href='editProduct.php?id=$id&&edit_auth=1'>修改</a>
                                              |<a href='deleteProduct.php?id=$id&&delete_auth=1'>删除</a></td>
                                              <td><a href=\"../product/monitorSwitch.php?status=1&&id=$id&&auth=1\" class=\"icon-5 info-tooltip\"></a><a href=\"../product/monitorSwitch.php?status=0&&id=$id&&auth=1\" class=\"icon-2 info-tooltip\"></a></td></tr>";
                                        }
                                    }else{
                                        echo '<tr><td colspan="10" style="color: red;font-size: 20px;text-align: center"> 你的访问权限不够,如果有疑问，请联系管理员！</td></tr>';
                                    }

                                    ?>
                                </table>
                                <!--  end product-table................................... -->
                            </form>
																											
                        </div>
                        <!--  end content-table  -->
						<table border="0" cellpadding="0" cellspacing="0" id="paging-table">
								<tr>
								<td>
									<a  id="firstPage" class="page-far-left"></a></td>
								<td>
									<a  id="frontPage" class="page-left"></a></td>
								<td>
									<div id="curPage" style="cursor:pointer;padding:0 10px 0 10px;"></div></td>
								<td>
									<a  id="nextPage" class="page-right"></a></td>
								<td>
									<a  id="lastPage" class="page-far-right"></a>
								</td>
								<td>
									<input type="text" id="inputPage" style="width:20px;"/>
									<span id="changePage">跳转</span></div>
								</td>
								</tr>
								</table>	
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
