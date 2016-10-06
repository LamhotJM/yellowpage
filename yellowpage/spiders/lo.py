import scrapy


class RedirectTest(scrapy.Spider):
    name = "redirecttest"
    start_urls = [
        'http://httpbin.org/get',
        'https://httpbin.org/redirect-to?url=http%3A%2F%2Fhttpbin.org%2Fip'
    ]
    handle_httpstatus_list = [302]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        self.logger.debug("(parse_page) response: status=%d, URL=%s" % (response.status, response.url))
        if response.status in (302,) and 'Location' in response.headers:
            self.logger.debug("(parse_page) Location header: %r" % response.headers['Location'])
            yield scrapy.Request(
                response.urljoin(response.headers['Location']),
                callback=self.parse_page)
