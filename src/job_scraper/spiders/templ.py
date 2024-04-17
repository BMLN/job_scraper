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








class JobSearch_Scraper(ABC, Spider):
    __mappings = ["search", ""]

    def __init__(self, companies=[]):
        super(Spider, self).__init__()
        
        self.start_urls = [ self.searchurl_for(company_name) for company_name in companies ]
        #if urls:
        #    self.data_extractors = lambda x: {"url": x}
        #self.linkextractor = self.extractor()
        # if len(proxy_token) > 6: #0 or 32 to be specific: 
        #     logging.info("enabled proxy for scrapy requests")
        #     self.start_requests = self.start_requests



    #interface

    def parse(self, response):
        jobs = self.extract_joburls(response)
        next = self.extract_nextpage(response)

        for x in jobs:
            for func in self.data_extractors():
                yield func(x) 
             #(self.parse_job(response))#yield {"url":x}
            #for each joburl, apply each func of get_extracts()
            #yield Request(x, callback=self.parse_job)
            #yield self.process_joburl(x) #Request(x, callback=self.parse_job)

        if next != None:
            yield response.follow(next, self.parse)


    def data_extractors(self):
        return [ lambda x: {"joburl" : str(x)} ]


    def outputs():
        return [[ dict ]]



    #interface requirements

    @abstractmethod
    def searchurl_for(self, company) -> Url:
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
        self.start_urls = jobs


    # Interface

    def parse(self, response):
        #return {"url": response}
        #print("parsing job")
        yield {
            "Name": self.extract_company(response),
            "Jobbezeichnung": self.extract_jobtitle(response),
            "Tätigkeitsbereich": None,
            "Aufgaben": self.extract_tasks(response),
            "Qualifikationen": self.extract_qualifications(response),
            "etc": None,
            "Standort": self.extract_location(response),
            "type": self.extract_employment(response)
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
    def extract_tasks(self, selector) -> str:
        pass

    @abstractmethod
    def extract_qualifications(self, selector) -> str:
        pass