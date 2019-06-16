
**Price-Monitor:京东价格监控**

**Python3+Requests/Selenium+Sqlite/Mysql+免费代理池/代理接口**

[![License](https://img.shields.io/badge/license-GPLv3-yellowgreen.svg)]()
[![Poweredby](https://img.shields.io/badge/Powered%20by-requests-green.svg)]()
[![Poweredby](https://img.shields.io/badge/Powered%20by-selenium-green.svg)]()

该项目README分为两部分：

- 电商价格监控网站介绍
- 本开源代码爬虫项目介绍和使用指南

# 电商价格监控

由该开源爬虫孵化的项目**电商价格监控**目前已上线运营：访问电商价格监控平台：

<a href="https://price.monitor4all.cn/">https://price.monitor4all.cn/</a>


**网站实现功能：**

**【功能一】自定义商品监控：设置商品ID和预期价格，当商品价格【低于】设定的预期价格后自动发送邮件提醒用户。**

**【功能二】品类商品订阅：用户订阅后，该类降价幅度大于7折的【自营商品】会被选出并发送邮件提醒用户。**





![Pagedemo](docs/Pagedemo.png)

![Pagedemo2](docs/Pagedemo2.png)

![Pagedemo3](docs/Pagedemo3.png)

![Structure](docs/Structure.png)

**申明：本项目仅限于爬取网上公开可见的商品信息，请勿用于任何商业用途。**

## 关于网站源码

该库仅为**爬虫模块**代码，网站前后端代码暂时未开源，采用的是Springboot+React，请关注博客，之后会另开新库开源。




## 电商价格监控 TODO List

**持续更新中**

### 功能

- [x] 京东卡券价格，京东精选价格爬取
- [ ] QQ微信第三方登录
- [ ] 会员功能
- [ ] 京东二手商品监控
- [ ] 支持亚马逊中国，天猫，淘宝等商城

### 技术

- [x] 代理池重构，单独检验代理对电商网站可达性
- [x] 支持2种代理接口：芝麻代理， Redis代理
- [x] 使用Springboot代替Django作为网站后台
- [x] <a href="https://github.com/qqxx6661/Price-monitor/issues/2">商品副标题抓取，PLUS会员价格</a>
- [x] <a href="https://github.com/qqxx6661/Price-monitor/issues/3">商品历史价格</a>
- [x] Selenium + PhantomJS/Headless Chrome 爬取
- [ ] 支持更多的代理接口：vps拨号代理
- [ ] Docker一键部署

### 其他功能（欢迎Issue提供意见）

- [ ] <a href="https://github.com/qqxx6661/Price-monitor/issues/1">小说更新监控</a>



# 本开源代码：Price-Monitor（京东价格监控）

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

主要包含以下库：

- requests
- lxml
- selenium(可选)

可以创建环境后，使用项目自带的requirements.txt一键安装环境

```
pip install -r requirements.txt
```

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

### PS

- 默认使用selenium渲染页面抓取京东商品，代码详见crawler_selenium.py，也可以使用JS爬取，详见crawler_js.py（如需要使用js爬取可以自行修改monitor_main.py对接）
- 代码默认使用了SQLite，如需切换到Mysql，请自行修改conn_sql.py的注释

## 老版本

- <a href="https://github.com/qqxx6661/Price-Monitor-py2">Python2+requests+sqlite+代理池+Flask(web)</a>

- <a href="https://github.com/qqxx6661/Price-monitor-php">Python2+requests+mysql+代理池+Php(web)</a>

## Contribution

- Issue

## Introduction

- Monitor price changes for items at JD.com, users could set price for specific item. Once the price is lower than excepted, the server will send an e-mail to user.


