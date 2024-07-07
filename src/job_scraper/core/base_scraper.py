

# output input functionality



# extend scrapy.spider:

# input: 3x[]: tags, urls, stringurls -> into one
# input: each either in form of file or list or singleton? check that

# output: [[ dict or whatever ]]



from typing import Iterable, override
from inspect import signature, Signature

from scrapy import Spider
from scrapy.http import Request

from job_scraper.core.url import Url
from datetime import date


#tags: ex. "Werkstudent IT", translate into url objects
#urls: url objects
#stringurls: full strings representing an url, translate into url objects






#no abstraction
#TODO: check settingshandling later
class BaseScraper(Spider):

    def __init__(self, name, inputs=[], extractors=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.start_urls = BaseScraper.parse_inputs(inputs)
        self.extractors = extractors



    #read inputs and return (start)urls
    #either Url or string or file or lists of eithers
    #TODO: url checking?
    def parse_inputs(inp):
        output = []

        match inp:
            case list():
                output += [ parse_inputs(x) for x in inp ] ##wrong
            case Url():
                output.append(inp)           
            case str():
                #read file
                if inp.endswith(".csv") or inp.endswith(".json"):
                    output += Url.from_file(inp) 
                #url
                else:
                    output.append(Url.parse(inp))
            case _:
                raise TypeError("unrecognized input type")

        return output


    #callable as inst method this way, good sol?
    def parse_exports(extractors) -> list[list]: 
        output = []
        
        for x in extractors if not isinstance(extractors, BaseScraper) else extractors.extractors:
            if (extractor_return := signature(x).return_annotation) != Signature.empty:
                output.append({
                    "format": "csv",
                    "overwrite": "true",
                    "item_classes": extractor_return
                })
        
        return output




    #scrapy interface

    @override #yes?
    def parse(self, response):
    #new is going to be:
    #def parse(self, response, source={})
        for extractor in self.extractors:
            for extracted_item in extractor(response):
                yield response.meta.get("source") | {"url": response.request.url} |  extracted_item | {"date": date.today()} 


    #TODO: change to generator
    @override
    def start_requests(self) -> Iterable[Request]:
        outs = []

        for url in self.start_urls:
            outs.append(Request(url=str(url), callback=self.parse, meta={"source": dict(url)}))
            #new is going to be:
            #outs.append(Request(url=str(url), callback=self.parse, cb_kwargs={"source": dict(url)}))

        return outs
