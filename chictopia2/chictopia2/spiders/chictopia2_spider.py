import scrapy

from chictopia2.items import Chictopia2Item

MAX_PAGE = 31  # 爬取页面数（30页，range(1,MAX_PAGE)为左闭右开区间）
URL_BASE = 'http://www.chictopia.com'


class Chictopia2Spider(scrapy.Spider):
    name = "chictopia2"
    allowed_domains = ["chictopia.com"]

# 从批文件读取用户名
    def __init__(self, user=None, *args, **kwargs):
        super(Chictopia2Spider, self).__init__(*args, **kwargs)
        self.start_urls = []
        for i in range(1, MAX_PAGE):
            url = str('http://www.chictopia.com/%s/%d' % (user, i))
            self.start_urls.append(url)

# 获得每个outfit的url，并传递给parseSet()进一步处理
    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        items = []
        item = Chictopia2Item()
        url_list = sel.xpath(
            '//div[@id="bodywrapper"]')
        for url in url_list:
            url_add = []
            url_add = url.xpath(
                '//div[@class="bold px12 white lh12 ellipsis"]/a/@href').extract()
            for url_add_0 in url_add:
                yield scrapy.Request(url=URL_BASE + str(url_add_0), callback=self.parseSet)

# 爬取每个outfit的url,vote等信息并下载图片
    def parseSet(self, response):
        sel = scrapy.selector.Selector(response)
        items = []
        item = Chictopia2Item()
        item['url'] = response.url
        item['vote'] = sel.xpath(
            '//div[@class="left action_unclicked_show cursor"]/text()').extract()[0].strip()
        item['comment'] = sel.xpath(
            '//div[@class="left action_unclicked_show cursor"]/text()').extract()[1].strip()
        item['favorite'] = sel.xpath(
            '//div[@class="left action_unclicked_show cursor"]/text()').extract()[2].strip()
        item['tags'] = sel.xpath(
            '//div[@class="left px10"]/a/text()').extract()
        item['desc'] = sel.xpath(
            '//div[@class="garmentLinks left"]/a/text()').extract()
        pics = []
        pics_new = []
        pics = sel.xpath(
            '//div[@style="display:inline-block"]/img/@src').extract()#爬取小图的url
        for pic in pics:
            pic_new = pic.replace('sm', '400')#修改小图像素，转变为大图url
            pics_new.append(pic_new)
        item['image_urls'] = pics_new
        items.append(item)

        return items
