# Web Crawler using Python Scrapy
## Introduction
  We use Python Scrapy to crawl users' information (project in folder chictopia1) and images (project in folder chictopia2) on website [Chictopia](http://www.chictopia.com/).
  
The codes run successfully on Windows 10. 
## Requirements
- Python3
- Scrapy

**note: we recommend installing [Anaconda3](https://www.anaconda.com/download/) and using command ```conda install scrapy``` to install Scrapy.**
## Usage
Execute (double-click) file *start.bat* on Windows.

## Details (How to create a Web Crawler project?——Project chictopia1 for example)
#### 1. open *cmd* window
#### 2. input command ```scrapy startproject lifesjules``` to create a web crawler project folder
#### 3. write *items.py* and create a new file *spider.py* (as for some complex projects, you may need to rewrite *pipelines.py*)

**items.py**
```python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LifesjulesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    friends = scrapy.Field()
    following = scrapy.Field()
    followers = scrapy.Field()
    entry_url = scrapy.Field()
    link = scrapy.Field()
    favlink = scrapy.Field()
```

**spider.py**
```python
import scrapy

from lifesjules.items import LifesjulesItem


class LifesjulseSpider(scrapy.Spider):
    name = "lifesjules"
    allowed_domains = ["chictopia.com"]

    def start_requests(self):
        start_urls = ['http://www.chictopia.com/lifesjules',
                      'http://www.chictopia.com/user/fave_photos/lifesjules'
                      ]
        yield scrapy.Request(url=str(start_urls[0]), callback=self.parse_user)

        reqs = []

        for i in range(1, 8):
            req = str('http://www.chictopia.com/lifesjules/%s' % i)
            reqs.append(req)
        for url in reqs:
            yield scrapy.Request(url=url, callback=self.parse)

        favreqs = []

        for j in range(1, 5):
            favreq = str(
                'http://www.chictopia.com/user/fave_photos/lifesjules?page=%s' % j)
            favreqs.append(favreq)
        for favurl in favreqs:
            yield scrapy.Request(url=favurl, callback=self.parse_fav)

    def parse_user(self, response):
        sel = scrapy.selector.Selector(response)
        items = []
        item = LifesjulesItem()
        item['entry_url'] = 'http://www.chictopia.com/lifesjules'
        item['name'] = sel.xpath(
            '//div[@itemprop="name"]/text()')[0].extract().strip() #加[0]后返回list下第一个元素，strip()过滤空格，换行符等
        item['desc'] = sel.xpath(
            '//div[@class="px10 ullink"]/p[1]/text()')[0].extract().strip() + sel.xpath(
            '//div[@class="px10 ullink"]/p[2]/text()')[0].extract().strip() + sel.xpath(
            '//div[@class="px10 ullink"]/p[3]/text()')[0].extract().strip()
        item['friends'] = sel.xpath(
            '//div[@id="friend_count"]/text()')[0].extract().strip()
        item['following'] = sel.xpath(
            '//div[@id="fave_count"]/text()')[0].extract().strip()
        item['followers'] = sel.xpath(
            '//div[@id="follower_count"]/text()')[0].extract().strip()
        items.append(item)
        return items

    def parse(self, response):
        url_list = response.xpath(
            '//div[@id="bodywrapper"]')
        items = []
        for url in url_list:
            item = LifesjulesItem()
            item['link'] = url.xpath(
                '//div[@class="bold px12 white lh12 ellipsis"]/a/@href').extract() #没加[0]，返回一个完整的list
            items.append(item)

        return items

    def parse_fav(self, response):
        url_list = response.xpath(
            '//div[@id="bodywrapper"]')
        items = []
        for url in url_list:
            item = LifesjulesItem()
            item['favlink'] = url.xpath(
                '//div[@class="bold px12 white lh12 ellipsis"]/a/@href').extract()
            items.append(item)

        return items
```

**pipelines.py**
```python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import JsonItemExporter


class LifesjulesPipeline(object):
	def __init__(self):
		self.file = open('lifesjules.json', 'wb')
		self.exporter = JsonItemExporter(
		   self.file, encoding="utf-8", ensure_ascii=False)
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

    def process_item(self, item, spider):
    	self.exporter.export_item(item)
        return item
```
#### 4. run our web crawler and save data to a *.json* file
open *cmd* window in project folder, and input command ```scrapy crawl lifesjules -o lifesjules.json -t json```
