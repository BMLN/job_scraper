from job_scraper.core import new_templ, url
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote

import json


class Stepstone_JobScraper(new_templ.JobSearchScraper):
    
    name = "stepstone_jobsearch_spider"
    allowed_domains = ["stepstone.de"]

    API_PAGESIZE = 0

    API_BASE = 'https://www.stepstone.de/public-api/resultlist/unifiedResultlist'
    API_HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://www.stepstone.de',
        'Accept-Language': 'de-DE,de;q=0.9',
        'Host': 'www.stepstone.de',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15',
        'Referer': 'https://www.stepstone.de/jobs/werkstudent-in-it?q=Werkstudent%2fin+IT',
        'Connection': 'keep-alive',
    }
    API_JSON = {
        'url': None,
        'lang': 'de',
        'siteId': 250,
        'userData': {
            'isUserLoggedIn': False,
            'candidateId': '',
            'userHashId': "e5bcd192-0d0f-42dd-ae38-92baf934ddd6", #use a random uuid
        },
        'isNonEUUser': False,
        'isBotCrawler': False,
        'uiLanguage': 'de',
        'fields': [
            'items',
            'pagination',
            'unifiedPagination',
        ],
    }

    custom_settings = {
        "CFM_MODE": "ROTATE",
        "CMF_SESSION_COUNT" : 30,
        "CFM_SESSION_LIMIT" : 50,
        "CFM_SESSION_INIT_THRESHOLD" : 10,
        "CFM_SESSION_EVAL_THRESHOLD" : 0.2,
        "CFM_MULTI_THRESHOLD" : 0,
        "CFM_MULTI_RANGE" : 30,
        "RETRY_TIMES" : 3
    }




    #interface requirements

    @classmethod
    @override
    def url_extractor(cls, response) -> [dict]:
        return [ {"url_text": job.get("title"), "url" : f"{"https://www.stepstone.de"}{job.get("url")}"} for job in (response.json().get("items") or []) ]


    @classmethod
    @override
    def nextractor(cls, response) -> str:
        next = response.json().get("unifiedPagination", {}).get("links", {}).get("next")

        if next:
            return json.dumps(cls.API_JSON | { "url": next })


    @override
    def parse(cls, response):
        api_call = url.Url(
            base=cls.API_BASE,
        )
        
        yield response.follow(
            str(api_call), 
            method="POST",
            headers=cls.API_HEADERS,
            body= json.dumps(cls.API_JSON | { "url": response.url }),
            callback=cls.parse_api
        )
        

    @classmethod
    def parse_api(cls, response):
        for x in cls.url_extractor(response):
            yield x
                
        if (next := cls.nextractor(response)): 
            yield response.follow(
                cls.API_BASE, 
                method="POST",
                headers=cls.API_HEADERS,
                body=next,
                callback=cls.parse_api
            )





class Stepstone_InfoScraper(new_templ.JobInfoScraper):
    
    name = "stepstone_jobinfo_spider"
    allowed_domains = ["stepstone.de"]



    custom_settings = {
        "CFM_MODE": "ROTATE",
        "CMF_SESSION_COUNT" : 30,
        "CFM_SESSION_LIMIT" : 50,
        "CFM_SESSION_INIT_THRESHOLD" : 10,
        "CFM_SESSION_EVAL_THRESHOLD" : 0.2,
        "CFM_MULTI_THRESHOLD" : 0,
        "CFM_MULTI_RANGE" : 30,
        "RETRY_TIMES" : 3
    }



    #interface requirements
    

    @classmethod
    @override
    def extract_jobtitle(cls, selector):
        return selector.xpath("//span[@data-at='header-job-title']//text()").get()

    @classmethod
    @override
    def extract_content(cls, selector) -> str:
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



    
    @classmethod
    @override
    def jobinfo_extractor(cls, response) -> list[dict]:
        data = response.xpath("//script[@type='application/ld+json']//text()").get() or str({})
        data = json.loads(data)
        
        return [{
                "title": data.get("title"),
                "content": data.get("description"), 
                "company": cls.extract_company(response),
                "field" : None,
                "industry" : data.get("industry"),
                "employment": data.get("employmentType"),
                "location" : cls.extract_location(response),
                "posted": data.get("datePosted")
            }]