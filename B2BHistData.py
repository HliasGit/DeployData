import Caching as ch
from constants import *

DEFAULT_HIST_BINS = 100
DEFAULT_FIR_CLASS = 'Syslog priority'
DEFAULT_IDS_CLASS = 'classification'

def manage_request(firewall_parameter, ids_parameter, bins, live_cache, glob_data_fir, glob_data_ids, mode, start=None, end=None):   
    
    print("Serving HISTOGRAM")
    print(" -> fir_str: ", firewall_parameter)
    print(" -> ids_str: ", ids_parameter)
    print(" -> bins: ", bins)
    print(" -> mode: ", mode)
    print(" -> start: ", start)
    print(" -> end: ", end)
    
    return ch.get_latest_hist(fir_str=firewall_parameter, ids_str=ids_parameter, bins=bins, live_cache=live_cache[HIST_PATH], glob_data_fir=glob_data_fir, glob_data_ids=glob_data_ids, mode=mode, start=start, end=end)


def manage_timeline_request(live_cache, glob_data_fir, glob_data_ids):
    print("Serving TIMELINE")
    return ch.get_latest_timeline(live_cache=live_cache[TIME_PATH], glob_data_fir=glob_data_fir, glob_data_ids=glob_data_ids)