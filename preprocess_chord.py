import pandas as pd
import numpy as np
import json

# Function to calculate the matrix and generate JSON for a chord diagram
def prepare_chord_data(input_csv):
    # Read the data
    data = pd.read_csv(input_csv)

    # Fill missing values in 'Direction' with 'empty' for consistent grouping
    data['Direction'] = data['Direction'].fillna('empty')

    # Step 1: Create a mapping for Source IPs and Destination Ports to indices
    source_ips = data['Source IP'].unique()
    destination_ports = data['Destination port'].unique()

    # Create indices for mapping
    source_ip_index = {ip: i for i, ip in enumerate(source_ips)}
    destination_port_index = {port: i + len(source_ips) for i, port in enumerate(destination_ports)}

    # Total number of nodes (Source IPs + Destination Ports)
    total_nodes = len(source_ips) + len(destination_ports)

    # Step 2: Initialize an empty matrix
    matrix = np.zeros((total_nodes, total_nodes), dtype=int)

    # Step 3: Populate the matrix
    for _, row in data.iterrows():
        src_idx = source_ip_index[row['Source IP']]
        dest_idx = destination_port_index[row['Destination port']]
        matrix[src_idx, dest_idx] += 1

    # Step 4: Prepare a JSON structure for D3.js
    nodes = [{'name': ip, 'group': 'source'} for ip in source_ips] + \
            [{'name': str(port), 'group': 'destination'} for port in destination_ports]

    # Define links (with direction as part of the structure)
    links = []
    for _, row in data.iterrows():
        src_idx = source_ip_index[row['Source IP']]
        dest_idx = destination_port_index[row['Destination port']]
        direction = row['Direction']
        links.append({
            'source': src_idx,
            'target': dest_idx,
            'value': 1,  # Each connection counts as 1; adjust if needed
            'direction': direction
        })

    # Combine nodes and links into a single structure
    chord_data = {
        'nodes': nodes,
        'matrix': matrix.tolist(),  # Convert numpy matrix to list for JSON
        'links': links
    }

    return chord_data

