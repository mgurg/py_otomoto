# -*- coding: utf-8 -*-

import requests, bs4, io, csv, datetime
from timeit import default_timer as timer
import re
import os
import pandas as pd

start = timer()

# LIST ALL HTML FILES
files = []

for file in os.listdir("./"):
    if file.endswith(".html"):
        files.append(file)
        #files.append(os.path.join("./", file))
        #print(os.path.join("./", file))

def parse_html2csv(html_file : str): # PARSE HTML TO CSV
    #html_file = "otomoto_2019-12-31.html"
    fname = 'carData_'+ html_file[8:18] +'.csv'
    carFile = io.open(fname, 'w', encoding="utf-8")
    #csv file header
    carFile.write('offer_id,city,region,model,year,mileage,fuel_type,displacement,price,currency,pub_date,duration,end_price'+'\n')

    carSoup = bs4.BeautifulSoup(io.open(html_file, mode="r", encoding="utf-8"), "lxml")
    carList = carSoup.select('article.offer-item')

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

        pub_date = html_file[8:18]
        duration = "1"
        end_price = "-1"

        # print(offer_id + ',' +
            #   city + ','+
            #   region  + ','+
            #   model + ','+
            #   year.strip() + ','+
            #   mileage.strip() + ','+
            #   fuel_type.strip() + ','+
            #   str(displacement) + ','+
            #   price[:-4].strip() + ','+
            #   currency.strip() + ','+
            #   pub_date + ',' +
            #   duration + ',' +
            #   end_price
            #   )

        carFile.write(offer_id + ',' +
              city + ','+
              region  + ','+
              model + ','+
              year.strip() + ','+
              mileage.strip() + ','+
              fuel_type.strip() + ','+
              str(displacement) + ','+
              price[:-4].strip() + ','+
              currency.strip() + ','+
              pub_date + ',' +
              duration + ',' +
              end_price + '\n'
              )
    carFile.close()


def merge_csv():
    #csv_file = "carData_2019-12-31.csv"
    csv_file = "carData_2020-01-01.csv"

    df2 = pd.read_csv(csv_file,index_col=False,encoding='utf-8')

    if os.path.isfile('my_df.csv') == False:
        my_df  = pd.DataFrame(columns =['offer_id','city','region','model','year','mileage','fuel_type','displacement','price','currency','pub_date','duration','end_price'])
        my_df.to_csv('my_df.csv',index=False)
    else:
        my_df = pd.read_csv("my_df.csv",encoding='utf-8')

    if my_df.empty:
        print('my_df is empty!')
        df2.to_csv('my_df.csv',index=False)
    else:
        my_df = pd.DataFrame(pd.concat([my_df, df2], ignore_index=True))
        my_df = my_df.drop_duplicates(subset=['offer_id'])
        my_df.to_csv('my_df.csv',index=False)

for f in files:
    print(f)
    #parse_html2csv(f)

merge_csv()

end = timer()
print(end - start)
