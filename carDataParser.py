# -*- coding: utf-8 -*-

import requests, bs4, io, csv, datetime
from timeit import default_timer as timer
import re
import os

start = timer()

files = []

for file in os.listdir("./"):
    if file.endswith(".html"):
        files.append(os.path.join("./", file))
        #print(os.path.join("./", file))

for f in files:
    print(f)

carSoup = bs4.BeautifulSoup(io.open("otomoto_2019-12-31.html", mode="r", encoding="utf-8"), "lxml")
carList = carSoup.select('article.offer-item')

now = datetime.datetime.now()

fname = 'carData_'+ str(now.date()) +'.csv'
carFile = io.open(fname, 'w', encoding="utf-8")

#csv file header
carFile.write('offer_id,city,region,model,year,mileage,displacement,fuel_type,price,pub_date,duration,end_price'+'\n')

i = 0
for car in carList:
    #OfferId = car.find('a', {'name': 'data-ad-id'}).get('value')

    # TODO: test regex performance
    #print(type(car))
    #print(car)
    #OfferId = car.find_all(re.compile("data-ad-id=\"(.*?)\""))
    #OfferId = re.search("(data-ad-id=)\"(.*?)\"", car)[0]

    offer_id = car.find("a")['data-ad-id']
    city = car.find('span',class_='ds-location-city').text.strip()
    region = car.find('span',class_='ds-location-region').text[1:-1].strip()
    model = car.find('a',class_='offer-title__link').text.strip()

    #params = car.find("li", class_='ds-param')

    year = car.find("li", {"data-code" : "year"}).text
    mileage = car.find("li", {"data-code" : "mileage"}).text[:-3].replace(" ", "")

    # try:
    #     displacement = car.find("li", {"data-code" : "engine_capacity"}).text[:-3].replace(" ", "")
    # except AttributeError:
    #     print(offer_id + ' no displacement value')
    #     displacement = -1

    displacement = car.find("li", {"data-code" : "engine_capacity"})
    if displacement is not None:
        displacement = displacement.get_text()[:-4].replace(" ", "").strip()
    else:
        print(offer_id + ' no displacement value')
        displacement = -1

    fuel_type = car.find("li", {"data-code" : "fuel_type"}).text

    price = car.find('span',class_='offer-price__number').text.replace(" ", "")
    currency = price[len(price)-4:]
    print(currency)

    print(offer_id + ',' +
          city + ','+
          region  + ','+
          model + ','+
          year.strip() + ','+
          mileage.strip() + ','+
          fuel_type.strip() + ','+
          str(displacement) + ','+
          price[:-4].strip()+','+
          currency.strip())

end = timer()
print(end - start)
