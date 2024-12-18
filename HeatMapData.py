import Caching as ch
from constants import *

DEFAULT_CLASS = 'classification'
DEFAULT_ORIGIN = 'ids'

def manage_heatmap_request(live_cache, class_sel, axis, origin, start, end, glob_data_fir, glob_data_ids):
    print("Serving HEATMAP")
    print(" axis ->", axis)
    return ch.get_latest_heatmap(live_cache[HEAT_PATH], class_sel, axis, origin, start, end, glob_data_fir, glob_data_ids)