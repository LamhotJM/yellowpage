from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request


class ScrapyOrgSpider(BaseSpider):
    name = "scrapy"
    allowed_domains = ["scrapy.org"]
    start_urls = ["http://blog.scrapy.org/"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        next_page = hxs.select("//div[@class='pagination']/a[@class='next_page']/@href").extract()
        if next_page:
            yield Request(next_page[0], self.parse)

        posts = hxs.select("//div[@class='post']")
        for post in posts:
            yield {
                'title': post.select("div[@class='bodytext']/h2/a/text()").extract(),
                'link': post.select("div[@class='bodytext']/h2/a/@href").extract(),
                'content': post.select("div[@class='bodytext']/p/text()").extract()
            }
