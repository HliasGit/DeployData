import pandas as pd

def df_heatmap():
    # Read the CSV file
    df = pd.read_csv('ids.csv')
    
    # Clean column names and ensure proper selection
    df = df.rename(columns=lambda x: x.strip())

    # remove all the rows with a label [1:2009702:4] ET POLICY DNS Update From External net 
    df = df[~df['label'].str.contains('ET POLICY DNS Update From External net')]
    
    # Extract unique sources and destinations
    sources = df['sourceIP'].unique().tolist()
    # destinations = df['destIP'].unique().tolist()
    destinations = df['classification'].unique().tolist()
    
    # Group the data and calculate the sum of counts for each category
    grouped = (
        df.groupby(['sourceIP', 'classification'])
        .size()  # Count occurrences of each classification
        .reset_index(name='count')  # Add a column for the count
    )
    
    # Aggregate to maztch the required content structure
    aggregated = (
        grouped.groupby(['sourceIP', 'classification'])
        .agg(
            values=('count', list),  # List of counts for this pair
            labels=('classification', list)  # List of unique classifications for this pair
        )
        .reset_index()
    )
    
    # Build the "content" array
    content = [
        {
            "source": row['sourceIP'],
            "destination": row['classification'],
            "values": row['values'],
            "labels": row['labels']
        }
        for _, row in aggregated.iterrows()
    ]
    
    # Assemble the final JSON structure
    result = {
        "sources": sources,
        "destination": destinations,
        "content": content
    }
    
    return result
