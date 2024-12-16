import Caching as ch
from constants import *

def manage_pie_chart_data(live_cache, glob_data_fir, glob_data_ids):        
    
    print("Serving PieCHART")
    
    return ch.get_latest_pie(live_cache=live_cache[PIE_PATH], glob_data_fir=glob_data_fir, glob_data_ids=glob_data_ids)