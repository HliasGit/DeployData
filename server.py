import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
import treatData

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getHeatMapData")
def get_heatMapData():
    data = treatData.df_heatmap()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
