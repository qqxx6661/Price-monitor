price-monitor
==========

# 简介

**电商价格监控系统-爬虫代码**

**完整监控系统项目地址：<a href="https://github.com/qqxx6661/flask_yzd">点我</a>**

**京东商城商品价格监控，用户自行设置商品和预期价格，低于预期价格后自动发送邮件提醒用户抢购。**

**目前已经开放（新版）测试：访问<a href="http://www.usau-buy.me/">电商价格监控系统</a>便可体验。**

![image](Demo.png)

**申明：该项目只限于爬取网上公开可见的商品信息，与商城无关。**

# 项目依赖

- requests
- gevent
- lxml
- beautifulsoup4

# 使用步骤

**该代码依托于<a href="https://github.com/qqxx6661/flask_yzd">完整监控系统</a>，所以还没有写单独的接口，可能给单独运行带来不便，不过代码简单易懂，适用于给刚接触python爬虫和requests的同学参考。**

0. 需要数据库文件，我会上传一个.db到项目上来。如果我忘了，请issue提醒我

1. 开启Proxypool代理池，开始爬取代理ip


```
    python Proxypool/proxypool.py
```
2. 运行主程序

```
    python Pricemonitor/main.py
```

# 文件结构

- ProxyPool:代理池，防止被封<a href="https://github.com/Greyh4t/ProxyPool">原作者项目地址</a>

- PriceMonitor

    - additemcrawl.py: 添加商品立即抓取（单次抓取）

    - conn_sql.py: 连接数据库

    - crawl.py: 爬虫核心代码

    - main.py: 程序入口

    - send_email.py: 邮件提醒模块


# Introduction

monitor price changes in JD.com, users can set expected price of specific item. Once the price is lower than excepted, the server will send an e-mail to user.



