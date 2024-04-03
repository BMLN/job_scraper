from abc import ABC, abstractmethod
from typing import override, Iterable
import logging
from scrapy import Spider
from scrapy.http import Request, Response



class Job_Scraper(ABC, Spider):
    __mappings = ["search", ""]

    def __init__(self, mappings={}, companies=["adidas"]):
        super(Spider, self).__init__()

        c = ["adidas ag"]
        self.start_urls = self.searchurls(c)
        #self.linkextractor = self.extractor()
        # if len(proxy_token) > 6: #0 or 32 to be specific: 
        #     logging.info("enabled proxy for scrapy requests")
        #     self.start_requests = self.start_requests
        self.mappings = mappings
        #quit(1)


    def searchurls(self, companies):
        output = []

        for company in companies:
            output.append(self.searchurl(company))

        return output


    def parse(self, response):
        jobs = self.extract_joburls(response)
        for x in jobs:
            yield Request(x, callback=self.parse_job(x))

        next = self.extract_nextpage(response)
        if next != None:
            yield response.follow(next, self.parse)

    
    def parse_job(self, response):
        yield {
            "Name": self.extract_company(response),
            "Jobbezeichnung": self.extract_jobtitle(response),
            "Tätigkeitsbereich": None,
            "Aufgaben": self.extract_tasks(response),
            "Qualifikationen": self.extract_qualifications(response),
            "etc": None
        }

    @abstractmethod
    def searchurl(self, company) -> str:
        pass

    @abstractmethod
    def extract_joburls(self) -> list[str]:
        pass
    
    @abstractmethod
    def extract_nextpage(self) -> str:
        pass

    @abstractmethod
    def extract_company(self, response) -> str:
        pass

    @abstractmethod
    def extract_jobtitle(self, response) -> str:
        pass

    @abstractmethod
    def extract_tasks(self, response) -> str:
        pass

    @abstractmethod
    def extract_qualifications(self, response) -> str:
        pass


    #DEPRECATED
    #@abstractmethod
    def set_mappings(mappings): #self
        pass

    def is_mapped(self):
        return len(set(__mappings) - set(self.mappings)) > 0

    def proxed(self):
        return False
        

    @override
    def start_requests(self):
        #adds proxy to the calls
        return super().start_requests()


    #@abstractmethod
    def get_search_field():
        pass
        #return self.page.apply
        #set_name()
    #    invoke_search()

    #other gets

    def search():
        return False
    def next():
        return False

