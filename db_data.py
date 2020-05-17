import sqlite3
import os
from sqlite3 import Error
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

# create a default path to connect to and create (if necessary) a database
# called 'pythonsqlite.db' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), cfg['development']['database'])

def create_connection(db_path=DEFAULT_PATH):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
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

def fetch_all_data(connection, sql_query):
    c = connection.cursor()
    c.execute(sql_query)
    db_data = c.fetchall()
    return  db_data

def fetch_single_item(connection, sql_query):
    # https://towardsdatascience.com/python-sqlite-tutorial-the-ultimate-guide-fdcb8d7a4f30
    c = connection.cursor()
    c.execute(sql_query)
    cnt = c.fetchone()
    return cnt

def fetch_db_data(connection, sql_query, all:bool):
    c = connection.cursor()
    c.execute(sql_query)
    if all == True:
        db_data = c.fetchall()
    else:
        db_data = c.fetchone()
    return  db_data
