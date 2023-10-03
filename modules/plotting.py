from matplotlib import pyplot as plt
import modules.tick_format
import os
from slugify import slugify

def plot_progress(result_history,start, stop, percentile, use_average,
                  finish_rate = None, split_name = None, ratio_format = False):
    plt.close()
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    fig.set_figheight(7)
    plt.xlabel("Percentage of attempts" if ratio_format else "Attempt")
    plt.ylabel("Time")
    if use_average:
        measure_name = "Average"
    elif percentile == 0.5:
        measure_name = "Median"
    elif percentile == 0:
        measure_name = "PB"
    else:
        measure_name = f"Percentile {percentile}"
    name_in_title = f": {split_name}" if split_name else ""
    finish_rate_in_title =  f" (Finish Rate: {finish_rate * 100:.2f}%)" if finish_rate else ""
    plt.title(f"{measure_name} Progress{name_in_title}{finish_rate_in_title}")
    xdata = range(start, stop + 1)
    if ratio_format:
        xdata = list(map(lambda x: x / stop * 100, xdata))
    ax.plot(xdata, result_history[start - 1:])
    ax.yaxis.set_major_formatter(modules.tick_format.formatter)
    # If we are looking at an individual split, save the graph into a folder instead.
    if split_name:
        output_dir = "skillissue_output/progress/"
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        plt.savefig(f"{output_dir}{slugify(split_name)}.png")
        return
    plt.show()
    

def plot_hist(weighted_attempts, start, stop, finish_rate = None, split_name = None, density = False):
    plt.close()
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    fig.set_figheight(7)
    plt.xlabel("Time")
    plt.ylabel(f"Weighted {'Density' if density else 'Frequency'}")
    name_in_title = f": {split_name}" if split_name else ""
    finish_rate_in_title =  f" (Finish rate: {finish_rate * 100:.2f}%)" if finish_rate else ""
    plt.title(f"Attempt Time Distribution{name_in_title}{finish_rate_in_title}")
    attempts = list(map(lambda x: x[2], weighted_attempts))[:stop - start + 1]
    weights = list(map(lambda x: x[1], weighted_attempts))[:stop - start + 1]
    ax.hist(attempts, weights=weights, density=density)
    ax.xaxis.set_major_formatter(modules.tick_format.formatter)
    if split_name:
        output_dir = "skillissue_output/hist/"
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        plt.savefig(f"{output_dir}{slugify(split_name)}.png")
        return
    plt.show()