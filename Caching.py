import hashlib
import PreprocessHist as ph
import preprocess_heat as ph_heat
import preprocess_pie as ph_pie
import preprocess_chord as ph_chord
from constants import *

import os
import json


global_cache_reference = None  # Use global properly

ALL_CACHES = [HIST_PATH, HEAT_PATH, TIME_PATH, PIE_PATH, CHORD_PATH]


def store_all_caches():
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)
    for cache in ALL_CACHES:
        check_storage_cache(cache)


def store_cache(cache_mem):
    if not global_cache_reference or global_cache_reference.get(cache_mem) is None:
        return

    for hash, data in global_cache_reference[cache_mem].items():
        print(f"Writing to STORAGE CACHE {cache_mem}: {hash}")
        write_data_file(cache_mem, hash, data)


def check_storage_cache(cache_mem):
    cache_path = f"{CACHE_PATH}/{cache_mem}"
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)
    if not os.path.exists(cache_path):
        print(f"Creating cache {cache_mem}")
        os.mkdir(cache_path)


def init(global_cache):
    global global_cache_reference
    global_cache_reference = global_cache
    store_all_caches()


def compute_hash(params: str) -> str:
    return hashlib.md5(params.encode()).hexdigest()


def load_data_file(source, hash):
    file_path = f"{CACHE_PATH}/{source}/{hash}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file), True
    return None, False


def write_data_file(source, hash, data):
    file_path = f"{CACHE_PATH}/{source}/{hash}.json"
    with open(file_path, "w") as file:
        json.dump(data, file)


# Unified Cache Retrieval
def get_cached_data(source, hash, live_cache, preprocess_fn, *args):
    if hash in live_cache["idx"]:
        print("HIT in LIVE CACHE")
        return live_cache["data"][hash]

    print("Not in LIVE CACHE")
    data, found_in_storage = load_data_file(source, hash)
    if found_in_storage:
        print(f"HIT in STORAGE CACHE {hash}")
    else:
        print("Not in STORAGE CACHE")
        data = preprocess_fn(*args)
        print(f"Writing to STORAGE CACHE {hash}")
        write_data_file(source, hash, data)

    live_cache["idx"].add(hash)
    live_cache["data"][hash] = data
    return data


# ============= HISTOGRAM CACHE =============
def get_latest_hist(fir_str, ids_str, bins, live_cache, glob_data_fir, glob_data_ids, mode, start, end):
    check_storage_cache(HIST_PATH)
    hash_key = f"{fir_str}-{ids_str}-{bins}-{mode}-{start}-{end}"
    hash = compute_hash(hash_key)
    return get_cached_data(HIST_PATH, hash, live_cache, ph.preprocess_hist, glob_data_fir, glob_data_ids, bins, fir_str, ids_str, mode, start, end)


# ============= TIMELINE CACHE =============
def get_latest_timeline(live_cache, glob_data_fir, glob_data_ids):
    check_storage_cache(TIME_PATH)
    hash = compute_hash("timeline")
    return get_cached_data(TIME_PATH, hash, live_cache, ph.preprocess_timeline, glob_data_fir, glob_data_ids)


# ============= HEATMAP CACHE =============
def get_latest_heatmap(live_cache, class_sel, axis, origin, start, end, glob_data_fir, glob_data_ids):
    check_storage_cache(HEAT_PATH)
    hash_key = f"{class_sel}-{origin}-{start}-{end}-{axis if axis else 'default'}"
    hash = compute_hash(hash_key)
    return get_cached_data(HEAT_PATH, hash, live_cache, ph_heat.preprocess_heat, glob_data_fir, glob_data_ids, start, end, origin, class_sel, axis)


# ============= PIECHART CACHE =============
def get_latest_pie(live_cache, glob_data_fir, glob_data_ids):
    check_storage_cache(PIE_PATH)
    hash = compute_hash("only-piechart")
    return get_cached_data(PIE_PATH, hash, live_cache, ph_pie.preprocess_pie, glob_data_fir, glob_data_ids)

# ============= CHORD DIAGRAM CACHE =============
def get_latest_cord(live_cache, glob_data_fir):
    check_storage_cache(CHORD_PATH)
    hash = compute_hash("chord")
    return get_cached_data(CHORD_PATH, hash, live_cache, ph_chord.prepare_chord_data, glob_data_fir)
