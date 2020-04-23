# -*- coding: utf-8 -*-
import os
import io
import json
import re
from dbData import create_connection,create_table,execute_query
from timeit import default_timer as timer
from datetime import datetime
import sys
import shutil

def get_db_car_list():
    # list all unique cars in database
    car_list = []
    conn = create_connection('pythonsqlite.db')
    c = conn.cursor()
    c.execute("""SELECT uid,price FROM otomoto_all""")
    x = dict(c.fetchall())
    print(x)

    # with open('.\scrapy_otomoto\scrapy_otomoto\spiders\db_car_list.txt', 'w', encoding="utf-8") as f:
    #     for item in car_list:
    #         f.write("%s\n" % item)

    return x

def get_file_list():
    files = []
    now = datetime.now()
    src = "./offers/"+ now.strftime('%Y%m%d')+'/'

    # list all unique cars data in files
    for file in os.listdir(src):
        if file.endswith(".html"):
            files.append(file) # just filename
            #files.append(os.path.join(src, file)) # file with path
            #print(os.path.join("./", file))
    return files

def compare_lists(a,b):
    #compare items in DB to file list
     return set(a).difference(b)

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

def parse_json2sql(fname):

    now = datetime.now()
    src = "./offers/"+ now.strftime('%Y%m%d')+'/'
    file_path = os.path.join(src, fname)

    with open(file_path) as f:
        data = json.load(f)
        #print(data)

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

def store_car_sql(connection, fname):
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
                    VALUES """.format(table_name=table_name) + '(' + str(parse_json2sql(fname))[1:-1]+')'

    #print(insert_sql)
    #conn = create_connection('pythonsqlite.db')
    create_table(connection, car_table_sql)
    execute_query(connection,insert_sql)
    #execute_query(conn, "DROP TABLE {table_name};".format(table_name=table_name))

def clean(file: str):
    destination = './'+datetime.today().strftime('%Y-%m-%d')
    shutil.move(file, destination+file)
    os.remove(file)

def main():
    tstart = timer()

    conn = create_connection('pythonsqlite.db')

    files = get_file_list()

    if not files:
        print("No offers to process")
    else:
        for fname in files:
            store_car_sql(conn, fname)

    conn.close()

    end = timer()
    print('Time: '+ str(end - tstart))

#----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
