

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



#tags: ex. "Werkstudent IT", translate into url objects
#urls: url objects
#stringurls: full strings representing an url, translate into url objects






#no abstraction
#TODO: check settingshandling later
class BaseScraper(Spider):

    def __init__(self, name, inputs=[], extractors=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("inp", inputs)
        print("kwatg", kwargs)
        self.name = name
        self.start_urls = BaseScraper.parse_inputs(inputs)
        self.extractors = extractors



    #read inputs and return (start)urls
    #either Url or string or file or lists of eithers
    #TODO: url checking?
    def parse_inputs(input):
        output = []

        match input:
            case list():
                output += [ parse_inputs(x) for x in input ] ##wrong
            case Url():
                output.append(input)           
            case str():
                #read file
                if input.endswith(".csv") or input.endswith(".json"):
                    output += Url.from_file(input) ##wrong
                #url
                else:
                    output.append(Url.parse(input))
            case _:
                raise TypeError("unrecognized input type")

        return output


    def parse_exports(self): 
        output = []
        
        for x in self.extractors:
            if (extractor_return := signature(x).return_annotation) != Signature.empty:
                output.append({
                    "format": "csv",
                    "overwrite": "true",
                    "item_classes": extractor_return
                })
        
        return output




    #scrapy interface

    @override
    def parse(self, response):
        for extractor in self.extractors:
            for extracted_item in extractor(response):
                yield response.meta.get("source") | extracted_item
        


    #TODO: change to generator
    @override
    def start_requests(self) -> Iterable[Request]:
        outs = []
        return outs
        for url in self.start_urls:
            outs.append(Request(url=str(url), callback=self.parse, meta={"source": dict(url)}))

        return outs

