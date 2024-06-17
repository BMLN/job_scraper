from job_scraper.core import new_templ
import scrapy 

from typing import override, Iterable
import re


class Arbeitsagentur_JobSearch_Scraper(templ.JobSearch_Scraper):

    name = "arbeitsagentur_jobsearch_spider"
    allowed_domains = ["arbeitsagentur.de"]

    __general_search_url = "https://www.arbeitsagentur.de/jobsuche/suche"
    __extractor = scrapy.linkextractors.LinkExtractor(
        restrict_xpaths = "//div[@id = 'ergebnisliste']",
        #restrict_text = "student"
    )



    # interface requirements

    @override
    def url_extractor(self, selector) -> list[dict]:
        return [ {"url_text": url.text, "url" : url.url} for url in cls.__extractor.extract_links(response) ]



    #TODO: javascript interaction
    @override
    def extract_nextpage(self, response):
        return None



    

class Arbeitsagentur_JobInfo_Scraper(templ.JobInfo_Scraper):
    
    name = "arbeitsagentur_jobinfo_spider"
    allowed_domains = ["arbeitsagentur.de"]




    
    # Interface Implementations

    @override
    def extract_jobtitle(self, selector):
        return selector.xpath("//div[@id='detail-kopfbereich-titel']//text()").get()
                 
    @override
    def extract_content(cls, selector) -> str:
        return selector.xpath("//div[@class='ba-layout-tile']//p").get()
        
    @override
    def extract_company(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-firma']//text()").get()

    @override
    def extract_field(cls, selector) -> str:
        return None

    @override
    def extract_industry(cls, selector) -> str:
        return None

    @override
    def extract_employment(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-angebotsart']//text()").get()

    @override
    def extract_location(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-arbeitsort']//text()").get()

    @override
    def extract_posting(cls, selector) -> str:
        return selector.xpath("//span[@id='detail-kopfbereich-veroeffentlichungsdatum']//text()").get()

