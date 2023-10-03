import argparse
from modules.restricted_types import *
from modules.analyze_split_data import *
from modules.read_splits_xml import SplitsXML
import xml.etree.ElementTree as ET

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
                        help="Number of seconds during which resets at the start of a run are not counted as a forfeit. Default 0.",
                        default=0)
    parser.add_argument("-P", "--per_split",
                        action="store_true",
                        help="Generate the output splitwise instead of based on the finish times. Stores the output plots in a folder.")
    parser.add_argument("-n", "--n_sims",
                        type=positive_int,
                        help="Specify how many simulations to perform when generating an aggregate splitwise histogram. Default 1000.",
                        default=1000)
    parser.add_argument("-g", "--game_time",
                        action="store_true",
                        help="Use LiveSplit GameTime instead of RealTime. Proceed with caution if using with -r, as that is still using real time.")
    #TODO fix finish ratio not respecting chosen bounds but always defaulting to full range and in general keep the information about missing splits longer

    args = parser.parse_args()
    args.drop_missing = args.drop_missing or args.use_average or args.hist

    try:
        splits_xml = SplitsXML(args)
    except OSError as err:
        print("Failed to read:", err.filename)
        return
    except ET.ParseError:
        print("Malformatted splits")
        return
    
    if args.per_split:
        splits = splits_xml.read_all_splits()
        analyze_split_data(args, splits)
    else:
        full_runs = splits_xml.read_finished_runs()
        analyze_split_data(args, [full_runs])

main()