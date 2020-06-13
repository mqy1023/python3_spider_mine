

通过link extractor和rule的形式并配置CrawlSpider完成招聘网站所有职位的爬取


> crawlspider是Spider的派生类(一个子类)，Spider类的设计原则是只爬取start_url列表中的网页，而CrawlSpider类定义了一些规则(rule)来提供跟进link的方便的机制，从爬取的网页中获取link并继续爬取的工作更适合。


* 1、LinkExtractors的目的很简单：提取链接

* 2、在rules中包含一个或多个Rule对象，每个Rule对爬取网站的动作定义了特定的操作。