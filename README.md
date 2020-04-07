# chess-analyzer
A small chess analysis library optimized for chess.com data.

This package has two main functionalities. First, it uses the bulk download endpoint from the chess.com API to download and save any users games as PNG files. The second is to parse the game files into game play metrics. The metrics are calculated using a pandas data frame that can also be used as a data object for further analysis such as in a Jupyter notebook.

### Example CLI Usage

The CLI module allows you to either download chess.com games as PGN files or run a basic analysis on a set of PGN files. All commands contain a `--help` flag with additional information.

Download png game files from chess.com API.

```
$ chess-analyzer acviana 2018-01 2020-05
Found 210 games from 2018-01 to 2020-05
```

Run a basic report against a set of PNG game files.

```
$ chess-analyzer analyze acviana
197 games found in data/*.pgn
Total Games: 197
Total Wins: 102 (52%)
Total Losses: 95 (48%)
Latest ELO: 649 (2020.04.01)
Best Win: -126 - supersnorre (773) vs acviana (647) 0-1
Total Opponents: 190
Repeat Opponents: 7


By time control:


Time Control: 60s
Total Games: 169
Total Wins: 90 (53%)
Total Losses: 79 (47%)
Latest ELO: 649 (2020.04.01)
Best Win: -101 - jogi221 (708) vs acviana (607) 0-1


Time Control: 600s
Total Games: 17
Total Wins: 10 (59%)
Total Losses: 7 (41%)
Latest ELO: 1114 (2019.04.14)
Best Win: -37 - ShabanAli (1151) vs acviana (1114) 0-1


Time Control: 300s
Total Games: 7
Total Wins: 1 (14%)
Total Losses: 6 (86%)
Latest ELO: 924 (2019.07.04)
Best Win: 61 - jessejoe521 (888) vs acviana (949) 0-1

...
```

### Example Jupyter Notebook Usage

The core Pandas object from the analysis functionality can be loaded directly into a Jupyter notebook for additional analysis. THe following script uses the Seaborn library to generate three histograms of the distribution of a player's ELO spread vs their opponents broken out by total games, wins, and losses.

```python
import pandas as pd
import seaborn as sns
from chess_analyzer.analysis import analysis_main

df = analysis_main(src="data/*.pgn", username="acviana")

sns.distplot(df.elo_spread)
sns.distplot(df[df.is_win].elo_spread)
sns.distplot(df[~df.is_win].elo_spread)

```

![example analysis histogram](https://www.dropbox.com/s/w7n6cafk11ailbm/chess-analyzer-example-histo.png "Logo Title Text 1")
