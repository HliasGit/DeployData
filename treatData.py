import pandas as pd

def df_heatmap():
    # Read the CSV file
    df = pd.read_csv('IDS-FILTERED.csv')
    
    # Select only the necessary columns and clean column names
    classification_df = df[['sourceIP', 'destIP', 'classification']].rename(columns=lambda x: x.strip())

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

    # Prepare the final output
    result = {
        "sourceIP": nested_df['sourceIP'].unique().tolist(),  # Unique sourceIP list
        "destIP": nested_df['destIP'].unique().tolist(),  # Unique destIP list
        "content": nested_df.to_dict(orient='records')  # Maintain the original content structure
    }

    return result
