import pandas as pd
import polars as pl

def preprocess_sankey(glob_data_fir: pl.DataFrame):
    # Convert Polars DataFrame to Pandas DataFrame
    df = glob_data_fir.to_pandas()
    
    # Filter necessary columns: Source IP and Destination Port
    df = df[['Source IP', 'Destination port']]
    
    # Define a function to categorize Source IPs into Node Names
    def categorize_ip(ip):
        if ip == "10.32.0.1":
            return "Firewall (Internet)"
        elif ip == "172.23.0.1":
            return "Firewall (Regional Bank Network)"
        elif ip == "10.32.0.100":
            return "Firewall (DataCenter Internet)"
        elif ip == "172.25.0.1":
            return "Firewall (DataCenter Mail/Financial)"
        elif re.match(r"10\.32\.0\.20[1-9]|10\.32\.1\.10[0-6]|10\.32\.5\.\d+", ip):
            return "Websites"
        elif re.match(r"172\.23\.214\.\d+|172\.23\.22[0-9]\.\d+", ip):
            return "Financial Servers"
        elif ip == "172.23.0.10":
            return "Domain Controller / DNS"
        elif ip == "172.23.0.2":
            return "Log Server"
        elif re.match(r"172\.23\..*", ip):
            return "Workstations"
        elif ip == "10.99.99.2":
            return "IDS (Snort)"
        else:
            return "Uncategorized"
    
    # Map Source IPs to Node Names
    df['Node Name'] = df['Source IP'].apply(categorize_ip)
    
    # Group by Node Name and Destination Port
    counts = df.groupby(['Node Name', 'Destination port']).size().reset_index(name='Count')
    
    # Convert the grouped data into a JSON-like format
    result = counts.pivot(index='Node Name', columns='Destination port', values='Count').fillna(0)
    json_data = []

    for port in result.columns:
        port_data = {
            f"Port {port}": [{node.lower(): result.at[node, port]} for node in result.index if result.at[node, port] > 0]
        }
        json_data.append(port_data)
    
    return json_data
