


##### 一、创建项目

`scrapy startproject qiushibaike`

* 进入项目目录`cd qiushibaike`

##### 二、`settings.py` 中设置

1、设置中关闭遵循网站爬虫协议

```python
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```

2、设置编码格式

```python
# 设置编码格式
FEED_EXPORT_ENCODING = 'utf-8'
```

##### 三、创建爬虫spider

`scrapy genspider qiushibaike_spider qiushibaike.com`

* 1、`qiushibaike.com` 是指定域名

* 2、可以看到`spiders` 目录中多了`qiushibaike_spider.py` 文件

* 3、编写`items.py` 文件

```python
import scrapy
class QiushibaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    _id = scrapy.Field()
```

* 4、编写`qiushibaike_spider.py` 文件

```python
# -*- coding: utf-8 -*-
import scrapy

from qiushibaike.items import QiushibaikeItem

class QiushibaikeSpiderSpider(scrapy.Spider):
    name = 'qiushibaike_spider'
    allowed_domains = ['qiushibaike.com']
    # start_urls = ['http://qiushibaike.com/']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'
    }

    # 定义请求链接
    def start_requests(self):
        urls = [
            'https://www.qiushibaike.com/text/page/1/',
            # 'https://www.qiushibaike.com/text/page/2/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers) # 回调我们的数据解析方

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'qiushi-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        content_left_div = response.xpath('//*[@class="col1 old-style-col1"]')
        content_list_div = content_left_div.xpath('./div')

        print('aaaa=', len(content_list_div))

        for content_div in content_list_div:
            item = QiushibaikeItem()
            item['author'] = content_div.xpath('./div/a[2]/h2/text()').get()
            item['content'] = content_div.xpath('./a/div/span/text()').getall()
            item['_id'] = content_div.attrib['id']

            yield item

        next_page = response.xpath('//*[@class="old-style-col1"]/ul/li[last()]/a').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

```

##### 四、执行爬虫命令

* 1、`scrapy crawl qiushibaike_spider`

* 2、保存输出文件到 `qiushibaike.json` 文件

   `scrapy crawl qiushibaike_spider -o qiushibaike.json`