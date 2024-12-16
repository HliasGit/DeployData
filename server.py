import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import Caching as ch

from constants import *

import polars as pl


# Module with functions that manage requests for the heatmap
import HeatMapData

# Module with functions that manage requests for the histogram
import B2BHistData

import PieChartData
import ChordData


FIREWALL_FILE = 'firewall.csv'
IDS_FILE = 'ids.csv'

pl_ids_data = None
pl_fir_data = None

pl_fir_data_aggregated_by_time = None
pl_ids_data_aggregated_by_time = None

# Cache that contains aggregated data with paths to files
cache = {
    HIST_PATH: {
        "idx": set(),
        "data": {}
    },
    HEAT_PATH: {
        "idx": set(),
        "data": {}
    },
    TIME_PATH: {
        "idx": set(),
        "data": {}
    },
    PIE_PATH: {
        "idx": set(),
        "data": {}
    },
    CHORD_PATH: {
        "idx": set(),
        "data": {}
    }
}

def load_ids():
    return pl.read_csv(IDS_FILE)

def load_fir():
    return pl.read_csv(FIREWALL_FILE)


print("Initializing cache...")
ch.init(global_cache=cache)

print("Loading IDS data...")
pl_ids_data = load_ids()
print("Loading firewall data...")
pl_fir_data = load_fir()


# ========================================
# ========================================
# ========================================




app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    data = None
    from base64 import b64decode
    with open("input_string.txt", "r") as file:
        data = file.read()
        data = b64decode(data).decode("utf-8")
    
    return f"""
    {data}
    """                       

@app.route("/getHeatMapData")
def get_heatMapData():
    protocol_sel = "Generic Protocol Command Decode"
    data = HeatMapData.manage_heatmap_request(
        live_cache=cache,
        protocol=protocol_sel
    )
    return jsonify(data)

@app.route("/getPieChartData")
def get_pieChartData():
    data = PieChartData.manage_pie_chart_data(
        live_cache=cache
    )
    return jsonify(data)

@app.route("/getChordDiagramData")
def get_ChordDiagramData():
    data = ChordData.manage_chord_diagram_data(
        live_cache=cache
    )
    return jsonify(data)

@app.route("/getB2BHistData")
def get_b2bHistData():
    firewall_parameter = request.args.get('fir')
    ids_parameter = request.args.get('ids')
    start = request.args.get('start')
    end = request.args.get('end')
    
    bins = None
    try:
        bins = int(request.args.get('bins'))
    except:
        bins = None
    
    mode = request.args.get('mode')

    if firewall_parameter is None:
        firewall_parameter = B2BHistData.DEFAULT_FIR_CLASS
    
    if ids_parameter is None:
        ids_parameter = B2BHistData.DEFAULT_IDS_CLASS

    if bins is None:
        bins = B2BHistData.DEFAULT_HIST_BINS

    if mode is None:
        mode = 'count'

    data = B2BHistData.manage_request(
        firewall_parameter=firewall_parameter,
        ids_parameter=ids_parameter,
        bins=bins,
        live_cache=cache,
        glob_data_fir=pl_fir_data,
        glob_data_ids=pl_ids_data,
        mode=mode,
        start=start,
        end=end
    )
    return jsonify(data)

@app.route("/getHistoTimeLineData")
def get_histoTimeLineData():
    data = B2BHistData.manage_timeline_request(
        live_cache=cache,
        glob_data_fir=pl_fir_data,
        glob_data_ids=pl_ids_data
    )

    return jsonify(data)

if __name__ == "__main__":
    print("Initializing cache...")
    ch.init()

    print("Loading IDS data...")
    pl_ids_data = load_ids()
    print("Loading firewall data...")
    pl_fir_data = load_fir()

    
    # app.run(debug=True)


