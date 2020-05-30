# -*- coding: utf-8 -*-

import os, io, sys, shutil
import re
import json
import pandas as pd
import yaml
import requests, bs4
from timeit import default_timer as timer
from datetime import datetime
from db_data import create_connection,create_table,execute_query, fetch_db_data

SPATH = os.path.dirname(os.path.abspath(__file__))

with open('config.yml', "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

def copy_data():
    '''Copy data for parsing from scrapy folder.'''
    files = []
    dirs = []
    items = [f for f in sorted(os.listdir(cfg['paths']['src']))]

    for item in items:
        if item.endswith('.html'):
            files.append(item)
        elif item.find('.') == -1 and item[:2] == '20':
            dirs.append(item)

    if len(files) == len(dirs) == 0:
        print('No files and folders to move')
        return None
    elif len(files) != len(dirs):
        sys.exit('Error: web scrapping content incorrect')
    else:
        print('Files:', *files)
        print('Folders:', *dirs)
        for i in range(len(files)):
            src = os.path.join(cfg['paths']['src'] + dirs[i])
            dst = os.path.join(cfg['paths']['dst'] + dirs[i])

            f_src = os.path.join(cfg['paths']['src'] + files[i])
            f_dst = os.path.join(cfg['paths']['dst'] + files[i])

            try:
                shutil.move(src, dst)
                shutil.move(f_src, f_dst)
            except OSError as err:
                print(err)

def get_files_list(connection):
    """Compare files on HDD with SQLite database to select files for parsing"""

    table_id_sql = """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table' AND
       name LIKE 'otomoto_2%'
    ORDER BY name ASC;"""

    table_id = fetch_db_data(connection, table_id_sql, all=True)
    db_files = [name[0]+'.html' for name in table_id]  # conert DB table names to file names

    files = []
    for file in os.listdir(cfg['paths']['dst']):
        if file.endswith(".html"):
            files.append(file)
            #files.append(os.path.join(abs_file_path, file))

    files_list = list(set(files).difference(db_files))

    #print('DB: ',db_files)
    #print('HDD: ', files)
    print('Files to process: ', *files_list)

    return files_list


def parse_html2db(connection, html_file : str):
    '''parse HTML data and insert into SQLite database'''

    f_path = os.path.join(cfg['paths']['dst'] + html_file)
    f_name = html_file.split('.')[0]
    f_date = f_name.split('_')[1]


    try:
        carSoup = bs4.BeautifulSoup(io.open(f_path, mode='r', encoding='utf-8'), 'lxml')
        carList = carSoup.select('article.offer-item')
    except FileNotFoundError:
        print(f'{html_file} not found!')
        return None

    sql_header = """
            INSERT INTO
            "{table_name}" (offer_id, uid, url, city,type,year,mileage,price,currency,s_date,e_date)
            VALUES
        """.format(table_name = f_name)

    sql_list=[sql_header]

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

        # TODO: Performance check:
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

        sql_row = """({offer_id},"{uid}","{url}","{city}","{type}",{year},{mileage},{price},"{currency}","{s_date}","{e_date}"),
        """.format(offer_id=offer_id,
                    uid = uid,
                    url = url,
                    city=city,
                    type=model,
                    year=year,
                    mileage=mileage,
                    price=price,
                    currency=currency,
                    s_date = "{}{}{}{}-{}{}-{}{}".format(*f_date),  # "2020-04-17",
                    e_date = "{}{}{}{}-{}{}-{}{}".format(*f_date),  # "2020-04-17",
                    )

        sql_list.append(sql_row.strip()+'\n')

    sql_new_table = """CREATE TABLE IF NOT EXISTS "{table_name}" (
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
        );""".format(table_name = f_name)

    create_table(connection, sql_new_table)

    query_content = '(' + ''.join(sql_list) + ')'.strip()
    last_char_index = query_content.rfind(",")  # remove last ,
    sql_content = query_content[:last_char_index] + ';'
    # print(sql_content)
    execute_query(connection, sql_content[1:].strip())


def merge_sql(connection):

    table_id_sql = """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table' AND
       name LIKE 'otomoto_2%'
    ORDER BY name ASC;"""

    table_id = fetch_db_data(connection, table_id_sql, all=True)
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
    cnt = fetch_db_data(connection, cnt_sql, all=False)

    if cnt[0] == 0:
        execute_query(connection, initial_transfer) # executescript ?
    else:
        execute_query(connection, merge_data)
        execute_query(connection, clean_up)
        execute_query(connection, group_data)
        execute_query(connection, final_clean)

# -----------------------------------------------------------------

def get_feature_files(fname):
    files = []
    dirname =  fname.split('_')[1][:-5]
    src =  os.path.join(cfg['paths']['dst'] + dirname)

    for file in os.listdir(src):
        if file.endswith(".html"):
            files.append(file)
    print('Feature files from', dirname, ':', len(files) )
    return files

def parse_json_key(json, key):
    # check whether key exist
    # if yes flatten list to string
    try:
        buf = json[key]
        if type(json[key]) == list:
            buf = ' '.join(json[key])
    except KeyError:
        return str(0)

    return buf

def parse_json2sql(fname, dirname):
    file_path =  os.path.join(cfg['paths']['dst'] + dirname + '/' + fname)

    print(file_path)
    with open(file_path) as f:
        data = json.load(f)

    offer_id = parse_json_key(data, 'ad_id')
    user_id = parse_json_key(data,'user_id')
    UID = fname[-13:-5] # split('.')
    private_business = parse_json_key(data,'private_business')
    region = parse_json_key(data,'region')
    subregion = parse_json_key(data,'subregion')
    city = parse_json_key(data,'subregion')
    make = parse_json_key(data,'make')
    model = parse_json_key(data,'model')
    year = parse_json_key(data,'year')
    mileage	= parse_json_key(data,'mileage')
    engine_code	= parse_json_key(data,'engine_code')
    engine_capacity	= parse_json_key(data,'engine_capacity')
    vin	= parse_json_key(data,'vin')
    fuel_type = parse_json_key(data,'fuel_type')
    engine_power = parse_json_key(data,'engine_power')
    gearbox	= parse_json_key(data,'gearbox')
    transmission = parse_json_key(data,'transmission')
    body_type = parse_json_key(data,'body_type')
    door_count = parse_json_key(data,'door_count')
    nr_seats = parse_json_key(data,'nr_seats')
    color = parse_json_key(data,'color')
    features = parse_json_key(data,'features')
    price_raw = parse_json_key(data,'price_raw')
    currency = parse_json_key(data,'currency')
    country_origin= parse_json_key(data,'country_origin')
    registration= parse_json_key(data,'registration')
    date = datetime.today().strftime('%Y-%m-%d') #format: "2020-03-32"

    return [offer_id,user_id,UID, private_business,region, subregion, city, make, model, year, mileage,
    engine_code, engine_capacity, vin, fuel_type, engine_power, gearbox, transmission, body_type,
    door_count,nr_seats, color, features, price_raw, currency, country_origin,registration, date]


def store_car_sql(connection, fname, dirname):
    table_name = 'all_offers'

    car_table_sql ="""CREATE TABLE IF NOT EXISTS "{table_name}" (
	"offer_id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"uid" TEXT,
	"private_business"	TEXT,
    "region"	TEXT,
    "subregion"	TEXT,
	"city"	TEXT,
	"make"	TEXT,
	"model"	TEXT,
	"year"	INTEGER,
	"mileage"	INTEGER,
	"engine_code" TEXT,
	"engine_capacity"	INTEGER,
	"vin" TEXT,
	"fuel_type"	TEXT,
	"engine_power" INTEGER,
	"gearbox" TEXT,
	"transmission" TEXT,
	"body_type" TEXT,
	"door_count" INTEGER,
	"nr_seats" INTEGER,
	"color" TEXT,
	"features" TEXT,
	"price_raw"	INTEGER NOT NULL,
	"currency"	TEXT,
	"country_origin"	TEXT,
	"registration" TEXT,
    "date" TEXT,
    PRIMARY KEY (offer_id, price_raw)
    );""".format(table_name=table_name)

    insert_sql = """INSERT OR IGNORE INTO "{table_name}"
                    VALUES """.format(table_name=table_name) + '(' + str(parse_json2sql(fname, dirname))[1:-1]+')'

    create_table(connection, car_table_sql)
    execute_query(connection,insert_sql)
    # execute_query(connection, "DROP TABLE {table_name};".format(table_name=table_name))

# ------------------------------------------------

def main():
    start = timer()

    conn = create_connection()

    copy_data()
    files = get_files_list(conn)

    if not files:
        print('Nothing to do')
    else:
        for f in files:
            print('....',f,'....')
            parse_html2db(conn, f)
            merge_sql(conn)
            feat_dir = get_feature_files(f)

            if not feat_dir:
                print("No features to process")
            else:
                dirname = f.split('_')[1][:-5]
                for feats in feat_dir:
                    store_car_sql(conn, feats, dirname)
            print('Feats:', feat_dir)
        print(f, '- done')

    conn.close()
    end = timer()
    print(end - start)

#--------------------------------------------------#

if __name__ == "__main__":
    main()
