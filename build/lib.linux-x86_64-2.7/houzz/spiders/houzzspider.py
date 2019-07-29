# -*- coding: utf-8 -*-
import scrapy
import proxylist
import logging
import useragent
from scrapy.http import Request, FormRequest
import time, re, random, base64
import logging
from houzz.items import HouzzItem
from time import sleep
import csv
import os
import json
import os.path
from io import StringIO
from datetime import datetime
from datetime import date
import sys
from scrapy.exceptions import CloseSpider
import urls

url_csv_file = "url1.csv"
us_city_csv_file = "us_city.csv"
email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', re.IGNORECASE)
sub_url_list = []

class HouzzspiderSpider(scrapy.Spider):
    name = "houzzspider"
    #allowed_domains = ["houzz.co.uk"]

    parent_url = 'https://www.houzz.co.uk/professionals/interior-designers/s/Interior-Designers/c/'

    country_url = 'https://www.countries-ofthe-world.com/all-countries.html'

    us_city_url = 'https://www.craigslist.org/about/sites#US'
    
    us_cities = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'Territories']

    # proxy list
    proxy_lists = proxylist.proxys
    proxy_lists1 = proxylist.proxys1
    proxy_lists2 = proxylist.proxys2
    proxy_lists3 = proxylist.proxys3

    useragent_lists = useragent.user_agent_list
    total_cnt = 0
    image_cnt = 0
    found_count = 0
    index = 0
    exists_count = 0

    start_urls = urls.start_urls

    def set_proxies(self, url, callback):
        req = Request(url=url, callback=callback,dont_filter=True)
        self.index = random.randrange(0, 10)

        # if int(self.index) % 3 == 0:
        #     proxy_url = self.proxy_lists[random.randrange(0,len(self.proxy_lists))]
        #     user_pass=base64.encodestring(b'silicons:1pRnQcg87F').strip().decode('utf-8')
        # elif int(self.index) % 3 == 1:
        #     proxy_url = self.proxy_lists1[random.randrange(0,len(self.proxy_lists1))]
        #     user_pass=base64.encodestring(b'user:p19gh1a').strip().decode('utf-8')
        # elif int(self.index) % 3 == 2:
        #     proxy_url = self.proxy_lists3[random.randrange(0,len(self.proxy_lists3))]
        #     user_pass=base64.encodestring(b'erwin05dec1998:APg28fvK').strip().decode('utf-8')

        # req.meta['proxy'] = "http://" + proxy_url
        # req.headers['Proxy-Authorization'] = 'Basic ' + user_pass

        # user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        # req.headers['User-Agent'] = user_agent
        
        return req

    def __init__(self,  category =0, *args, **kwargs):
        super(HouzzspiderSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        # req = self.set_proxies("https://www.houzz.co.uk/pro/black-and-milk-residential/black-and-milk-interior-design-london", self.parse_detail)
        # yield req
        # return

        # req = self.set_proxies("http://www.kiadesigns.co.uk/", self.parse_website_url)
        # item = HouzzItem()
        # req.meta["item"] = item
        # yield req
        # return

        # req = self.set_proxies("https://www.houzz.co.uk/professionals/interior-designers/c/Moldova/d/100/p/30", self.parse_content)
        # item = HouzzItem()
        # req.meta["first"] = True
        # yield req
        # return

        if int(self.category) == 0 or self.category == "":
            raise CloseSpider("Index is not valid.")

        if int(self.category) > 7:
            raise CloseSpider("Index must be not high.")

        index = int(self.category)
        url_list = []
        i = (index - 1) * 200
        last_index = index * 200
        
        if last_index > len(self.start_urls):
            last_index = len(self.start_urls)

        while (i < last_index):
            url_list.append(self.start_urls[i])
            i +=  1
        
        #for url in self.start_urls:
        for url in url_list:
            url = url + "/d/100"
            req = self.set_proxies(url, self.parse_content)
            req.meta["first"]  = True
            yield req
    
    # def parse_country_url(self, response):
    #     with open(url_csv_file, 'w') as csvfile:
    #         csv_writer = csv.writer(csvfile)
            
    #     content = response.xpath("//div[@class='container list-container']/div/ul/li[not(contains(@class, 'letter'))]")
    #     for row in content:
    #         country = row.xpath(".//text()").extract()
    #         country =  "".join(country)

    #         req = self.set_proxies(self.parent_url + country, self.parse_parent_url)
    #         req.meta["param"] = country
    #         req.meta["type"] = "country"
    #         yield req
    
    # def parse_us_city_url(self, response):
    #     with open(us_city_csv_file, 'w') as csvfile:
    #         csv_writer = csv.writer(csvfile)
        
    #     for city in self.us_cities:
    #         req = self.set_proxies(self.parent_url + city, self.parse_parent_url)
    #         req.meta["param"] = city
    #         req.meta["type"] = "us_city"
    #         yield req

    def parse_content(self, response):
        count = response.xpath("//h1[@class='header-2 header-dt-1 main-title']/text()").extract_first()
        count = int(re.sub("[^\d-]+", "", count))

        if response.meta["first"] == True:
            self.total_cnt += count
            print "Total:", self.total_cnt
        
        script_element = response.xpath("//div[contains(@class, 'whiteCard pro-card')]")
        
        if len(script_element) > 0:
            self.found_count += len(script_element)

            for row in script_element:
                item = HouzzItem()
                item["url"] = response.url
                try:
                    item["sub_url"] = row.xpath(".//a[@class='pro-title']/@href").extract_first()
                    exists = 0
                    for sub_item in sub_url_list:
                        if item["sub_url"] == sub_item:
                            exists = 1
                    
                    if exists == 1:
                        self.exists_count += 1
                        continue
                    else:
                        sub_url_list.append(item["sub_url"])

                    item["phone"] = row.xpath(".//span[@class='pro-list-item--text']/text()").extract_first()
                    
                    addressLocality = row.xpath(".//li[@class='pro-list-item pro-location']//span[@itemprop='addressLocality']/text()").extract_first()
                    if addressLocality == None:
                        addressLocality = ""

                    addressRegion = row.xpath(".//li[@class='pro-list-item pro-location']//span[@itemprop='addressRegion']/text()").extract_first()
                    if addressRegion == None:
                        addressRegion = ""

                    postalCode = row.xpath(".//li[@class='pro-list-item pro-location']//span[@itemprop='postalCode']/text()").extract_first()
                    if postalCode == None:
                        postalCode = ""

                    addressCountry = row.xpath(".//li[@class='pro-list-item pro-location']//span[@itemprop='addressCountry']/text()").extract_first()
                    if addressCountry == None:
                        addressCountry = ""

                    item["location"] = addressLocality.encode("utf-8") + " " + addressRegion.encode("utf-8") + " " + postalCode.encode("utf-8") + " " + addressCountry.encode("utf-8")

                    item["name"] = row.xpath(".//a[@class='pro-title']/text()").extract_first().encode("utf-8")
                    req = self.set_proxies(item["sub_url"], self.parse_detail)
                    req.meta["item"] = item
                    yield req
                except:
                    print "Parsing Error ->". response.url

        else:
            print "Not Found ->", response.url
        
        next_link = response.xpath("//a[@class='navigation-button next']")
        if len(next_link) > 0:
            url = next_link.xpath("@href").extract_first()
            req = self.set_proxies(url, self.parse_content)
            req.meta["first"] = False
            yield req
        else:
            print "Not Found Next Page ->", response.url
            print "Total Items:", self.total_cnt, "Found Items:", self.found_count ,"Exists Count:", self.exists_count
    
    def parse_detail(self, response):
        item = response.meta["item"]
        #item["review_count"] = response.xpath("//span[@itemprop='reviewCount']/text()").extract_first()
        item["website_url"] = response.xpath("//a[@class='proWebsiteLink']/@href").extract_first()
        try:
            item["contact"] = response.xpath("//div[@class='info-list-text']/b[contains(text(), 'Contact')]/../text()").extract_first().replace(": ","")
        except:
            item["contact"] = ""

        #item["desc"] = " ".join(response.xpath("//div[@class='profile-content-wide about-section']/div[contains(@class, 'profile-about')]//text()").extract())
        #item["professional_info"] = " ".join(response.xpath("//div[@class='professional-info-content']//text()").extract())
        #item["typical_job_cost"] = " ".join(response.xpath("//div[@class='info-list-text']/b[contains(text(), 'Typical Job Costs')]/..//text()").extract())
        yield item
        # return
        # #item["email"] = []

        # if item["website_url"] == None:
        #     yield item
        # else:
        #     try:
        #         req = self.set_proxies(item["website_url"], self.parse_website_url)
        #         req.meta["item"] = item
        #         yield req
        #     except:
        #         print "*****************************"
        #         print item
        #         return

    def parse_website_url(self, response):
        item = response.meta["item"]
        
        urls=[]
        for email in email_regex.findall(response.body):
    		item["email"].append(email)
        
        href_links = response.xpath("//a")
        for href in href_links:
            url_text = href.xpath("text()").extract_first()
            if url_text != None:
                url_text = url_text.strip().lower()
                if 'contact'  in url_text or 'about' in url_text:
                    urls.append(response.urljoin(href.xpath("@href").extract_first()))
        
        call_urls = []
        for url in urls:
            exists = 0
            for row in call_urls:
                if url == row:
                    exists = 1
            if exists == 0:
                call_urls.append(url)
        
        for url in call_urls:
            req = self.set_proxies(url, self.parse_email)
            req.meta["item"] = item
            yield req

    def parse_email(self, response):
        item = response.meta["item"]
        try:
            for email in email_regex.findall(response.body):
                #print email
                item["email"].append(email)
        except:
            print "**************************"
            print item
        
        emails = []
        
        for email in item["email"]:
            exists = 0
            for row in emails:
                if email == row:
                    exists = 1
            
            if exists == 0:
                if ".jpg" in email or ".jpeg" in email or ".png" in email or ".bmp" in email or ".doc" in email or ".txt" in email or ".xls" in email:
                    error = 0
                else:
                    emails.append(email)
        
        item["email"] = emails
        yield item