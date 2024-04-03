import scrapy
import templ
from typing import override


class StepstoneSpiderSpider(templ.Job_Scraper):
    f = 0
    name = "stepstone_spider"
    allowed_domains = ["stepstone.de"]
    start_urls = [] #["https://www.stepstone.de"]

    __search_url = "https://stepstone.de/jobs/"
    __extractor = scrapy.linkextractors.LinkExtractor(
        #allow = "/www\.stepstone\.de\/stellenangebote--.*/",
        allow = "/stellenangebote--", #some problems with regex, rly correct?
        restrict_xpaths = "//div[contains(@class, 'results')]"
    )

    @override
    def searchurl(self, company):
        #return self.__search_url + str(company)
        #return "file:///Users/lorandbanki/Desktop/Arbeit/job_scraper/xpath.html"
        return "https://stepstone.de/jobs/adidas"

    @override
    def extract_joburls(self, response):
        return self.__extractor.extract_links(response)

    def l(self, response):
        a = self.extract_joburls(response)
        print(a)

        #for them page.parse
        for x in a:
            yield{
                "p" : StepstoneSpiderSpider.f,
                "url": x.url[:-10]
            }


    def parse(self, response):
        print("ayoo captain jack")
        yield self.l(response)
        
        StepstoneSpiderSpider.f += 1
        nx = response.xpath("//nav[contains(@aria-label, 'pagination')]//a[@href]/@href").extract()[-1]
        #print("next:", nx)
        yield response.follow(nx, self.l) #funktioniert anscheinend?????


        
