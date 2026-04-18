import requests

cache = {}

def cached_get(url):
    if url in cache:
        return cache[url]

    response = requests.get(url).text
    cache[url] = response
    return response

def parse_time(t):
    minutes, seconds = t.split(':')
    return int(minutes) * 60 + float(seconds)