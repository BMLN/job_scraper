#     __general_search_url = "https://www.stepstone.de/jobs/{company}"
# templ.Url(base.format(company = mappings_comp[company]))\
#             .param("fu", 1000000)\
#             .param("ct", 229)



#     __general_url = "https://de.indeed.com/jobs"
#         return str(templ.Url(self.__general_url).param("q", search_tag))



#     __general_search_url = "https://www.arbeitsagentur.de/jobsuche/suche"
#         #str(company) +  + " Werkstudent")
#         url = templ.Url(self.__general_search_url.format())\
#             .param("was", str(company))\
#             .param("angebotsart", 34)\
#             .param("berufsfeld", "Informatik")



from job_scraper.core.base_scraper import BaseScraper
from abc import abstractmethod, ABC
from typing import override




#TODO: add verification?
class JobSearchScraper(BaseScraper, ABC):
  
    def __init__(self, inputs=[], *args, **kwargs):
        super().__init__(
            name=self.name,
            inputs=inputs, 
            extractors= [ self.url_extractor ],
            *args,
            **kwargs
        )


    @override
    def parse(self, response):
        yield from super().parse(response)
        
        if (next := self.nextractor(response)) != None:
            yield response.follow(next, callback=self.parse, meta={"source": response.meta.get("source")})



    #interface requirements

    @classmethod
    @abstractmethod
    def url_extractor(cls, response) -> [dict]:
        pass

    # may just implement as extractor?
    @classmethod
    @abstractmethod
    def nextractor(cls, response) -> str:
        pass








class JobInfoScraper(BaseScraper, ABC):
    
    def __init__(self, inputs=[], *args, **kwargs):
        super().__init__(
            name=self.name,
            inputs=inputs, 
            extractors= [ self.jobinfo_extractor ],
            *args,
            **kwargs
        )


    #interface

    @classmethod
    def jobinfo_extractor(cls, response) -> list[dict]:
        return [{
            "title": cls.extract_jobtitle(response),
            "content": cls.extract_content(response), 
            "company": cls.extract_company(response),
            "field" : cls.extract_field(response),
            "industry" : cls.extract_industry(response),
            "employment": cls.extract_employment(response),
            "location" : cls.extract_location(response),
            "posted": cls.extract_posting(response)
        }]

    
    

    # Interface Requirements

    @abstractmethod
    def extract_jobtitle(cls, selector) -> str:
        pass

    @abstractmethod
    def extract_content(cls, selector) -> str:
        pass

    @abstractmethod
    def extract_company(cls, selector) -> str:
        pass

    @abstractmethod
    def extract_field(cls, selector) -> str:
        pass

    @abstractmethod
    def extract_industry(cls, selector) -> str:
        pass

    @abstractmethod
    def extract_employment(cls, selector) -> str:
        pass

    @abstractmethod
    def extract_location(cls, selector) -> str:
        pass

    @abstractmethod
    def extract_posting(cls, selector) -> str:
        pass