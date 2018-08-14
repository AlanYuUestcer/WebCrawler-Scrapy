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
#### 2. run command ```scrapy startproject chictopia1``` to create a web crawler project folder
#### 3. write *items.py* and create a new file *chictopia1_spider.py* in folder *spiders* (as for some complex projects, you may need to rewrite *pipelines.py*)

**items.py**
```python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Chictopia1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    friends = scrapy.Field()
    following = scrapy.Field()
    followers = scrapy.Field()
    entry_url = scrapy.Field()
```

**chictopia1_spider.py**
```python
import scrapy

from chictopia1.items import Chictopia1Item

URL_BASE = 'http://www.chictopia.com'


class Chictopia1Spider(scrapy.Spider):
    name = "chictopia1"
    allowed_domains = ["chictopia.com"]

    def __init__(self, user=None, *args, **kwargs):
        super(Chictopia1Spider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.chictopia.com/%s" % (user)]

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        items = []
        item = Chictopia1Item()
        entry_url_0 = str(
            sel.xpath('//div[@class="left pagination"]/a/@href')[0].extract().strip())
        entry_url_1 = entry_url_0.strip('/2')

        item['entry_url'] = URL_BASE + '/' + entry_url_1
        item['name'] = sel.xpath(
            '//div[@itemprop="name"]/text()')[0].extract().strip()
        item['desc'] = sel.xpath(
            '//div[@class="px10 ullink"]/p/text()').extract()
        item['friends'] = sel.xpath(
            '//div[@id="friend_count"]/text()')[0].extract().strip()
        item['following'] = sel.xpath(
            '//div[@id="fave_count"]/text()')[0].extract().strip()
        item['followers'] = sel.xpath(
            '//div[@id="follower_count"]/text()')[0].extract().strip()
        items.append(item)

        return items

```

#### 4. run our web crawler and save data to a *.json* file
open *cmd* window in project folder, and run command ```scrapy crawl chictopia1 -o chictopia1.json -t json```
