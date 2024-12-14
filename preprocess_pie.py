import pandas as pd

def preprocess_pie():
    # Read the CSV file
    df = pd.read_csv('firewall.csv')
    
    # Clean column names and ensure proper selection
    df = df.rename(columns=lambda x: x.strip())

    print(df)


    # drop every column but Operations and Destination Service
    df = df[['Operation', 'Destination service']]

    print(df)
    counts = df.groupby(['Operation', 'Destination service']).size().reset_index(name='Count')

    # Convert the grouped data into a more readable format
    result = counts.pivot(index='Operation', columns='Destination service', values='Count').fillna(0)

    # Save the result to a file
    print(result)

    json_data = []

    for col in result.columns:
        service_data = {col: [{op.lower(): result.at[op, col]} for op in result.index]}
        json_data.append(service_data)
    
    return json_data
