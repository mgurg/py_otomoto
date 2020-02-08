import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('./my_df.csv')

data.hist(bins=50,figsize=(20,15))

plt.savefig('foo.png', bbox_inches='tight')
#plt.savefig('foo.pdf')
#
#
