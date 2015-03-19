import pandas as pd
o = open('data1_7.csv','rU')
data_set1 = pd.read_csv(o,engine='python')

o = open('filtered_data.csv','rU')
data_set2 = pd.read_csv(o,engine='python')
merged_data = pd.concat([data_set1,data_set2])
merged_data.to_csv('filtered_data.csv', index=False,encoding = 'utf-8')