import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import Caching as ch

import polars as pl


# Module with functions that manage requests for the heatmap
import treatData

# Module with functions that manage requests for the histogram
import B2BHistData


FIREWALL_FILE = 'firewall.csv'
IDS_FILE = 'ids.csv'

pl_ids_data = None
pl_fir_data = None

pl_fir_data_aggregated_by_time = None
pl_ids_data_aggregated_by_time = None

# Cache that contains aggregated data with paths to files
cache = {
    "hist": {
        "idx": set(),
        "data": {}
    }
}

def load_ids():
    return pl.read_csv(IDS_FILE)

def load_fir():
    return pl.read_csv(FIREWALL_FILE)


print("Initializing cache...")
ch.init()

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
   
    return "<p>Hello, World!</p>"

@app.route("/getHeatMapData")
def get_heatMapData():
    data = treatData.df_heatmap()
    return jsonify(data)

@app.route("/getB2BHistData")
def get_b2bHistData():
    firewall_parameter = request.args.get('firParam')
    ids_parameter = request.args.get('idsParam')
    bins = request.args.get('bins')

    if firewall_parameter is None:
        firewall_parameter = B2BHistData.DEFAULT_FIR_CLASS
    
    if ids_parameter is None:
        ids_parameter = B2BHistData.DEFAULT_IDS_CLASS

    if bins is None:
        bins = B2BHistData.DEFAULT_HIST_BINS

    data = B2BHistData.manage_request(
        firewall_parameter=firewall_parameter,
        ids_parameter=ids_parameter,
        bins=bins,
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


