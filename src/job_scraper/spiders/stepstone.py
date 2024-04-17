import scrapy
from job_scraper.spiders import templ
from typing import override
import re
import logging




class Stepstone_JobSearch_Scraper(templ.JobSearch_Scraper):
    name = "stepstone_jobsearch_spider"
    allowed_domains = ["stepstone.de"]

    __general_search_url = "https://www.stepstone.de/jobs/{company}"
    __company_search_url = "https://www.stepstone.de/cmp/de{company}/jobs"
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
            #return #write to other file


    @override
    def exctract_nextpage(self, selector):
        if self.has_applied_filters(selector):
            super().extract_nextpage(selector)
        else:
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
        return "file:///Users/lorandbanki/Desktop/Arbeit/job_scraper/xpathstuff2.html"
        #return "file:///Users/lorandbanki/Desktop/Arbeit/job_scraper/jobsite.html"
        url = templ.Url(base(company = company))\
            .param("fu", 1000000)\
            .param("ct", 229)

        return str(url)

    @override
    def extract_joburls(self, selector):
        links = self.__extractor.extract_links(selector)
        return [ str(x.url) for x in links ]

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
