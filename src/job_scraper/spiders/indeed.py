import scrapy
from job_scraper.spiders import templ
import os

from scrapy.utils.project import get_project_settings


class Indeed_CompanyKey_Scraper(templ.Key_Scraper):
    name = "indeed_companykey_spider"
    allowed_domains = ["de.indeed.com"]
    start_urls = []
    print(get_project_settings())
    # custom_settings = get_p{
    #     "SELENIUM_DRIVER_NAME" = "safari",
    #     "DOWNLOADER_MIDDLEWARES" = {
    #         "scrapy_selenium.SeleniumMiddleware": 800
    #     }
    # }
        


    # interface requirements
    
    @override
    def extract_key(self, selector):
        return {"ey":"lmao"}