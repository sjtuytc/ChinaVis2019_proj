from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import Response
import csv
import json
import math
import pandas as pd
import collections
import numpy as np
from IPython import embed

app = Flask(__name__)

start_path = './data/start.csv'
end_path = './data/end.csv'
data_start = pd.read_csv(start_path)
data_end = pd.read_csv(end_path)

start_time = 1525104120
end_time = 1525193987
gap = 900

latitude_unit = 0.001
longitude_unit = 0.001
latitude_start = 30.409
latitude_end = 30.510
longitude_start = 103.984
longitude_end = 104.061


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_scatter_speed/', methods=['GET'])
def get_scatter_speed():
    data_path = "data/speed_scatter.json"
    with open(data_path, 'r') as f:
        send_data = json.load(f)
    # embed()
    return json.dumps(send_data)

@app.route('/get_speed/', methods=['GET'])
def get_speed():
    send_data = {}
    time_unit = request.args.get('time_unit', type=int, default=600)
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    prefix = "./data/speed_data_thre"
    postfix = ".json"
    for tempstr in ['0.0','0.3','1.0']:
        data_path = prefix + tempstr + postfix

        with open(data_path, 'r') as f:
            data = json.load(f)

            overall_count = 0
            send_data[tempstr] = []
            for key in data["data"].keys():
                overall_count += data["data"][key]['count']
                if data["data"][key]['count'] <3: continue
                send_data[tempstr].append({'time':key,'value':[key,data["data"][key]['average_speed']]})
        # embed()
    return json.dumps(send_data)

@app.route('/get_data_flow', methods=['GET'])
def get_data_flow():
    flow_data_path = "./data/flow_data.json"
    with open(flow_data_path, 'r') as f:
        flow_data = json.load(f)
    want_time = request.args.get('time_unit', type=int, default=start_time)
    time_unit = 1800
    time_label = int(want_time/time_unit)*time_unit
    print(time_label) #1525104120 gap:900
    # embed()
    return json.dumps(flow_data[str(time_label)],cls=NumpyEncoder)

@app.route('/get_flow/', methods=['GET'])
def get_flow():
    time_unit = request.args.get('time_unit', type=int, default=600)
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    data_path = "./data/area_data_timeunit%d_latunit%.6f_longunit%.6f_mini.json" % (time_unit, latitude_unit, longitude_unit)

    latitude_label = int((latitude - latitude_start) / latitude_unit)
    longitude_label = int((longitude - longitude_start) / longitude_unit)
    area = str(latitude_label) + "_" + str(longitude_label)

    with open(data_path, 'r') as f:
        data = json.load(f)
        if area in data["data"].keys():
            _send_data = data["data"][area]
        else:
            _send_data = {}
        send_data = []
        for key in _send_data.keys():
            send_data.append({'time':key,'value':[key,_send_data[key]]})

    return json.dumps(send_data)

@app.route('/get_street_flow/', methods=['GET'])
def get_street_flow():
    time_unit = request.args.get('time_unit', type=int, default=600)
    street = request.args.get('street', type=str)
    data_path = "./data/street-time-mini-per%d.json" % time_unit

    with open(data_path, 'r') as f:
        data = json.load(f)
        if street in data.keys():
            _send_data = data[street]
        else:
            _send_data = {}
        send_data = []
        for key in _send_data.keys():
            send_data.append({'time':key,'value':[key,_send_data[key]]})

    return json.dumps(send_data)


if __name__ == '__main__':
    app.run(debug=True)