import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
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



def main():
    database = 'pythonsqlite.db'
    sql_create_table = """ CREATE TABLE "cars" (
	"offer_id"	INTEGER NOT NULL,
	"city"	TEXT,
	"region"	TEXT,
	"model"	TEXT,
	"year"	INTEGER,
	"mileage"	INTEGER,
	"fuel_type"	TEXT,
	"displacement"	INTEGER,
	"price"	INTEGER,
	"currency"	TEXT,
	"pub_date"	TEXT,
	"duration"	INTEGER,
	"end_price"	INTEGER,
	PRIMARY KEY("offer_id")
    );"""
     # create a database connection

    create_users = """
    INSERT INTO
    cars (offer_id,city,region,model,year,mileage,fuel_type,displacement,price,currency,pub_date,duration,end_price)
    VALUES
    (6069449316,'Prudnik','Opolskie','Toyota Yaris II',2009,153000,'Diesel',-1,12999,'PLN','2019-12-31',7,12999);
    """


    conn = create_connection(database)
    create_table(conn, sql_create_table)
    execute_query(conn, create_users)

#------------------


main()