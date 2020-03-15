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
    start_urls = ['https://www.otomoto.pl/osobowe/toyota/yaris/ii-2005-2011/']

    def parse(self, response):
        print(response.status)

        lastPage =  response.xpath("//span[@class='page']//text()").extract()[-1]# extract offer list
        #print(lastPage)

        offers = response.xpath("//div[@class='offers list']").extract() # extract offer list
        print(type(offers))
		

        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first()) # extract of ld+json from page
        #print(type(data))

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


        # with open('page'+str(current_page)+'.html', 'wb') as html_file:
        #     html_file.write(response.body)
        #print("procesing:"+response.url)

        now = datetime.datetime.now()

        with open('./otomoto_'+now.strftime('%Y%m%d')+'.html', 'a',encoding='utf-8') as f:
            for item in offers:
				# remove double spaces to shrink file size
                f.write("%s\n" % item.replace("  ", ""))

        with open('./otomoto_'+now.strftime('%Y%m%d')+'.json', 'a') as j:
            # this would place the entire output on one line
            # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
            json.dump(data, j, indent=4)

    # def parse_item(self, response):
	#       with open('page.html', 'wb') as html_file:
	# 	        html_file.write(response.body)
    #     #pass