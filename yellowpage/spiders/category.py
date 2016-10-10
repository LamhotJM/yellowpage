import scrapy
from scrapy.selector import Selector
from scrapy.item import Field, Item
from scrapy.http import Request
import json

class YellowPagesSpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["yellowpages.sg"]
    start_urls = [
        'http://www.yellowpages.sg',
    ]

    def parse(self, response):
        url = Selector(response)
        EVENT_LINK_XPATH = ".//*[@id='block-browse-category-browse-category']/div/div/div/div/p/a"
        events = url.xpath(EVENT_LINK_XPATH)
        count = 0
        for event_link in events:
            count += 1
            urlCategories = url.xpath(
                ".//*[@id='block-browse-category-browse-category']/div/div/div/div/p/a/@href").extract()
            urlCategories = urlCategories[count].strip() if urlCategories else ''

            crawlUrl = "http://www.yellowpages.sg" + urlCategories
            yield Request(crawlUrl, self.parse_sub_categories)

            with open('category.txt', 'a') as f:
                f.write('{0}\n'.format(crawlUrl))


    def parse_sub_categories(self, response):
        responds = json.loads(response.body_as_unicode())
        body = '<html><body>' + str(responds) + '</body></html>'
        linkHref = Selector(text=body).xpath("//div/div/div/div/p/a").extract()
        count = 0
        for event_link in linkHref:
            count += 1
            subUrlCategory = Selector(text=body).xpath("//html/body/div/div/div/div/p/a/@href").extract()
            subUrlCategory = subUrlCategory[count].strip() if subUrlCategory else ''

            itemUrlSubCategory = "http://www.yellowpages.sg" + subUrlCategory
            yield Request(itemUrlSubCategory, self.parse_final_sub_categories)
            with open('sub_category.txt', 'a') as f:
                f.write('{0}\n'.format(itemUrlSubCategory))

    def parse_final_sub_categories(self, response):
        responds = json.loads(response.body_as_unicode())
        body = '<html><body>' + str(responds) + '</body></html>'
        linkHref = Selector(text=body).xpath("//div/div/div/div/p/a").extract()
        count = 0
        for event_link in linkHref:
            count += 1
            subUrlCategory = Selector(text=body).xpath("//html/body/div/div/div/div/p/a/@href").extract()
            subUrlCategory = subUrlCategory[count].strip() if subUrlCategory else ''

            itemUrlSubCategory = "http://www.yellowpages.sg" + subUrlCategory
            clean = itemUrlSubCategory.replace("\\", "")
            cleanQuote = clean.replace("'", "")
            with open('final_sub_category.txt', 'a') as f:
                f.write('{0}\n'.format(cleanQuote))
