# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import Response, HtmlResponse, TextResponse, Request
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


from cloudscraper import create_scraper

import pandas as pd
from urllib.parse import urlparse


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
#TODO: pass delay/etc from settings.py
class CloudFlareMiddleware:
    
    browser = {
        "mobile": False,
        "desktop": True
    }
    scraper = create_scraper(debug=False)

    #def __init__(self, settings={}):
    #    self.scraper = create_scraper(debug=False)
    #    #self.proxy_list = queue.Queue()
    #    #for x in parse_inputs(settings.get("PROXY_INPUTS")): self.proxy_list.put(x)

    #@classmethod
    #def from_crawler(cls, crawler):
    #    return cls(crawler.settings)




    def process_request(self, request, spider):
        output = HtmlResponse(request.url)
        output.status = 500
        url = request.url
        proxies = {} #cloudscraper provides proxylist
                
        #print("requesting", request.url)
        for x in range(400000000): #super cool very gud delay func
            pass

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        } 
        try:
            with CloudFlareMiddleware.scraper.get(url=url, proxies=proxies, timeout=60*2) as resp:
                output = HtmlResponse(
                    resp.url, 
                    status=resp.status_code, 
                    headers=resp.headers, 
                    #body=resp.content, #problem?
                    body=str(resp.content),
                    encoding="utf-8",
                    request=request,
                    #meta= {"dont_redirect": True}
                )

                #TODO: add url check if still base
                

                if """<span id="challenge-error-text">Enable JavaScript and cookies to continue</span>""" in str(output.body):
                    print("didnt solve challenge")
                    output.status = 500
            
                if """<h1 data-translate="block_headline">Sorry, you have been blocked</h1>""" in str(output.body):
                    print("blocked on used ip")
                    output.status = 503
        
        except:
            pass
        
        
        #print(resp.content)
        return output

# class ErrorMiddleware(HttpErrorMiddleware):
    
#     @override





#TODO: read from settings and set defaults
class CloudFlareMiddleware2:
    
    CFM_SESSION_INIT_THRESHOLD = 5
    CFM_SESSION_EVAL_THRESHOLD = 0.8
    
    CFM_MULTI_THRESHOLD = 3
    CFM_MULTI_MINSESSIONS = 3
    CFM_MULTI_MAXSESSIONS = 10

    CFM_MAX_CREATED_SESSIONS = 20


    def __init__(self, settings={}):
        self.__sessions = []
        #TODO: settings init
        #self.CFM_MULTI_THRESHOLD = 3
        #self.CFM_MAX_CREATED_SESSIONS = 20

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def new_session(self, *args, **kwargs):
        self.__sessions.append((new_sess := self.CfSession(len(self.__sessions) + 1, *args, **kwargs)))
        
        return new_sess

    #TODO: cleaner
    def eval_session(self, session):
        if session.fails + session.success < self.CFM_SESSION_INIT_THRESHOLD:
            return True
        elif session.success / (session.fails + session.success) < self.CFM_SESSION_EVAL_THRESHOLD:
            return False
        else:
            return True 


    def get_sessions(self, session_key=0, retry_times=0):
        output = []
        session_key = session_key if session_key else 0
        retry_times = retry_times if retry_times else 0

        if self.__sessions and self.eval_session(self.__sessions[session_key]) and retry_times < self.CFM_MULTI_THRESHOLD:
            output.append(self.__sessions[session_key])
        else:
            evaled_sessions = [ session for session in self.__sessions if self.eval_session(session) ]
            new_sessions = [ self.new_session() for x in range(self.CFM_MULTI_MINSESSIONS - len(evaled_sessions)) ] #TODO: CFM_MAX_CREATED_SESSIONS
            
            output += evaled_sessions[session_key:] + new_sessions + evaled_sessions[:session_key]
                #sess = self.__sessions[ (session_key + x) % len(self.__sessions) ]
            
        print(f"{len(self.__sessions)} total sessions, {len([ session for session in self.__sessions if self.eval_session(session) ])} working")
        #while len(output) < self.CFM_MULTI_MINSESSIONS and len(output) < self.CFM_MULTI_MAXSESSIONS and len(self.__sessions) < self.CFM_MAX_CREATED_SESSIONS:
        #    output.append(self.new_sess())

        return output


    def process_request(self, request, spider):
        
        for session in self.get_sessions(request.meta.get("session_key"), request.meta.get("retry_times")):
            response = session.process_request(request)
                
            if 200 <= response.status < 300:
                break
        
        #print(response.body)
        return response



    class CfSession():
        def __init__(self, session_key, *args, **kwargs):
            self.session = create_scraper(*args, **kwargs)
            self.session_key = session_key
            self.success = 0
            self.fails = 0

        @classmethod
        def to_req_params(cls, request):
            PARAMS = ["method", "url", "params", "data", "json", "headers", "cookies", "files", "auth", "timeout", "allow_redirects", "proxies", "verify", "stream", "cert"]

            output =  { key : value for key, value in { key if key[0] != "_" else key[1:] : value for key, value in request.__dict__.items() }.items() if key in PARAMS }
            output["headers"] = dict(output["headers"].to_unicode_dict())

            return output

        def send(self, *args, **kwargs):
            for x in range(400000000): #super cool very gud delay func
                pass

            try:
                with self.session.request(*args, **kwargs) as resp:
                    return resp
                

            except Exception as e:
                print(e)
                return None
            

        def create_scrapyresponse(self, request, response):
            output = HtmlResponse(request.url, status=500, request=request, encoding="utf-8")

            #TODO: add url check if still base
            if not response:
                return output
                
            elif urlparse(request.url).hostname != urlparse(response.url).hostname:
                print("got redirected")
                return output

            elif """<span id="challenge-error-text">Enable JavaScript and cookies to continue</span>""" in str(response.content):
                print("didnt solve challenge")
                return output
            
            elif """<h1 data-translate="block_headline">Sorry, you have been blocked</h1>""" in str(response.content):
                print("blocked on used ip")
                return output.replace(status = 503)

            else:
                return  HtmlResponse(
                        response.url, 
                        status=response.status_code, 
                        headers=response.headers, 
                        body=response.content,
                        encoding="utf-8",
                        request=request, #set afterwards? #not needed?
                        #meta=request.meta | {"session_key" : self.session_key}#{"dont_redirect": True}
                    )


        def process_request(self, request):
            params = self.to_req_params(request)

            response = self.send(**params)
            response = self.create_scrapyresponse(request, response)

            if 200 <= response.status < 300:
                self.success += 1
            else:
                self.fails += 1

            return response
