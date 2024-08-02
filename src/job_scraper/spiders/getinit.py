from job_scraper.core import new_templ, url
import scrapy
from typing import override, Iterable

from urllib.parse import urlencode, parse_qsl, parse_qs, urlparse, urlunparse




class GetInIT_JobSearch_Scraper(new_templ.JobSearchScraper):

    name = "getinit_jobsearch_spider"
    allowed_domains = ["get-in-it.de"]

    __base = "https://www.get-in-it.de/jobsuche"
    __extractor = scrapy.linkextractors.LinkExtractor(
        restrict_xpaths = "//div[@class='container']//a[contains(@class, 'CardJob_jobCard')]",
        #restrict_text = "student"
    )

    API_BASE = "https://www.get-in-it.de/api/v2/open/job/search"
    API_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "de-DE,de;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
    }


    @classmethod
    def __parse_to_api_params(cls, url):
        params = parse_qs(urlparse(url).query)
        params["filter[thematic_priority][]"] = [ int(x) for x in params.pop("thematicPriority", []) ]

        return params

        

    # interface requirements

    @classmethod  
    @override
    def url_extractor(cls, selector):
        search_results = selector.json().get("items", {}).get("results")
        
        return [ { "url_text": job.get("title"), "url" : f"{"https://www.get-in-it.de"}{job.get("url")}" } for job in search_results ]



    @classmethod  
    @override
    def nextractor(cls, response): #through some calcs
    
        total = response.json().get("total")
        curr = parse_qs(urlparse(response.url).query).get("start", 0) + parse_qs(urlparse(response.url).query).get("limit", 0)
        curr = sum(int(x) for x in curr)
        
        if total and curr < total: 
            next = urlparse(response.url)
            search_params = parse_qs(next.query)
            search_params["start"] = curr 
            search_params["limit"] = 100
            next = next._replace(query=urlencode(search_params, doseq=True))

            return urlunparse(next)



    @classmethod
    @override
    def parse(self, response):
        api_call = url.Url(
            base=self.API_BASE,
            params= self.__parse_to_api_params(response.url) | {"start": 0, "limit": 100},
        )

        yield response.follow(
            str(api_call), 
            headers=self.API_HEADERS,
            callback=self.parse_from_api
        )
        
        

    @classmethod
    def parse_from_api(self, response):

        for x in self.url_extractor(response):
            yield x
                
        if (next := self.nextractor(response)): 
            yield response.follow(
                next, 
                headers=self.API_HEADERS,
                callback=self.parse_from_api
            )




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

