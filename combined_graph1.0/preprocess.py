import json
import pandas as pd
import numpy as np

data_path = './data/raw_data.txt'
data = []
for line in open(data_path,"r"):
    data.append(line)

start = np.zeros([len(data),3])
end = np.zeros([len(data),3])
min_start=data[0].split(',')[1]
max_start=0
min_end=data[0].split(',')[2]
max_end=0
for i in range(len(data)):
    a = data[i].split(',')
    start[i][0] = a[1]
    end[i][0] = a[2]
    start[i][1:3] = a[3:5]
    end[i][1:3] = a[5:7]
    if a[1]>max_start:
        max_start = a[1]
    if a[1]<min_start:
        min_start = a[1]
    if a[2]>max_end:
        max_end = a[2]
    if a[2]<min_end:
        min_end = a[2]

print(min_start)
print(max_start)
print(min_end)
print(max_end)

# pd.DataFrame(start).to_csv('./data/start.csv')
# pd.DataFrame(end).to_csv('./data/end.csv')


