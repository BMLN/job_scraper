from job_scraper.core import new_templ, url
import scrapy 

from typing import override, Iterable
from urllib.parse import parse_qsl, parse_qs, urlparse, urlencode, urlunparse


class Arbeitsagentur_JobSearch_Scraper(new_templ.JobSearchScraper):

    name = "arbeitsagentur_jobsearch_spider"
    allowed_domains = ["arbeitsagentur.de"]

    API_PAGESIZE = 100

    API_BASE = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
    API_HEADERS = {
        "Accept":"application/json, text/plain, */*",
        "Origin":"https://www.arbeitsagentur.de",
        "Host":"rest.arbeitsagentur.de",
        "Accept-Language":"de-DE,de;q=0.9",
        "Accept-Encoding":"gzip, deflate, br",
        "Connection":"keep-alive",
        "X-API-Key":"jobboerse-jobsuche"
    }



    # interface requirements

    @classmethod  
    @override
    def url_extractor(cls, response) -> list[dict]:
        return [ {"url_text": job.get("titel"), "url" : f"{"https://www.arbeitsagentur.de/jobsuche/jobdetail/"}{job.get("refnr")}"} for job in response.json().get("stellenangebote") or [] ]


    @classmethod  
    @override
    def nextractor(cls, response):
        data = response.json()
        total = data.get("maxErgebnisse", 0)
        page = data.get("page", 1)
        size = data.get("size", cls.API_PAGESIZE)

        if page * size < total:
            next = urlparse(response.url)
            search_params = parse_qs(next.query)
            search_params["page"] = page + 1 
            next = next._replace(query=urlencode(search_params, doseq=True))

            return urlunparse(next)
            

    @override
    def parse(cls, response):
        api_call = url.Url(
            base=cls.API_BASE,
            params= dict(parse_qsl(urlparse(response.url).query)) | {"page": 1, "size": cls.API_PAGESIZE}
        )
        
        yield response.follow(
            str(api_call), 
            headers=cls.API_HEADERS,
            callback=cls.parse_api
        )
        

    @classmethod
    def parse_api(cls, response):
        for x in cls.url_extractor(response):
            yield x
                
        if (next := cls.nextractor(response)): 
            yield response.follow(
                next, 
                headers=cls.API_HEADERS,
                callback=cls.parse_api
            )


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

