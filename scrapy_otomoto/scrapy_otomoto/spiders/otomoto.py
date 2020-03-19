# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import re

class OtomotoSpider(scrapy.Spider):
    name = 'otomoto'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    }

    allowed_domains = ['otomoto.pl']
    start_urls = ['https://www.otomoto.pl/osobowe/toyota/yaris/ii-2005-2011/']

    def parse(self, response):
        print(response.status)

        lastPage =  response.xpath("//span[@class='page']//text()").extract()[-1]# extract offer list
        #print(lastPage)

        offers = response.xpath("//div[@class='offers list']").extract() # extract offer list
        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first()) # extract of ld+json from page
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
                f.write("%s\n" % item.replace("  ", ""))

        with open('./otomoto_'+now.strftime('%Y%m%d')+'.json', 'a') as j:
            # this would place the entire output on one line
            # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
            json.dump(data, j, indent=4)

        with open('./otomoto_'+now.strftime('%Y%m%d')+'.txt', 'a',encoding='utf-8') as u:
            for url in offer_url:
                u.write("%s\n" % item)

        for url in offer_url:
            yield scrapy.Request(url, callback=self.parse_item)

    # parse car subpages
    def parse_item(self, response):
        pattern = re.compile(r"""(GPT.targeting = )(.*?);""")
        result = re.search(pattern, response.text)

        file_name =  response.url[-13:]
        with open(file_name, "a") as text_file:
            text_file.write(result.group(2))
            # ID6CDXN8
            # ID6CQOCT
            # ID6CRr7q
            # ID6CTQ4D