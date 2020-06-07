

#### 爬取京东某个商品详情页

##### 一、ORM库peewee

打开models.py

* 1、配置mysql

```
db = MySQLDatabase("jd_spider", host="127.0.0.1", port=3333, user="root", password="root")
```
需要建好`jd_spider`数据database

* 2、执行`python3 models.py`, 生成数据table

* 3、执行`python3 jd_selenium_spider.py`, 爬取数据并写入到数据库中
