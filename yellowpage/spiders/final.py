# -*- coding: utf-8 -*-
import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.item import Field, Item


class YellowpagesItem(Item):
    companyName = Field()
    companyAddress = Field()
    companyPhone = Field()


class YellowpagesSpider(Spider):
    name = 'final'
    start_urls = ['http://www.yellowpages.sg/search/all/Credit+Reporting+Agencies', ]
    allowed_domains = ['yellow-pages.ph']
    TIMEZONE = ''
    BASE_URL = 'http://www.yellow-pages.ph'

    def __init__(self, name=None, **kwargs):
        super(YellowpagesSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        sel = Selector(response)

       # EVENT_LINK_XPATH = '//section[@class="regular"]//div[@class="result-img"]/a/@href'

        #events = sel.xpath(EVENT_LINK_XPATH).extract()
       # if events:
           # for event_link in events:
              #  event_link = event_link if event_link.startswith('http') else self.BASE_URL + event_link
               # yield Request(url=event_link, dont_filter=True, callback=self.parse_event)
        #else:
           # return

       # NEXT_XPATH = '//a[text()="Next"]/@href'
        #next_page = sel.xpath(NEXT_XPATH).extract()
        #next_page = (
         #   next_page[0] if next_page[0].startswith('http') else self.BASE_URL + next_page[0]) if next_page else ''
        #if next_page:
         #   yield Request(url=next_page, callback=self.parse)

    def parse_events(self, response):
        item = YellowpagesItem(url=response.url)
        yield item

    def parse_event(self, response):
        sel = Selector(response)
        url = response.url
        #g_data = soup.find_all("a", {"class": "normal_title"})
        #g_data2 = soup.find_all("div", {"class": "address"})

        COMPANY_NAME_XPATH = '//*[@id="item1"]/div[2]/div[1]/div[1]/h2/a'
        COMPANY_ADDESS_XPATH = '//h2[@itemprop="alternateName"]/text()'
        COMPANY_PHONE_XPATH = '//h3[@itemprop="address"]/text()'

        companyName = sel.xpath(COMPANY_NAME_XPATH).extract()
        companyName = companyName[0].strip() if companyName else ''
        companyAddress = sel.xpath(COMPANY_ADDESS_XPATH).extract()
        companyAddress = companyAddress[0].strip().strip('(').strip(')') if companyAddress else ''
        companyPhone = sel.xpath(COMPANY_PHONE_XPATH).extract()
        companyPhone = companyPhone[0].strip() if companyPhone else ''
        item = YellowpagesItem(companyName=companyName,
                               companyAddress=companyAddress,
                               companyContact=companyPhone)


        try:
            yield item
            print "hello"
        except Exception as e:
            print "*** ITEM DROPPED %s" % (str(e))
            with open('dropped.txt', 'a+') as d:
                d.write(url + '\t-\t' + str(e) + '\n')
