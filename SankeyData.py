import Caching as ch
from constants import *

def manage_sankey_data(live_cache, glob_data_fir):        
    
    print("Serving Chord Diagram")
    
    return ch.get_latest_sankey(live_cache=live_cache[CHORD_PATH], glob_data_fir=glob_data_fir)