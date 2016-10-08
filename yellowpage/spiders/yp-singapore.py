import scrapy
from scrapy.selector import Selector
from scrapy.item import Field, Item
from scrapy.http import Request



class YellowpagesItem(Item):
    companyName = Field()
    companyAddress = Field()
    companyPhone = Field()
    totalResult = Field()


class YellowPagesSpider(scrapy.Spider):
    handle_httpstatus_list = [302]
    name = "yellowpagesg"
    allowed_domains = ["yellowpages.sg"]
    start_urls = [
        'http://www.yellowpages.sg/category/real-estate-developers?',
    ]
    TIMEZONE = ''
    BASE_URL = 'http://www.yellowpages.sg'
    url = "per=20&page=1&ajax=1&sort=all"

    def parse(self, response):
        url = Selector(response)

        strTemp = url.css('.breadcrumb>li::text').extract_first()
        totals = [int(s) for s in strTemp.split() if s.isdigit()]
        totalResult = str(totals).strip('[]')

        if totalResult < 20:
            yield Request(callback=self.parse_test)
        else:
            import math
            totalPage = int(math.ceil(float(totalResult) / 20))
            for i in range(1, totalPage):
                crawlUrl = "http://www.yellowpages.sg/category/real-estate-developers?per=20&page=" + str(
                    i) + "&ajax=1&sort=all"
                yield Request(crawlUrl, self.parse_test)

    def parse_test(self, response):
        url = Selector(response)
        EVENT_LINK_XPATH = '//div[@class="company_items"]'
        events = url.xpath(EVENT_LINK_XPATH)
        count = 0
        for event_link in events:
            if events:
                count += 1
                companyName = event_link.xpath('//*[@class="mapItem"]/@data-comp-name').extract()
                companyName = companyName[count].strip() if companyName else ''
                companyAddress = event_link.xpath('//*[@class="mapItem"]/@data-comp-addr').extract()
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
