from job_scraper.core import new_templ
from typing import override

from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote



class Indeed_JobScraper(new_templ.JobSearchScraper):
    
    name = "indeed_jobsearch_spider"
    allowed_domains = ["de.indeed.com"]

    __extractor = LinkExtractor(
        #allow = "https://de.indeed.com/rc/clk?", "https://de.indeed.com/pagead/clk?", #needed for whatever reason hmm
        allow = r"(de.indeed.com\/(rc|pagead)\/(clk\?))",
        restrict_xpaths = "//div[@id='mosaic-jobResults']//ul//td[contains(@class, 'resultContent')]//h2[contains(@class, 'jobTitle')]//a",
        #restrict_text = "student" #filter is gonna be applied on the dataset separately
    )

    #additionals? direct search?
    #@classmethod
    

    

    #interface requirements

    @classmethod
    @override
    def url_extractor(cls, response) -> [dict]:
        return [ {"url_text": url.text, "url" : url.url} for url in cls.__extractor.extract_links(response) ]


    #TODO: fix: problems if  less <5?
    @classmethod
    @override
    def nextractor(cls, response) -> str:
        nxt = response.xpath("//nav[@role='navigation']//li//a//@href").getall()

        #return None #TODO
        if len(nxt) > 0:
            if nxt[-1] != "#":
                url = str(nxt[-1])

                return unquote(url)







class Indeed_InfoScraper(new_templ.JobInfoScraper):

    name = "indeed_jobinfo_spider"
    allowed_domains = ["de.indeed.com"]



    #interface requirements
    




    @classmethod
    @override
    def extract_jobtitle(cls, selector) -> str:
        return selector.xpath("//h1[contains(@class, 'jobsearch-JobInfoHeader-title')]//text()").get()

    @classmethod
    @override
    def extract_content(cls, selector) -> str:
        return selector.xpath("//div[@id='jobDescriptionText']").get()

    @classmethod       
    @override
    def extract_company(cls, selector) -> str:
        output = selector.xpath("//div[@data-testid='jobsearch-CompanyInfoContainer']//text()").getall()
        output = [ x for x in output if ("css" in x ) == False] #why necessary ? :o only running spider demanding it, fine with html otherwise

        if len(output) > 0:
            output = output[0]

        return output

    @classmethod       
    @override
    def extract_field(cls, selector) -> str:
        return None

    @classmethod       
    @override
    def extract_industry(cls, selector) -> str:
        return None

    @classmethod       
    @override
    def extract_employment(cls, selector) -> str:
        output = selector.xpath("//div[@id='salaryInfoAndJobType']//text()").getall()
        #print(output)

        output = [ x for x in output if ("css" in x ) == False] #why necessary ? :o only running spider demanding it, fine with html otherwise

        if len(output) > 0:
            output = output[0]

        return output 

    @classmethod       
    @override
    def extract_location(cls, selector) -> str:
        return selector.xpath("//div[@class='jobsearch-BodyContainer']//div[@id='jobLocationText']//text()").get()

    @classmethod       
    @override
    def extract_posting(cls, selector) -> str:
        return None

