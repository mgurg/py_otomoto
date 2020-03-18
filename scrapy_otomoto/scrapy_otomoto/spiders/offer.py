# -*- coding: utf-8 -*-
import scrapy
import json
import datetime

# https://www.scrapingbee.com/blog/web-scraping-with-scrapy/
# https://towardsdatascience.com/scrape-multiple-pages-with-scrapy-ea8edfa4318

# TODO: PAgination
# https://stackoverflow.com/questions/54716360/incremental-pagination-in-scrapy-python
# https://towardsdatascience.com/scrape-multiple-pages-with-scrapy-ea8edfa4318

class OtomotoSpider(scrapy.Spider):
    name = 'otomoto'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    }

    allowed_domains = ['otomoto.pl']
    start_urls = ['https://www.otomoto.pl/oferta/toyota-yaris-1-3-vvt-i-salon-polska-serwis-aso-automat-klima-parktronic-ID6CWMXd.html#a11f29a30d']

    def parse(self, response):
        print(response.status)

        with open('page.html', 'wb') as html_file:
             html_file.write(response.body)
        print("procesing:"+response.url)

