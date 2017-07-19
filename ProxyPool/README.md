# ProxyPool
Crawl and validate proxies from Internet

# Features
fake-useragent from https://github.com/hellysmile/fake-useragent

# Requirement
```
requests
gevent
lxml
beautifulsoup4
```
# How to use
just run in terminal
```
python proxypool.py
```
then
```
http://localhost:8000
```
or
```
http://localhost:8000/?num=1&port=80&type=3&protocol=http&minscore=0&area=北京
```
# Other
```
the parameter "type" means anonymous level
0: unknown
1: transparent
2: anonymous
3: high anonymous
```
