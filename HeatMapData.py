import Caching as ch

def manage_heatmap_request(live_cache, protocol):
    print("Serving HEATMAP")
    return ch.get_latest_heatmap(live_cache["hist"], protocol)