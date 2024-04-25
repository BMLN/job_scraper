#import job_scraper
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

from argparse import ArgumentParser
import os
from csv import DictReader

from job_scraper.spiders import stepstone, indeed, getinit


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

            

def output_feeds(output_locations, outputs_classes):
    output = {}
    locations = output_locations if isinstance(output_locations, list) else [ output_locations ]

    for output_location, output_classes in zip(locations, outputs_classes):
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
        out = [ x[field] for x in data ][:2]

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

#jank af
#works tho
def exec_args(__args):
    print("exec:", __args)
    output = { arg : None for arg in __args.keys() }

    for key, value in __args.items():
        if isinstance(value, tuple) == False:
            output[key] = value
        else:
            processed = value[0](**value[1])
            print(processed)
            output[key] = processed
    print("npnp")
    print(output)

    return output


#DEPR:
@defer.inlineCallbacks
def crawl(processes):
    for x in processes:
        yield x.crawl()


def sequentially(process, spiders, settings, args):
    spider = __spiders[spiders[0]]["spider"]
    spider_settings = settings[0]
    spider_args = args[0]
    
    new_settings = get_project_settings()
    if spider_settings != None:
        for key, value in spider_settings.items():
            new_settings.set(key, value)   
    #also need to overwrite everything set before
    for key, value in new_settings.items():
        process.settings.set(key, value)


    spider_args = exec_args(spider_args)

    #print(new_settings.get("FEEDS").attributes)

    deferred = process.crawl(spider, **spider_args)
    if len(spiders) > 1:
        deferred.addCallback(lambda _ : sequentially(process, spiders[1:], settings[1:], args[1:]))



__spiders = {
    "stepstone_jobsearch_spider" : {
        "spider" : stepstone.Stepstone_JobSearch_Scraper,
        "settings" : None,
        "params" : {"companies" : DEFAULT_COMPANIES}
    },
    "stepstone_jobinfo_spider" : {
        "spider" : stepstone.Stepstone_JobInfo_Scraper,
        "settings" : None,
        "params": {"jobs": (read_field, {"path": "./output/stepstone_jobs.csv" , "field":"joburl"})}
    },
    "indeed_jobsearch_spider" : {
        "spider" : indeed.Indeed_JobSearch_Scraper,
        "settings" : None,
        "params" : {"companies" : DEFAULT_COMPANIES}
    },
    "indeed_jobinfo_spider" : {
        "spider" : indeed.Indeed_JobInfo_Scraper,
        "settings" : None,
        "params": {"jobs": (read_field, {"path": "./output/indeed_jobs.csv" , "field":"joburl"})}
    },
    "getinit_jobsearch_spider" : {
        "spider" : getinit.GetInIT_JobSearch_Scraper,
        "settings" : None,
        "params" : {"companies" : DEFAULT_COMPANIES}
    },
    "getinit_jobinfo_spider" : {
        "spider" : getinit.GetInIT_JobInfo_Scraper,
        "settings" : None,
        "params": {"jobs": (read_field, {"path": "./output/getinit_jobs.csv" , "field":"joburl"})}
    },
}

__out_keys = {
    "stepstone_jobsearch_spider" : "stepstone_urls_out",
    "stepstone_jobinfo_spider" : "stepstone_info_out",
    "indeed_jobsearch_spider" : "indeed_urls_out",
    "indeed_jobinfo_spider" : "indeed_info_out",
    "getinit_jobsearch_spider" : "getinit_urls_out",
    "getinit_jobinfo_spider" : "getinit_info_out"
}



if __name__ == "__main__":
    arg_parser = ArgumentParser(description="scrapes jobinformation from different websites")

    arg_parser.add_argument("--companies", nargs="+", help="list of search", default=DEFAULT_COMPANIES)#[:2])
    arg_parser.add_argument("--settings", type=str, help="path of settings.py", default=None)
    arg_parser.add_argument("--force", action="store_true", help="flag to force crawling even if a file already exists", default=False)

    #TODO:--stepstone flag
    arg_parser.add_argument("--stepstone", action="append_const", const=["stepstone", 1], dest="crawlers", help="flag to crawl stepstone")
    arg_parser.add_argument("--stepstone_urls", action="append_const", const="stepstone_jobsearch_spider", dest="crawlers", help="flag to crawl the stepstone search")
    arg_parser.add_argument("--stepstone_info", action="append_const", const="stepstone_jobinfo_spider", dest="crawlers", help="flag to crawl stepstone jobs for their information")

    arg_parser.add_argument("--stepstone_urls_out", nargs="+", help="provides stepstone jobs", default=["./output/stepstone_jobs.csv", "./output/stepstone_err.csv"])
    arg_parser.add_argument("--stepstone_info_out", type=str, help="path of settings.py", default="./output/stepstone_info.csv")


    arg_parser.add_argument("--indeed_urls", action="append_const", const="indeed_jobsearch_spider", dest="crawlers", help="flag to crawl the indeed search")
    arg_parser.add_argument("--indeed_info", action="append_const", const="indeed_jobinfo_spider", dest="crawlers", help="flag to crawl indeed jobs for their information")

    arg_parser.add_argument("--indeed_urls_out", nargs="+", help="provides indeed jobs", default=["./output/indeed_jobs.csv", "./output/indeed_err.csv"])
    arg_parser.add_argument("--indeed_info_out", type=str, help="path of settings.py", default="./output/indeed_info.csv")


    arg_parser.add_argument("--getinit_urls", action="append_const", const="getinit_jobsearch_spider", dest="crawlers", help="flag to crawl the stepstone search")
    arg_parser.add_argument("--getinit_info", action="append_const", const="getinit_jobinfo_spider", dest="crawlers", help="flag to crawl stepstone jobs for their information")

    arg_parser.add_argument("--getinit_urls_out", nargs="+", help="provides getinit jobs", default=["./output/getinit_jobs.csv", "./output/getinit_err.csv"])
    arg_parser.add_argument("--getinit_info_out", type=str, help="path of settings.py", default="./output/getinit_info.csv")





    # arg_parser.add_argument("--arbeitsagentur", action="append_const", const="arbeitsagentur", dest="crawlers", help="flag to crawl arbeitsagentur")
    # arg_parser.add_argument("--arbeitsagentur_joburls", nargs="+", help="provides arbeitsagentur jobs", default="./output/arbeitsagentur_jobs.csv")
    # arg_parser.add_argument("--arbeitsagentur_jobinfo", type=str, help="path of settings.py", default="./output/arbeitsagentur_jobs.csv")

    #add general joburl/jobinfo flags


    #set argument
    args = vars(arg_parser.parse_args())
    if args["settings"] != None:
        os.environ["SCRAPY_SETTINGS_MODULE"] = args["settings"]
    #settings = get_project_settings()
    print(args)



    #run
    # if args["crawlers"] != None:
    #     for x in args["crawlers"]:
    #         __joburls, __jobinfo = args[str(x + "_joburls")], args[str(x + "_jobinfo")]
    #         __spider_names = list(__spiders[x].keys())
            
    #         #jobsearch
    #         if already_exists(__joburls) == False or args["force"]:
    #             spider_name = __spider_names[0]
    #             inputlist = args["companies"]
    #             __output_files = __joburls if isinstance(__joburls, list) else [__joburls]
    #             __output_types = __spiders[x][spider_name].outputs()
    #             output_settings = output_feeds(__output_files, __output_types)

    #             settings.set("FEEDS", output_settings)
    #             crawl(spider_name, settings, inputlist)

    #         #jobinfo
    #         if already_exists(__jobinfo) == False or args["force"]:
    #             spider_name = __spider_names[1]
    #             inputlist = read_field(__joburls[0], "joburl")
    #             __output_files = __jobinfo if isinstance(__jobinfo, list) else [__jobinfo]
    #             __output_types = list(__spiders[x].values())[1].outputs()
    #             output_settings = output_feeds(__output_files, __output_types)

    #             settings.set("FEEDS", output_settings)
    #             crawl(spider_name, settings, inputlist)


    #its bad tbh
    for key, value in __out_keys.items():
        __feeds = output_feeds(args[value], __spiders[key]["spider"].outputs())
        __spiders[key]["settings"] = { "FEEDS" : output_feeds(args[value], __spiders[key]["spider"].outputs()) }




    if args["crawlers"] != None:
        c = args["crawlers"]
        c_settings = [ __spiders[x]["settings"] for x in c ]
        c_params = [ __spiders[x]["params"] for x in c ]

        #c_params [ __spiders[x]["args"] for x in c ]

        p = CrawlerProcess()
        sequentially(p, c, c_settings, c_params)
        p.start()