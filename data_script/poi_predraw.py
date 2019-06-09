import json
from IPython import embed
filename = "data/poi.json"

with open(filename, 'r') as f:
    poi_raw = json.load(f)

poi_raw[0]
