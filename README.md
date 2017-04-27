price-monitor
==========

# 简介 Introduction

**京东商城商品价格监控，用户自行设置商品和预期价格，低于预期价格后自动发送邮件提醒用户抢购。**

monitor price changes in JD.com, users can set expected price of specific item. Once the price is lower than excepted, the server will send an e-mail to user. 

**以后将逐步支持更多商城： 天猫，淘宝，亚马逊等**

Amazon-CN, Amazon-US, Tmall will be supported in the future

该项目由网页端      (php)-----Mysql-----后台监控(Python)      组成。

目前库中只有后台监控(price-monitor-server)的源代码，之后将全部放上。

**目前已经开放测试：访问<a href="http://monitor.usau-buy.me/">电商价格监控系统</a>便可体验。**

# 项目依赖

**php**

**mysql**

**python**

- requests
- mysql-connector-python
- bs4
- lxml


# 使用步骤 Usage

- 建立Mysql数据库pricemonitor，内有两张表user， monitor。sql文件见mysql文件夹。数据库默认账号密码为root

- 在price-monitor-server文件夹新建mailbox.txt文件，内容为三行

       第一行为发送邮箱地址
       第二行为发送邮箱密码
       第三行为邮箱的stmp

       举例：
```
xxxxxxxxx@xxx.edu.cn  
xxxxxxxx
stmp.xxx.edu.cn
```
至此，你已经搭建好爬虫，可以自行在数据库添加条目，然后执行conn_sql.py进行测试！

- 若您需要搭建自己的网页端，则配置apache+php+mysql或者nginx+php+mysql的组合，之后放入php文件夹price（待上传）


# 待完成 to be done...
