from job_scraper.spiders import templ
import scrapy 

from typing import override, Iterable
import re


class Arbeitsagentur_JobSearch_Scraper(templ.JobSearch_Scraper):

    name = "arbeitsagentur_jobsearch_spider"
    allowed_domains = ["arbeitsagentur.de"]

    __general_search_url = "https://www.arbeitsagentur.de/jobsuche/suche"
    __extractor = scrapy.linkextractors.LinkExtractor(
        restrict_xpaths = "//div[@id = 'ergebnisliste']",
        restrict_text = "student"
    )



    # interface requirements

    @override
    def searchurl_for(self, company):
        #str(company) +  + " Werkstudent")
        url = templ.Url(self.__general_search_url.format())\
            .param("was", str(company))\
            .param("angebotsart", 34)\
            .param("berufsfeld", "Informatik")

        return str(url)


    @override
    def extract_source(self, response):
        ret = re.search("was=(.*?)&", response.request.url)
        if ret != None:
            ret = ret.group()[4:-1]

        return ret


    @override
    def extract_joburls(self, selector):

        links = self.__extractor.extract_links(selector)

        return [ str(x.url) for x in links ]


    #TODO: javascript interaction
    @override
    def extract_nextpage(self, response):
        return None



    

class Arbeitsagentur_JobInfo_Scraper(templ.JobInfo_Scraper):
    
    name = "arbeitsagentur_jobinfo_spider"
    allowed_domains = ["arbeitsagentur.de"]

    
    # Interface Implementations

    @override
    def extract_jobtitle(self, selector):
        
        output = selector.xpath("//div[@id='detail-kopfbereich-titel']//text()").get()
        
        return output


    @override
    def extract_company(self, selector):
        
        output = selector.xpath("//span[@id='detail-kopfbereich-firma']//text()").get()
        
        return output


    @override
    def extract_location(self, selector):
        
        output = selector.xpath("//span[@id='detail-kopfbereich-arbeitsort']//text()").get()
        
        return output


    @override
    def extract_employment(self, selector):
        
        output = selector.xpath("//span[@id='detail-kopfbereich-angebotsart']//text()").get()
        
        return output


    @override
    def extract_tasks(self, selector):

        return None


    @override
    def extract_qualifications(self, selector):
        
        return None


    @override
    def extract_etc(self, selector):
                
        #return "-"
        #output = selector.xpath("//div[@class='ba-layout-tile']//child:**[2]")
        #print(output)
        #print(output.getall())
        return None

    
    @override
    def extract_rawtext(self, selector):
        #output = selector.xpath("//p[@id='detail-beschreibung-beschreibung']//child::*").getall()
        output = selector.xpath("//div[@class='ba-layout-tile']//text()").getall()
        

        return output