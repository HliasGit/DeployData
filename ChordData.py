import Caching as ch
from constants import *

def manage_chord_diagram_data(live_cache):        
    
    print("Serving Chord Diagram")
    
    return ch.get_latest_cord(live_cache=live_cache[CHORD_PATH])