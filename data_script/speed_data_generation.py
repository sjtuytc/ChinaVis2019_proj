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

output_path = "./data/speed_data_thre%.1f.json" % (lower_bound)

# MAIN PROGRAM
all_speed_data = collections.OrderedDict()
all_speed_data["longitude_start"] = longitude_start
all_speed_data["longitude_end"] = longitude_end
all_speed_data["latitude_start"] = latitude_start
all_speed_data["latitude_end"] = latitude_end
all_speed_data["time_unit"] = time_unit
all_speed_data["data"] = collections.OrderedDict()


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



with open(data_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # 进度提示
        print(n)
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
            order_data["avg_time"] = avg(order_data["avg_time"], order_data["count"], time)
            order_data["avg_longitude"] = avg(order_data["avg_longitude"], order_data["count"], longitude)
            order_data["avg_speed"] = avg(order_data["avg_speed"], order_data["count"], cur_speed)
            if cur_speed > order_data["max_speed"]:
                order_data["max_speed"] = cur_speed
            if cur_speed < order_data["min_speed"]:
                order_data["min_speed"] = cur_speed
            order_data["count"] += 1
        else: #记录当前order
            cur_speed = -1
            if not order_data["start_flag"]:
                all_order.append(order_data)
            n+=1
            order_data = collections.OrderedDict()
            order_data["start_flag"] = False
            order_data["order"] = order
            order_data["avg_time"] = time
            order_data["avg_longitude"] = longitude
            order_data["avg_latitude"] = latitude
            order_data["max_speed"] = -1
            order_data["min_speed"] = 1000
            order_data["avg_speed"] = 0
            order_data["count"] = 0
        pre_order = order
        pre_time = time
        pre_long = longitude
        pre_lat = latitude

print("lower bound", lower_bound, "higher bound",higher_bound, "total", n, "miss number", miss)

for order_data in all_order:
    time_label = int(order_data["avg_time"]/time_unit)*time_unit
    cur_speed = order_data["avg_speed"]
    if time_label in all_speed_data["data"].keys():
        cur_count = all_speed_data["data"][time_label]["count"]
        all_speed_data["data"][time_label]["average_speed"] = \
            avg(all_speed_data["data"][time_label]["average_speed"], cur_count, cur_speed)
        all_speed_data["data"][time_label]["count"] += 1
    else:
        all_speed_data["data"][time_label] = collections.OrderedDict()
        all_speed_data["data"][time_label]["count"] = 1
        all_speed_data["data"][time_label]["average_speed"] = cur_speed

# 按时间排序
all_speed_data["data"] = collections.OrderedDict(sorted(all_speed_data["data"].items(), key=lambda t: t[0]))
# embed()
with open(output_path,'w') as writer:
    writer.write(json.dumps(all_speed_data))

#         # 速度信息
#         if cur_speed > 0 and cur_register!= pre_registered: #记录当前速度
#             pre_registered = order
#             if time_label in all_speed_data["data"].keys():
#                 cur_count = all_speed_data["data"][time_label]["count"]
#                 all_speed_data["data"][time_label]["average_speed"] = \
#                 (all_speed_data["data"][time_label]["average_speed"] * cur_count + cur_speed) \
#                 / (cur_count + 1)
#                 all_speed_data["data"][time_label]["count"] += 1
#
#             else: #增加time_label
#                 all_speed_data["data"][time_label] = collections.OrderedDict()
#                 all_speed_data["data"][time_label]["count"] = 1
#                 all_speed_data["data"][time_label]["average_speed"] = cur_speed
#
#         pre_order = order
#
#         pre_time_label = time_label
#         pre_label = label
#         pre_time = time
#         pre_lat = latitude
#         pre_long = longitude
#
# print("thre", thre, "total", n, "miss number", miss)
#

