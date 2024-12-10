import json
import polars as pl

def preprocess_hist(glob_data_fir: pl.DataFrame, glob_data_ids: pl.DataFrame, bins, fir_str, ids_str):
    
    # Get the unique values of the fir_str and ids_str
    fir_values = glob_data_fir[fir_str].unique().to_list()
    ids_values = glob_data_ids[ids_str].unique().to_list()

    return json.dumps([fir_values, ids_values])

    # TODO: COMPLETE THIS FUNCTION
