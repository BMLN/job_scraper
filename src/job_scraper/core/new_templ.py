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



import base_spiders
from abc import abstractmethod, ABC
from typing import override




#TODO: add verification?
class JobSearchScraper(base_spiders.BaseScraper, ABC):
    
    def __init__(self, inputs, *args, **kwargs):
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
            yield response.follow(next, self.parse)



    #interface requirements

    @classmethod
    @abstractmethod
    def url_extractor(cls) -> list[dict]:
        pass

    # may just implement as extractor?
    @classmethod
    @abstractmethod
    def nextractor(cls) -> str:
        pass








class JobInfoScraper(base_spiders.BaseScraper, ABC):
    
    def __init__(self, inputs, *args, **kwargs):
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
            "Name": cls.extract_company(response),
            "Jobbezeichnung": cls.extract_jobtitle(response),
            #"Tätigkeitsbereich": None,
            #"Aufgaben": self.extract_tasks(response),
            #"Qualifikationen": self.extract_qualifications(response),
            #"etc": self.extract_etc(response),
            "Standort": cls.extract_location(response),
            "Anstellungsart": cls.extract_employment(response),
            "job_node" : cls.extract_jobnode(response)
            #"raw_text": self.extract_rawtext(response)
        }]

    
    

    # Interface Requirements

    @abstractmethod
    def extract_jobtitle(self, selector) -> str:
        pass

    @abstractmethod
    def extract_company(self, selector) -> str:
        pass

    @abstractmethod
    def extract_location(self, selector) -> str:
        pass

    @abstractmethod
    def extract_employment(self, selector) -> str:
        pass

    @abstractmethod
    def extract_jobnode(self, selector) -> str:
        pass
