import argparse
import xml.etree.ElementTree as ET
from datetime import datetime as dt
import re
from modules.weighted_utils import *
from modules.restricted_types import *
from modules.plotting import *

DEFAULT_DT = dt.strptime("0:0:0.00", "%H:%M:%S.%f")

def main():
    parser = argparse.ArgumentParser(description="Visualize your skill progression in a speedrun using your splits file.")
    parser.add_argument("filename",
                        help="LiveSplit splits file (.lss)")
    parser.add_argument("-w", "--weight",
                        type=restricted_float,
                        help="Weight decay factor. The lower the values, the more your recent times are prioritized. Values between [0,1]. Default 15/16.",
                        default=15/16)
    parser.add_argument("-m", "--min_weight",
                        type=restricted_float,
                        help="Increase this to drop old attempts completely. After the weight of a time has decayed to this value, the time will be dropped. Useful with -H. Default 0.",
                        default=0)
    parser.add_argument("-d", "--drop_missing",
                        action="store_true",
                        help="By default, resets are counted as infinite time runs, essentially treating them as forfeits. This option ignores them instead.")
    parser.add_argument("-s", "--start",
                        type=positive_int,
                        help="Older attempts than this will not be shown in the resulting graph. Default 1.",
                        default=1)
    parser.add_argument("-p", "--percentile",
                        type=restricted_float,
                        help="Use a different percentile than the default median (0.5). 0 is equal to personal best.",
                        default=0.5)
    parser.add_argument("-a", "--use_average",
                        action="store_true",
                        help="Uses average instead of percentile for calculations. Forces -d and ignores -p.")
    parser.add_argument("-H", "--hist", "--histogram",
                        action="store_true",
                        help="Output a histogram visualizing the distribution of your times instead of a progression chart. Forces -d and ignores -p and -a.")
    parser.add_argument("-r", "--remake_window",
                        type=positive_int,
                        help="Number of seconds during which resets at the start of a run are not counted as a forfeit.",
                        default=0)
    #TODO parser.add_argument("-P", "--per_split",
    #TODO                     action="store_true",
    #TODO                     help="Generate the output splitwise instead of based on the finish times. Stores the output plots in a folder.")

    args = parser.parse_args()

    try:
        tree = ET.parse(args.filename)
    except OSError as err:
        print("Failed to read:", err.filename)
        exit()
    except ET.ParseError:
        print("Malformatted splits")
        exit()

    weight = args.weight
    drop_missing = args.drop_missing or args.use_average or args.hist
    start = args.start
    percentile = args.percentile
    use_average = args.use_average
    hist = args.hist
    min_weight = args.min_weight
    remake_window = args.remake_window

    # Read run times from splits file into an array
    root = tree.getroot()
    attempts = []
    missing = 0
    nof_attempts = 0
    for attempt in root.find("AttemptHistory").findall("Attempt"):
        nof_attempts += 1
        realtime = attempt.find("RealTime")
        if realtime != None:
            text = re.search("[^.]*...", realtime.text).group()
            t = dt.strptime(text, "%H:%M:%S.%f")
            attempts.append((t - DEFAULT_DT).total_seconds())
            continue
        missing += 1
        if not drop_missing:
            started = dt.strptime(attempt.attrib["started"], "%m/%d/%Y %H:%M:%S")
            ended = dt.strptime(attempt.attrib["ended"], "%m/%d/%Y %H:%M:%S")
            attempt_time = ended - started
            if attempt_time.seconds > remake_window:
                attempts.append(float("inf"))
            else:
                # Undo the added missing time in case run was shorter than remake_window
                missing -= 1

    # Calculate statistic using a weighted window moving from past towards present
    weighted_attempts = list(filter(lambda x: x[1] > min_weight, list(map(
        lambda x: (x[0], weight ** x[0], x[1]),
        enumerate(reversed(attempts))
    ))))

    finish_rate = (nof_attempts - missing) / nof_attempts

    if hist:
        plot_hist(weighted_attempts, start, len(attempts), finish_rate)
        return
    
    weighted_utils = WeightedUtils(weighted_attempts)
    result_history = []
    for i in range(len(attempts)):
        latest_attempt = (len(attempts) - i - 1)
        if use_average:
            result = weighted_utils.weighted_average(
                sum(weight ** x for x in range(latest_attempt, len(attempts))),
                min_index=latest_attempt
            )
        else:
            result = weighted_utils.weighted_percentile(
                percentile,
                sum(weight ** x for x in range(latest_attempt, len(attempts))),
                min_index=latest_attempt
            )
        result_history.append(result)
    
    plot_progress(result_history, start, len(attempts), percentile, use_average, finish_rate)

main()