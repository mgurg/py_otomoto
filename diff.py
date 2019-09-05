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

# ---------- SQLite ----------

start = time.time()

# file1 ='_ALL.csv'
# file2 ='_NEW.csv' 

file1 ='current.csv'
file2 ='Data_2019-09-04.csv' 

names = ['IDX','Price','City', 'Region', 'Model', 'Year', 'Mileage', 'Displacement', 'Petrol', 'Start', 'Duration', 'EndPrice']
df1 = pandas.read_csv(file1,skiprows = 1, 
                  index_col=False, 
                  names = names, 
                  encoding='utf-8')

df2 = pandas.read_csv(file2,skiprows = 1, 
                  index_col=False, 
                  names = names, 
                  encoding='utf-8')

i=0

#-----------START OPTIMISATION-----------

# df1.to_sql(name='projects', index=False, con=conn, if_exists='replace')
# sys.exit()

#-----------END OPTIMISATION-----------

df2['Start']='2019-09-04' # or: print(file2[5:15])

df3 = pandas.DataFrame(pandas.concat([df1, df2], ignore_index=True))
df3 = df3.drop_duplicates(subset=['IDX'])

df3['Start'].fillna(0) 
df3['Duration'].fillna(0) 

export_csv = df3.to_csv (r'.\dataframe.csv', index = None, header=True, encoding="utf-8") #Don't forget to add '.csv' at the end of the path

print('DF3')
print(df3) 

df4 = pandas.read_csv('dataframe.csv',skiprows = 1, 
                  index_col=False, 
                  names = names, 
                  encoding='utf-8')

for j, row in enumerate(df4.itertuples(), 1):
    df4_IDX = row.IDX
    i=i+1
    print(j)

    for k, row in enumerate(df2.itertuples(), 1):
        if (df4_IDX == row.IDX):
            
            df4.at[i-1, 'Duration'] = df4.iloc[i-1,10] + 1 # increase day counter
            df4.at[i-1, 'EndPrice'] = df2.iloc[k-1,1] # assign last price from today file

#print('DF4')
#print (df4.dtypes)
#print(df4)

export_csv = df4.to_csv (r'.\dataframe2.csv', index = None, header=True, encoding="utf-8") #Don't forget to add '.csv' at the end of the path


df4.to_sql(name='projects', index=False, con=conn, if_exists='replace')

end = time.time()
print(end - start)




