from modules.weighted_utils import *
from modules.plotting import *
import numpy as np

AGGREGATE_DATAPOINTS = 1000

def analyze_split_data(args, splits):   
    """Calculate statistic from split data using a weighted window moving from past towards present and visualize it."""
    aggregate_result_history = np.zeros(AGGREGATE_DATAPOINTS)
    aggregate_sim_results = np.zeros(args.n_sims)
    splitwise_analysis = len(splits) > 1
    # Loop through each split in the splits object. If there are several splits, analyze each individually
    # and then perform aggreate analysis.
    for split in splits:
        weighted_attempts = list(filter(lambda x: x[1] > args.min_weight, list(map(
            lambda x: (x[0], args.weight ** x[0], x[1]),
            enumerate(reversed(split.attempts))
        ))))

        finish_rate = (split.nof_attempts - split.missing) / split.nof_attempts

        weighted_utils = WeightedUtils(weighted_attempts)

        if args.hist:
            plot_hist(weighted_attempts, args.start, len(split.attempts), finish_rate, split.name)
            if splitwise_analysis:
                sim_results = weighted_utils.simulate(
                    args.n_sims,
                    max_index=len(split.attempts) - args.start + 1,
                )
                aggregate_sim_results += np.array(sim_results)
            continue
        
        result_history = []
        # Loop through different weighted window positions.
        # Always starts from first attempt and then increasing weight towards the cutoff.
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
    
        for i in range(AGGREGATE_DATAPOINTS):
            aggregate_result_history[i] += result_history[int(len(split.attempts) * i / AGGREGATE_DATAPOINTS)]

        plot_progress(result_history, args.start, len(split.attempts),
                      args.percentile, args.use_average, finish_rate, split.name)
        
    if splitwise_analysis:
        if args.hist:
            plot_hist(list(map(lambda x: (None, 1, x), aggregate_sim_results)),
                      0, args.n_sims, density=True)
            return
        plot_progress(aggregate_result_history, args.start, AGGREGATE_DATAPOINTS,
                      args.percentile, args.use_average, ratio_format=True)


