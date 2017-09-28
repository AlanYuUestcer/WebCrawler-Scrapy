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
