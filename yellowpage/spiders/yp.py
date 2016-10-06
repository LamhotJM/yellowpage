# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector, XPathSelector
from scrapy.http.request import Request

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.item import Field, Item
from urlparse import urljoin


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


class YpSpider(scrapy.Spider):
    name = "yp"
    allowed_domains = ['yellowpages.sg']
    start_urls = ['http://www.yellowpages.sg/category/credit-reporting-agencies',
                  'http://www.yellowpages.sg/category/detective-agencies',
                  ]
    TIMEZONE = ''
    BASE_URL = 'http://www.yellow-pages.sg'

    def __init__(self, name=None, **kwargs):
        super(YpSpider, self).__init__(name, **kwargs)


def parse(self, response):
    if response.status in [301, 302] and 'Location' in response.headers:
        # test to see if it is an absolute or relative URL
        newurl = urljoin(Request.url, response.headers['location'])
        # or
        newurl = response.headers['location']
        yield Request(url=newurl, meta=Request.meta, callback=self.parse_whatever)

    hxs = Selector(response)
    posts = hxs.select(".//*[@id='item1']/div[2]")
    for post in posts:
        yield {
            'company_name': post.select(".//*[@id='item1']/div[2]/div[1]/div[1]/h2/a").extract(),
            'address': post.select(".//*[@id='item1']/div[2]/div[2]/div[2]").extract(),
            'phone': post.select(".//*[@id='item1']/div[2]/div[3]/div[1]/span").extract()
        }
