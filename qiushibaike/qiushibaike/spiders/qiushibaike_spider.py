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

        for content_div in content_list_div:
            item = QiushibaikeItem()
            item['author'] = content_div.xpath('./div/a[2]/h2/text()').get()
            item['content'] = content_div.xpath('./a/div/span/text()').getall()
            item['_id'] = content_div.attrib['id']

            yield item

        next_page = response.xpath('//*[@class="old-style-col1"]/ul/li[last()]/a').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
