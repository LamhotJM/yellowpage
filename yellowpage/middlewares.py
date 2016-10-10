__author__ = 'MisT'
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy import log
import os
from urlparse import urljoin


class ypRedirect(RedirectMiddleware):
    def process_response(self, request, response, spider):
        print 'ypRedirect...'
        log.msg("ypRedirect...", level=log.INFO)
        if request.method == 'HEAD':
            if response.status in [301, 302, 303, 307] and 'Location' in response.headers:
                redirected_url = urljoin(request.url, response.headers['location'])
                print '302(h):', redirected_url
                os.system("pause")
            else:
                return response

        if response.status in [302, 303] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            print '302:', redirected_url
            os.system("pause")
        return response
