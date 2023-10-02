


# skillissue

**Visualize your skill progression in a speedrun using your splits file.**

### Install requirements: ```pip install -r requirements.txt```
### Usage: ```python skillissue.py [-h] [-w WEIGHT] [-m MIN_WEIGHT] [-d] [-s START] [-p PERCENTILE] [-a] [-H] filename```

### Positional arguments:
  `filename`: LiveSplit splits file (.lss)

### Options
* `-h`, `--help`: show this help message and exit

* `-w WEIGHT`, `--weight WEIGHT`: Weight decay factor. The lower the values, the more your recent times are prioritized. Values between [0,1]. Default 15/16.

* `-m MIN_WEIGHT`, `--min_weight MIN_WEIGHT`: Increase this to drop old attempts completely. After the weight of a time has decayed to this value, the time will be dropped. Useful with -H. Default 0.

* `-d`, `--drop_missing`: By default, resets are counted as infinite time runs. This option ignores them instead.

* `-s START`, `--start START`: Older attempts than this will not be shown in the resulting graph. Default 1.

* `-p PERCENTILE`, `--percentile PERCENTILE`: Use a different percentile than the default median (0.5). 0 is equal to personal best.

* `-a`, `--use_average`: Uses average instead of percentile for calculations. Forces -d and ignores -p.

* `-H`, `--hist`, `--histogram`: Output a histogram visualizing the distribution of your times instead of a progression chart. Forces -d and ignores -p and -a.

### Sample graph

![Sample graph](sample_figure.png)
