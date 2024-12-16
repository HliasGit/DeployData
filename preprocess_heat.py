import polars as pl
import pandas as pd
import datetime as dt

def preprocess_heat(glob_data_fir, glob_data_ids, start=None, end=None, origin="ids", class_sel="classification", axis="default"):
    # Ensure "time" columns are in datetime format
    glob_data_fir = glob_data_fir.with_columns(
        pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M")
    )
    glob_data_ids = glob_data_ids.with_columns(
        pl.col("time").str.strptime(pl.Datetime, "%m/%d/%Y %H:%M")
    )

    # Determine the minimum and maximum times from the datasets
    data_min_time = min(glob_data_fir["time"].min(), glob_data_ids["time"].min())
    data_max_time = max(glob_data_fir["time"].max(), glob_data_ids["time"].max())

    # Parse user-provided time range or use dataset's time range
    min_time = dt.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") if start else data_min_time
    max_time = dt.datetime.strptime(end, "%Y-%m-%d %H:%M:%S") if end else data_max_time

    # Select the dataset and corresponding X_AXIS column based on the origin
    df = None

    if axis is None:
        axis = "default"

    if axis == "default":
        if origin == "fir":
            df = glob_data_fir
            X_AXIS = "Source IP"
        elif origin == "ids":
            df = glob_data_ids
            X_AXIS = "sourceIP"
        else:
            raise ValueError("Invalid origin. Expected 'fir' or 'ids'.")
    elif axis == "pie":
        X_AXIS = "Destination service"
        class_sel = "Operation"
        df = glob_data_fir

    # Filter the dataframe based on the time range
    df = df.filter((pl.col("time") >= min_time) & (pl.col("time") <= max_time))

    # Convert to pandas for further processing
    df = df.to_pandas()

    # Group by the IP column and the selected class column, and count occurrences
    grouped_df = df.groupby([X_AXIS, class_sel]).size().reset_index(name='count')

    # Extract unique source IPs and classes
    sources = grouped_df[X_AXIS].unique().tolist()
    possible_classes = sorted(grouped_df[class_sel].unique().tolist())

    # Create a dictionary to hold the aggregated data
    content = {source: {class_: 0 for class_ in possible_classes} for source in sources}

    # Fill the dictionary with the data from grouped_df
    for _, row in grouped_df.iterrows():
        source = row[X_AXIS]
        class_ = row[class_sel]
        count = row['count']
        content[source][class_] = count


    # If there are more than 15 unique IPs, group them based on the first three numbers
    if axis == "default":
        if len(sources) > 15:
            grouped_content = {}
            for source in sources:
                grouped_key = '.'.join(source.split('.')[:3]) + '.0/24'
                if grouped_key not in grouped_content:
                    grouped_content[grouped_key] = {class_: 0 for class_ in possible_classes}
                for class_ in possible_classes:
                    grouped_content[grouped_key][class_] += content[source][class_]
            content = grouped_content
            sources = list(grouped_content.keys())


    # Assemble the final JSON structure
    result = {
        "sources": sources,
        "classes": possible_classes,
        "content": content,
        "start": min_time.isoformat()[:16],
        "end": max_time.isoformat()[:16]
    }

    return result
