

# output input functionality



# extend scrapy.spider:

# input: 3x[]: tags, urls, stringurls -> into one
# input: each either in form of file or list or singleton? check that

# output: [[ dict or whatever ]]



from typing import Iterable, override

from scrapy import Spider
from scrapy.http import Request

from url import Url

from itertools import chain

#tags: ex. "Werkstudent IT", translate into url objects
#urls: url objects
#stringurls: full strings representing an url, translate into url objects






#no abstraction
#TODO: check settingshandling later
class BaseScraper(Spider):

    def __init__(self, name, inputs=[], extractors=[], *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.name = name
        self.start_urls = list(chain(*BaseScraper.parse_inputs(inputs)))
        self.extractors = extractors

        #self.custom_settings = {"KEY": "VALUE"}
        from scrapy.utils.project import get_project_settings

        self.settings = get_project_settings()
        self.settings.set("KEY", "VALUE")


    #read inputs and return (start)urls
    #either Url or string or file or lists of eithers
    #TODO: url checking?
    def parse_inputs(input):
        output = []

        match input:
            case list():
                output += [ BaseScraper.parse_inputs(x) for x in input ]
            case Url():
                output.append(input)           
            case str():
                #read file
                if input.endswith(".csv") or input.endswith(".json"):
                    output += Url.from_file(input)
                #url
                else:
                    output.append(Url.parse(input))
            case _:
                raise TypeError("unrecognized input type")

        return output


    def parse(self, response):
        for extractor in self.extractors:
            for extracted_item in extractor(response):
                yield response.meta.get("source") | extracted_item
        

    #TODO
    #rename to outputs or something
    def extractor_types(self):
        return self.extractors
    

    #TODO: change to generator
    @override
    def start_requests(self) -> Iterable[Request]:
        outs = []
        for url in self.start_urls:
            outs.append(Request(url=str(url), meta={"source": dict(url)}, callback=self.parse))

        #print(outs)
        return outs








    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        #print(settings.attributes.items())

    # def output_feeds(self):
    #     output = {}
        
    #     for key, value in self.writes.items():
    #         output[key] = {
    #         "format": "csv",
    #         "overwrite": "true",
    #         "item_classes": value
    #     }





if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess()

    process.crawl(BaseScraper, name="", inputs=["www.google.de"])
    process.start() 