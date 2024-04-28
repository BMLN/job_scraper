from abc import ABC, abstractmethod
from typing import override, Iterable
import logging
from scrapy import Spider, Field
from scrapy.item import Item
from scrapy.http import Request, Response
from urllib.parse import urlencode






class Url:
    def __init__(self, base, params={}):
        self.base = base
        self.params = params

    def __str__(self):        
        if isinstance(self.base, str) == False:
            raise TypeError 
        
        out = str(self.base)
        if len(self.params) > 0:
            out += "?" + urlencode(self.params)

        return out

    def param(self, key, value):
        self.params[key] = value
        return self


class Error(Item):
    url = Field()
    err = Field()








class Mapping_Scraper(ABC, Spider):

    def __init__(self, search_tags=[]):#, keys=[]):
        super(Spider, self).__init__()
        self.start_urls = [ self.searchurl_for(search_tag) for search_tag in search_tags ]
        #self.

    # def __init__(self, searches=[], keys=[]): #{fields : keys} -> values
    #     super(Spider, self).__init__()
    #     self.__config = config
    #     self.__extractors =  [ key : values for key, values in self.mappings().items() if key in keys ]



    #interface

    def parse(self, response):
        for x in self.mappings():
            yield x(response)



    #interface requirements

    @abstractmethod
    def searchurl_for(self, search_tag) -> Url:
        pass

    @abstractmethod
    def mappings(self):
        pass







#TODO: source from initial requests
#TODO: remove janky implementation for != None urls
class JobSearch_Scraper(ABC, Spider):

    def __init__(self, companies=[]):
        super(Spider, self).__init__()
        
        self.start_urls = [ self.searchurl_for(company_name) for company_name in companies ]
        self.start_urls = [ x for x in self.start_urls if (str(None) in x) == False ]#[:5] #TODO: REMOVE AFTER TESTING 
        #if urls:
        #    self.data_extractors = lambda x: {"url": x}
        #self.linkextractor = self.extractor()
        # if len(proxy_token) > 6: #0 or 32 to be specific: 
        #     logging.info("enabled proxy for scrapy requests")
        #     self.start_requests = self.start_requests



    #interface

    def parse(self, response):
        source = self.extract_source(response)
        jobs = self.extract_joburls(response)
        next = self.extract_nextpage(response)

        for x in jobs:
            for func in self.data_extractors():
                yield func(source, x) 
             #(self.parse_job(response))#yield {"url":x}
            #for each joburl, apply each func of get_extracts()
            #yield Request(x, callback=self.parse_job)
            #yield self.process_joburl(x) #Request(x, callback=self.parse_job)

        if next != None:
            yield response.follow(next, self.parse)


    def data_extractors(self):
        return [ lambda source, joburl: {"source" : str(source), "joburl" : str(joburl)} ]


    def outputs():
        return [[ dict ]]



    #interface requirements

    @abstractmethod
    def searchurl_for(self, company) -> Url:
        pass

    @abstractmethod
    def extract_source(self, response):
        pass

    @abstractmethod
    def extract_joburls(self, selector) -> list[str]:
        pass
    
    @abstractmethod
    def extract_nextpage(self, selector) -> str:
        pass








class JobInfo_Scraper(ABC, Spider):
    

    def __init__(self, jobs=[]):
        super(Spider, self).__init__()
        self.start_urls = jobs#[:1] #TODO: REMOVE AFTER TESTING


    # Interface

    def parse(self, response):
        #return {"url": response}
        #print("parsing job")
        yield {
            "Name": self.extract_company(response),
            "Jobbezeichnung": self.extract_jobtitle(response),
            #"Tätigkeitsbereich": None,
            #"Aufgaben": self.extract_tasks(response),
            #"Qualifikationen": self.extract_qualifications(response),
            #"etc": self.extract_etc(response),
            "Standort": self.extract_location(response),
            "Anstellungsart": self.extract_employment(response),
            "job_node" : self.extract_jobnode(response)
            #"raw_text": self.extract_rawtext(response)
        }


    def outputs():
        return [[ dict ]]



    # Interface Requirements

    @abstractmethod
    def extract_jobtitle(self, selector) -> str:
        pass

    @abstractmethod
    def extract_company(self, selector) -> str:
        pass

    @abstractmethod
    def extract_location(self, selector) -> str:
        pass

    @abstractmethod
    def extract_employment(self, selector) -> str:
        pass

    @abstractmethod
    def extract_jobnode(self, selector) -> str:
        pass

    
    #DEPR - move to TM/IE
    @abstractmethod
    def extract_tasks(self, selector) -> str:
        pass

    #DEPR - move to TM/IE
    @abstractmethod
    def extract_qualifications(self, selector) -> str:
        pass

    #DEPR - move to TM/IE
    @abstractmethod
    def extract_etc(self, selector) -> str:
        pass

    #DEPR - move to TM/IE
    @abstractmethod
    def extract_rawtext(self, selector) -> str:
        pass