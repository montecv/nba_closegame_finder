import argparse
from app.logic import get_matches_coef


def main():
    parser = argparse.ArgumentParser(
        description="NBA CloseGame finder"
    )

    parser.add_argument("start_date", help="Start date (YYYYMMDD)")
    parser.add_argument("end_date", help="End date (YYYYMMDD)")

    parser.add_argument("--hide-coef", action="store_false", help="Hide coefficient in output")
    parser.add_argument("--top_n", type=int, default=None, help="Show only top N matches by coefficient")

    args = parser.parse_args()

    results = get_matches_coef(args.start_date, args.end_date)

    if args.top_n:
        results = results[:args.top_n]

    if args.hide_coef:
        for r in results:
            print(f"{r['date']} | {r['teams']} | coef={r['coef']}")
    else:
        for r in results:
            print(f"{r['date']} | {r['teams']}")

if __name__ == "__main__":
    main()