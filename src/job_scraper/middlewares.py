# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import Response, HtmlResponse, TextResponse, Request
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware
from scrapy.exceptions import CloseSpider 

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


from cloudscraper import create_scraper

from itertools import repeat
import pandas as pd
from urllib.parse import urlparse
import uuid


from threading import Lock



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




def rotate(l):
    return l[1:] + l[:1]

def index(l):
    return l



#TODO: read from settings and set defaults
class CloudFlareMiddleware2:
    
    #Default params
    DEFAULT_CFM_MODE = "STANDARD"


    DEFAULT_CFM_SESSION_COUNT = 10
    DEFAULT_CFM_SESSION_LIMIT = 20
    DEFAULT_CFM_SESSION_INIT_THRESHOLD = 5
    DEFAULT_CFM_SESSION_EVAL_THRESHOLD = 0.8
    
    DEFAULT_CFM_MULTI_THRESHOLD = 1
    DEFAULT_CFM_MULTI_RANGE = 3



    def __init__(self, crawler, settings={}):
        
        for cls_attr in dir(self):
            if "DEFAULT_" in cls_attr and cls_attr.index("DEFAULT_") == 0:
                if (cfm_var := cls_attr.replace("DEFAULT_", "", 1)) in settings: 
                    setattr(self, cfm_var, settings.get(cfm_var))
                else:
                    setattr(self, cfm_var, getattr(self, cls_attr))        

        self.crawler = crawler
        self.lock = Lock()
        self.sessioncount = 0
        self.__sessions = []


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler, crawler.settings)


    def get_sessions2(self, session_key=0, retry_times=0):
        session_key = session_key if session_key else 0
        retry_times = retry_times if retry_times else 0

        output = self.__sessions[session_key:] + self.__sessions[:session_key]
        output = [ x for x in output if self.eval_session(x) ]
        while len(self.__sessions) < self.CFM_MAX_CREATED_SESSIONS and len(output) < self.CFM_MULTI_MINSESSIONS:
            output.append(self.new_session())

        multi_active = retry_times >= self.CFM_MULTI_THRESHOLD

        if len(output) == 0: 
            raise CloseSpider

        #manipulate sessionslist according to mode
        if self.CFM_MODE == None:
            output = [ output[0] ]
            self.__sessions = self.__sessions
        elif self.CFM_MODE == "STANDARD":
            if output[0].session_key != session_key:
                multi_active = True
            self.__sessions = self.__sessions[session_key:] + self.__sessions[:session_key]

        elif self.CFM_MODE == "ROTATE": #ofc it doesnt work, where is rotate stored?
            output = output[1:] + output[:1] #error if only 1
            self.__sessions = self.__sessions[1:] + self.__sessions[:1]
        elif self.CFM_MODE == "BEST":
            print("TODO")
            #output = best
        elif self.CFM_MODE == "RANDOM":
            print("TODO")
            #output = random

        #return accordingly
        if multi_active:
            output = [ output[0] ]
        else:
            output = output[:min(self.CFM_MULTI_MAXSESSIONS, len(output))]

        print(f"{len(self.__sessions)} total sessions, {len([ session for session in self.__sessions if self.eval_session(session) ])} working")

        return output


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
        self.lock.acquire() #even necessary?
        try:
            sessions = self.get_sessions2(request.meta.get("session_key"), request.meta.get("retry_times"))
        #except: #how should it fail?
        finally:
            self.lock.release()

        for session in sessions:
            response = session.process_request(request)
                
            if 200 <= response.status < 300:
                break
        
        #print(response.body)
        return response




    def get_session3(session_key=None):

        while len(self.__sessions) < self.CFM_MAX_CREATED_SESSIONS and len(output) < self.CFM_MULTI_MINSESSIONS:
            self.new_session()
        output = next((x for x in self.__sessions if self.eval_session(x)), None )
        
        if output == None:
            raise CloseSpider("err")

        match self.CFM_MODE:
            case "STANDARD":
                return output
            case "ROTATE":
                self.__sessions = self.__sessions[1:] + self.__sessions[:1] 
                return output 
            case "RANDOM":
                print("TODO")
            case "BEST":
                print("TODO")
            case _:
                print("TODO")


    def get_session5(self):

        #mode defs
        match self.CFM_MODE:
            case "STANDARD": #EXHAUST
                cfm_sort = lambda x : x[1:] + x[:1] if x and previous_request and previous_request.session_key == x[0].session_key and x[0].history[0] != "SUCCESS" else x 
            case "ROTATE":
                cfm_sort = lambda x : x[1:] + x[:1] if x and previous_request and previous_request.session_key == x[0].session_key else x
            case "RANDOM":
                print("TODO")
            case "BEST":
                print("TODO")
            case _:
                print("TODO")


        with self.lock:
            previous_request = self.__sessions[0] if self.__sessions else None
            new_sessions = []
            
            #eval and fill sessions
            while len(new_sessions) < min(self.CFM_SESSION_COUNT, self.CFM_SESSION_LIMIT - self.sessioncount):
                if self.__sessions:
                    if (session := self.__sessions.pop()).eval():
                        new_sessions.append(session)
                else:
                    self.sessioncount += 1
                    new_sessions.append(self.CfSession(self.CFM_SESSION_INIT_THRESHOLD, self.CFM_SESSION_EVAL_THRESHOLD)))

            #update and apply mode 
            self.__sessions = cfm_sort(new_sessions)
            
            #return if any
            if self.__sessions:
                return self.__sessions[0]



    #TODO: session creation
    def get_session4(self, session_key=None, retry_times=None):
        """ returns the first usable session according to the CFM_MODE
        """
        
        #assert len(self.__sessions) > 0, f"CFM can't get a session with {len(self.sessions)} sessions!"

        new_sessions = self.CFM_MULTI_MINSESSIONS
        out_index = None

        match self.CFM_MODE:
        
            case "STANDARD":
                for x, session in enumerate(self.__sessions):
                    if self.history[0].session_key == session.sess_key and self.history[0].eval():
                        out_index = x
                        break
                    if self.history[0].session_key != session.sess_key and session.eval():
                        out_index = x
                        break
                        

            case "ROTATE":
                for x, session in enumerate(self.__sessions):
                    if self.history[0].session_key != session.sess_key and self.__sessions.eval():
                        out_index = x
                        break
                        
            case "RANDOM":
                print("TODO")

            case "BEST":
                print("TODO")

            case _:
                raise ValueError("CFM_MODE has to match one of the modes ['STANDARD', 'ROTATE', 'RANDOM', 'BEST']")
                
        if out_index:
            self.__sessions = self.__sessions[out_index:] + self.__sessions[:out_index]
            return self.__sessions[0]

        
        

    def process_request(self, request, spider):

        if request.meta.get("retry_times", 0) >= self.CFM_MULTI_THRESHOLD or (self.CFM_MODE == "STANDARD" and self.__sessions and self.__sessions[0].history[0] != "SUCCESS"):
            request_range = self.DEFAULT_CFM_MULTI_RANGE
        else:
            request_range = 1

        for session in ( self.get_session5() for x in range(request_range) ): #cleaner iterator?
            if session:            
                response = session.process_request(request)
                
                if 200 <= response.status < 300:
                    break
                    
            else:
                break
                        
        if not session or not response: #not response necessary?
            self.crawler.engine.close_spider(spider, "CFM has no available session left")
            raise CloseSpider(reason="stop me baby") #this on its own doesnt trigger twisted from middleware: github.com/scrapy/issues/2578

        return response





    class CfSession():
        def __init__(self, init_threshold=0, eval_threshold=1, *args, **kwargs):
            self.session = create_scraper(*args, **kwargs)
            self.session_key = uuid.uuid4()
            self.history = [ None for x in range(1) ]
            self.success = 0
            self.fails = 0
            self.init_threshold = init_threshold
            self.eval_threshold = eval_threshold

        @classmethod
        def to_req_params(cls, request):
            PARAMS = ["method", "url", "params", "body", "data", "json", "headers", "cookies", "files", "auth", "timeout", "allow_redirects", "proxies", "verify", "stream", "cert"]
            output =  { key : value for key, value in { key if key[0] != "_" else key[1:] : value for key, value in request.__dict__.items() }.items() if key in PARAMS }
            
            output["headers"] = dict(output["headers"].to_unicode_dict())
            if "body" in output: output["data"] = output.pop("body")

            return output

        def eval(self):            
            if (total_requests := self.fails + self.success): 
                if total >= self.init_threshold:
                    #if self.history: # -> this equals retry times
                    #    if not all(( x == "SUCCESS" for x in self.history if x )):
                    #        return False
                        
                    if self.success / (self.fails + self.success) < self.eval_threshold:
                        return False

            return True 


        def send(self, *args, **kwargs):
            #for x in range(400000000): #super cool very gud delay func
            for x in range(200000000):
                pass

            try:
                with self.session.request(timeout=60, *args, **kwargs) as resp:
                    return resp
                

            except Exception as e:
                print(e)
                return None
            

        def create_scrapyresponse(self, request, response):
            output = HtmlResponse(request.url, status=500, request=request, encoding="utf-8")

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
                if self.history: 
                    self.history = self.history[1:] + [ "SUCCESS" ]
                self.success += 1
            else:
                if self.history: 
                    self.history = self.history[1:] + [ "FAILED"]
                self.fails += 1

            return response
