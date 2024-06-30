# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import Response, HtmlResponse, TextResponse
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


from cloudscraper import create_scraper
import queue
import pandas as pd

class JobScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class JobScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, settings={}):
        self.proxy = JobScraperDownloaderMiddleware.proxy_str(
            settings.get("PROXY_HOST"),
            settings.get("PROXY_AUTH")
        )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    #adds proxy to requests
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        request.meta["proxy"] = self.proxy


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    @classmethod
    def proxy_str(cls, proxy_host, proxy_auth):
        return "http://" + str(proxy_auth) + "@" + str(proxy_host)


def parse_inputs(input):
        output = []

        match input:
            case list():
                output += [ parse_inputs(x) for x in input ]            
            case str():
                #read file
                if input.endswith(".csv"):
                    output += pd.read_csv(input).apply(lambda x: "{}:{}".format(x["ip"], x["port"]), axis=1).values.tolist()
                elif input.endswith(".json"):
                    output += pd.read_json(input).apply(lambda x: "{}:{}".format(x["ip"], x["port"]), axis=1).values.tolist()
                else:
                    output.append(input)
            case _:
                raise TypeError("unrecognized input type")

        return output



#TODO: passing a session
class CloudFlareMiddleware:
    def __init__(self, settings={}):
        self.scraper = create_scraper()
        #self.proxy_list = queue.Queue()
        #for x in parse_inputs(settings.get("PROXY_INPUTS")): self.proxy_list.put(x)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)




    def process_request(self, request, spider):
        output = HtmlResponse(request.url)
        url = request.url
        proxies = {} #cloudscraper provides proxylist
                
        print("requesting", request.url)
        with self.scraper.get(url=url, proxies=proxies, timeout=60*2) as resp:
            for x in range(50000000): #super cool very gud delay func
                pass
            output = HtmlResponse(
                resp.url, 
                status=resp.status_code, 
                headers=resp.headers, 
                #body=resp.content, #problem?
                body=str(resp.content),
                encoding="utf-8",
                request=request
            )

            if """<span id="challenge-error-text">Enable JavaScript and cookies to continue</span>""" in str(output.body):
                print("didnt solve challenge")
                output.status = 500
        
            if """<h1 data-translate="block_headline">Sorry, you have been blocked</h1>""" in str(output.body):
                print("blocked on used ip")
                output.status = 503

        #print(resp.content)
        return output

# class ErrorMiddleware(HttpErrorMiddleware):
    
#     @override
