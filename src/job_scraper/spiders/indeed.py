#sc_tags
# no entry vs just cant search -> use a filter check?
mappings_comp = {
    "Adidas": "0kf%3Afcckey%287f9e37cf52823de0%29%3B",
    "Airbus": "0kf%3Afcckey%28542cd993303a0af1%29%3B",
    "Allianz": "0kf%3Afcckey%2849c194c298f9e8ab%29%3B",
    "BASF": "0kf%3Afcckey%28e52b8d98ce1b9bd6%29%3B",
    "Bayer": "0kf%3Afcckey%28c80e7ceae59adb32%29%3B",
    "Beiersdorf": "0kf%3Afcckey%28c3f07f3464f67ce1%29%3B",
    "BMW": "0kf%3Afcckey%28f3774117e317f6fe%29%3B",
    "Brenntag": "0kf%3Afcckey%285f55c55b3d54bcad%29%3B",
    "Commerzbank": None,  #cant access
    "Continental": "0kf%3Afcckey%28a622be31ab4d1630%29%3B",
    "Covestro": "0kf%3Afcckey%28eac8463a66841599%29%3B",
    "Daimler Truck": "0kf%3Afcckey%288462355875d09496%29%3B",
    "Deutsche Bank": "0kf%3Afcckey%282c15c2180b5fa05e%29%3B",
    "Deutsche Börse": "0kf%3Afcckey%2808d700c827322986%29%3B",
    "Deutsche Post": "0kf%3Afcckey%28fbccf6c522cc15e9%29%3B",
    "Deutsche Telekom": "0kf%3Afcckey%28ab29256fb6bd4b9b%29%3B",
    "E.ON": "0kf%3Afcckey%2822703c005eff4044%29%3B",
    "Fresenius": "0kf%3Afcckey%28c455cfb882fdd02b%29%3B",
    "Hannover Rück": "0kf%3Afcckey%28369531a10bd2384a%29%3B",
    "Heidelberg Materials": "0kf%3Afcckey%284157d3b1cb10734e%29%3B",
    "Henkel": "0kf%3Afcckey%2806d5bde2bebf208f%29%3B",
    "Infineon": "0kf%3Afcckey%28e9afa588f8da14ed%29%3B",
    "Mercedes-Benz Group": None, #no matches available?
    "Merck": "0kf%3Afcckey%280fa702df80dee049%29%3B",
    "MTU Aero Engines" : "0kf%3Afcckey%286957b4bdf27bdda4%29%3B",
    "Münchner Rück" : None, #no matches,
    "Porsche AG" : "0kf%3Afcckey%2814a557f88aaacc1b%29%3B",
    "Porsche SE" : None, #no matches
    "Qiagen": "0kf%3Afcckey%28b9d75c03c58c936f%29%3B",
    "Rheinmetall": "0kf%3Afcckey%2852bf96eed3429552%29%3B",
    "RWE": "0kf%3Afcckey%2845c44d607c0f379e%29%3B",
    "SAP": "0kf%3Afcckey%28e2c9cc0096a62957%29%3B",
    "Sartorius": "0kf%3Afcckey%28df7916122576fa45%29%3B",
    "Siemens": "0kf%3Afcckey%2804859a4685a9d49a%29%3B",
    "Siemens Energy" : "0kf%3Afcckey%28edac69bff2dabae1%29%3B",
    "Siemens Healthineers" : "0kf%3Afcckey%28f6785058a8bee50e%29%3B",
    "Symrise": "0kf%3Afcckey%2860a5f9e6679e9e01%29%3B",
    "Volkswagen" : "0kf%3Afcckey%28a2f79f1c3091568f%29%3B",
    "Vonovia": "0kf%3Afcckey%28f419a14b2d800795%29%3B",
    "Zalando": "0kf%3Acmpsec%28NKR5F%29fcckey%2804a6aab76d29c65c%29%3B"
}
from urllib.parse import unquote
mappings_comp = { key : unquote(value) if value != None else None for key, value in mappings_comp.items() }

#IT = "cmpsec%28NKR5F%29"
searchs = {
    "Adidas": "0kf%3Afcckey%287f9e37cf52823de0%29cmpsec%28NKR5F%29%3B",
    "Airbus": "0kf%3Afcckey%28542cd993303a0af1%29cmpsec%28NKR5F%29%3B",
    "allianz": "0kf%3Afcckey%2849c194c298f9e8ab%29cmpsec%28NKR5F%29%3B",
    "basf": "0kf%3Afcckey%28e52b8d98ce1b9bd6%29cmpsec%28NKR5F%29%3B",
    "bayer": "0kf%3Afcckey%28c80e7ceae59adb32%29cmpsec%28NKR5F%29%3B",
    "beiersdorf": "0kf%3Afcckey%28c3f07f3464f67ce1%29cmpsec%28NKR5F%29%3B",
    "bmw": "0kf%3Afcckey%28f3774117e317f6fe%29cmpsec%28NKR5F%29%3B",
    "Brenntag": "0kf%3Afcckey%285f55c55b3d54bcad%29cmpsec%28NKR5F%29%3B",
    "Commerzbank": "",  #cant access
    "Contintental": "0kf%3Afcckey%28a622be31ab4d1630%29cmpsec%28NKR5F%29%3B",
    "Covestro": "0kf%3Afcckey%28eac8463a66841599%29cmpsec%28NKR5F%29%3B",
    "Daimler Truck": "0kf%3Afcckey%288462355875d09496%29cmpsec%28NKR5F%29%3B",
    "Deutsche Bank": "0kf%3Afcckey%282c15c2180b5fa05e%29cmpsec%28NKR5F%29%3B",
    "Deutsche Börse": "0kf%3Afcckey%2808d700c827322986%29cmpsec%28NKR5F%29%3B",
    "Deutsche Post": "0kf%3Afcckey%28fbccf6c522cc15e9%29cmpsec%28NKR5F%29%3B",
    "Deutsche Telekom": "0kf%3Afcckey%28ab29256fb6bd4b9b%29cmpsec%28NKR5F%29%3B",
    "E.ON": "0kf%3Afcckey%2822703c005eff4044%29cmpsec%28NKR5F%29%3B",
    "Fresenius": "0kf%3Afcckey%28c455cfb882fdd02b%29cmpsec%28NKR5F%29%3B",
    "Hannover Rück": "0kf%3Afcckey%28369531a10bd2384a%29cmpsec%28NKR5F%29%3B",
    "Heidelberg Materials": "0kf%3Afcckey%284157d3b1cb10734e%29cmpsec%28NKR5F%29%3B",
    "Henkel": "0kf%3Afcckey%2806d5bde2bebf208f%29cmpsec%28NKR5F%29%3B",
    "Infineon": "0kf%3Afcckey%28e9afa588f8da14ed%29cmpsec%28NKR5F%29%3B",
    "Mercedes-Benz Group": "", #no matches available?
    "Merck": "0kf%3Afcckey%280fa702df80dee049%29cmpsec%28NKR5F%29%3B",
    "MTU Aero Engines" : "0kf%3Afcckey%286957b4bdf27bdda4%29cmpsec%28NKR5F%29%3B",
    "Münchner Rück" : "", #no matches,
    "Porsche AG" : "0kf%3Afcckey%2814a557f88aaacc1b%29cmpsec%28NKR5F%29%3B",
    "Porsche SE": "", #no matches
    "Qiagen": "0kf%3Afcckey%28b9d75c03c58c936f%29cmpsec%28NKR5F%29%3B",
    "Rheinmetall": "0kf%3Afcckey%2852bf96eed3429552%29cmpsec%28NKR5F%29%3B",
    "RWE": "0kf%3Afcckey%2845c44d607c0f379e%29cmpsec%28NKR5F%29%3B",
    "SAP": "0kf%3Afcckey%28e2c9cc0096a62957%29cmpsec%28NKR5F%29%3B",
    "Sartorius": "0kf%3Afcckey%28df7916122576fa45%29cmpsec%28NKR5F%29%3B",
    "Siemens": "0kf%3Afcckey%2804859a4685a9d49a%29cmpsec%28NKR5F%29%3B",
    "Siemens Energy" : "0kf%3Afcckey%28edac69bff2dabae1%29cmpsec%28NKR5F%29%3B",
    "Siemens Healthineers" : "0kf%3Afcckey%28f6785058a8bee50e%29cmpsec%28NKR5F%29%3B",
    "Symrise": "0kf%3Afcckey%2860a5f9e6679e9e01%29cmpsec%28NKR5F%29%3B",
    "Volkswagen" : "0kf%3Afcckey%28a2f79f1c3091568f%29cmpsec%28NKR5F%29%3B",
    "Vonovia": "0kf%3Afcckey%28f419a14b2d800795%29cmpsec%28NKR5F%29%3B",
    "Zalando": "0kf%3Acmpsec%28NKR5F%29fcckey%2804a6aab76d29c65c%29%3B"
}











import scrapy
from job_scraper.spiders import templ
from typing import override

from scrapy.utils.project import get_project_settings

from job_scraper.selenium.http import SeleniumRequest
from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC
#from selenium import webdriver
#from shutil import which

import os

#TODO: finish, selenium x proxy request -> problematic?
class Indeed_CompanyMapping_Scraper(templ.Mapping_Scraper):
    name = "indeed_companymapping_spider"
    allowed_domains = ["de.indeed.com"]
    __general_url = "https://de.indeed.com/jobs"


    #selenium setuptesting

    # #aleister = webdriver.Safari()
    # #print(which("safaridriver"))
    # #aleister.get("http://www.python.org")

    # #aleister = webdriver.Chrome()
    # #print(which("safaridriver"))
    # #aleister.get("http://www.python.org")

    # #todo: change2general configuration
    # x = {
    #     "SELENIUM_DRIVER_NAME" : "chrome",
    #     "SELENIUM_DRIVER_EXECUTABLE_PATH" : None, #which("safaridriver"),
    #     "SELENIUM_DRIVER_ARGUMENTS" : ["-headless", "--log-level=3"],
    #     #"DOWNLOADER_MIDDLEWARES" : {
    #     #    "scrapy_selenium.SeleniumMiddleware": 800
    #     #}
    #     "DOWNLOADER_MIDDLEWARES" : {
    #         "job_scraper.middlewares.JobScraperDownloaderMiddleware": 350,
    #         "job_scraper.selenium.middlewares.SeleniumMiddleware": 800,
    #     }
    # }  
    # settings = get_project_settings()
    # settings.setdict(x)

    # custom_settings = settings

    # @override
    # def start_requests(self):
    #     return [
    #         SeleniumRequest(
    #             url=start_url,
    #             callback=self.parse,
    #             #wait_until=EC.element_to_be_clickable
    #         ) for start_url in self.start_urls
    #     ]




    # interface requirements
    
    @override 
    def searchurl_for(self, search_tag):
        return str(templ.Url(self.__general_url).param("q", search_tag))


    #TODO: proper tagging
    @override
    def source_tag(self, response):
        src = response.request.url
        if "scrapeops" in src:
            src = unquote(src)
        src = src[src.index("/jobs?q=")+len("/jobs?q="):]
        if "&" in src:
            src = src[:src.index("&")]

        return src


    @override
    def mappings(self, response, tag):
        output = []
        comp_tag = tag.lower().replace("-", "+") #.lower().replace(" ", "").replace("-", "") #not used yet since tag comes from url currently and not from a proper init
        filters = response.xpath("//div[@role='search']").xpath(".//ul[contains(@class, 'dropdownList')]")

        for x in filters:
            if x.xpath("@id").get() == "filter-fcckey-menu": 
                names = x.xpath(".//li//text()").getall()
                #names = [ x[:x.rindex("(")] for x in names ]
                
                links = x.xpath(".//li//a//@href").getall()
                links = [ x[x.index("&sc=")+4:x.index("&sc=")+4+33] for x in links ]

        for x in zip(names, links):
            name_tag = x[0][:x[0].rindex("(")]
            name_count = x[0][x[0].rindex("(")+1:x[0].rindex(")")]

            if comp_tag in name_tag.lower().replace(" ", "+").replace("-","+"): #flag for on/off for check?
                output.append( {"name": name_tag, "counts": name_count, "mapping": x[1]} )


        return output




    #DEPRECATED?
    def extract_branchen(self, response):
        #buttons = response.xpath("//div[@role='search']").xpath(".//div[contains(@class, 'Filter')]//ul").xpath("(child::*)").xpath(".//button")
        #labels = buttons.xpath(".//text()")
        
        # buttons = response.request.meta["driver"].find_elements(By.XPATH, '//div[@id="app-searchBar"]//button')
        # print("buttons", buttons)
        # if buttons != None and len(buttons) > 0:
        #     response.request.meta["driver"].find_elements(By.XPATH, '//div[@id="app-searchBar"]//button').click()
        # #print("yyyy", response.request.meta)
        # return {"content": "empty"}
        buttons = response.xpath("//div[@role='search']").xpath(".//div[contains(@class, 'Filter')]//ul").xpath("(child::*)").xpath(".//button")


        return None
    


class Indeed_JobSearch_Scraper(templ.JobSearch_Scraper):
    
    name = "indeed_jobsearch_spider"
    allowed_domains = ["de.indeed.com"]

    __base = "https://de.indeed.com/jobs"
    __extractor = scrapy.linkextractors.LinkExtractor(
        allow = "https://de.indeed.com/rc/clk?", #needed for whatever reason hmm
        restrict_xpaths = "//div[@id='mosaic-jobResults']//ul//td[contains(@class, 'resultContent')]",
        restrict_text = "student"
    )



    # Interface Requirements

    @override
    def searchurl_for(self, company):
        #return "file:///Users/lorandbanki/Desktop/Arbeit/April/job_scraper/html/indeed.html"
        #return "file:///Users/lorandbanki/Desktop/Arbeit/job_scraper/jobsite.html"
        #params not correct, set manually
        url = templ.Url(self.__base)\
            .param("q", "Werkstudent IT")\
            .param("sc", mappings_comp[company])

        return str(url)


    @override
    def extract_joburls(self, selector):
        links = self.__extractor.extract_links(selector)
        return [ str(x.url) for x in links ]

    @override
    def extract_nextpage(self, selector):
        nxt = selector.xpath("//nav[@role='navigation']//li//a/@href").getall()

        if len(nxt) > 1:
            if nxt[-1] != "#":
                url = str(nxt[-1])

                return unquote(url)


    @override
    def extract_source(self, selector):
        return selector.xpath("//div[@role='search']//a[@id='filter-fcckey']//text()").get()






#TODO:

class Indeed_JobInfo_Scraper(templ.JobInfo_Scraper):
    
    name = "indeed_jobinfo_spider"
    allowed_domains = ["de.indeed.com"]

    
    # Interface Implementations

    @override
    def extract_jobtitle(self, selector):
        
        output = selector.xpath("//h1[contains(@class, 'jobsearch-JobInfoHeader-title')]//text()").get()
        
        return output


    @override
    def extract_company(self, selector):
        
        output = selector.xpath("//div[@data-testid='jobsearch-CompanyInfoContainer']//text()").getall()
        output = [ x for x in output if ("css" in x ) == False] #why necessary ? :o only running spider demanding it, fine with html otherwise

        if len(output) > 0:
            output = output[0]

        return output


    @override
    def extract_location(self, selector):
        
        return selector.xpath("//div[@class='jobsearch-BodyContainer']//div[@id='jobLocationText']//text()").get()
        

    @override
    def extract_employment(self, selector):
        output = selector.xpath("//div[@id='salaryInfoAndJobType']//text()").getall()
        print(output)

        output = [ x for x in output if ("css" in x ) == False] #why necessary ? :o only running spider demanding it, fine with html otherwise

        if len(output) > 0:
            output = output[0]

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
        output = selector.xpath("//div[@id='jobDescriptionText']//text()").getall()
        

        return output
    

    @override 
    def extract_jobnode(self, selector):
        return selector.xpath("//div[@id='jobDescriptionText']").get()