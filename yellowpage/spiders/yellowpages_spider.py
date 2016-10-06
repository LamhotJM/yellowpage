# -*- coding: utf-8 -*-
import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.item import Field, Item


class YellowpagesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    business_name1 = Field()
    business_name2 = Field()
    address = Field()
    city = Field()
    zip = Field()
    phone = Field()
    url = Field()


class YellowpagesSpider(Spider):
    name = 'ye'
    start_urls = ['http://www.yellow-pages.ph/search/schools/cebu/page-1', ]
    allowed_domains = ['yellow-pages.ph']
    TIMEZONE = ''
    BASE_URL = 'http://www.yellow-pages.ph'

    def __init__(self, name=None, **kwargs):
        super(YellowpagesSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        sel = Selector(response)

        EVENT_LINK_XPATH = '//section[@class="regular"]//div[@class="result-img"]/a/@href'

        events = sel.xpath(EVENT_LINK_XPATH).extract()
        if events:
            for event_link in events:
                event_link = event_link if event_link.startswith('http') else self.BASE_URL + event_link
                yield Request(url=event_link, dont_filter=True, callback=self.parse_event)
        else:
            return

        NEXT_XPATH = '//a[text()="Next"]/@href'
        next_page = sel.xpath(NEXT_XPATH).extract()
        next_page = (
            next_page[0] if next_page[0].startswith('http') else self.BASE_URL + next_page[0]) if next_page else ''
        if next_page:
            yield Request(url=next_page, callback=self.parse)

    def parse_events(self, response):
        item = YellowpagesItem(url=response.url)
        yield item

    def parse_event(self, response):
        sel = Selector(response)
        url = response.url

        BUSINESS_NAME1_XPATH = '//h1[@itemprop="name"]/text()'
        BUSINESS_NAME2_XPATH = '//h2[@itemprop="alternateName"]/text()'
        ADDRESS_XPATH = '//h3[@itemprop="address"]/text()'
        CITY_XPATH = '//input[@id="map_location_name"]/@value'
        PHONE_XPATH = '//h4[@itemprop="telephone"]/text()'


        business_name1 = sel.xpath(BUSINESS_NAME1_XPATH).extract()
        business_name1 = business_name1[0].strip() if business_name1 else ''
        business_name2 = sel.xpath(BUSINESS_NAME2_XPATH).extract()
        business_name2 = business_name2[0].strip().strip('(').strip(')') if business_name2 else ''
        address = sel.xpath(ADDRESS_XPATH).extract()
        address = address[0].strip() if address else ''
        city = sel.xpath(CITY_XPATH).extract()
        city = city[0].strip() if city else ''
        zip = re.findall(r'(\d+)$', address, re.I)
        zip = zip[0].strip() if zip else ''
        phone = sel.xpath(PHONE_XPATH).extract()
        phone = ', '.join([x.strip() for x in phone if x.strip()]) if phone else ''

        item = YellowpagesItem(business_name1=business_name1,
                               business_name2=business_name2,
                               address=address,
                               city=city,
                               zip=zip,
                               phone=phone)
        try:
            yield item
        except Exception as e:
            print "*** ITEM DROPPED %s" % (str(e))
            with open('dropped.txt', 'a+') as d:
                d.write(url + '\t-\t' + str(e) + '\n')

    def check_item(self, item):
        if not item['business_name1']:
            raise AssertionError('No business_name1')
        if not item['business_name2']:
            raise AssertionError('No business_name2')
        if not item['address']:
            raise AssertionError('No address')
        if not item['city']:
            raise AssertionError('No city')
        if not item['zip']:
            raise AssertionError('No zip')
        if not item['phone']:
            raise AssertionError('No phone')
