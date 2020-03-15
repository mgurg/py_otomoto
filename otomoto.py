# -*- coding: utf-8 -*-
import scrapy


class OtomotoSpider(scrapy.Spider):
    name = 'otomoto'
    allowed_domains = ['otomoto.pl']
    start_urls = ['http://otomoto.pl/']

    def parse(self, response):
        pass
