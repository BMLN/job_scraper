from job_scraper.core import new_templ
import scrapy 

from typing import override, Iterable
import re


class Arbeitsagentur_JobSearch_Scraper(new_templ.JobSearchScraper):

    name = "arbeitsagentur_jobsearch_spider"
    allowed_domains = ["arbeitsagentur.de"]

    __general_search_url = "https://www.arbeitsagentur.de/jobsuche/suche"
    __extractor = scrapy.linkextractors.LinkExtractor(
        restrict_xpaths = "//div[@id = 'ergebnisliste']",
        #restrict_text = "student"
    )



    # interface requirements

    @classmethod  
    @override
    def url_extractor(cls, selector) -> list[dict]:
        return [ {"url_text": url.text, "url" : url.url} for url in cls.__extractor.extract_links(response) ]



    #TODO: javascript interaction
    @classmethod  
    @override
    def extract_nextpage(cls, response):
        return None



    

class Arbeitsagentur_JobInfo_Scraper(new_templ.JobInfoScraper):
    
    name = "arbeitsagentur_jobinfo_spider"
    allowed_domains = ["arbeitsagentur.de"]




    
    # Interface Implementations

    @classmethod       
    @override
    def extract_jobtitle(cls, selector):
        return selector.xpath("//div[@id='detail-kopfbereich-titel']//text()").get()
              
    @classmethod     
    @override
    def extract_content(cls, selector) -> str:
        return selector.xpath("//div[@class='ba-layout-tile']//p").get()
        
    @classmethod  
    @override
    def extract_company(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-firma']//text()").get()

    @classmethod  
    @override
    def extract_field(cls, selector) -> str:
        return None

    @classmethod  
    @override
    def extract_industry(cls, selector) -> str:
        return None

    @classmethod  
    @override
    def extract_employment(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-angebotsart']//text()").get()

    @classmethod  
    @override
    def extract_location(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-arbeitsort']//text()").get()

    @classmethod  
    @override
    def extract_posting(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-veroeffentlichungsdatum']//text()").get()

