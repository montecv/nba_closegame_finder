import re
from bs4 import BeautifulSoup
from .utils import cached_get

BASE_URL = "https://www.basketball-reference.com"


def get_games_by_date(date):
    url = f"{BASE_URL}/boxscores/?month={date.month}&day={date.day}&year={date.year}"
    html = cached_get(url)
    soup = BeautifulSoup(html, "html.parser")

    links = soup.select("td.gamelink a")
    return [BASE_URL + l["href"] for l in links]

def get_team_names(game_url):
    html = cached_get(game_url)
    html = re.sub("<!--|-->", "", html)

    soup = BeautifulSoup(html, "html.parser")
    teams = soup.select("div.scorebox strong a")

    return f'{teams[0].text} vs {teams[1].text}'

def get_play_by_play(game_url):
    game_id = game_url.split("/")[-1]
    play_by_play_url = f"{BASE_URL}/boxscores/pbp/{game_id}"

    html = cached_get(play_by_play_url)
    html = re.sub("<!--|-->", "", html)

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "pbp"})

    if not table: return []

    rows = table.find_all("tr")
    data = []

    for row in rows:
        cols = [c.text.strip() for c in row.find_all(["th", "td"])]
        if cols:
            data.append(cols)

    return data
