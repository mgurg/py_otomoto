import pandas

names = ['IDX','Price','City', 'Region', 'Model', 'Year', 'Mileage', 'Displacement', 'Petrol', 'Start', 'Duration', 'EndPrice']
df1 = pandas.read_csv('dataframe.csv',skiprows = 1, 
                  index_col=False, 
                  names = names, 
                  encoding='utf-8')
print(df1)


i=0

df2 = pandas.read_csv('_NEW.csv',skiprows = 1, 
                  index_col=False, 
                  names = names, 
                  encoding='utf-8')

df1["Duration"].fillna(0) 
print (df1.dtypes)

for counter, row in df1.iterrows():
    df1_IDX = row['IDX']
    i=i+1

    for index, row in df2.iterrows():
        if (df1_IDX == row['IDX']):
            print(df1.iloc[i-1,10]) 
            
            df1.at[i-1, 'Duration'] = df1.iloc[i-1,10] + 1 # increase day counter
            df1.at[i-1, 'EndPrice'] = df2.iloc[index,1] # assign last price from today file


export_csv = df1.to_csv (r'.\dataframe.csv', index = None, header=True, encoding="utf-8") #Don't forget to add '.csv' at the end of the path

print(df1)