# NBA CloseGame Finder

Find the most exciting NBA games based on how close and competitive they were in the end of the game.

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python main.py 20260220 20260325

or

python main.py 20260220 20260325 --hide-coef 

or 

python main.py 20260220 20260325 --hide-coef --top_n 5 
```

## How it works

Each game gets a score based on how close it was:

Coef = min(average score difference except first 3 quarters, final score difference)

Lower coefficient → Game is more exciting

More overtimes → Less coefficient

## Data source

Data is taken from `basketball-reference.com`
