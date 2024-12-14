import polars as pl
import datetime as dt
import numpy as np


def preprocess_hist(glob_data_fir: pl.DataFrame, glob_data_ids: pl.DataFrame, bins, fir_str, ids_str, mode):
    # Ensure time columns are in datetime format
    glob_data_fir = glob_data_fir.with_columns(pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M"))
    glob_data_ids = glob_data_ids.with_columns(pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M"))


    # Get the unique values of the fir_str and ids_str
    fir_values = glob_data_fir[fir_str].unique().to_list()
    ids_values = glob_data_ids[ids_str].unique().to_list()

    # Time calculations
    min_time = min(glob_data_fir["time"].min(), glob_data_ids["time"].min())
    max_time = max(glob_data_fir["time"].max(), glob_data_ids["time"].max())
    interval = (max_time - min_time).total_seconds() / bins

    # Create intervals and midpoints
    intervals = [min_time + dt.timedelta(seconds=interval * i) for i in range(bins+1)]
    intervals_str = [interval.isoformat()[:16] for interval in intervals]
    print(f"Sending {len(intervals_str)} intervals")

    mid_points = [min_time + dt.timedelta(seconds=interval * i + i * interval/2) for i in range(bins)]
    mid_points_str = [mid_point.isoformat()[:16] for mid_point in mid_points]

    # Pre-compute counts for all intervals at once
    def get_counts(df, class_col, class_values, intervals):
        counts = []
        for i in range(len(intervals)-1):
            interval_data = df.filter(
                (pl.col("time") >= intervals[i]) & (pl.col("time") < intervals[i+1])
            ).group_by(class_col).agg(pl.count())
            
            # Create ordered counts list
            interval_counts = [0] * len(class_values)
            for row in interval_data.iter_rows():
                try:
                    idx = class_values.index(row[0])
                    interval_counts[idx] = row[1]
                except ValueError:
                    continue
                    
            counts.append(interval_counts)
        return counts

    # Get counts for both datasets
    fir_counts = get_counts(glob_data_fir, fir_str, fir_values, intervals)
    ids_counts = get_counts(glob_data_ids, ids_str, ids_values, intervals)

    # Apply log transformation if needed
    if mode == 'log':
        fir_counts = [np.log2(np.array(counts) + 1).tolist() for counts in fir_counts]
    elif mode == 'unique':
        fir_counts = [[ 1 if count > 0 else 0 for count in counts] for counts in fir_counts]

    # Build result dictionary
    data = {
        "classifications": {"top": fir_values, "bottom": ids_values},
        "times": intervals_str,
        "content": [{"top": fir, "bottom": ids} for fir, ids in zip(fir_counts, ids_counts)]
    }

    return data


def preprocess_timeline(glob_data_fir: pl.DataFrame, glob_data_ids: pl.DataFrame):
    # Ensure time columns are in datetime format
    glob_data_fir = glob_data_fir.with_columns(pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M"))
    glob_data_ids = glob_data_ids.with_columns(pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M"))

    # Time calculations
    min_time = min(glob_data_fir["time"].min(), glob_data_ids["time"].min())
    max_time = max(glob_data_fir["time"].max(), glob_data_ids["time"].max())

    # TODO: Implement computation for the timeline

    data = {
        "times" : {
            "begin" : min_time.isoformat()[:16],
            "end" : max_time.isoformat()[:16],
        },
        "content": {
        }
    }


    return data