from scrapy.utils.project import get_project_settings
from job_scraper.spiders import indeed


from scrapy.crawler import CrawlerProcess, CrawlerRunner
import pandas as pd



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

settings = get_project_settings()




#indeed

#joburl

# __feeds = {"./output/indeed_joburls.csv" : {
#             "format": "csv",
#             "overwrite": "true",
#             "item_classes": [dict]
#         }
#     }      
# settings.set("FEEDS", __feeds)


# process = CrawlerProcess(
#     settings = settings
#     )
# process.crawl("indeed_jobsearch_spider", [ key for key, value in indeed.mappings_comp.items() if value != None])
# process.start()


# exit()





# jobinfo

urls = pd.read_csv("./output/indeed_joburls.csv")
urls = urls["joburl"].to_list()

__feeds = {"./output/indeed_info.csv" : {
            "format": "csv",
            "overwrite": "true",
            "item_classes": [dict]
        }
    }      
settings.set("FEEDS", __feeds)


process = CrawlerProcess(
    settings = settings
    )
process.crawl("indeed_jobinfo_spider", urls)
process.start()















# __feeds = {"./output/arbeitsagentur_joburls.csv" : {
#             "format": "csv",
#             "overwrite": "true",
#             "item_classes": [dict]
#         }
#     }      
# settings.set("FEEDS", __feeds)


# process = CrawlerProcess(
#     settings = settings
#     )
# process.crawl("arbeitsagentur_jobsearch_spider", DEFAULT_COMPANIES)
# process.start()


# exit()




# # jobinfo

# urls = pd.read_csv("./output/arbeitsagentur_joburls.csv")
# urls = urls["joburl"].to_list()

# __feeds = {"./output/arbeitsagentur_info.csv" : {
#             "format": "csv",
#             "overwrite": "true",
#             "item_classes": [dict]
#         }
#     }      
# settings.set("FEEDS", __feeds)


# process = CrawlerProcess(
#     settings = settings
#     )
# process.crawl("arbeitsagentur_jobinfo_spider", urls)
# process.start()





# get-in-it
# #joburls
# from job_scraper.spiders import getinit

# __feeds = {"./output/get-in-it_joburls.csv" : {
#             "format": "csv",
#             "overwrite": "true",
#             "item_classes": [dict]
#         }
#     }      
# settings.set("FEEDS", __feeds)


# process = CrawlerProcess(
#     settings = settings
# )
# process.crawl("getinit_jobsearch_spider", [ value for key, value in getinit.DEFAULT_MAPPINGS.items() if value != None ])
# process.start()


# exit()




# # jobinfo

# urls = pd.read_csv("./output/get-in-it_joburls.csv")
# urls = urls["joburl"].to_list()

# __feeds = {"./output/get-in-it_info.csv" : {
#             "format": "csv",
#             "overwrite": "true",
#             "item_classes": [dict]
#         }
#     }      
# settings.set("FEEDS", __feeds)


# process = CrawlerProcess(
#     settings = settings
#     )
# process.crawl("getinit_jobinfo_spider", urls)
# process.start()