import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.item import Field, Item
from scrapy.http import Request


class YellowpagesItem(Item):
    companyName = Field()
    companyAddress = Field()
    companyPhone = Field()
    url = Field()


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://www.yellowpages.sg/category/real-estate-developers',
    ]
    TIMEZONE = ''
    BASE_URL = 'http://www.yellowpages.sg'

    def parse(self, response):
        sel = Selector(response)

        EVENT_LINK_XPATH = '//div[@class="company_items"]//div[@class="box-head-left"]/h2/a/@href'

        events = sel.xpath(EVENT_LINK_XPATH).extract()
        if events:
            for event_link in events:
                event_link = event_link if event_link.startswith('http') else self.BASE_URL + event_link
                yield Request(url=event_link, dont_filter=True, callback=self.parse_event)
        else:
            return

        NEXT_XPATH = './/*[@id="load_ajax_company"]/div[3]/div[2]/ul/li[1]'
        next_page = sel.xpath(NEXT_XPATH).extract()
        next_page = (
            next_page[0] if next_page[0].startswith('http') else self.BASE_URL + next_page[0]) if next_page else ''
        if next_page:
            yield Request(url=next_page, callback=self.parse)

    def parse_events(self, response):
        item = YellowpagesItem(url=response.url)
        yield item

    def parse_event(self, response):
        url = Selector(response)

        companyName = url.xpath('//*[@class="mapItem"]/@data-comp-name').extract()
        companyName = companyName[0].strip() if companyName else ''
        companyAddress = url.xpath('//*[@class="mapItem"]/@data-comp-addr').extract()
        companyAddress = companyAddress[0].strip() if companyAddress else ''
        companyPhone = url.xpath('.//*[@id]/div[2]/div[3]/div[1]//a//@href').extract()
        companyPhone = companyPhone[0].strip() if companyPhone else ''

        item = YellowpagesItem(companyName=companyName,
                               companyAddress=companyAddress,
                               companyPhone=companyPhone)

        try:
            yield item
        except Exception as e:
            print "*** ITEM DROPPED %s" % (str(e))
            with open('dropped.txt', 'a+') as d:
                d.write(url + '\t-\t' + str(e) + '\n')
