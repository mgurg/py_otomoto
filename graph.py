import pandas, sys, time
import sqlite3

# ---------- SQLite ----------

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

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

database = "data\mydb.db3"
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                    id integer PRIMARY KEY,
                                    price integer,
                                    city text,
                                    region text,
                                    model text,
                                    year integer,
                                    mileage integer,
                                    displacement integer,
                                    petrol text,
                                    start text,
                                    duration integer,
                                    endPrice integer
                                    ); """

# create a database connection
conn = create_connection(database)
 
# create tables
if conn is not None:
    # create table
    create_table(conn, sql_create_projects_table)
 
else:
    print("Error! cannot create the database connection.")


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE year=2008")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


select_all_tasks(conn)

# ---------- SQLite ----------





