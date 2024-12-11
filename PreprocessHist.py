import json
import polars as pl
import datetime as dt
import numpy as np


def preprocess_hist(glob_data_fir: pl.DataFrame, glob_data_ids: pl.DataFrame, bins, fir_str, ids_str):
    # Ensure time columns are in datetime format
    glob_data_fir = glob_data_fir.with_columns(pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M"))
    glob_data_ids = glob_data_ids.with_columns(pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M"))

    # Get the unique values of the fir_str and ids_str
    fir_values = glob_data_fir[fir_str].unique().to_list()
    ids_values = glob_data_ids[ids_str].unique().to_list()

    data = {}

    # Extract the unique classifications
    classifications = {
        "top": fir_values,
        "bottom": ids_values
    }

    data["classifications"] = classifications

    # Extract the minimum and maximum time values for both datasets
    fir_min_time = glob_data_fir["time"].min()
    ids_min_time = glob_data_ids["time"].min()
    fir_max_time = glob_data_fir["time"].max()
    ids_max_time = glob_data_ids["time"].max()

    # Calculate overall min and max time
    min_time = min(fir_min_time, ids_min_time)
    max_time = max(fir_max_time, ids_max_time)

    # Calculate the interval in seconds
    total_seconds = (max_time - min_time).total_seconds()
    interval = total_seconds / bins

    # Create the intervals
    # Get the first mid point
    mid = min_time + dt.timedelta(seconds=interval // 2)
    

    mid_points = [mid + dt.timedelta(seconds=interval * i) for i in range(bins)]
    intervals = [min_time + dt.timedelta(seconds=interval * i) for i in range(bins)]

    # Add the last data time in the intervals
    intervals.append(max_time)

    mid_points_str = [mid_point.isoformat() for mid_point in mid_points]

    # Truncate the intervals to the nearest minute
    mid_points_str = [mid_point[:16] for mid_point in mid_points_str]

    # Add intervals to data

    data["times"] = mid_points_str

    # Now we need to count the number of occurrences for each classification in each interval
    data["content"] = []

    # Iterate over each interval
    for i in range(bins):  # Avoid accessing intervals_str[i + 1] out of range
        fir_counts = []  # Reset for each time interval
        ids_counts = []  # Reset for each time interval

        # Filter data for the current time interval
        interval_start = intervals[i]
        interval_end = intervals[i + 1]

        fir_interval_data = glob_data_fir.filter(
            (pl.col("time") >= interval_start) & (pl.col("time") < interval_end)
        )
        ids_interval_data = glob_data_ids.filter(
            (pl.col("time") >= interval_start) & (pl.col("time") < interval_end)
        )

        # Count classifications for "top"
        for classification in classifications["top"]:
            fir_counts.append(fir_interval_data.filter(pl.col(fir_str) == classification).shape[0])

        # Count classifications for "bottom"
        for classification in classifications["bottom"]:
            ids_counts.append(ids_interval_data.filter(pl.col(ids_str) == classification).shape[0])

        # Append results to content
        data["content"].append({
            "top": fir_counts,
            "bottom": ids_counts
        })

    return data
