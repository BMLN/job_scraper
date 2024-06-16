from job_scraper.core import new_templ
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote



class LinkedIn_JobScraper(new_templ.JobSearchScraper):
    
    name = "linkedin_jobsearch_spider"
    allowed_domains = ["de.linkedin.com"]

    __extractor = LinkExtractor(
        restrict_xpaths = "//main[@id='main-content']//ul//li//div[contains(@class, 'job-search')]//a[contains(@class, 'full-link')]",
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







class LinkedIn_InfoScraper(new_templ.JobInfoScraper):

    name = "linkedin_jobinfo_spider"
    allowed_domains = ["de.linkedin.com"]
    



    #interface requirements
    
    @override
    def extract_jobtitle(cls, selector) -> str:
        output = selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//h1//text()").get()
        
        return output

    @override
    def extract_content(cls, selector) -> str:
        return selector.xpath("//div[contains(@class, 'job-posting')]//div[contains(@class, 'core-section')]//div[contains(@class, 'description__text')]//div").get()

    @override
    def extract_company(cls, selector) -> str:
        output = selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//h4//a[contains(@class, 'org-name')]//text()").get()

        return output

    @override
    def extract_field(cls, selector) -> str:
        output = selector.xpath("//ul[contains(@class, 'job-criteria-list')]//li//span//text()")

        if len(output) > 0:
            return output[2]

    @override
    def extract_industry(cls, selector) -> str:
        output = selector.xpath("//ul[contains(@class, 'job-criteria-list')]//li//span//text()")

        if len(output) > 0:
            return output[3]

    @override
    def extract_employment(cls, selector) -> str:
        output = selector.xpath("//ul[contains(@class, 'job-criteria-list')]//li//span//text()")

        if len(output) > 0:
            return output[0]

    @override
    def extract_location(cls, selector) -> str:
        output = selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//h4//span")

        if len(output) > 0:
            return output[1].xpath(".//text()").get()

    @override
    def extract_posting(cls, selector) -> str:
        output = selector.xpath("//section[contains(@class, 'container')]//div[contains(@class, 'info-container')]//span[contains(@class, 'posted-time-ago')]//text()")

        return output
