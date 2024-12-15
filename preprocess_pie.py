import pandas as pd
import polars as pl

def preprocess_pie(glob_data_fir: pl.DataFrame, glob_data_ids):
    # Read the CSV file
    df = glob_data_fir.to_pandas()
    
    # drop every column but Operations and Destination Service
    df = df[['Operation', 'Destination service']]

    counts = df.groupby(['Operation', 'Destination service']).size().reset_index(name='Count')

    # Convert the grouped data into a more readable format
    result = counts.pivot(index='Operation', columns='Destination service', values='Count').fillna(0)

    json_data = []

    for col in result.columns:
        service_data = {col: [{op.lower(): result.at[op, col]} for op in result.index if result.at[op, col] > 0]}
        json_data.append(service_data)
    
    return json_data
