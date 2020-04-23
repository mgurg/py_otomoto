import sqlite3
import os
from sqlite3 import Error

# create a default path to connect to and create (if necessary) a database
# called 'pythonsqlite.db' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'pythonsqlite.db')

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



