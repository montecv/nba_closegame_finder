import os
import pickle
import random
import requests
import time

CACHE_FILE = "cache.pkl"

class BlockedBySiteError(Exception):
    pass

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
else:
    cache = {}


def save_cache():
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)

def cached_get(url):
    if url in cache:
        return cache[url]

    time.sleep(random.uniform(2, 5))
    response = requests.get(url).text
    cache[url] = response
    save_cache()

    return response

def parse_time(t):
    minutes, seconds = t.split(':')
    return int(minutes) * 60 + float(seconds)
