import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from timeit import default_timer as timer

start = timer()
df = pd.read_csv('./my_df.csv')

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

general()
displacement()
duration()
mileage()

end = timer()
print(end - start)