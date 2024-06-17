from job_scraper.core import new_templ
import scrapy
from typing import override, Iterable






class GetInIT_JobSearch_Scraper(new_templ.JobSearchScraper):

    name = "getinit_jobsearch_spider"
    allowed_domains = ["get-in-it.de"]

    __base = "https://www.get-in-it.de/jobsuche"
    __extractor = scrapy.linkextractors.LinkExtractor(
        restrict_xpaths = "//div[@class='container']//a[contains(@class, 'CardJob_jobCard')]",
        #restrict_text = "student"
    )



    # interface requirements

    @classmethod  
    @override
    def url_extractor(cls, selector):
        return [ {"url_text": url.text, "url" : url.url} for url in cls.__extractor.extract_links(response) ]



    #TODO: javascript interaction
    @classmethod  
    @override
    def extract_nextpage(cls, response):
        return None









class GetInIT_JobInfo_Scraper(new_templ.JobInfoScraper):
    
    name = "getinit_jobinfo_spider"
    allowed_domains = ["get-in-it.de"]

    


    # Interface Implementations

    @classmethod
    @override
    def extract_jobtitle(cls, selector):
        return selector.xpath("//h1[contains(@class, 'JobHeaderRegular_jobTitle')]//text()").get()
   
    @classmethod              
    @override
    def extract_content(cls, selector) -> str:
        return selector.xpath("(//div[@class='container']//div[contains(@class, 'JobDescription')]//section)").getall()
   
    @classmethod     
    @override
    def extract_company(cls, selector) -> str:
        return selector.xpath("//p[contains(@class, 'JobHeaderRegular_companyTitle')]//text()").get()

    @classmethod
    @override
    def extract_field(cls, selector) -> str:
        jobinfos = selector.xpath("//div[contains(@class, 'JobInfo')]//div[contains(@class, 'JobInfo') and contains(@class, 'row')]")

        if len(jobinfos) > 0:
            return jobinfos[0].getall()[1:]

    @classmethod
    @override
    def extract_industry(cls, selector) -> str:
        return None

    @classmethod
    @override
    def extract_employment(cls, selector) -> str:
        return None

    @classmethod
    @override
    def extract_location(cls, selector) -> str:
        return selector.xpath("//div[contains(@class, 'JobHeaderRegular_jobLocation')]//text()").get()

    @classmethod
    @override
    def extract_posting(cls, selector) -> str:
        return None

