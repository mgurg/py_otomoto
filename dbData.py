import sqlite3
import pandas as pd
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table(conn, table_name, create_table_sql=' '):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    # master_table
    # create_table_sql = """CREATE TABLE "{table_name}" (
	# "offer_id"	INTEGER NOT NULL PRIMARY KEY,
	# "city"	TEXT,
	# "region"	TEXT,
	# "model"	TEXT,
	# "year"	INTEGER,
	# "mileage"	INTEGER,
	# "fuel_type"	TEXT,
	# "displacement"	INTEGER,
	# "price"	INTEGER,
	# "currency"	TEXT,
	# "pub_date"	TEXT,
	# "duration"	INTEGER,
	# "end_price"	INTEGER
    # );""".format(table_name=table_name)

    # car_table
    # car_table_sql ="""CREATE TABLE "{table_name}" (
	# "offer_id"	INTEGER NOT NULL PRIMARY KEY,
	# "user_id"	INTEGER,
	# "UID" TEXT,
	# "private_business"	TEXT,
	# "city"	TEXT,
	# "region"	TEXT,
	# "make"	TEXT,
	# "model"	TEXT,
	# "year"	INTEGER,
	# "mileage"	INTEGER,
	# "engine_code" TEXT,
	# "displacement"	INTEGER,
	# "vin" TEXT,
	# "fuel_type"	TEXT,
	# "engine_power" INTEGER,
	# "gearbox" TEXT,
	# "transmission" TEXT,
	# "body_type" TEXT
	# "door_count" INTEGER,
	# "nr_seats" INTEGER
	# "colour" TEXT,
	# "features" TEXT,
	# "price_raw"	INTEGER,
	# "currency"	TEXT,
	# "country_origin"	TEXT,
	# "registration" TEXT,
	# "pub_date"	TEXT,
	# "duration"	INTEGER,
	# "end_price"	INTEGER
    # );""".format(table_name=table_name)

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


database = 'pythonsqlite.db'

     # create a database connection

create_users = '''
    INSERT INTO
    cars (offer_id,city,region,model,year,mileage,fuel_type,displacement,price,currency,pub_date,duration,end_price)
    VALUES
    (6069449316,'Prudnik','Opolskie','Toyota Yaris II',2009,153000,'Diesel',-1,12999,'PLN','2019-12-31',7,12999),
    (6068202189,'Włocławek','Kujawsko-pomorskie','Toyota Yaris II',2008,110000,'Benzyna',1298,17600,'PLN','2019-12-31',21,16900),
    '''
def get_tables_list():
    db = sqlite3.connect('pythonsqlite.db')
    table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", db)

    pdToList = list(table['name'])
    # print(table['name'])
    #print(pdToList)
    return pdToList

def merge_tables():
    #tables = get_tables_list()
    conn = create_connection('pythonsqlite.db')
    table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    pdToList = list(table['name'])


    for f in pdToList:
        if f != "mtable":
            print(f)
            execute_query(conn, """INSERT INTO mtable SELECT * FROM otomoto_2020-02-26;""")
            print (f +  ': done')



#conn = create_connection(database)
#create_table(conn, sql_create_table)
#execute_query(conn, create_users)
#merge_tables()


# https://stackoverflow.com/questions/14303573/join-two-different-tables-and-remove-duplicated-entries

# CREATE TABLE car_XXXXXXXXX (
# 	"offer_id"	INTEGER NOT NULL PRIMARY KEY,
# 	"user_id"	INTEGER,
# 	"UID" TEXT,
# 	"private_business"	TEXT,
# 	"city"	TEXT,
# 	"region"	TEXT,
# 	"make"	TEXT,
# 	"model"	TEXT,
# 	"year"	INTEGER,
# 	"mileage"	INTEGER,
# 	"engine_code" TEXT,
# 	"displacement"	INTEGER,
# 	"vin" TEXT,
# 	"fuel_type"	TEXT,
# 	"engine_power" INTEGER,
# 	"gearbox" TEXT,
# 	"transmission" TEXT,
# 	"body_type" TEXT
# 	"door_count" INTEGER,
# 	"nr_seats" INTEGER
# 	"colour" TEXT,
# 	"features" TEXT,
# 	"price_raw"	INTEGER,
# 	"currency"	TEXT,
# 	"country_origin"	TEXT,
# 	"registration" TEXT,
# 	"pub_date"	TEXT,
# 	"duration"	INTEGER,
# 	"end_price"	INTEGER
#     );


# CREATE TABLE otomoto_DATE (
# 	"offer_id"	INTEGER NOT NULL PRIMARY KEY,
# 	"city"	TEXT,
# 	"region"	TEXT,
# 	"model"	TEXT,
# 	"year"	INTEGER,
# 	"mileage"	INTEGER,
# 	"fuel_type"	TEXT,
# 	"displacement"	INTEGER,
# 	"price"	INTEGER,
# 	"currency"	TEXT,
# 	"pub_date"	TEXT,
# 	"duration"	INTEGER,
# 	"end_price"	INTEGER
#     );