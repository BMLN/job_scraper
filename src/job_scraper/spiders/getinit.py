

DEFAULT_MAPPINGS = {
    "Adidas" : None, 
    "Airbus" : 82,
    "Allianz" : 4, 
    "BASF" : 2417,
    "Bayer" : 1376,
    "Beiersdorf" : 2037, 
    "BMW" : 173, 
    "Brenntag" : None,
    "Commerzbank" : 40, 
    "Continental" : None, 
    "Covestro" : 3476,
    "Daimler Truck" : 7285,
    "Deutsche Bank" : None,
    "Deutsche Börse" : None,
    "Deutsche Post" : 1246,
    "Deutsche Telekom" : None,
    "E.ON" : 280,
    "Fresenius" : 2860,
    "Hannover Rück" : 2516,
    "Heidelberg Materials" : None,
    "Henkel" : None,
    "Infineon" : None,
    "Mercedes-Benz Group" : None,
    "Merck" : None,
    "MTU Aero Engines" : 250,
    "Münchner Rück" : None,
    "Porsche AG" : None,
    "Porsche SE" : None,
    "Qiagen" : None,
    "Rheinmetall" : 178,
    "RWE" : None,
    "SAP" : 7049,
    "Sartorius" : None,
    "Siemens" : None,
    "Siemens Energy" : None,
    "Siemens Healthineers" : None,
    "Symrise" : None,
    "Volkswagen" : None,
    "Vonovia" : None,
    "Zalando" : None
}






from job_scraper.spiders import templ
import scrapy
from typing import override, Iterable






class GetInIT_JobSearch_Scraper(templ.JobSearch_Scraper):

    name = "getinit_jobsearch_spider"
    allowed_domains = ["get-in-it.de"]

    __base = "https://www.get-in-it.de/jobsuche"
    __extractor = scrapy.linkextractors.LinkExtractor(
        restrict_xpaths = "//div[@class='container']//a[contains(@class, 'CardJob_jobCard')]",
        restrict_text = "student"
    )



    # interface requirements

    @override
    def searchurl_for(self, company):
        #IT inherently filtered?
        url = templ.Url(self.__base.format())\
            .param("company", str(company))\

        return str(url)


    @override
    def extract_source(self, selector):
        
        return selector.xpath("//div[contains(@class, 'FilterCompany_filterCompany')]//div[@class='rbt-token-label']//text()").get()


    @override
    def extract_joburls(self, selector):

        links = self.__extractor.extract_links(selector)

        return [ str(x.url) for x in links ]


    #TODO: javascript interaction
    @override
    def extract_nextpage(self, response):
        return None









class GetInIT_JobInfo_Scraper(templ.JobInfo_Scraper):
    
    name = "getinit_jobinfo_spider"
    allowed_domains = ["get-in-it.de"]

    


    # Interface Implementations

    @override
    def extract_jobtitle(self, selector):
        
        return selector.xpath("//h1[contains(@class, 'JobHeaderRegular_jobTitle')]//text()").get()


    @override
    def extract_company(self, selector):
        
        return selector.xpath("//p[contains(@class, 'JobHeaderRegular_companyTitle')]//text()").get()


    @override
    def extract_location(self, selector):
        
        return selector.xpath("//div[contains(@class, 'JobHeaderRegular_jobLocation')]//text()").get()



    @override
    def extract_employment(self, selector):
        
        return None


    @override
    def extract_tasks(self, selector):
        
        return selector.xpath("//div[@class='container']//section[@data-section-name='tasks']//ul//li//text()").getall()


    @override
    def extract_qualifications(self, selector):
        
        return selector.xpath("//div[@class='container']//section[@data-section-name='requirements']//ul//li//text()").getall()


    @override
    def extract_etc(self, selector):
        
        return None

    
    @override
    def extract_rawtext(self, selector):
        
        #raw = selector.xpath("(//div[@class='container']//div[contains(@class, 'JobDescription']//child::*)[2]//text()").getall()
        return selector.xpath("(//div[@class='container']//div[contains(@class, 'JobDescription')]//child::*)[3]//text()").getall()
