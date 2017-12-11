# This is a piece of code that use webdrivers to load&render a page with Scrapy and Selenium.
# 
# This work is based on the snippets [wynbennett](http://snippets.scrapy.org/users/wynbennett/) [posted here](http://snippets.scrapy.org/snippets/21/) some time ago
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
##from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
##from CrawltstItem.items import myItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

 
import time
import pprint

class myItem(scrapy.Item):
    item = scrapy.Field()

class WebDriverSpider(CrawlSpider):
    name = "crawltst"
    start_urls = ["https://www.amazon.com/"]
 
    rules = (
        Rule(LinkExtractor(allow=('\.html', ), allow_domains=('amazon.com', )), callback='parse_page',follow=False),
        )
 
    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        #create a profile with specific add-ons
        #and do this. Firefox to load it
##        profile = FirefoxProfile(profile_directory="/home/yourUser/.mozilla/firefox/selenium/")
##        self.selenium = webdriver.Firefox(profile)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--ignore-certificate-errors')

        self.selenium = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"C:/Users/home/chromedriver.exe")#webdriver.Firefox()
        self.selenium.get("http://www.python.org")
        assert "Python" in self.selenium.title
        elem = self.selenium.find_element_by_name("q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in self.selenium.page_source
##        .close()

    def __del__(self):
        self.selenium.quit()
        print (self.verificationErrors)
        CrawlSpider.__del__(self)
 
    def parse_page(self, response):
        #normal scrapy result
        hxs = HtmlXPathSelector(response)
        #webdriver rendered page
        sel = self.selenium
        sel.get(response.url)
 
        if sel:
            #Wait for javascript to load in Selenium                                                                                       
            time.sleep(2.5)
 
        #Do some crawling of javascript created content with Selenium                                                                      
        item = myItem()
        item['url'] = response.url
        item['title'] = hxs.select('//title/text()').extract()
 
 
        #something u can do only with webdrivers
        item['thatDiv'] = sel.find_element_by_id("thatDiv")
 
# Snippet imported from snippets.scrapy.org (which no longer works)
# author: rollsappletree
# date  : Aug 25, 2011
 
