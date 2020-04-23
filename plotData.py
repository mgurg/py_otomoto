import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from timeit import default_timer as timer

# Necessary to run script on VM machine
import os
def setup():
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


df = pd.read_csv('./my_df.csv')


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
    setup()
    num_test()

    general()
    displacement()
    duration()
    mileage()

    end = timer()
    print(end - start)


