# -*- coding: utf-8 -*-
import os
import io
import json
import re
from dbData import create_connection,create_table,execute_query
from timeit import default_timer as timer

import pandas as pd
from pandas.io.json import json_normalize

tstart = timer()

def get_current_car_list():
    # list all unique cars in database
    car_list = []
    conn = create_connection('pythonsqlite.db')
    c = conn.cursor()
    x=c.execute("""SELECT name FROM sqlite_master where type='table'""")
    for y in x.fetchall():
        item = ''.join(y)
        if item[0] == 'c': # ('car_ID6CXnaK',)
            car_list.append(item[4:])
    return car_list

def get_file_list():
    # list all unique cars data in files
    files_list = []

    for file in os.listdir("./archive/cars/"):
        if file.endswith(".html"):
            #files.append(file) # just filename
            files.append(os.path.join("./archive/cars/", file)) # file with path
            #print(os.path.join("./", file))
    return files_list

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
    with open(fname) as f:
        data = json.load(f)

    offer_id = parse_json_key(data, 'ad_id')
    user_id = parse_json_key(data,'user_id')
    UID = fname[-13:-5]
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

    return [offer_id,user_id,UID, private_business,region, subregion, city, make, model, year, mileage,
    engine_code, engine_capacity, vin, fuel_type, engine_power, gearbox, transmission, body_type,
    door_count,nr_seats, color, features, price_raw, currency, country_origin,registration]

def store_car_sql(fname):
    table_name = 'car_'+fname[-13:-5]

    car_table_sql ="""CREATE TABLE "{table_name}" (
	"offer_id"	INTEGER NOT NULL PRIMARY KEY,
	"user_id"	INTEGER,
	"UID" TEXT,
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
	"price_raw"	INTEGER,
	"currency"	TEXT,
	"country_origin"	TEXT,
	"registration" TEXT
    );""".format(table_name=table_name)

    insert_sql = """INSERT INTO "{table_name}"
                    VALUES """.format(table_name=table_name) + '(' + str(parse_json2sql(fname))[1:-1]+')'

    #print('(' + str(parse_json2sql(fname))[1:-1]+')')
    print(insert_sql)
    #conn = create_connection('pythonsqlite.db')
    #create_table(conn, table_name, car_table_sql)
    #execute_query(conn,insert_sql)
    #execute_query(conn, "DROP TABLE {table_name};".format(table_name=table_name))

files = []

for file in os.listdir("./archive/cars/"):
    if file.endswith(".html"):
        files.append(file[:-5]) # just filename
        #files.append(os.path.join("./archive/cars/", file)) # file with path
        #print(os.path.join("./", file))

parsing_list = compare_lists(files, get_current_car_list())
print(parsing_list)

if not parsing_list:
  print("Nothing here")
else:
    i = 0
    for fname in parsing_list:
        i=i+1
        #print(str(i)+' : '+ fname)
        #parse_json2sql(fname)
        #store_car_sql(fname)


# with open('./otomoto_20200320.html', 'r', encoding="utf-8") as myfile:
#   data = myfile.read()

# #regex - 0.0034
# # pattern = re.compile(r"""(GPT.targeting = )(.*?);""")
# # result = re.search(pattern, data)
# # car_json = json.loads(result.group(2))


# # python - 0.026
# start = data.find('GPT.targeting = ')+len('GPT.targeting = ')
# stop = data.find(';', start)
# json_data = data[start:stop]
# car_json = json.loads(json_data)


# print(car_json)
# print(car_json['features'])

end = timer()
print('Time: '+ str(end - tstart))

# https://medium.com/@amirziai/flatten-json-on-python-package-index-pypi-9e4951693a5a
# features_list = ["abs" , "cd" , "central-lock" , "front-electric-windows" ,
# "electronic-rearview-mirrors" , "electronic-immobiliser" , "front-airbags" ,
# "front-passenger-airbags" , "original-radio" , "assisted-steering" , "alarm" ,
# "alloy-wheels" , "asr" , "park-assist" , "lane-assist" , "bluetooth" , "automatic-wipers" ,
# "blind-spot-sensor" , "automatic-lights" , "both-parking-sensors" , "rear-parking-sensors" ,
# "panoramic-sunroof" , "electric-exterior-mirror" , "electric-interior-mirror" ,
# "rear-electric-windows" , # "electric-adjustable-seats" , "esp" , "aux-in" , "sd-socket" ,
# "usb-socket" , "towing-hook" , # "head-display" , "isofix" , "rearview-camera" ,
# "automatic-air-conditioning" , "quad-air-conditioning" , # "dual-air-conditioning" ,
# "air-conditioning" , "onboard-computer" , "side-window-airbags" , "shift-paddles" ,
# "mp3" , "gps" , "dvd" , "speed-limiter" , "auxiliary-heating" , "heated-windshield" ,
# "heated-rearview-mirrors" , # "front-heated-seats" , "rear-heated-seats" , "driver-knee-airbag" ,
# "front-side-airbags" , "rear-passenger-airbags" , # "tinted-windows" , "radio" , "adjustable-suspension" ,
# "roof-bars" , "system-start-stop" , "sunroof" , "daytime-lights" , # "leds" , "fog-lights" , "xenon-lights" ,
# "leather-interior" , "velour-interior" , "cruise-control" , "active-cruise-control" , # "tv" ,
# "steering-whell-comands" , "cd-changer"]