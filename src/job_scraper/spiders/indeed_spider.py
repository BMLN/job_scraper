import scrapy
import templ
import os


#class IndeedSpiderSpider(scrapy.Spider, templ.Job_Scraper):
class IndeedSpiderSpider(object):#templ.Job_Scraper):
    name = "indeed_spider"
    allowed_domains = ["de.indeed.com"]
    start_urls = ["https://de.indeed.com/jobs"]
    #allowed_domains = ["uni-due.de"]
    #start_urls = ["https://uni-due.de/aktuell/"]
    

    #def __init__(self, **kwargs):
    #    print(kwargs)
    #    super().__init__(**kwargs)
        #quit(1)


    def parse(self, response):
        print(os.environ["TEST"])
        print("yes indeed")

        yield {
            "text": "lul"
        }
        # d = scrapy.linkextractors.LinkExtractor().extract_links(response)
        # #print(d)
        # for link in d:
        #     yield {"text": link.text, "url" : link.url}
        #r = scrapy.http.FormRequest.from_response(response, formdata={"q":"adidas", "l": None, "from":"searchOnHP"})
        #print("r-done!")

        pass

    def set_mappings():
        return False