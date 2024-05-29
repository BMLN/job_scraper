import new_templ
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote



class Indeed_JobSearch_Scraper(new_templ.JobSearchScraper):
    
    name = "indeed_jobsearch_spider"
    allowed_domains = ["de.indeed.com"]

    __extractor = LinkExtractor(
        allow = "https://de.indeed.com/rc/clk?", #needed for whatever reason hmm
        restrict_xpaths = "//div[@id='mosaic-jobResults']//ul//td[contains(@class, 'resultContent')]",
        #restrict_text = "student" #filter is gonna be applied on the dataset separately
    )

    #additionals? direct search?
    #@classmethod
    


    #interface requirements

    @classmethod
    @override
    def url_extractor(cls, response):
        return [ {"url" : url} for url in cls.__extractor.extract_links(response) ]


    @classmethod
    @override
    def nextractor(cls, response):
        nxt = response.xpath("//nav[@role='navigation']//li//a/@href").getall()

        if len(nxt) > 1:
            if nxt[-1] != "#":
                url = str(nxt[-1])

                return unquote(url)



















if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess()

    process.crawl(Indeed_JobSearch_Scraper, inputs=["www.google.de"])
    process.start() 