import pandas, sys, time, random
from matplotlib import pyplot as plt
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


def select_all_tasks(conn, year):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT price FROM projects WHERE year=?", (year,)) # average price
    # cur.execute("SELECT price FROM projects WHERE year=?", (year,))
 
    rows = cur.fetchall()

    #print(min(rows))

    # for row in rows:
    #     #print(row)
    #     print('Histogram')


select_all_tasks(conn, 2008)


# ------ HISTOGRAM -----

random.seed(1)

def count_elements(seq) -> dict:
     """Tally elements from `seq`."""
     hist = {}
     for i in seq:
         hist[i] = hist.get(i, 0) + 1
     return hist

def ascii_histogram(seq) -> None:
    """A horizontal frequency-table/histogram plot."""
    counted = count_elements(seq)
    for k in sorted(counted):
        print('{0:5d} {1}'.format(k, '+' * counted[k]))

vals = [2000, 3000, 4000, 5000, 6000, 700, 8000, 9000, 10000,11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
# Each number in `vals` will occur between 5 and 15 times.
freq = [0,0,5,5,10, 15,15,15,15,15,1,5,15,5,0,0,0,0,0]
#freq = (random.randint(5, 15) for _ in vals)

#print(freq)

data = []
for f, v in zip(freq, vals):
    data.extend([v] * f)

ascii_histogram(data)



# plt.plot([0,1,2,3,4], label='y = x')
# plt.title('Y = X Straight Line')
# plt.ylabel('Y Axis')
# plt.yticks([1,2,3,4])
# plt.legend(loc = 'best')
# plt.show()

# ---------- SQLite ----------





