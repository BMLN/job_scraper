from job_scraper.core import new_templ
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote



class Stepstone_JobScraper(new_templ.JobSearchScraper):
    
    name = "stepstone_jobsearch_spider"
    allowed_domains = ["stepstone.de"]

    __extractor = LinkExtractor(
        #allow = "/www\.stepstone\.de\/stellenangebote--.*/",
        allow = "/stellenangebote--", #some problems with regex, rly correct?
        #restrict_xpaths = "//div[contains(@class, 'results')]"
        restrict_xpaths = "(//div[@data-genesis-element = 'CARD_GROUP_CONTAINER'])[1]"
    )


    #interface requirements

    @classmethod
    @override
    def url_extractor(cls, response) -> [dict]:
        return [ {"url_text": url.text, "url" : url.url} for url in cls.__extractor.extract_links(response) ]


    #TODO: add filtercheck
    @classmethod
    @override
    def nextractor(cls, response) -> str:
        nxt = selector.xpath("//nav[contains(@aria-label, 'pagination')]//a[@href]/@href").extract()
        
        if len(nxt) > 1:
            return nxt[-1]
        else:
            return None




class Stepstone_InfoScraper(new_templ.JobInfoScraper):
    
    name = "stepstone_jobinfo_spider"
    allowed_domains = ["stepstone.de"]





    #interface requirements
    

    @classmethod
    @override
    def extract_jobtitle(cls, selector):
        return selector.xpath("//span[@data-at='header-job-title']//text()").get()

    @classmethod
    @override
    def extract_content(cls, selector) -> str:
        return None
        return selector.xpath("//div[@data-atx-component='JobAdContent']").get()

    @classmethod       
    @override
    def extract_company(cls, selector):
        elem = selector.xpath("//div[@id='job-ad-content']//div[@data-at='job-ad-header']").xpath(".//li[contains(@class, 'company-name')]//text()")
        elem_texts = elem.getall()

        if len(elem_texts) > 0:
            #icon_info = elem_texts[0]
            #company_info = elem_texts[1]
            return elem_texts[-1]

    @classmethod       
    @override
    def extract_field(cls, selector) -> str:
        return None

    @classmethod       
    @override
    def extract_industry(cls, selector) -> str:
        company_info = selector.xpath("//div[@data-at='job-ad-company-card']//span//text()")

        if len(company_info) >= 1:
            return company_info[1].get()
            
    @classmethod       
    @override
    def extract_employment(cls, selector) -> str:
        return selector.xpath("//div[@id='job-ad-content']//div[@data-at='job-ad-header']").xpath(".//li[contains(@class, 'work-type')]//text()").get()

    @classmethod           
    @override
    def extract_location(cls, selector):
        elem = selector.xpath("//div[@id='job-ad-content']").xpath(".//li[contains(@class, 'location')]//text()")
        elem_texts = elem.getall()

        if len(elem_texts) == 2:
            #icon_info = elem_texts[0]
            #location_info = elem_texts[1]
            return elem_texts[1]

    @classmethod       
    @override
    def extract_posting(cls, selector) -> str:
        return selector.xpath("//div[@id='job-ad-content']//div[@data-at='job-ad-header']").xpath(".//li[contains(@class, 'date')]//text()").get()
