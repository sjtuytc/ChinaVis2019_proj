"""
这个文件用来统计不同区域一天中流量随时间的变化情况
输入数是是轨迹数据："./data/1.txt"
输出数据:"./data/area_data_timeunit?_latunit?_longunit?.json"
其中timeunit表示统计时间单元的长度，latunit表示单位区域的纬度间隔，longunit表示单位区域的经度间隔

"""

import math
import json
import collections
from IPython import embed
from utils import *
import operator
import requests
import pickle
import os

# PARAMETER
data_path = "./data/1.txt"
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
time_unit = 1800
# output_path = "./data/flow_data_time_unit%.1f.json" % (time_unit)
output_path = "./data/flow_data.json"
flow_pickle = "./data/flow_pkl.pk"

all_flow_data = collections.OrderedDict()
# MAIN PROGRAM

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
miss = 0
order_data = collections.OrderedDict()
order_data["start_flag"] = True
all_order = []

sample_interval = 100
if not os.path.exists(flow_pickle):
    with open(data_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 进度提示
            n += 1
            # if n>1000: break
            print(n)
            if n % sample_interval != 0: continue
            t = line.strip('\n').split(',')
            order = t[0]
            time = int(t[1])
            latitude = float(t[3])
            longitude = float(t[2])
            time_label = int(time/time_unit)*time_unit
            # latitude_label = int((latitude-latitude_start)/latitude_unit)
            # longitude_label = int((longitude-longitude_start)/longitude_unit)
            # label = str(latitude_label) + "_" + str(longitude_label)

            if time_label not in all_flow_data.keys():
                all_flow_data[time_label] = []
            else:
                all_flow_data[time_label].append([longitude, latitude])
    with open(flow_pickle, 'wb+') as f:
        pickle.dump(all_flow_data, f)
else:
    with open(flow_pickle, 'rb+') as f:
        all_flow_data = pickle.load(f)

batch_counter = 0
temperal_string = ""

pre = "http://api.map.baidu.com/geoconv/v1/?coords="
post = "&from=3&to=5&ak=c6pIzPd8WxIKNAb3HxWSpboGhsS1ErDR"


def send_request(location_string, key_label):
    url = pre + location_string + post
    r = requests.get(url)
    dict = {}
    while r.status_code == 400:
        r = requests.get(url)
    dict = json.loads(r.text)
    # except:
    #     embed()
    converted_all = []
    # embed()
    if 'result' not in dict.keys():
        embed()
    for idx, location in enumerate(dict['result']):
        long = location['x']
        lat = location['y']
        converted_all.append([long,lat, key_label[idx]])
    return converted_all

batch_label = []
converted_flow_data = collections.OrderedDict()
for key in all_flow_data.keys():
    converted_flow_data[key] = []
    for item in all_flow_data[key]:
        if batch_counter < 100:
            batch_counter += 1
            batch_label.append(key)
            if temperal_string == "":
                temperal_string += str(item[0]) + "," + str(item[1])
            else:
                temperal_string += ";" + str(item[0]) + "," + str(item[1])
        else:
            converted = send_request(temperal_string, batch_label)
            for converted_item in converted:
                converted_flow_data[converted_item[2]].append([converted_item[0], converted_item[1]])
            batch_counter = 0
            temperal_string = ""
            batch_label = []
if temperal_string != "":
    converted = send_request(temperal_string, batch_label)
    for converted_item in converted:
        converted_flow_data[converted_item[2]].append([converted_item[0], converted_item[1]])

for key in all_flow_data.keys():
    print(key, "total", len(converted_flow_data[key]))
embed()


with open(output_path,'w') as writer:
    writer.write(json.dumps(converted_flow_data))