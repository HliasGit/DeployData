# End Points

- `getHeatMapData` - Get IDS heat map data
  - Returns a JSON object with the following attributes
    1. `sourceIP` - List of source IP addresses
    2. `destIP` - List of destination IP addresses
    3. `content` - List of dictionaries with
        - `sourceIP` - Source IP address
        - `destIP` - Destination IP address
        - `classifications` - List of classifications (`classification`), with counts (`count`)

- `getB2BHistData` - Get histogram data with time information
  - Returns a JSON object with the following attributes
    1. `times` - List of time intervals which are binned. Each element is a time point in the `ISO FORMAT` and refers to the start of the time interval
    2. `classifications` - List of classifications as requested by the user. This contains the following attributes
        - `top` - List of classification names for the top graph
        - `bottom` - List of classification names for the bottom graph
    3. `content` - List of dictionaries. Each element has the following attributes
        - `top` - List of counts for each classification on the top graph
        - `bottom` - List of counts for each classification on the bottom graph
  - Requires a `firParam` and `idsParam` field in the query string. Here
    - `fir` - Parameter for the active classification on the firewall graph (top graph)
    - `ids` - Parameter for the active classification on the ids graph (bottom graph) 
    - `bins` - Number of bins in which the time is divided into
    - `mode` - Provides additional information about the firewall visualization (`count` for default, `log` for log scale, `unique` for unique counts).
    

# Where to find data?

```bash
wget https://zenodo.org/records/14504722/files/data_final.tar.xz
tar -xvf data_final.tar.xz
```

You can find the data in a .tar.xz file by following the link above
Then, extract the data and place it in the root folder of the repository.

# Running with ngrok

```bash
mkdir ngrok_bin
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvf ngrok-v3-stable-linux-amd64.tgz -C ngrok_bin
./ngrok_bin/ngrok config add-authtoken <Your_Auth_Token>
./ngrok_bin/ngrok http 5000
```
