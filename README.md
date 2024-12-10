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
    1. `times` - List of time intervals which are binned. Each element is a time point in the format `YYYY-MM-DD HH:MM`
    2. `classifications` - List of classifications as requested by the user
    3. `content` - List of dictionaries. Each element has the following attributes
        - `top` - List of counts for each classification on the top graph
        - `bottom` - List of counts for each classification on the bottom graph
