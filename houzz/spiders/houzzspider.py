# -*- coding: utf-8 -*-
import scrapy
import proxylist
import logging
import useragent
from scrapy.http import Request, FormRequest
import time, re, random, base64
import logging
from houzz.items import HouzzItem, EmailItem
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
import codecs

url_csv_file = "url1.csv"
email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', re.IGNORECASE)
sub_url_list = []

remian_csv_file = "remain.csv"
source_csv_file = "source.csv"
email_csv_file = "email.csv"
dest_csv_file = "remain_email.csv"
complete_csv_file = "data.csv"
country_csv_file = "country.csv"
us_city_csv_file = "us_city.csv"
us_region_csv_file = "us_region.csv"
russian_city_csv_file = "russian_city.csv"
india_city_csv_file = "india_city.csv"
uk_city_csv_file = "uk_city.csv"
url_city_csv = "url_city.csv"

additional_india_csv_file = "add_india.csv"

additional_india_cities=[
    "Firozabad", "Darbhanga", "Mau", "Karimnagar", "Raichur", "Bidar", "Morena", "Vellore", "Jaunpur", "Begusarai", "Murwara", "Katni", "Kharagpur"
]

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

        if int(self.index) % 2 == 0:
            proxy_url = self.proxy_lists[random.randrange(0,len(self.proxy_lists))]
            user_pass=base64.encodestring(b'silicons:1pRnQcg87F').strip().decode('utf-8')
        elif int(self.index) % 2 == 1:
            proxy_url = self.proxy_lists3[random.randrange(0,len(self.proxy_lists3))]
            user_pass=base64.encodestring(b'erwin05dec1998:APg28fvK').strip().decode('utf-8')

        req.meta['proxy'] = "http://" + proxy_url
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass

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

        # req = self.set_proxies("https://www.scalez.info/", self.parse_website_url)
        # req.meta["url"] = "https://www.scalez.info/"
        # yield req
        # return

        # req = self.set_proxies("https://www.houzz.co.uk/professionals/interior-designers/c/Moldova/d/100/p/30", self.parse_content)
        # item = HouzzItem()
        # req.meta["first"] = True
        # yield req
        # return
        if self.category == "country":
            #req = self.set_proxies("https://www.countries-ofthe-world.com/all-countries.html", self.parse_country)
            #yield req

            # req = self.set_proxies("https://www.craigslist.org/about/sites#US", self.parse_us_cities)
            # yield req

            # req = self.set_proxies("https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Russia", self.parse_russian_cities)
            # yield req

            # req = self.set_proxies("https://en.wikipedia.org/wiki/List_of_towns_in_India_by_population", self.parse_india_cities)
            # yield req

            # req = self.set_proxies("https://en.wikipedia.org/wiki/List_of_million-plus_urban_agglomerations_in_India", self.parse_india_cities)
            # yield req

            #req = self.set_proxies("https://en.wikipedia.org/wiki/India", self.parse_add_india_cities)
            #yield req
            #return

            # req = self.set_proxies("http://www.ukcities.co.uk/populations/", self.parse_uk_cities)
            # yield req
            
            req = self.set_proxies(self.parent_url, self.parse_check_url)
            yield req
            

        elif self.category == "email":
            with open(remian_csv_file) as csvfile:
                reader = csv.reader(csvfile)
                print ( "-----------------CSV Read------------------" )
                item_list = []
                for item in reader:
                        obj = {}
                        website = item[0]
                        if website != "null":
                            website = website.replace("http://", "")
                            if '@' not in website and '.' in website and 'facebook' not in website and 'google' not in website and 'twitter' not in website:
                                item_list.append("http://" + website)
                                
                self.total_cnt = len(item_list)
                
                for url in item_list:
                    req = self.set_proxies(url, self.parse_website_url)
                    req.meta["url"] = url
                    yield req

        elif self.category == "check":
            item_list = []
            print "Read Source CSV->"
            with open(source_csv_file) as csvfile:
                reader = csv.reader(csvfile)
                i = 0
                for item in reader:
                    obj = {}
                    for k in range(0, 8):
                        obj[k] = item[k]
                    item_list.append(obj)
                    
                    i+=1
            
            print "Check duplication of Source CSV->"
            real_list = []
            for i, item in enumerate(item_list):
                if i % 100 == 0:
                    print i

                exists = 0
                for item1 in real_list:
                    if item[5] == item1[5]:
                        exists += 1
                
                if exists == 0:
                    real_list.append(item)
                
            print "Export into Complete CSV->"
            with open(complete_csv_file, 'w') as csvfile:
                csv_writer = csv.writer(csvfile)
                for i, item in enumerate(real_list):
                    if i % 100 == 0:
                        print i
                    csv_writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]])
            
            return
        
        elif self.category == "write":
            ifile = open(email_csv_file, "rb")
            reader = csv.reader(ifile)
            ofile = open("write.csv", "wb")
            writer = csv.writer(ofile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_ALL)

            for row in reader:
                writer.writerow(row)

            ifile.close()
            ofile.close()

        elif self.category == "merge":
            item_list = []

            # print "Read Url City CSV->"
            # url_city_list = []
            # with open(url_city_csv) as csvfile:
            #     reader = csv.reader(csvfile)
            #     for item in reader:
            #         obj = {}
            #         obj["url"] = item[0]
            #         obj["country"] = item[1]
            #         obj["city"] = item[2]
            #         url_city_list.append(obj)
            
            print "Read Source CSV->"
            with open(complete_csv_file) as csvfile:
                reader = csv.reader(csvfile)
                i = 0
                for item in reader:
                    if i > 0:
                        obj = {}
                        obj["name"] = item[0]
                        obj["contact"] = item[1]
                        obj["format_address"] = item[2]
                        obj["locality"] = item[3]
                        obj["region"] = item[4]
                        obj["postal_code"] = item[5]
                        obj["country"] = item[6]
                        obj["phone"] = item[7]
                        obj["website_url"] = item[8]

                        obj["contact_url"] = []
                        obj["contact_urls"] = ""
                        obj["emails"] = ""
                        obj["email"] = []

                        if item[9] != "":
                            obj["contact_urls"] = item[9]

                        if item[10] != "":
                            obj["emails"] = item[10]
                        
                        obj["url"] = item[11]
                        obj["country_url"] = item[12]
                        
                        item_list.append(obj)

                    print i
                    i += 1
            
            print "Read Email CSV->"
            email_item_list = []
            with open(dest_csv_file) as csvfile:
                reader = csv.reader(csvfile)
                i = 0
                for item in reader:
                    if i > 0:
                        obj = {}
                        obj["website_url"] = item[1]
                        obj["email"] = item[2].split(",")
                        obj["contact_url"] = item[0]
                        email_item_list.append(obj)
                    i+=1
                    print i
            
            print "Export Contact to Source CSV->"
            for i, item in enumerate(item_list):
                if item["website_url"] == "":
                    continue
                print i

                for email_item in email_item_list:
                    if item["website_url"] == email_item["website_url"]:
                        for sub_emails in email_item["email"]:
                            exists = 0

                            for email in item["email"]:
                                if sub_emails == email:
                                    exists = 1

                            if exists == 0:
                                item["email"].append(sub_emails)

                                contact_exists = 0
                                for contact in item["contact_url"]:
                                    if contact == email_item["contact_url"]:
                                        contact_exists = 1

                                if contact_exists == 0:
                                    item["contact_url"].append(email_item["contact_url"])
            
            print "Export into Email CSV->"
            with open(email_csv_file, 'w') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Name", "Contact", "Full Address", "Locality","Region","Postal Code","Search Country", "Phone","Web Site", "Email", "Contact URL","Url", "Country & City URL"])
                for i, item in enumerate(item_list):
                    print i
                    email_str = ""
                    contact_str = ""
                    if item["emails"] !="":
                        email_str = item["emails"]
                    else:
                        email_str = ",".join(item["email"])

                    if item["contact_urls"] != "":
                        contact_str = item["contact_urls"]
                    else:
                        contact_str = ",".join(item["contact_url"])

                    csv_writer.writerow([
                        item["name"],
                        item["contact"],
                        item["format_address"],
                        item["locality"],
                        item["region"],
                        item["postal_code"],
                        item["country"],
                        item["phone"],
                        item["website_url"],
                        email_str,
                        contact_str,
                        item["url"],
                        item["country_url"],
                    ])

        else:
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
        self.found_count += 1

        print "Total:", self.total_cnt, " Found:", self.found_count
        item = EmailItem()
        item["website_url"] = response.meta["url"]
        item["email"] = []

        urls=[]
        for email in email_regex.findall(response.body):
    		item["email"].append(email)
        
        href_links = response.xpath("//a")
        for href in href_links:
            url_text = href.xpath("text()").extract_first()
            if url_text != None:
                url_text = url_text.strip().lower()
                if 'contact'  in url_text or 'about' in url_text:
                    url = href.xpath("@href").extract_first()
                    if ('mailto' in url) or ('javascript' in url):
                        print url
                    else:
                        urls.append(response.urljoin(url))

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
        
        if len(item["email"]) > 0:
            item["contact_url"] = response.url
            yield item
    
    def parse_check_url(self, response):
        url_country_list = []
        for url in self.start_urls:
            obj = {}
            obj["url"] = url
            obj["country"] = ""
            obj["city"] = ""
            url_country_list.append(obj)
        
        country_list = []
        with open(country_csv_file) as csvfile:
            reader = csv.reader(csvfile)
            for item in reader:
                country_list.append(item[0].encode('utf-8'))

        russian_city_list = []
        with open(russian_city_csv_file) as csvfile:
            reader = csv.reader(csvfile)
            for item in reader:
                russian_city_list.append(item[0].encode('utf-8'))

        india_city_list = []
        with open(india_city_csv_file) as csvfile:
            reader = csv.reader(csvfile)
            for item in reader:
                try:
                    india_city_list.append(item[0].encode('utf-8'))
                except:
                    print item

        uk_city_list = []
        with open(uk_city_csv_file) as csvfile:
            reader = csv.reader(csvfile)
            for item in reader:
                uk_city_list.append(item[0].encode('utf-8'))

        for item in url_country_list:
            url_country = item["url"].split("%5B")[0]
            url_country = url_country.replace("https://www.houzz.co.uk/professionals/interior-designers/s/Interior-Designers/c/", "").replace("%20", " ")
            for country in country_list:
                if country == url_country:
                    item["country"] = country
            
            for us_city in self.us_cities:
                if us_city == url_country:
                    item["country"] = "US"
                    item["city"] = us_city

            for ru_city in russian_city_list:
                if ru_city == url_country:
                    item["country"] = "Russia"
                    item["city"] = ru_city
            
            for in_city in india_city_list:
                if in_city == url_country:
                    item["country"] = "India"
                    item["city"] = in_city

            for uk_city in uk_city_list:
                if uk_city == url_country:
                    item["country"] = "United Kindom"
                    item["city"] = uk_city
            
            if item["country"] == "":
                item["country"] = "India"
                item["city"] = url_country

        with open(url_city_csv, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for i, item in enumerate(url_country_list):
                csv_writer.writerow([item["url"], item["country"], item["city"]])
        
    def parse_us_cities(self, response):
        us_city_list = []
        
        city_divs = response.xpath("//div[@class='colmask']//ul/li")
        for row in city_divs:
            city = row.xpath("a/text()").extract_first()
            us_city_list.append(city)

        with open(us_city_csv_file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for i, item in enumerate(us_country_list):
                csv_writer.writerow([item])
    
    def parse_russian_cities(self, response):
        russian_city_list = []
        
        city_divs = response.xpath("//table[@class='wikitable sortable']//tr")
        for row in city_divs:
            cols = row.xpath("td//a/text()").extract()
            if len(cols) > 0:
                russian_city_list.append(cols[0])

        with open(russian_city_csv_file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for i, item in enumerate(russian_city_list):
                csv_writer.writerow([item])

    def parse_uk_cities(self, response):
        uk_city_list = []
        
        city_divs = response.xpath("//table[@class='table table-striped']//tr")
        for row in city_divs:
            cols = row.xpath("td/text()").extract()
            if len(cols) > 0:
                uk_city_list.append(cols[0])
        
        with open(uk_city_csv_file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for i, item in enumerate(uk_city_list):
                csv_writer.writerow([item])
    

    def parse_india_cities(self, response):
        india_city_list = []
        
        city_divs = response.xpath("//table[@class='wikitable sortable']//tr")
        for row in city_divs:
            cols = row.xpath("td//a/text()").extract()
            if len(cols) > 0:
                india_city_list.append(cols[0])

        with open(india_city_csv_file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for i, item in enumerate(india_city_list):
                csv_writer.writerow([item])

    def parse_add_india_cities(self, response):
        india_city_list = []
        
        with open(additional_india_csv_file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
        
        city_divs = response.xpath("//table[contains(@class, 'wikitable sortable')]/tr")
        for row in city_divs:
            cols = row.xpath("td/a")
            for col in cols:
                href = response.urljoin(col.xpath("@href").extract_first())
                name = col.xpath("text()").extract_first()
                print href
                req = self.set_proxies(href, self.parse_detail_add_india_cities)
                yield req
    
    def parse_detail_add_india_cities(self, response):
        items =  response.xpath("//table[@class='navbox']//tr/td//a")
        with open(additional_india_csv_file, 'a') as csvfile:
            csv_writer = csv.writer(csvfile)

            for row in items:
                name = row.xpath("text()").extract_first()
                if name is not None:
                    csv_writer.writerow([name.encode('utf-8')])        
    
    def parse_country(self, response):
        country_list = []
        country_divs = response.xpath("//ul[@class='column']")
        for div in country_divs:
            lis = div.xpath(".//li[not(contains(@class, 'letter'))]")

            for row in lis:
                country = row.xpath(".//text()").extract()
                country_list.append("".join(country))
        
        with open(country_csv_file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for i, item in enumerate(country_list):
                csv_writer.writerow([item])
        