from job_scraper.core import new_templ, url
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote

import json


#TODO: javascript
class Monster_JobScraper(new_templ.JobSearchScraper):
    
    name = "monster_jobsearch_spider"
    allowed_domains = ["monster.de", "appsapi.monster.io"]

    
    API_PAGESIZE = 9
    
    API_BASE = "https://appsapi.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/de-DE"
    API_HEADERS = {
        "accept": "application/json",
        "accept-language": "de-DE,de;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://www.monster.de",
        "referer": "https://www.monster.de/jobs/suche?q=adidas",
    }
    API_PARAMS = {"apikey":"AE50QWejwK4J73X1y1uNqpWRr2PmKB3S"}
    API_JSON = {
            "jobQuery": {
                "query" : None,
                "locations": [
                    {
                        "country": "de",
                        "address": "",
                        "radius": {
                            "unit": "km",
                            "value": 20
                        }
                    }
                ]
            },
            "jobAdsRequest": {
                "position": [
                    1,2,3,4,5,6,7,8,9
                ],
                "placement": {
                    "channel": "MOBILE",
                    "location": "JobSearchPage",
                    "property": "monster.de",
                    "type": "JOB_SEARCH",
                    "view": "CARD"
                }
            },
            "fingerprintId": None,
            "offset": 0,
            "pageSize": 9,
            "includeJobs": [],
            "paidJobsOnly": True
        }

        
    @classmethod
    def __url_to_jsondata(cls, url):
        output = cls.API_JSON
        
        __query = None
        __positions = None
        __fingerprintId = None

        output["jobQuery"]["query"] = "adidas"
        output["fingerprintId"] = "z41ad53fa720dc7ca6cb4f6e4f2b8f658"

        #output[""]
        
        output = json.dumps(output)
        #print(output)
        return output


    #interface requirements

    @classmethod
    @override
    def url_extractor(cls, response) -> [dict]:
        job_postings = [ job.get("jobPosting") or {} for job in (response.json().get("jobResults") or []) ]
        
        return [
            {
                "url_text" : posting.get("title"),
                "url" : posting.get("url"),
                "title": posting.get("title"),
                "content": posting.get("description"),
                "company": (posting.get("hiringOrganization") or {}).get("name"),
                "field": None,
                "industry": posting.get("industry"),
                "employment": posting.get("employmentType"),
                "location": ((posting.get("jobLocation") or [{}])[0].get("address") or {}).get("postalCode"),
                "posted": posting.get("datePosted")
            } 
            for posting in job_postings
        ]


    @classmethod
    @override
    def nextractor(cls, response) -> str:
        api_json = response.json().get("jobRequest")
        
        if api_json:
            api_json["offset"] = api_json.get("offset", 0) + cls.API_PAGESIZE
            api_json = json.dumps(api_json)

        return api_json


    @classmethod
    @override
    def parse(self, response):
        api_call = url.Url(
            base=self.API_BASE,
            params=self.API_PARAMS,
        )
        
        yield response.follow(
            str(api_call), 
            method="POST", 
            headers=self.API_HEADERS,
            body=self.__url_to_jsondata(response.url),
            callback=self.parse_from_api
        )
        
        

    @classmethod
    def parse_from_api(self, response):
        for x in self.url_extractor(response):
            yield x
                
        if (next := self.nextractor(response)): 
            
            yield response.follow(
                response.url, 
                method="POST", 
                headers=self.API_HEADERS,
                body=next,
                callback=self.parse_from_api
            )





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



#TODO: put InfoScraper into JobScrpaer for monster# nope -> different source material
#TODO: paging, how many items at once? how to change page, etc