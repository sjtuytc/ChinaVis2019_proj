"""
这个文件用来统计不同区域一天中流量岁时间的变化情况
输入数是是轨迹数据："./data/1.txt"
输出数据:"./data/area_data_timeunit?_latunit?_longunit?.json"
其中timeunit表示统计时间单元的长度，latunit表示单位区域的纬度间隔，longunit表示单位区域的经度间隔

每个输出的json文件格式为
{
    "longitude_start": ,
    "longitude_end": ,
    "latitude_start": ,
    "latitude_end": ,
    "longitude_unit": ,
    "latitude_unit": ,
    "time_unit": ,
    "data":{
                "launit_longunit":{
                                        "start_time":{
                                                        "count": ,
                                                        "value":[{"order":,"time":,"longitude":,"latitude":}]
                                                        }
                                    }
            }
}
launit and longunit 表示 从小的经纬度到开始的第几个区域，计算方式：
launit = int((latitude-latitude_start)/latitude_unit)
longunit = int((longitude-longitude_start)/longitude_unit)
第一个区域为"0_0"
start_time = int(time/time_unit)*time_unit

mini文件
{
    "longitude_start": ,
    "longitude_end": ,
    "latitude_start": ,
    "latitude_end": ,
    "longitude_unit": ,
    "latitude_unit": ,
    "time_unit": ,
    "data":{
                "launit_longunit":{
                                        "start_time": count
                                    }
            }
}
"""

import math
import json
import collections
from IPython import embed
from utils import *
import numpy as np

# PARAMETER
data_path = "./data/1.txt"
time_unit = 3600
latitude_unit = 0.001
longitude_unit = 0.001
latitude_start = 30.409
latitude_end = 30.510
longitude_start = 103.984
longitude_end = 104.061
center_long = 104.061
center_lat = 30.510
lower_bound = 1.0
higher_bound = 10.0
start_time = 1525104000
end_time = 1525190340

output_path = "./data/speed_scatter.json"

# MAIN PROGRAM
all_speed_data = []
speed_grid = np.zeros((200,90))

# VATIABLES INITIALIZATION
pre_registered = ""
cur_register = ""
pre_order = ""
pre_time_label = 0
pre_label = ""
pre_time = 0
pre_lat = 0.0
pre_long = 0.0
cur_speed = -1
n=0
sample_interval = 10
miss = 0
order_data = collections.OrderedDict()
order_data["start_flag"] = True
all_order = []

with open(data_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # 进度提示
        print(n)
        n +=1

        # if n%sample_interval!=0: continue
        t = line.strip('\n').split(',')
        order = t[0]
        time = int(t[1])
        latitude = float(t[3])
        longitude = float(t[2])
        time_label = int(time/time_unit)*time_unit
        latitude_label = int((latitude-latitude_start)/latitude_unit)
        longitude_label = int((longitude-longitude_start)/longitude_unit)
        label = str(latitude_label) + "_" + str(longitude_label)
        cur_register = order

        # 判断离中心距离
        dis = getDistance(latitude, longitude, center_lat, center_long)
        # print(dis)
        if not lower_bound < dis < higher_bound:
            miss +=1
            continue

        # 是同一个order
        if order == pre_order:
            dis = getDistance(latitude, longitude, pre_lat, pre_long) # 单位km
            time_interval = time - pre_time
            cur_speed = dis / time_interval * 1000 * 3.6 #单位km/h
        else: #记录当前order
            cur_speed = -1
        if cur_speed != -1 and cur_speed<90 and cur_speed>0:
            time_idx = int((time-start_time)/(end_time-start_time)*199)
            speed_idx = int((cur_speed-90)/90*89)
            # all_speed_data.append([time*1000, cur_speed])
            speed_grid[time_idx][speed_idx] +=1

        pre_order = order
        pre_time = time
        pre_long = longitude
        pre_lat = latitude


# smooth
smooth_speed_grid = np.zeros((200, 90))
for i in range(200):
    for j in range(90):
        for shifti in range(max(i - 1, 0), min(i + 1, 199)):
            for shiftj in range(max(j-2,0), min(j+2, 89)):
                smooth_speed_grid[i][j]+=speed_grid[shifti][shiftj]

# normalize
print("before normalize; max, min, mean ", np.max(smooth_speed_grid), np.min(smooth_speed_grid), np.mean(speed_grid))
for i in range(200):
    for j in range(90):
        if smooth_speed_grid[i][j]>np.mean(smooth_speed_grid):
            _range = np.max(smooth_speed_grid) - np.mean(smooth_speed_grid)
            smooth_speed_grid[i][j] = (smooth_speed_grid[i][j]-np.mean(smooth_speed_grid))/_range +0.5
        else:
            _range = np.mean(smooth_speed_grid) - np.min(smooth_speed_grid)
            smooth_speed_grid[i][j] = (smooth_speed_grid[i][j] - np.mean(smooth_speed_grid)) / _range + 0.5
print("max, min, mean", np.max(smooth_speed_grid), np.min(smooth_speed_grid), np.mean(smooth_speed_grid))

# clip in [0,1]
smooth_speed_grid = np.clip(smooth_speed_grid, 0, 1)
send_data = []
for i in range(200):
    for j in range(90):
        send_data.append([i,j, smooth_speed_grid[i][j]])
with open(output_path,'w') as writer:
    writer.write(json.dumps(send_data))