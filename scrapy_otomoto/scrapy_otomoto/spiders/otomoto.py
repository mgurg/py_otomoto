# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import re
import os
import sys
import pathlib
import shutil

class OtomotoSpider(scrapy.Spider):
    name = 'otomoto'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    }

    allowed_domains = ['otomoto.pl']
    start_urls = ['https://www.otomoto.pl/osobowe/toyota/yaris/ii-2005-2011/']

    def parse(self, response):
        f_car_list = "db_car_list.txt"
        lines = []
        if pathlib.Path(f_car_list).exists ():
            with open(f_car_list, encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    lines.append(line)
        else:
            pass

        print(response.status)

        lastPage =  response.xpath("//span[@class='page']//text()").extract()[-1]# extract offer list

        offers = response.xpath("//div[@class='offers list']").extract() # extract offer list
        #data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first()) # extract of ld+json from page
        offer_url =  response.css('article').xpath('@data-href').getall()

        current_page = response.meta.get("page", 1)
        next_page = current_page + 1

        if current_page < int(lastPage):
            isTruncated = True
        else:
            isTruncated = False

        if isTruncated == True:
            yield scrapy.Request(
                url="https://www.otomoto.pl/osobowe/toyota/yaris/ii-2005-2011/?page={page}".format(page=next_page),
                callback=self.parse,
                meta={'page': next_page},
                dont_filter=True
        )

        if isTruncated == False:
            print(lastPage)

        now = datetime.datetime.now()

        with open('./otomoto_'+now.strftime('%Y%m%d')+'.html', 'a',encoding='utf-8') as f:
            for item in offers:
				# remove double spaces to shrink file size
                f.write("%s" % item.replace("  ", ""))

        #JSON
        #with open('./otomoto_'+now.strftime('%Y%m%d')+'.json', 'a') as j:
            # this would place the entire output on one line
            # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
            #json.dump(data, j, indent=4)

        with open('./otomoto_'+now.strftime('%Y%m%d')+'.txt', 'a',encoding='utf-8') as u:
            for url_item in offer_url:
                u.write("%s\n" % url_item)


        for url in offer_url:
            if url[-13:-5] in lines:
                print(url[-13:-5]+' already present')
            else:
                print(url[-13:-5]+' not present yet')
                yield scrapy.Request(url, callback=self.parse_item)

    # parse car subpages
    def parse_item(self, response):

        #regex - 0.0034
        pattern = re.compile(r"""(GPT.targeting = )(.*?);""")
        result = re.search(pattern, response.text)

        # # python - 0.026
        # start = data.find('GPT.targeting = ')+len('GPT.targeting = ')
        # stop = data.find(';', start)
        # json_data = data[start:stop]
        # car_json = json.loads(json_data)

        #file_name =  response.url[-13:] # ID6CDXN8.html
        file_name = str(response.url).rpartition('-')[2]
        script_dir = os.path.dirname(__file__)
        now = datetime.datetime.now()

        if not os.path.exists(now.strftime('%Y%m%d')):
            try:
                os.mkdir(now.strftime('%Y%m%d'))
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s" % path)

        rel_path = now.strftime('%Y%m%d') + '/'+ file_name
        abs_file_path = os.path.join(script_dir, rel_path)

        print(abs_file_path)

        with open(abs_file_path, "a+") as text_file:
            text_file.write(result.group(2))
            # ID6CDXN8
            # ID6CQOCT

    # def parse_list(self):
    #     with open('./otomoto_'+now.strftime('%Y%m%d')+'.txt', "rt", ,encoding='utf-8') as f:
    #         start_urls = [url.strip() for url in f.readlines()]
    #     print(start_urls)