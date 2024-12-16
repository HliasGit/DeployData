import pandas as pd
import numpy as np
import polars as pl
# Function to calculate the matrix and generate JSON for a chord diagram
def prepare_chord_data(glob_data_fir: pl.DataFrame):
    data = glob_data_fir.to_pandas()

    # Create a mapping for Destination Service and Destination Ports to indices
    destination_service= data['Destination service'].unique()
    destination_ports = data['Destination port'].unique()

    # Create indices for mapping
    service_index = {service: i for i, service in enumerate(destination_service)}
    destination_port_index = {port: i + len(destination_service) for i, port in enumerate(destination_ports)}

    # Total number of nodes (Destination Service + Destination Ports)
    total_nodes = len(destination_service) + len(destination_ports)

    # Initialize an empty matrix
    matrix = np.zeros((total_nodes, total_nodes), dtype=int)

    # Populate the matrix
    for _, row in data.iterrows():
        src_idx = service_index[row['Destination service']]
        dest_idx = destination_port_index[row['Destination port']]
        matrix[src_idx, dest_idx] += 1

    # Step 4: Prepare a JSON structure
    nodes = [{'name': service, 'group': 'service'} for service in destination_service] + \
            [{'name': str(port), 'group': 'port'} for port in destination_ports]

    # Define links (with direction as part of the structure)
    links = []
    for _, row in data.iterrows():
        src_idx = service_index[row['Destination service']]
        dest_idx = destination_port_index[row['Destination port']]
        operation = row['Operation']
        links.append({
            'source': src_idx,
            'target': dest_idx,
            'value': 1,  # Each connection counts as 1; adjust if needed
            'operation': operation
        })

    # Combine nodes and links into a single structure
    chord_data = {
        'nodes': nodes,
        'matrix': matrix.tolist(),  # Convert numpy matrix to list for JSON
        'links': links
    }

    return chord_data

