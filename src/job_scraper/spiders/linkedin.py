from job_scraper.core import new_templ, url
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl



class LinkedIn_JobScraper(new_templ.JobSearchScraper):
    
    name = "linkedin_jobsearch_spider"
    allowed_domains = ["de.linkedin.com"]

    __extractor = LinkExtractor(
        restrict_xpaths = "//li//div//a[contains(@class, 'full-link')]"
    )

    API_BASE = "https://de.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    

    #interface requirements

    @classmethod
    @override
    def url_extractor(cls, response) -> [dict]:
        return [ {"url_text": url.text, "url": urlunparse(urlparse(url.url)._replace(query=""))} for url in cls.__extractor.extract_links(response) ]


    #+10, site itself does the wrong calls?
    #try first, catch later
    @classmethod
    @override
    def nextractor(cls, response) -> str:
        next = urlparse(response.url)
        next_params = dict(parse_qsl(next.query))
        next_params["start"] = "10" if "start" not in next_params else str(int(next_params["start"]) + 10)
        next = next._replace(query=urlencode(next_params))
        next = urlunparse(next)

        return next


    @classmethod
    @override
    def parse(self, response):
        api_call = url.Url(
            base=self.API_BASE,
            params=dict(parse_qsl(urlparse(response.url).query))
        )
        
        yield response.follow(str(api_call), callback=self.parse_from_api)
        
        
    
    @classmethod
    def parse_from_api(self, response):
        for x in self.url_extractor(response):
            yield x
        
        if (next := self.nextractor(response)): 
            
            yield response.follow(
                next,
                callback= self.parse_from_api
            )








class LinkedIn_InfoScraper(new_templ.JobInfoScraper):

    name = "linkedin_jobinfo_spider"
    allowed_domains = ["de.linkedin.com"]
    



    #interface requirements
    
    @classmethod
    @override
    def extract_jobtitle(cls, selector) -> str:
        output = selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//h1//text()").get()
        
        return output
    
    @classmethod
    @override
    def extract_content(cls, selector) -> str:
        return None
        return selector.xpath("//div[contains(@class, 'job-posting')]//div[contains(@class, 'core-section')]//div[contains(@class, 'description__text')]//div").get()
    
    @classmethod
    @override
    def extract_company(cls, selector) -> str:
        output = selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//h4//a[contains(@class, 'org-name')]//text()").get()

        return output
    
    @classmethod
    @override
    def extract_field(cls, selector) -> str:
        output = selector.xpath("//ul[contains(@class, 'job-criteria-list')]//li//span//text()")

        if len(output) > 0:
            return output[2].get()
    
    @classmethod
    @override
    def extract_industry(cls, selector) -> str:
        output = selector.xpath("//ul[contains(@class, 'job-criteria-list')]//li//span//text()")

        if len(output) > 0:
            return output[3].get()
    
    @classmethod
    @override
    def extract_employment(cls, selector) -> str:
        output = selector.xpath("//ul[contains(@class, 'job-criteria-list')]//li//span//text()")

        if len(output) > 0:
            return output[1].get()
    
    @classmethod
    @override
    def extract_location(cls, selector) -> str:
        output = selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//h4//span")

        if len(output) > 0:
            return output[1].xpath(".//text()").get()
    
    @classmethod
    @override
    def extract_posting(cls, selector) -> str:
        return selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//span[contains(@class, 'posted-time-ago')]//text()").get()
