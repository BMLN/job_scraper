import scrapy
import templ
import os
from typing import override

class StepstoneSpiderSpider(templ.Job_Scraper):
    name = "indeed_spider"
    allowed_domains = ["de.indeed.com"]
    start_urls = []

    __search_url = "https://de.indeed.com/jobs?q="
   
    @override
    def search_url(self, company):
        return self.__search_url + str(company)




    def parse(self, response):
        css = ""
        extractor = scrapy.linkextractors.LinkExtractor(
            
        )
        print("ayoo captain jack")
        yield{
            "test": "done"
        }
