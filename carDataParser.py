# -*- coding: utf-8 -*-

import requests, bs4, io, csv
from timeit import default_timer as timer
import re
import os
import pandas as pd
import shutil
from datetime import datetime
from dbData import create_connection,create_table,execute_query

def copy_data():
    now = datetime.now()

    src = './scrapy_otomoto/scrapy_otomoto/spiders/' + now.strftime('%Y%m%d') + '/'
    dest = './offers/' + now.strftime('%Y%m%d') + '/'

    f_src = './scrapy_otomoto/scrapy_otomoto/spiders/' + 'otomoto_'+ now.strftime('%Y%m%d')+'.html'
    f_dest = './'

    try:
        shutil.move(src, dest)
        shutil.move(f_src, f_dest)
    except:
        print('Move folder error')


def get_files_list():

    conn = create_connection('pythonsqlite.db')
    table_id_sql = """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table' AND
       name LIKE 'otomoto_2%'
    ORDER BY name ASC;"""

    c = conn.cursor()
    c.execute(table_id_sql)
    table_id = c.fetchall()

    db_files = [i[0]+'.html' for i in table_id]

    files = []
    for file in os.listdir('./'):
        if file.endswith(".html"):
            files.append(file)
            #files.append(os.path.join(abs_file_path, file))
            #print(os.path.join("./", file))
    files_list = set(files).difference(db_files)

    #print('DB: ',db_files)
    #print('HDD: ', files)
    print('Files to process: ', list(files_list))

    return list(files_list)


def parse_html2db(html_file : str): # PARSE HTML TO CSV
    fname = 'otomoto_'+ html_file[8:18] +'.csv'

    #csv_header = 'offer_id,city,region,model,year,mileage,fuel_type,displacement,price,currency,pub_date,duration,end_price'+'\n'
    #csv_list=[csv_header]

    sql_header = """
            INSERT INTO
            "{table_name}" (offer_id, uid, url, city,type,year,mileage,price,currency,s_date,e_date)
            VALUES
        """.format(table_name= fname[:-6].replace("-", ""))

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


        url = car.find("a")['href'].split("#")[0]
        uid = url[-13:-5]
        #print(uid)

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
            # print(offer_id + ' no displacement value')
            displacement = str(-1)

        #fuel_type = car.find("li", {"data-code" : "fuel_type"}).text.strip()

        car_value = car.find('span',class_='offer-price__number').text.replace(" ", "")
        price = car_value.splitlines()[1]
        currency = str(car_value.splitlines()[2]) #currency = price[len(price)-4:].strip()

        #print(html_file)
        #pub_date = html_file[8:16]
        #print(pub_date)
        #duration = "1"
        #end_price = "-1"

        # csv_rows = offer_id + ',' +\
        #             city + ','+\
        #             region  + ','+\
        #             model + ','+\
        #             year + ','+\
        #             mileage + ','+\
        #             fuel_type + ','+\
        #             displacement + ','+\
        #             price + ','+\
        #             currency + ','+\
        #             pub_date + ',' +\
        #             duration + ',' +\
        #             end_price+'\n'

        sql_row = """("{offer_id}",
                        "{uid}",
                        "{url}",
                        "{city}",
                        "{type}",
                        "{year}",
                        "{mileage}",
                        "{price}",
                        "{currency}",
                        "{s_date}",
                        "{e_date}"),
        """.format(offer_id=offer_id,
                    uid = uid,
                    url = url,
                    city=city,
                    type=model,
                    year=year,
                    mileage=mileage,
                    price=price,
                    currency=currency,
                    s_date =datetime.today().strftime('%Y-%m-%d'),# "2020-04-17",
                    e_date = datetime.today().strftime('%Y-%m-%d'),#"2020-04-17",
                    )

        sql_list.append(sql_row)
        #csv_list.append(csv_rows)

    # export to csv at once
    #carFile = io.open(fname, 'w', encoding="utf-8")
    #csv_content = ''.join(csv_list).strip()
    #carFile.write(csv_content)
    #carFile.close()

    #print('CHK: ', fname)
    #print(fname[:-6].replace("-", ""))

    sql_str = """CREATE TABLE IF NOT EXISTS "{table_name}" (
	    "offer_id"	INTEGER NOT NULL PRIMARY KEY,
        "uid"   TEXT,
        "url" TEXT,
	    "city"	TEXT,
	    "type"	TEXT,
	    "year"	INTEGER,
	    "mileage"	INTEGER,
	    "price"	INTEGER,
	    "currency"	TEXT,
        "s_date" TEXT,
        "e_date" TEXT
        );""".format(table_name=fname[:-6].replace("-", ""))

    # export to SQLite in one query
    conn = create_connection('pythonsqlite.db')
    create_table(conn, fname[:-6].replace("-", ""), sql_str)

    query_content = '(' + ''.join(sql_list) + ')'.strip()
    last_char_index = query_content.rfind(",")
    sql_content = query_content[:last_char_index]+';'

    #print(sql_content)

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

def merge_sql():
    conn = create_connection('pythonsqlite.db')

    table_id_sql = """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table' AND
       name LIKE 'otomoto_2%'
    ORDER BY name ASC;"""

    c = conn.cursor()
    c.execute(table_id_sql)
    table_id = c.fetchall()
    print(''.join(table_id[-1]))

    temp_table = """--create temporary table
    CREATE TABLE IF NOT EXISTS "temp_table" (
	    "offer_id"	INTEGER NOT NULL,
        "uid"   TEXT,
		"year" INTEGER,
		"mileage" INTEGER,
		"price" INTEGER,
        "s_date" TEXT,
        "e_date" TEXT)"""

    all_table = """--create otomoto_all table
    CREATE TABLE IF NOT EXISTS "otomoto_all" (
	    "offer_id"	INTEGER NOT NULL,
        "uid"   TEXT,
		"year" INTEGER,
		"mileage" INTEGER,
		"price" INTEGER,
        "s_date" TEXT,
        "e_date" TEXT)"""

    initial_transfer = """-- prepare otomoto_all
    INSERT INTO otomoto_all(offer_id,uid,year,mileage,price,s_date,e_date)
    SELECT offer_id,uid,year,mileage,price,s_date,e_date from "{table_name}";
    """.format(table_name = ''.join(table_id[0])) #first table otomoto_2020mmdd

    merge_data = """-- copy data
    INSERT INTO temp_table(offer_id,uid,year,mileage,price,s_date,e_date)
    SELECT offer_id,uid,year,mileage,price,s_date,e_date from otomoto_all
    UNION
    SELECT offer_id,uid,year,mileage,price,s_date,e_date from "{table_name}";
    """.format(table_name = ''.join(table_id[-1])) #last table otomoto_2020mmdd

    clean_up = """--clean otomoto_all
    delete from otomoto_all;"""

    group_data = """-- group values
    INSERT INTO otomoto_all(offer_id,uid,year,mileage,price,s_date,e_date)
    SELECT
        offer_id,
	    uid,
	    year,
        mileage,
	    price,
        min(s_date) AS S_DATE,
        max(e_date) AS E_DATE
    FROM
        temp_table
    GROUP BY
        offer_id;
    """

    final_clean = """
    -- clean temp table
    delete from temp_table;"""


    execute_query(conn, temp_table)
    execute_query(conn, all_table)

    c.execute("""SELECT count(*) FROM otomoto_all""") # is otomoto_all empty?
    cnt = c.fetchone()

    if cnt[0] == 0:
        execute_query(conn, initial_transfer) # executescript ?
    else:
        execute_query(conn, merge_data)
        execute_query(conn, clean_up)
        execute_query(conn, group_data)
        execute_query(conn, final_clean)

def clean(file: str):
    destination = './offers/'
    shutil.move(file, destination+file)
    #os.remove(file)

def main():
    start = timer()
    copy_data()
    files = get_files_list()

    if not files:
        print("Nothing here")
    else:
        for f in files:
            print('....')
            parse_html2db(f)
            merge_sql()
            clean(f)
            print(f+' - done')

    end = timer()
    print(end - start)

#--------------------------------------------------#

if __name__ == "__main__":
    main()
