

#### 爬取csdn论坛`https://bbs.csdn.net/`话题topic列表数据和答案answer数据

##### 一、ORM库peewee

打开models.py

* 1、配置mysql

```
db = MySQLDatabase("csdn_spider", host="127.0.0.1", port=3333, user="root", password="root")
```
需要建好`csdn_spider`数据database

* 2、执行`python3 models.py`, 生成数据table

* 3、执行`python3 spider.py`, 爬取数据并写入到数据库中
