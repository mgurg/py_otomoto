import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt
from timeit import default_timer as timer

# Necessary to run script on VM machine
import os
def openblas_setup():
    # incorrect cpu detection in openblas

    # https://github.com/numpy/numpy/issues/11517
    # https://github.com/xianyi/OpenBLAS/issues/2306
    # OPENBLAS_CORETYPE=Sandybridge
    # OPENBLAS_CORETYPE=prescott
    os.environ["OPENBLAS_CORETYPE"] ="Sandybridge"
    #os.environ["OPENBLAS_CORETYPE"] = "prescott"
    #os.environ["OMP_NUM_THREADS"] = "1"
    #os.environ["OPENBLAS_VERBOSE"] =2
    p = os.getenv("OPENBLAS_CORETYPE")
    print(p)

def get_sqlite_data():
    sql_query ="""SELECT * FROM v_cars;"""
    conn = sqlite3.connect("pythonsqlite.db")
    data = pd.read_sql_query(sql_query, conn)
    conn.close()
    return data

def optimize_df():
    #df['offer_id'] = df['offer_id'].astype(np.uint32)
    df['offer_id'] = pd.to_numeric (df['offer_id'], downcast='unsigned')
    df['s_date'] = pd.to_datetime(df['s_date'])
    df['e_date'] = pd.to_datetime(df['e_date'])
    df['year'] = pd.to_numeric(df['year'], downcast='unsigned')
    df['mileage'] = pd.to_numeric(df['mileage'], downcast='unsigned')
    df['engine_capacity'] = pd.to_numeric(df['engine_capacity'], downcast='unsigned')
    df['engine_power'] = pd.to_numeric(df['engine_power'], downcast='unsigned')
    df['door_count'] = pd.to_numeric(df['door_count'], downcast='unsigned')
    df['nr_seats'] = pd.to_numeric(df['nr_seats'], downcast='unsigned')
    df['price'] = pd.to_numeric(df['price'], downcast='float')
    df['price_raw'] = pd.to_numeric(df['price_raw'], downcast='float')

#car features
def benefits_to_set(value):
    if str(value) == 'nan': return set(["nan"])
    return {attr.lower().strip() for attr in value}

def norm_name(name):
    return 'f_{0}'.format( name.lower().strip() )

def feature_columns():
    benefits_series = df['features'].str.split(' ').map(benefits_to_set)
    all_benefits = {benefit for row in benefits_series for benefit in row}

    feat_names = [norm_name(x) for x in all_benefits]

    for benefit in all_benefits:
        df[ norm_name(benefit) ] = benefits_series.map(lambda x: benefit in x).astype(np.int8)

    return feat_names

def general_features():
    df['duration'] = (df['e_date'] - df['s_date']).dt.days.astype(np.uint16)
    df['price_chng'] = (df['price'] - df['price_raw'])


# --- IMG ---
def plot_year():
    year_list = df['year'].unique()

    x = []
    y = []
    for i in year_list:
        x.append(i)
        y.append(df[df['year'] == i ].shape[0])

    sdf = pd.DataFrame(dict(x=x, y=y)).sort_values(by=['x'])

    sns.set_style("darkgrid")
    sns.set_context("talk")
    plt.figure(figsize=(20,6))
    ax = sns.barplot(x=x, y=y, data=sdf, palette=("YlGnBu"))
    ax.set(xlabel='rocznik', ylabel='liczba ogłoszeń')

    plt.savefig('./img/sns_year.png')

def num_test():
    A = np.matrix([[1.], [3.]])
    B = np.matrix([[2., 3.]])
    l =np.dot(A, B)
    #print('np: ',np.__version__)
    #print(np.show_config())
    print(l)

def general():
    df.hist(bins=50,figsize=(20,15))
    plt.savefig('./img/0.png', bbox_inches='tight')
    plt.close('all')

def displacement():
    disp_counter = df['displacement'].nunique()
    df['displacement'].hist(bins=disp_counter,figsize=(20,5))
    plt.savefig('./img/displacement.png', bbox_inches='tight')
    plt.close('all')


def duration():
    offer_duration = df['duration'].max()
    df['duration'].hist(bins=offer_duration,figsize=(20,5))
    plt.savefig('./img/duration.png', bbox_inches='tight')
    plt.close('all')

def mileage():
    ## 99 percentile
    df_mileage = df[df['mileage'] < np.percentile(df['mileage'],99)]
    df_mileage['mileage'].hist(bins=150,figsize=(20,5))
    plt.savefig('./img/mileage.png', bbox_inches='tight')
    plt.close('all')

if __name__ == "__main__":
    start = timer()
    openblas_setup()

    df = get_sqlite_data()
    optimize_df()

    general_features()
    feature_columns()

    plot_year()
    #num_test()

    #general()
    #displacement()
    #duration()
    #mileage()

    end = timer()
    print(end - start)


