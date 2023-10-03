from modules.weighted_utils import *
from modules.plotting import *

def analyze_split_data(args, split):   
    """Calculate statistic from split data using a weighted window moving from past towards present and visualize it."""
    weighted_attempts = list(filter(lambda x: x[1] > args.min_weight, list(map(
        lambda x: (x[0], args.weight ** x[0], x[1]),
        enumerate(reversed(split.attempts))
    ))))

    finish_rate = (split.nof_attempts - split.missing) / split.nof_attempts

    if args.hist:
        plot_hist(weighted_attempts, args.start, len(split.attempts), finish_rate)
        return
    
    weighted_utils = WeightedUtils(weighted_attempts)
    result_history = []
    for i in range(len(split.attempts)):
        latest_attempt = (len(split.attempts) - i - 1)
        if args.use_average:
            result = weighted_utils.weighted_average(
                sum(args.weight ** x for x in range(latest_attempt, len(split.attempts))),
                min_index=latest_attempt
            )
        else:
            result = weighted_utils.weighted_percentile(
                args.percentile,
                sum(args.weight ** x for x in range(latest_attempt, len(split.attempts))),
                min_index=latest_attempt
            )
        result_history.append(result)
    
    plot_progress(result_history, args.start, len(split.attempts), args.percentile, args.use_average, finish_rate)