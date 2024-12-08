import pandas as pd

def df_heatmap():
    # Read the CSV file
    df = pd.read_csv('IDS-0406-replacement.csv')
    
    # Select only the necessary columns and clean column names
    source_df = df[[' sourceIP']].rename(columns=lambda x: x.strip())
    destionation_df = df[[' destIP']].rename(columns=lambda x: x.strip())
    classification_df = df[[' sourceIP', ' destIP', ' classification']].rename(columns=lambda x: x.strip())

    # Group by sourceIP and destIP, then count occurrences of each classification
    reduced_df = (
        classification_df
        .groupby(['sourceIP', 'destIP', 'classification'])
        .size()  # Count occurrences of each classification
        .reset_index(name='count')  # Add a column for counts
    )

    # Nest classifications under each (sourceIP, destIP) pair
    nested_df = (
        reduced_df
        .groupby(['sourceIP', 'destIP'])
        .apply(lambda x: x[['classification', 'count']].to_dict(orient='records'))
        .reset_index(name='classifications')  # Nested classification data
    )

    # Convert the DataFrame to a dictionary
    source_df = source_df.to_dict(orient='records')
    destionation_df = destionation_df.to_dict(orient='records')
    nested_dict = nested_df.to_dict(orient='records')
    
    # Return as a dictionary
    return {"sourceIP": source_df, "destinationIP": destionation_df, "content": nested_dict}
