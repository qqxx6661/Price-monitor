
# Price-Monitor

**京东商品价格监控系统**

[![License](https://img.shields.io/badge/license-GPLv3-yellowgreen.svg)]()
[![Poweredby](https://img.shields.io/badge/Powered%20by-requests-green.svg)]()
[![Poweredby](https://img.shields.io/badge/Powered%20by-selenium-green.svg)]()

## 简介

用户自行设定指定商品的监控价格，运行爬虫脚本不间断获取价格数据，商品降价到设定价格后发送邮件提醒用户。

主要技术实现：Python爬虫/IP代理池/JS接口爬取/Selenium页面爬取

## README文档导航

- 若您只想**使用该项目监控京东商品**，请查看：[电商价格监控网站](#电商价格监控网站)
- 若您想搭建**京东商品页的爬虫代码**，请查看：[核心爬虫代码](#核心爬虫代码)
- 若您想搭建**京东商品监控项目（爬虫队列+数据存储+邮件提醒）**，请查看：[监控系统搭建](#监控系统搭建)


## 电商价格监控网站<span id="电商价格监控网站"></span>

由该开源**爬虫模块**孵化的项目**电商价格监控**目前已上线运营：

<a href="https://price.monitor4all.cn/">https://price.monitor4all.cn/</a>


**网站实现功能：**

**【功能一】自定义商品监控：设置商品ID和预期价格，当商品价格【低于】设定的预期价格后自动发送邮件提醒用户。**

**【功能二（暂时关闭）】品类商品订阅：用户订阅后，该类降价幅度大于7折的【自营商品】会被选出并发送邮件提醒用户。**

**【功能三】查看京东商品数据和商品价格趋势图**



![Pagedemo](docs/Pagedemo.png)

![Pagedemo2](docs/Pagedemo2.png)

![Pagedemo3](docs/Pagedemo3.png)

![Pagedemo3](docs/Pagedemo4.png)

### 网站架构

![Structure](docs/Structure.png)

**申明：本项目仅限于爬取网上公开可见的商品信息，请勿用于任何商业用途。**

### 该网站页面源码

网站前后端代码暂时未开源，采用的是SpringBoot + React，请关注博客，之后会另开新库开源。

### 网站功能 TODO

- [x] 京东卡券价格，京东精选价格爬取
- [ ] QQ微信第三方登录
- [ ] 会员功能
- [ ] 京东二手商品监控
- [ ] 支持亚马逊中国，天猫，淘宝等商城

### 网站技术 TODO

- [x] 代理池重构，单独检验代理对电商网站可达性
- [x] 支持代理接口：芝麻代理，Tor代理，自行搭建代理池
- [x] <a href="https://github.com/qqxx6661/Price-monitor/issues/2">商品副标题抓取，PLUS会员价格</a>
- [x] <a href="https://github.com/qqxx6661/Price-monitor/issues/3">商品历史价格</a>
- [x] Selenium + Headless Chrome 爬取
- [x] Docker一键部署
- [ ] 支持更多的代理接口：vps拨号代理

### 其他功能 TODO（欢迎Issue提供意见）

- [ ] <a href="https://github.com/qqxx6661/Price-monitor/issues/1">小说更新监控</a>



## 核心爬虫代码

请先使用`pip install -r requirements.txt`安装依赖库

你需要的仅仅只是这两个爬虫类：

- crawler_selenium: (推荐) 使用selenium+chrome访问京东商品单页进行爬取

- crawler_js.py: 使用requests访问京东商品数据接口进行爬取

两个类下方都有测试代码，可以调试，并且都可以接入http/https代理。

**代码里面包括了商品名称，副标题，PLUS价格，历史最高最低价等。**

由于电商经常会更新接口，所以爬虫代码往往具有时效性，若发现代码报错不要慌，自行尝试修改。

## 监控系统搭建

请先使用`pip install -r requirements.txt`安装依赖库

监控系统由如下部分组成：

- 数据库：负责数据的存储
- 爬虫任务队列：
    - 生产者：负责将用户设定的商品加入待爬队列
    - 消费者：收到消息后进行数据的抓取
- 邮件提醒任务队列：
    - 生产者：数据抓取后，与用户设定数据进行对比，需要发送提醒则发送消息
    - 消费者：异步发送提醒邮件

下面我们一步步搭建系统

### 数据库模块

数据库采用MySQL，Python使用SQLAlchemy连接数据库，主要涉及文件：



数据表有三张：

- pm_mail_record：邮件发送记录表
- pm_monitor_item：用户监控商品表
- pm_user：用户信息表

```

-- ----------------------------
-- Table structure for pm_mail_record
-- ----------------------------

DROP TABLE IF EXISTS `pm_mail_record`;
CREATE TABLE `pm_mail_record` (
 `id` int(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
 `address` varchar(64) NOT NULL COMMENT '邮箱地址',
 `from` varchar(64) NOT NULL COMMENT '发件人昵称',
 `to` varchar(64) NOT NULL COMMENT '收件人昵称',
 `subject` varchar(64) NOT NULL COMMENT '主题',
 `content` varchar(16384) NOT NULL COMMENT '内容',
 `is_sent` tinyint(3) NOT NULL COMMENT '1-发送成功, 0-发送失败',
 `gmt_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
 `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='邮件发送记录';

-- ----------------------------
-- Table structure for pm_user
-- ----------------------------
DROP TABLE IF EXISTS `pm_user`;
CREATE TABLE `pm_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  `email` varchar(40) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL COMMENT '是否活跃账号',
  `is_superuser` tinyint(1) NOT NULL COMMENT '是否管理员',
  `is_olduser` tinyint(1) DEFAULT '0',
  `gmt_create` datetime DEFAULT NULL,
  `gmt_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pm_monitor_item
-- ----------------------------
DROP TABLE IF EXISTS `pm_monitor_item`;
CREATE TABLE `pm_monitor_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_price` varchar(10) NOT NULL,
  `item_id` bigint(20) NOT NULL,
  `category_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `subtitle` varchar(512) DEFAULT NULL,
  `price` varchar(32) DEFAULT NULL,
  `plus_price` varchar(32) DEFAULT NULL,
  `max_price` varchar(32) DEFAULT NULL,
  `min_price` varchar(32) DEFAULT NULL,
  `discount` varchar(32) DEFAULT NULL,
  `last_price` varchar(32) DEFAULT NULL,
  `note` varchar(128) DEFAULT NULL COMMENT '备注（保留字段）',
  `sale` varchar(128) DEFAULT NULL,
  `label` varchar(128) DEFAULT NULL,
  `store_name` varchar(128) DEFAULT NULL,
  `is_ziying` tinyint(1) DEFAULT NULL COMMENT '是否自营',
  `is_alert` tinyint(1) NOT NULL COMMENT '是否已经提醒',
  `gmt_create` datetime DEFAULT NULL,
  `gmt_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```


## 文件结构

- docs:文档

- PriceMonitor

    - monitor_main.py: 程序入口

    - CONFIG.py: 常用参数设置
    
    - create_db.py: 创建数据库

    - conn_sql.py: 数据操作库
    
    - logger.conf: 日志参数设置
    
    - proxy.py: 代理IP获取
    
    - crawler_selenium/js.py: 爬虫脚本(二选一，默认采用crawler_selenium.py，如需要使用js爬取可以自行修改monitor_main.py对接)
    
    - mailbox.txt: 邮箱参数设置
    
    - mail.py: 邮件模块

- requirements.txt: 安装依赖




## 使用步骤

### 项目依赖

Python 3.5/3.6

主要需要以下库：

- requests
- lxml
- selenium

可以创建环境后，使用项目自带的requirements.txt一键安装环境

```
pip install -r requirements.txt
```

我们的爬虫有两种方式：

- Js接口爬取
- Selenium+Chrome网页渲染爬取

默认使用Selenium+Chrome进行京东商品爬取，因为Js接口变化频繁，需要频繁修改代码。



若您使用默认的Selenium+Chrome，您还需要安装好Chrome，以及Selenium用来操控Chrome的ChromeDriver。

http://npm.taobao.org/mirrors/chromedriver/

推荐采用2.35/2.36

若您在Windows下调试本项目，可以将ChromeDriver放置在任何配置了环境变量的目录下，我放在了C:/Windows/chromedriver.exe

若您使用Js爬取，不需要任何额外的库

### 1. 运行脚本，新建Sqlite数据库，添加测试商品

```
python PriceMonitor/create_db.py
```

我们有两张表User（用户表）和Monitor（商品表）：

```
取自create_db.py，给出了下列字段（SQLAlchemy格式），英文名称还是比较容易理解的，就不单个说明了。

User表：

column_id = Column(Integer, primary_key=True, autoincrement=True)
user_name = Column(String(32), nullable=False, unique=True)
email = Column(String(64), nullable=False, unique=True)

Monitor表：

column_id = Column(Integer, primary_key=True, autoincrement=True)
item_id = Column(BIGINT, nullable=False)
item_name = Column(String(128))
item_price = Column(String(32))
user_price = Column(String(32))
discount = Column(String(32))
lowest_price = Column(String(32))
highest_price = Column(String(32))
last_price = Column(String(32))
plus_price = Column(String(32))
subtitle = Column(String(128))
user_id = Column(Integer, ForeignKey('user.column_id'))
note = Column(String(128))
update_time = Column(DateTime)
add_time = Column(DateTime)
status = Column(Boolean, nullable=False)
user = relationship(User)
```

创建成功后可以使用<a href="http://sqlitebrowser.org/"> sqlitedatabasebrowser</a>图形化的查看数据库结构和数据。

可以通过conn_sql.py里运行现成代码添加用户和商品，如下方代码所示：

```
# add user named 'test'
sql.write_user('test', '404013419@qq.com')

# add test item
sql.write_item(['1306761', '15', '1'])  # 京东商品五月花抽纸编号为1306761，监控价格15元，用户id是刚才写入的账号的自增编号1('test', '404013419@qq.com')
```

![Sqlitedemo](docs/Sqlitedemo.png)

### 2. 设置邮件提醒的发件邮箱

简易教程请查看：<a href="https://github.com/qqxx6661/Price-monitor/blob/master/docs/SetupEmail.md">设置发件邮箱</a>

### 3. 你可以选择开启代理池抓取（3.1）或者直接使用本地抓取（3.2）


#### 3.1 开启Redis代理池，可以采用<a href="https://github.com/ShichaoMa/proxy_factory">proxy_factory</a>基于redis的简单代理工厂，感谢作者ShichaoMa。

**当然你也可以自行对接自己的代理池，只需修改proxy.py对应代码**

启动redis代理池后，修改CONFIG.py的设置：

```
PROXY_CRAWL = 1
PROXY_POOL_IP = "127.0.0.1"  # Your redis server ip
```

#### 3.2 直接采用本地IP进行监控（注意：请将抓取间隔CRAWL_TIME调大，避免自己的IP被禁）

```
PROXY_CRAWL = 0
```

### 4. 运行监控主程序

```
python monitor_main.py
```







## 老版本

- <a href="https://github.com/qqxx6661/Price-Monitor-py2">Python2+requests+sqlite+代理池+Flask前后端</a>

- <a href="https://github.com/qqxx6661/Price-monitor-php">Python2+requests+mysql+代理池+Php前后端</a>

## Contribution

- Issue, Pull Request

## Introduction

This open-source code focuses on monitoring price changes at JD.com, users could set expect price for specific item. 

Once the price is lower than excepted, the server will send an e-mail to user.

If you are interested in it, feel free to contract yangzd1993@foxmail.com