from job_scraper.core import new_templ
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote



#TODO: javascript
class Monster_JobScraper(new_templ.JobSearchScraper):
    
    name = "monster_jobsearch_spider"
    allowed_domains = ["monster.de"]

    __extractor = LinkExtractor(
        restrict_xpaths = "//div[@id='JobCardGrid']//a[@data-testid='jobTitle']",
    )


    

    #interface requirements

    @classmethod
    @override
    def url_extractor(cls, response) -> [dict]:
        return [ {"url_text": url.text, "url" : url.url} for url in cls.__extractor.extract_links(response) ]


    #TODO:javascript
    @classmethod
    @override
    def nextractor(cls, response) -> str:
        pass








class Monster_InfoScraper(new_templ.JobInfoScraper):

    name = "monster_jobinfo_spider"
    allowed_domains = ["monster.de"]
    



    #interface requirements
        
    @classmethod
    @override
    def extract_jobtitle(cls, selector) -> str:
        return selector.xpath("//div[@id='job-view-header']//h2[@data-testid='jobTitle']//text()").get()
        
    @classmethod    
    @override
    def extract_content(cls, selector) -> str:
        return selector.xpath("//div[contains(@class, 'DescriptionContainer')]//div//div").get()
         
    @classmethod   
    @override
    def extract_company(cls, selector) -> str:
        output = selector.xpath("//div[@id='job-view-header']//li[@data-testid='company']//text()").get()

        return output
    
    @classmethod
    @override
    def extract_field(cls, selector) -> str:
        return None
    
    @classmethod
    @override
    def extract_industry(cls, selector) -> str:
        output = selector.xpath("//div[contains(@class, 'numbers-and-facts')]//table//tr")
        
        if len(output) > 0:
            output = output[2].xpath(".//td//text()")
            if output:
                return output[1]
    
    @classmethod
    @override
    def extract_employment(cls, selector) -> str:
        output = selector.xpath("//div[contains(@class, 'numbers-and-facts')]//table//tr")
        
        if len(output) > 0:
            output = output[1].xpath(".//td//text()")
            if output:
                return output[1]
    
    @classmethod
    @override
    def extract_location(cls, selector) -> str:
        return selector.xpath("//div[@id='job-view-header']//li[@data-testid='jobDetailLocation']//text()")
    
    @classmethod
    @override
    def extract_posting(cls, selector) -> str:
        return selector.xpath("//div[@id='job-view-header']//li[@data-testid='jobDetailDataRecency']//text()")
