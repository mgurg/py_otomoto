# -*- coding: utf-8 -*-

import requests, bs4, io, csv
from timeit import default_timer as timer
import re
import os
import pandas as pd
import shutil
from datetime import datetime
from db_data import create_connection,create_table,execute_query,fetch_all_data,fetch_single_item

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


def get_files_list(connection):

    table_id_sql = """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table' AND
       name LIKE 'otomoto_2%'
    ORDER BY name ASC;"""

    table_id = fetch_all_data(connection, table_id_sql)

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


def parse_html2db(connection, html_file : str): # PARSE HTML TO CSV
    fname = 'otomoto_'+ html_file[8:18] +'.csv'

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
    create_table(connection, sql_str)

    query_content = '(' + ''.join(sql_list) + ')'.strip()
    last_char_index = query_content.rfind(",")
    sql_content = query_content[:last_char_index]+';'

    #print(sql_content)
    execute_query(connection, sql_content[1:].strip())

def merge_sql(connection):

    table_id_sql = """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table' AND
       name LIKE 'otomoto_2%'
    ORDER BY name ASC;"""

    table_id = fetch_all_data(connection, table_id_sql)
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

    # create tables if missing
    execute_query(connection, temp_table)
    execute_query(connection, all_table)

    cnt_sql = """SELECT count(*) FROM otomoto_all"""
    cnt = fetch_single_item(connection, cnt_sql)

    if cnt[0] == 0:
        execute_query(connection, initial_transfer) # executescript ?
    else:
        execute_query(connection, merge_data)
        execute_query(connection, clean_up)
        execute_query(connection, group_data)
        execute_query(connection, final_clean)

def clean(file: str):
    destination = './offers/'
    shutil.move(file, destination+file)
    #os.remove(file)

def main():
    start = timer()

    conn = create_connection()

    copy_data()
    files = get_files_list(conn)

    if not files:
        print("Nothing here")
    else:
        for f in files:
            print('....')
            parse_html2db(conn, f)
            merge_sql(conn)
            clean(f)
            print(f+' - done')

    conn.close()
    end = timer()
    print(end - start)

#--------------------------------------------------#

if __name__ == "__main__":
    main()
