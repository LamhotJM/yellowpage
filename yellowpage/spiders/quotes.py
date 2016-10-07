import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.item import Field, Item
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import unittest
from selenium import webdriver


class YellowpagesItem(Item):
    companyName = Field()
    companyAddress = Field()
    companyPhone = Field()
    url = Field()

class QuotesSpider(scrapy.Spider):
    def __init__(self):
        self.driver = webdriver.Chrome()

    name = "quotes"
    allowed_domains = ["yellowpages.sg"]
    start_urls = [
        'http://www.yellowpages.sg/category/real-estate-developers',
        # 'http://www.yellowpages.sg/category/enrichment-courses'
    ]
    TIMEZONE = ''
    BASE_URL = 'http://www.yellowpages.sg'

    def parse(self, response):
        url = Selector(response)
        EVENT_LINK_XPATH = '//div[@class="company_items"]'
        events = url.xpath(EVENT_LINK_XPATH)
        count = 0

        self.driver.get(response.url)
        self.driver.set_window_size(800, 600)

        while True:
            next = self.driver.find_element_by_xpath(".//*[@id='load_ajax_company']/div[3]/div[2]/ul/li[2]/a")
            try:
                next.click()

                for event_link in events:
                    if events:
                        count += 1
                        companyName = event_link.xpath('//*[@class="mapItem"]/@data-comp-name').extract()
                        companyName = companyName[count].strip() if companyName else ''
                        companyAddress = url.xpath('//*[@class="mapItem"]/@data-comp-addr').extract()
                        companyAddress = companyAddress[count].strip() if companyAddress else ''
                        companyPhone = url.xpath('.//*[@id]/div[2]/div[3]/div[1]//a//@href').extract()
                        companyPhone = companyPhone[count].strip() if companyPhone else ''
                        item = YellowpagesItem(companyName=companyName,
                                               companyAddress=companyAddress,
                                               companyPhone=companyPhone)
                        with open('result.txt', 'a') as f:
                            f.write('{0},{1},{2}\n'.format(item['companyName'],
                                                           item['companyAddress'],
                                                           item['companyPhone']))

                        try:
                            yield item

                        except Exception as e:
                            print "*** ITEM DROPPED %s" % (str(e))
                            with open('dropped.txt', 'a+') as d:
                                d.write(url + '\t-\t' + str(e) + '\n')

                    else:
                        return
            except:
                break

        self.driver.close()