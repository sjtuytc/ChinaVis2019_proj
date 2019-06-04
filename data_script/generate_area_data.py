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


import json
import collections
from IPython import embed

# hyper parameter
data_path = "./data/1.txt"
time_unit = 600
latitude_unit = 0.001
longitude_unit = 0.001
latitude_start = 30.409
latitude_end = 30.510
longitude_start = 103.984
longitude_end = 104.061
output_path = "./data/area_data_timeunit%d_latunit%.6f_longunit%.6f.json" % (time_unit, latitude_unit, longitude_unit)
output_mini_path = "./data/area_data_timeunit%d_latunit%.6f_longunit%.6f_mini.json" % (time_unit, latitude_unit, longitude_unit)

# code
all_area_data  = collections.OrderedDict()
all_area_data["longitude_start"] = longitude_start
all_area_data["longitude_end"] = longitude_end
all_area_data["latitude_start"] = latitude_start
all_area_data["latitude_end"] = latitude_end
all_area_data["longitude_unit"] = longitude_unit
all_area_data["latitude_unit"] = latitude_end
all_area_data["time_unit"] = time_unit
all_area_data["data"] = collections.OrderedDict()

all_area_data_mini  = collections.OrderedDict()
all_area_data_mini["longitude_start"] = longitude_start
all_area_data_mini["longitude_end"] = longitude_end
all_area_data_mini["latitude_start"] = latitude_start
all_area_data_mini["latitude_end"] = latitude_end
all_area_data_mini["longitude_unit"] = longitude_unit
all_area_data_mini["latitude_unit"] = latitude_end
all_area_data_mini["time_unit"] = time_unit
all_area_data_mini["data"] = collections.OrderedDict()


pre_order = ""
pre_time_label = 0
pre_label = ""

n=0
with open(data_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # 进度提示
        print(n)
        n+=1

        t = line.strip('\n').split(',')
        order = t[0]
        time = int(t[1])
        latitude = float(t[3])
        longitude = float(t[2])
        time_label = int(time/time_unit)*time_unit
        latitude_label = int((latitude-latitude_start)/latitude_unit)
        longitude_label = int((longitude-longitude_start)/longitude_unit)
        label = str(latitude_label) + "_" + str(longitude_label)

        # 车还没从已统计的区域出来
        if order==pre_order and time_label==pre_time_label and label==pre_label:
            continue

        order_data = collections.OrderedDict()
        order_data["order"] = order
        order_data["time"] = time
        order_data["longitude"] = longitude
        order_data["latitude"] = latitude

        if label in all_area_data["data"].keys():
            if time_label in all_area_data["data"][label].keys():
                all_area_data["data"][label][time_label]["count"] += 1
                all_area_data["data"][label][time_label]["value"].append(order_data)
                all_area_data_mini["data"][label][time_label] += 1
            else:
                all_area_data["data"][label][time_label] = collections.OrderedDict()
                all_area_data["data"][label][time_label]["count"] = 1
                all_area_data["data"][label][time_label]["value"] = [order_data]
                all_area_data_mini["data"][label][time_label] = 1

        else:
            all_area_data["data"][label] = collections.OrderedDict()
            all_area_data["data"][label][time_label] = collections.OrderedDict()
            all_area_data["data"][label][time_label]["count"] = 1
            all_area_data["data"][label][time_label]["value"] = [order_data]
            all_area_data_mini["data"][label] = collections.OrderedDict()
            all_area_data_mini["data"][label][time_label] = 1

        pre_order = order
        pre_time_label = time_label
        pre_label = label

# 按时间排序
for area in all_area_data["data"].keys():
    all_area_data["data"][area] = collections.OrderedDict(sorted(all_area_data["data"][area].items(), key=lambda t: t[0]))
    all_area_data_mini["data"][area] = collections.OrderedDict(sorted(all_area_data_mini["data"][area].items(), key=lambda t: t[0]))


with open(output_path,'w') as writer:
    writer.write(json.dumps(all_area_data))

with open(output_mini_path,'w') as writer:
    writer.write(json.dumps(all_area_data_mini))