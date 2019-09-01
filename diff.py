import pandas

names = ['IDX','Price','City', 'Region', 'Model', 'Year', 'Mileage', 'Displacement', 'Petrol', 'Start', 'Duration', 'EndPrice']
df1 = pandas.read_csv('_ALL.csv',skiprows = 1, 
                  index_col=False, 
                  names = names)
print(df1)

i=0

df2 = pandas.read_csv('_NEW.csv',skiprows = 1, 
                  index_col=False, 
                  names = names)

for counter, row in df1.iterrows():
    df1_IDX = row['IDX']
    i=i+1

    for index, row in df2.iterrows():
        if (df1_IDX == row['IDX']):
            counter = df1.iloc[i-1,9]
            print(df2.iloc[i-1,1]) 
            inc_counter= counter+1
            
            df1.at[i-1, 'Duration'] = inc_counter
            df1.at[i-1, 'EndPrice'] = df2.iloc[index,1]


print(df1)