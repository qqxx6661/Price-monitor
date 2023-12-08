
# Price-Monitor

**JD商品价格监控**

[![License](https://img.shields.io/badge/license-GPLv3-yellowgreen.svg)]()
[![Poweredby](https://img.shields.io/badge/Powered%20by-requests-green.svg)]()
[![Poweredby](https://img.shields.io/badge/Powered%20by-selenium-green.svg)]()

## 简介

用户自行设定指定商品的监控价格，运行脚本获取价格数据。

**申明：本脚本没有涉及JD账号登录，没有抓取任何JD敏感信息，仅在手动执行一次脚本时会读取JD公开商品页面的商品名称和价格，如有任何敏感侵权问题，请联系我删除。**

**申明：本脚本没有涉及JD账号登录，没有抓取任何JD敏感信息，仅在手动执行一次脚本时会读取JD公开商品页面的商品名称和价格，如有任何敏感侵权问题，请联系我删除。**

**申明：本脚本没有涉及JD账号登录，没有抓取任何JD敏感信息，仅在手动执行一次脚本时会读取JD公开商品页面的商品名称和价格，如有任何敏感侵权问题，请联系我删除。**



## 核心代码

请先使用`pip install -r requirements.txt`安装依赖库

你需要的仅仅只是这两个Crawler类：

- crawler_selenium: (推荐) 使用selenium+chrome访问某东商品单页进行爬取

- crawler_js.py: 使用requests访问某东商品数据接口进行爬取

两个类下方都有测试代码，可以调试，并且都可以接入http/https代理。

**代码里面包括了商品名称，副标题，PLUS价格，历史最高最低价等。**

由于电商经常会更新接口，所以Crawler代码往往具有时效性，若发现代码报错不要慌，自行尝试修改。


### 使用selenium+chrome注意事项

需要安装chrome和chromedriver

若您使用默认的Selenium+Chrome，您还需要安装好Chrome，以及Selenium用来操控Chrome的ChromeDriver。

http://npm.taobao.org/mirrors/chromedriver/

若您在Windows下调试本项目，可以将ChromeDriver放置在任何配置了环境变量的目录下，我放在了C:/Windows/chromedriver.exe

若您使用Js爬取，不需要任何额外的库

