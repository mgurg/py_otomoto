# -*- coding: utf-8 -*-

import requests, bs4, io, csv, datetime
from timeit import default_timer as timer
import re
import os
import pandas as pd
import shutil
from dbData import create_connection,create_table,execute_query

start = timer()

def parse_html2csv(html_file : str): # PARSE HTML TO CSV
    fname = 'otomoto_'+ html_file[8:18] +'.csv'

    csv_header = 'offer_id,city,region,model,year,mileage,fuel_type,displacement,price,currency,pub_date,duration,end_price'+'\n'
    csv_list=[csv_header]

    sql_header = """
            INSERT INTO
            "{table_name}" (offer_id,city,region,model,year,mileage,fuel_type,displacement,price,currency,pub_date,duration,end_price)
            VALUES
        """.format(table_name= fname[:-4])

    sql_list=[sql_header]

    carSoup = bs4.BeautifulSoup(io.open(html_file, mode="r", encoding="utf-8"), "lxml")
    carList = carSoup.select('article.offer-item')

    for car in carList:
        # TODO: test regex performance
            #OfferId = car.find_all(re.compile("data-ad-id=\"(.*?)\""))
            #OfferId = re.search("(data-ad-id=)\"(.*?)\"", car)[0]

        offer_id = car.find("a")['data-ad-id']
        city = car.find('span',class_='ds-location-city').text.strip()
        region = car.find('span',class_='ds-location-region').text[1:-1].strip()
        model = car.find('a',class_='offer-title__link').text.strip()

        #params = car.find("li", class_='ds-param')
        year = car.find("li", {"data-code" : "year"}).text.strip()
        mileage = car.find("li", {"data-code" : "mileage"}).text[:-3].replace(" ", "").strip()

        # Performance check required:
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
            displacement = str(-1)

        fuel_type = car.find("li", {"data-code" : "fuel_type"}).text.strip()

        car_value = car.find('span',class_='offer-price__number').text.replace(" ", "")
        price = car_value.splitlines()[1]
        currency = str(car_value.splitlines()[2]) #currency = price[len(price)-4:].strip()

        pub_date = html_file[8:18]
        duration = "1"
        end_price = "-1"

        csv_rows = offer_id + ',' +\
                    city + ','+\
                    region  + ','+\
                    model + ','+\
                    year + ','+\
                    mileage + ','+\
                    fuel_type + ','+\
                    displacement + ','+\
                    price + ','+\
                    currency + ','+\
                    pub_date + ',' +\
                    duration + ',' +\
                    end_price+'\n'

        sql_row = """("{offer_id}",
                        "{city}",
                        "{region}",
                        "{model}",
                        "{year}",
                        "{mileage}",
                        "{fuel_type}",
                        "{displacement}",
                        "{price}",
                        "{currency}",
                        "{pub_date}",
                        "{duration}",
                        "{end_price}"),
        """.format(offer_id=offer_id,
                    city=city,
                    region=region,
                    model=model,
                    year=year,
                    mileage=mileage,
                    fuel_type=fuel_type,
                    displacement=displacement,
                    price=price,
                    currency=currency,
                    pub_date=pub_date,
                    duration=duration,
                    end_price=end_price)

        sql_list.append(sql_row)
        csv_list.append(csv_rows)

    # export to csv at once
    carFile = io.open(fname, 'w', encoding="utf-8")
    csv_content = ''.join(csv_list).strip()
    carFile.write(csv_content)
    carFile.close()

    # export to SQLite in one query
    conn = create_connection('pythonsqlite.db')
    create_table(conn, fname[:-4])
    query_content = '(' + ''.join(sql_list) + ')'.strip()
    last_char_index = query_content.rfind(",")
    sql_content = query_content[:last_char_index]+';'

    execute_query(conn, sql_content[1:].strip())

def merge_csv(csv_file : str):
# merge two csv files form consecutive days  into one my_df file
    #csv_file = "carData_2019-12-31.csv"
    #csv_file = "carData_2020-01-01.csv"

    df2 = pd.read_csv(csv_file,index_col=False,encoding='utf-8')

    if os.path.isfile('my_df.csv') == False:
        my_df  = pd.DataFrame(columns =['offer_id','city','region','model','year','mileage','fuel_type','displacement','price','currency','pub_date','duration','end_price'])
        my_df.to_csv('my_df.csv',index=False)
    else:
        my_df = pd.read_csv("my_df.csv",encoding='utf-8')

    if my_df.empty:
        print('my_df is empty!')
        df2.to_csv('my_df.csv',index=False)
        return #jump out from merge_csv(csv_file : str)
    else:
        print('my_df is NOT empty!')
        my_df = pd.DataFrame(pd.concat([my_df, df2], ignore_index=True))
        my_df = my_df.drop_duplicates(subset=['offer_id'])
        my_df.to_csv('my_df.csv',index=False)

def fill_csv(csv_file : str):
# compare entries
    my_df = pd.read_csv('my_df.csv',
                   index_col=False,
                   encoding='utf-8')

    df2 = pd.read_csv(csv_file,
                  index_col=False,
                  encoding='utf-8')


    for j, jrow in enumerate(my_df.itertuples(), 1):
        my_df_IDX = jrow.offer_id

        for k, krow in enumerate(df2.itertuples(), 1):
            if (my_df_IDX == krow.offer_id):

                my_df.at[j-1, 'duration'] = my_df.iloc[j-1]['duration'] + 1 # increase day counter
                my_df.at[j-1, 'end_price'] = df2.iloc[k-1]['price'] # assign last price from today file


    #my_df['offer_id'] = my_df['offer_id'].astype('int64')
    my_df.to_csv (r'.\my_df.csv', index = None, header=True, encoding="utf-8")


def clean(file: str):
    destination = './archive/'
    #shutil.move(file, destination+file)
    #os.remove(file[:-4]+'csv')

#--------------------------------------------------#

# LIST ALL HTML FILES
files = []

for file in os.listdir("./"):
    if file.endswith(".html"):
        files.append(file)
        #files.append(os.path.join("./", file))
        #print(os.path.join("./", file))


if not files:
  print("Nothing here")
else:
    for f in files:
        print('....')
        #os.remove('my_df.csv')
        csv_file = f[:-4]+'csv'
        parse_html2csv(f)
        merge_csv(csv_file)
        fill_csv(csv_file)
        clean(f)
        print(f+' - done')

end = timer()
print(end - start)