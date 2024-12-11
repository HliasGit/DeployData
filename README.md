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
    - `firParam` - Parameter for the active classification on the firewall graph (top graph)
    - `idsParam` - Parameter for the active classification on the ids graph (bottom graph) 
    - `bins` - Number of bins in which the time is divided into

