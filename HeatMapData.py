import Caching as ch
from constants import *

def manage_heatmap_request(live_cache, protocol):
    print("Serving HEATMAP")
    return ch.get_latest_heatmap(live_cache[HEAT_PATH], protocol)