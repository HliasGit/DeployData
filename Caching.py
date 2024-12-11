import hashlib
import PreprocessHist as ph

import os
import json
import time



CACHE_PATH = "cache"
HIST_PATH = "hist"

ALL_CACHES = [HIST_PATH]


def init():
    # Create cache folder  
    try:
        os.mkdir(CACHE_PATH)
        for cache in ALL_CACHES:
            os.mkdir(f"{CACHE_PATH}/{cache}")
        # Create hist folder
    except FileExistsError:
        print(" Cache Directory Already Exists")
        pass

def compute_hash(params: str) -> str:
    return hashlib.md5(params.encode()).hexdigest()

def load_data_file(source, hash):
    try:
        data = json.load(open(f"{CACHE_PATH}/{source}/{hash}.json"))
        return data, True
    except FileNotFoundError:
        return None, False

def write_data_file(source, hash, data):
    json.dump(data, open(f"{CACHE_PATH}/{source}/{hash}.json", "w"))


# ============= HISTOGRAM CACHE =============
def get_latest_hist(fir_str, ids_str, bins, live_cache, glob_data_fir, glob_data_ids):
    
    string = f"{fir_str}-{ids_str}-{bins}"

    hash = compute_hash(string)
    if hash in live_cache["idx"]:
        print("HIT in LIVE CACHE")
        return live_cache["data"][hash]
    
    print("Not in LIVE CACHE")

    data, res = load_data_file(HIST_PATH, hash)
    if not res:
        print("Not in STORAGE CACHE")
        live_cache["idx"].add(hash)
        live_cache["data"][hash] = ph.preprocess_hist(glob_data_fir, glob_data_ids, bins, fir_str, ids_str)
        write_data_file(HIST_PATH, hash, live_cache["data"][hash])
        return live_cache["data"][hash]
    else:
        print("HIT in STORAGE CACHE")
        live_cache["idx"].add(hash)
        live_cache["data"][hash] = data
        return data

# ============= HISTOGRAM CACHE =============
