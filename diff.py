import pandas, sys, time

start = time.time()

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

#sys.exit()

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

#df4['Duration'].fillna(0) 
#df4.fillna(0, inplace=True) 

for counter, row in df4.iterrows():
    df4_IDX = row['IDX']
    i=i+1
    print(counter)

    for index, row in df2.iterrows():
        if (df4_IDX == row['IDX']):
            #print(df4.at[i-1, 'Duration']+1) 
            
            df4.at[i-1, 'Duration'] = df4.iloc[i-1,10] + 1 # increase day counter
            df4.at[i-1, 'EndPrice'] = df2.iloc[index,1] # assign last price from today file

#print('DF4')
#print (df4.dtypes)
#print(df4)

export_csv = df4.to_csv (r'.\dataframe2.csv', index = None, header=True, encoding="utf-8") #Don't forget to add '.csv' at the end of the path

end = time.time()
print(end - start)