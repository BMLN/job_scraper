from argparse import ArgumentParser, Action, ArgumentTypeError
import os

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor


from job_scraper.core.base_scraper import BaseScraper
from job_scraper.spiders import new_indeed, new_stepstone

from inspect import ismethod, getmro



AVAIL_EXTRACTIONS = [
    new_indeed.Indeed_JobScraper,
    new_indeed.Indeed_InfoScraper,
    
    new_stepstone.Stepstone_JobScraper,
    new_stepstone.Stepstone_InfoScraper
]


#args_parse
def spider_texts(extractions):
    output = ""
    
    for extraction_class in extractions:
        __e = extraction_class() 
        if output:
            output += ", "
        output += str(extraction_class.name) + ": " + str([ x["item_classes"] for x in __e.parse_exports() ])
        del __e

    output = "controls scraping for one of the following options and its available outputs: " + output

    return output




#deprecated
class AppendWithDefault(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setvalue = [] if getattr(namespace, self.dest) == self.default else getattr(namespace, self.dest)
        setupdate = []
        if self.default:
            setupdate.append(self.default)
        if values:
            setupdate.append(values)
        setvalue.append(setupdate)

        setattr(namespace, self.dest, setvalue)

#deprecated
class AppendSpiderParams(Action):
    spiderparams = ["crawler", "setting_args", "args"]

    def __call__(self, parser, namespace, values, option_string=None):
        setvalues = { key : [] for key in self.spiderparams } if getattr(namespace, self.dest) == self.default else getattr(namespace, self.dest)
        
        input_values = [ self.default ] + values
        input_values = dict(zip(self.spiderparams, input_values))
        for key, value in input_values.items():
            setvalues[key].append(value)
        
    
        setattr(namespace, self.dest, setvalues)


#may simply just impl set/get_attr for dict access/casting, so no additional logic required for add_crawl
class KeyPair(object):
    def __init__(self, keypairstr):
        try:
            key, value = keypairstr.split("=")
            self.key = key
            self.value = value
        except:
            raise ArgumentTypeError(keypairstr + " isn't a valid Key=Value pair")

    def __repr__(self):
        return self.key + "=" + self.value

    def to_dict(keypairs):
        return { x.key : x.value for x in keypairs}


def parser_addspider(parser, spider_cls):
    
    __spider = spider_cls()
    parser.add_argument(
        "--" + spider_cls.name, 
        action="append_const", 
        dest="crawlers", 
        const=spider_cls, 
        default=[], 
        help= "outputs: " + str([ x["item_classes"] for x in __spider.parse_exports() ])
    )
    del __spider

    






#crawling
def sequentially(process, spiders, spider_args, setting_args, outputs):
    
    if spiders and spider_args and setting_args and outputs:
        
        spider = spiders.pop()
        sp_args = spider_args.pop()
        st_args = setting_args.pop()
        o_args = outputs.pop()

        deferred = add_crawl(process, spider, sp_args, st_args, o_args)
        deferred.addCallback(lambda _ : sequentially(process, spiders, spider_args, setting_args, outputs))


def add_crawl(process, spider, spider_args, setting_args, outputs):
    
    #add spider to process
    #may require present files? -> check if additional io necessary
    deferred = process.crawl(spider, **KeyPair.to_dict(spider_args))


    #update settings accordingly 
    #for extra passed --s(ettings)
    for key, value in KeyPair.to_dict(setting_args).items():
        process.settings.set(key, value)

    #and the --outputs designations
    for crawler in process.crawlers: #should always be one, since sequential
        for key, value in zip(outputs, crawler.spider.parse_exports()):
            process.settings.get("FEEDS").set(key, value)

    
    return deferred








if __name__ == "__main__":
    
    #run spiders via input, outputs
    arg_parser = ArgumentParser(description="controls scraping for the following options and their available outputs: ")
    arg_parser.add_spider = parser_addspider

    #program args
    arg_parser.add_argument("--settings", type=str, help="path of settings.py", default=None)
    arg_parser.add_argument("--spider_outputs")
    
    #crawler args
    for x in AVAIL_EXTRACTIONS: arg_parser.add_spider(arg_parser, x) #parser_addspider(arg_parser, x)

    arg_parser.add_argument("--outputs", type=str, nargs="*", action="append", default=[], help=str())
    arg_parser.add_argument("--s", type=KeyPair, nargs="*", action="append", default=[]) 
    arg_parser.add_argument("--a", type=KeyPair, nargs="*", action="append", default=[])

    
    #set args
    args = vars(arg_parser.parse_args())
    if args["settings"]:
        os.environ["SCRAPY_SETTINGS_MODULE"] = args["settings"]
    #print(args)





    #run
    spiders = args["crawlers"]
    spider_args = args["a"]
    setting_args = args["s"]
    outputs = args["outputs"]

    if not (len(spiders) == len(spider_args) == len(setting_args) == len(outputs)):
        exit('please provide each type of scraper with "a", "s" and "outputs" arguments! (they may be empty)')
   

    process = CrawlerProcess(settings=get_project_settings())
    sequentially(process, spiders, spider_args, setting_args, outputs)
    process.start()

