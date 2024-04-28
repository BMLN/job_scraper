import scrapy
from job_scraper.spiders import templ
from typing import override
import re
import logging




mappings_comp = {
    "Adidas": "adidas-AG-41866",
    "Airbus": "Airbus-Group-500",
    "Allianz": "allianz-versicherungs-ag-30958",
    "BASF": "BASF-SE-7616",
    "Bayer": "bayer-318068",
    "Beiersdorf": "Beiersdorf-AH-8453",
    "BMW": "BMW-Group-27361",
    "Brenntag": "Brenntag-GmbH-24117",
    "Commerzbank": "Commerzbank-AG-9509",  
    "Continental": "Continental-AG-3975",
    "Covestro": None, #none
    "Daimler Truck": "Daimler-Truck-AG-283584",
    "Deutsche Bank": "deutsche-bank-33645",
    "Deutsche Börse": "deutsche-börse-group-167150",
    "Deutsche Post": "deutsche-post-ag-136538",
    "Deutsche Telekom": None, #none
    "E.ON": "eon-2346",
    "Fresenius": "fresenius-se-&-co-kgaa-9881",
    "Hannover Rück": "hannover-rück-se-4647",
    "Heidelberg Materials": "heidelberg-materials-ag-25005",
    "Henkel": "henkel-ag-&-co-kgaa-28132",
    "Infineon": None, #none
    "Mercedes-Benz Group": "mercedes-benz-group-ag-25115",
    "Merck": "merck-kgaa-darmstadt_germany-5838",
    "MTU Aero Engines" : "MTU-Aero-Engines-AG-33244",
    "Münchner Rück" : None, #no matches,
    "Porsche AG" : "porsche-ag-4166",
    "Porsche SE" : "porsche-automobil-holding-se-130455",
    "Qiagen": "qiagen-gmbh-1827",
    "Rheinmetall": "rheinmetall-1262",
    "RWE": "rwe-generation-se-148648",
    "SAP": "sap-se-215050",
    "Sartorius": "sartorius-32291",
    "Siemens": "siemens-ag-4831",
    "Siemens Energy" : "siemens-gamesa-renewable-energy-220386",
    "Siemens Healthineers" : "siemens-healthineers-ag-358280",
    "Symrise": "symrise-ag-112974",
    "Volkswagen" : "volkswagen-infotainment-gmbh-148893",
    "Vonovia": "vonovia-76597",
    "Zalando": "zalando-se-71523"
}


#TODO: none cmps arent filtered
class Stepstone_JobSearch_Scraper(templ.JobSearch_Scraper):
    name = "stepstone_jobsearch_spider"
    allowed_domains = ["stepstone.de"]

    __general_search_url = "https://www.stepstone.de/jobs/{company}"
    __company_search_url = "https://www.stepstone.de/cmp/de/{company}/jobs"
    __extractor = scrapy.linkextractors.LinkExtractor(
        #allow = "/www\.stepstone\.de\/stellenangebote--.*/",
        allow = "/stellenangebote--", #some problems with regex, rly correct?
        #restrict_xpaths = "//div[contains(@class, 'results')]"
        restrict_xpaths = "(//div[@data-genesis-element = 'CARD_GROUP_CONTAINER'])[1]"
    )


    #gets all lists
    #sel = selector.xpath("//div[contains(@data-at, 'content-container')][1]").xpath("(child::*)[2]").xpath(".//ul//text()")

    def has_applied_filters(self, selector, filter_count):
        sel = selector.xpath("(//div[contains(@data-at, 'filters-container')])//div[contains(@class, 'filtertag')]//text()")#.xpath("(//div[contains(@class, 'filtertag')])")
        
        return len(sel.getall()) == filter_count


    @override
    def parse(self, response):
        if self.has_applied_filters(response, 2):
            return super().parse(response)
        else:
            logging.warning( str("didnt apply filter on " + str(response.request.url) + "!") )
            return templ.Error(
                url = response.request.url,
                err = "err"
            )


    # @override
    # def extract_nextpage(self, selector):
    #     if self.has_applied_filters(selector):
    #         super().extract_nextpage(selector)
    #     else:
    #         return None

    #TODO
    @override 
    def extract_source(self, selector):
        return None



    @override
    def outputs():
        outs = templ.JobSearch_Scraper.outputs()
        outs.append([templ.Error])
        return outs



    # Interface Requirements

    @override
    def searchurl_for(self, company, is_company=False):
        #return self.__search_url + str(company)
        base = self.__general_search_url if is_company is False else self.__company_search_url
        base = self.__company_search_url

        #return "file:///Users/lorandbanki/Desktop/Arbeit/job_scraper/xpathstuff2.html"
        #return "file:///Users/lorandbanki/Desktop/Arbeit/job_scraper/jobsite.html"
        url = templ.Url(base.format(company = mappings_comp[company]))\
            .param("fu", 1000000)\
            .param("ct", 229)

        return str(url)

    @override
    def extract_joburls(self, selector):
        if self.has_applied_filters(selector, 2):
            links = self.__extractor.extract_links(selector)
            return [ str(x.url) for x in links ]
        else:
            print("yh")
            return []

    #TODO: add filtercheck
    @override
    def extract_nextpage(self, selector):
        nxt = selector.xpath("//nav[contains(@aria-label, 'pagination')]//a[@href]/@href").extract()
        
        if len(nxt) > 1:
            return nxt[-1]
        else:
            return None




class Stepstone_JobInfo_Scraper(templ.JobInfo_Scraper):
    
    name = "stepstone_jobinfo_spider"
    allowed_domains = ["stepstone.de"]

    
    # Interface Implementations

    @override
    def extract_jobtitle(self, selector):
        ret = re.search("--(.*?)--", selector.request.url)
        if ret != None:
            ret = ret.group()[2:-2]

        return ret


    @override
    def extract_company(self, selector):
        elem = selector.xpath("//div[@id='job-ad-content']").xpath(".//li[contains(@class, 'company-name')]//text()")
        elem_texts = elem.getall()

        if len(elem_texts) == 2:
            #icon_info = elem_texts[0]
            #company_info = elem_texts[1]
            return elem_texts[1]


    @override
    def extract_location(self, selector):
        elem = selector.xpath("//div[@id='job-ad-content']").xpath(".//li[contains(@class, 'location')]//text()")
        elem_texts = elem.getall()

        if len(elem_texts) == 2:
            #icon_info = elem_texts[0]
            #location_info = elem_texts[1]
            return elem_texts[1]


    @override
    def extract_employment(self, selector):
        elem = selector.xpath("//div[@id='job-ad-content']").xpath(".//li[contains(@class, 'contract-type')]//text()")
        elem_texts = elem.getall()

        if len(elem_texts) == 2:
            #icon_info = elem_texts[0]
            #employment_info = elem_texts[1]
            return elem_texts[1]


    @override
    def extract_tasks(self, selector):
        tasks = selector.xpath("//div[contains(@data-at, 'content-container')][1]").xpath(".//div[contains(@class, 'text-description')]").xpath(".//ul//child::*//text()") 

        return tasks.getall()


    @override
    def extract_qualifications(self, selector):
        qualifications = selector.xpath("//div[contains(@data-at, 'content-container')][1]").xpath(".//div[contains(@class, 'text-profile')]").xpath(".//ul//child::*//text()") 

        return qualifications.getall()


    @override 
    def extract_etc(self, selector):
        return None

    @override
    def extract_rawtext(self, selector):
        #return selector.xpath("//div[@data-atx-component='JobAdContent']//text()").getall()
        return None


    @override
    def extract_jobnode(self, selector):
        return selector.xpath("//div[@data-atx-component='JobAdContent']").get()
