import os
import pickle
import random
import re
import requests
import time

from bs4 import BeautifulSoup


BASE_URL = "https://www.basketball-reference.com"
CACHE_FILE = "cache.pkl"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
else:
    cache = {}


def save_cache():
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)

def get_games_by_date(date):
    url = f"{BASE_URL}/boxscores/?month={date.month}&day={date.day}&year={date.year}"

    if url in cache:
        links = cache[url]
    else:
        time.sleep(random.uniform(2, 5))
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        links = [BASE_URL + l["href"] for l in soup.select("td.gamelink a")]
        cache[url] = links
        save_cache()

    return links

def get_game_data(game_url):
    if game_url in cache:
        return cache[game_url]

    time.sleep(random.uniform(2, 5))
    game_data = {}

    game_id = game_url.split("/")[-1]
    play_by_play_url = f"{BASE_URL}/boxscores/pbp/{game_id}"

    html = requests.get(play_by_play_url).text
    html = re.sub("<!--|-->", "", html)
    soup = BeautifulSoup(html, "html.parser")
    teams = soup.select("div.scorebox strong a")

    if len(teams) < 2:
        title = soup.title.string if soup.title else "No found"
        raise ValueError(f"{game_url}: {title}")

    game_data['teams'] = f'{teams[0].text} vs {teams[1].text}'
    table = soup.find("table", {"id": "pbp"})
    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = [c.text.strip() for c in row.find_all(["th", "td"])]
        if cols:
            data.append(cols)
    game_data['pbp'] = data

    cache[game_url] = game_data
    save_cache()

    return game_data