import Caching as ch


DEFAULT_HIST_BINS = 100
DEFAULT_FIR_CLASS = 'Syslog priority'
DEFAULT_IDS_CLASS = 'classification'

def manage_request(firewall_parameter, ids_parameter, bins, live_cache, glob_data_fir, glob_data_ids):        
    return ch.get_latest_hist(fir_str=firewall_parameter, ids_str=ids_parameter, bins=bins, live_cache=live_cache["hist"], glob_data_fir=glob_data_fir, glob_data_ids=glob_data_ids)
