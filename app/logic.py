from datetime import datetime, timedelta

from .scraper import get_games_by_date, get_game_data
from .utils import parse_time, BlockedBySiteError


def average_score_diff(data):
    if not data:
        return 0

    total_weighted = 0
    total_time = 0

    for i in range(len(data) - 1):
        t1, diff = data[i]
        t2, _ = data[i + 1]

        duration = t1 - t2
        total_weighted += diff * duration
        total_time += duration

    last_time, last_diff = data[-1]
    total_weighted += last_diff * last_time
    total_time += last_time

    return total_weighted / total_time if total_time else 0


def daterange(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def get_matches_coef(start_date_str: str, end_date_str: str):
    try:
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
    except ValueError:
        raise ValueError("Date should be in YYYYMMDD (example: 20260414)")

    results = []

    for date in daterange(start_date, end_date):
        print(date.date())
        games = get_games_by_date(date)

        for game_url in games:
            try:
                game_data = get_game_data(game_url)
                teams = game_data['teams']
                pbp_data = game_data['pbp']
            except BlockedBySiteError:
                print("Seems like we are blocked for 5 minutes or 1 hour. Stop getting info.")
                return sorted(results, key=lambda r: r["coef"])

            data_scores = []
            is_clutch_time = False
            overtime_count = 0
            final_diff = 0

            for play in pbp_data:
                if play == ['4th Q']:
                    is_clutch_time = True
                    continue

                if play and play[0].endswith(" OT"):
                    overtime_count += 1

                if is_clutch_time and len(play) > 4:
                    if '-' in play[3]:
                        a, b = play[3].split('-')
                        diff = int(a) - int(b)
                        final_diff = diff
                        data_scores.append([parse_time(play[0]), diff])

            avg_diff = abs(average_score_diff(data_scores))
            coef = min(avg_diff, abs(final_diff))
            if overtime_count:
                coef = coef/2**overtime_count

            results.append({
                "date": date.strftime("%Y%m%d"),
                "teams": teams,
                "coef": round(coef, 3)
            })

    return sorted(results, key=lambda r: r["coef"])
