#import job_scraper
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

from argparse import ArgumentParser
import os
from csv import DictReader

from job_scraper.spiders import stepstone


DEFAULT_SETTINGS = None
DEFAULT_CRAWLERS = ["stepstone"]
DEFAULT_COMPANIES = [
            "Adidas", 
            "Airbus", 
            "Allianz", 
            "BASF", 
            "Bayer", 
            "Beiersdorf", 
            "BMW", 
            "Brenntag",
            "Commerzbank", 
            "Continental", 
            "Covestro",
            "Daimler Truck",
            "Deutsche Bank",
            "Deutsche Börse",
            "Deutsche Post",
            "Deutsche Telekom",
            "E.ON",
            "Fresenius",
            "Hannover Rück",
            "Heidelberg Materials",
            "Henkel",
            "Infineon",
            "Mercedes-Benz Group",
            "Merck",
            "MTU Aero Engines",
            "Münchner Rück",
            "Porsche AG",
            "Porsche SE",
            "Qiagen",
            "Rheinmetall",
            "RWE",
            "SAP",
            "Sartorius",
            "Siemens",
            "Siemens Energy",
            "Siemens Healthineers",
            "Symrise",
            "Volkswagen",
            "Vonovia",
            "Zalando"]
urls = False 

d = ["mercedes benz", "adidas ag"]

__spiders = {
    "stepstone": {
            "stepstone_jobsearch_spider" : stepstone.Stepstone_JobSearch_Scraper,
            "stepstone_jobinfo_spider" : stepstone.Stepstone_JobInfo_Scraper
    },
    "arbeitsagentur": {
    }
}


def output_feeds(output_locations, outputs_classes):
    output = {}

    for output_location, output_classes in zip(output_locations, outputs_classes):
        output[output_location] = {
            "format": "csv",
            "overwrite": "true",
            "item_classes": output_classes
        }

    return output
    #return { str("./output/" + str(type)) : __feeds }


def crawl(spider_name, settings, input_list):
    process = CrawlerProcess(
        settings = settings
    )
    process.crawl(spider_name, input_list) #["file:///Users/lorandbanki/Desktop/Arbeit/job_scraper/jobsite.html"])
    process.start()


def crawl1(settings):
    return CrawlerRunner(settings)

def read_field(path, field):
    out = None
    with open(path, "r") as file:
        data = DictReader(file)
        out = [ x[field] for x in data ]

    return out

def already_exists(file_or_files):
    if isinstance(file_or_files, str):
        return os.path.exists(file_or_files) 
    elif isinstance(file_or_files, list):
        output = False
        for x in file_or_files:
            if os.path.exists(x):
                output = True
                break
        return output 
    else:
        raise TypeError


@defer.inlineCallbacks
def crawl(processes):
    for x in processes:
        yield x.crawl()






if __name__ == "__main__":
    arg_parser = ArgumentParser(description="scrapes jobinformation from different websites")

    arg_parser.add_argument("--companies", nargs="+", help="list of search", default=DEFAULT_COMPANIES)#[:2])
    arg_parser.add_argument("--settings", type=str, help="path of settings.py", default=None)
    arg_parser.add_argument("--force", action="store_true", help="flag to force crawling even if a file already exists", default=False)


    arg_parser.add_argument("--stepstone", action="append_const", const="stepstone", dest="crawlers", help="flag to crawl stepstone")
    arg_parser.add_argument("--stepstone_joburls", nargs="+", help="provides stepstone jobs", default=["./output/stepstone_jobs.csv", "./output/stepstone_err.csv"])
    arg_parser.add_argument("--stepstone_jobinfo", type=str, help="path of settings.py", default="./output/stepstone_jobs.csv")

    arg_parser.add_argument("--arbeitsagentur", action="append_const", const="arbeitsagentur", dest="crawlers", help="flag to crawl arbeitsagentur")
    arg_parser.add_argument("--arbeitsagentur_joburls", nargs="+", help="provides arbeitsagentur jobs", default="./output/arbeitsagentur_jobs.csv")
    arg_parser.add_argument("--arbeitsagentur_jobinfo", type=str, help="path of settings.py", default="./output/arbeitsagentur_jobs.csv")

    


    #set argument
    args = vars(arg_parser.parse_args())
    if args["settings"] != None:
        os.environ["SCRAPY_SETTINGS_MODULE"] = args["settings"]
    settings = get_project_settings()



    #run
    if args["crawlers"] != None:
        for x in args["crawlers"]:
            __joburls, __jobinfo = args[str(x + "_joburls")], args[str(x + "_jobinfo")]
            __spider_names = list(__spiders[x].keys())
            
            #jobsearch
            if already_exists(__joburls) == False or args["force"]:
                spider_name = __spider_names[0]
                inputlist = args["companies"]
                __output_files = __joburls if isinstance(__joburls, list) else [__joburls]
                __output_types = __spiders[x][spider_name].outputs()
                output_settings = output_feeds(__output_files, __output_types)

                settings.set("FEEDS", output_settings)
                crawl(spider_name, settings, inputlist)

            #jobinfo
            if already_exists(__jobinfo) == False or args["force"]:
                spider_name = __spider_names[1]
                inputlist = read_field(__joburls[0], "joburl")
                __output_files = __jobinfo if isinstance(__jobinfo, list) else [__jobinfo]
                __output_types = list(__spiders[x].values())[1].outputs()
                output_settings = output_feeds(__output_files, __output_types)

                settings.set("FEEDS", output_settings)
                crawl(spider_name, settings, inputlist)