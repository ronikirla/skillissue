from matplotlib import pyplot as plt
import modules.tick_format

def plot_progress(result_history, start, stop, percentile, use_average, finish_rate):
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    fig.set_figheight(7)
    plt.xlabel("Attempt")
    plt.ylabel("Time")
    if use_average:
        measure_name = "Average"
    elif percentile == 0.5:
        measure_name = "Median"
    elif percentile == 0:
        measure_name = "PB"
    else:
        measure_name = f"Percentile {percentile}"
    plt.title(f"{measure_name} progress (Finish rate: {finish_rate * 100:.2f}%)")
    ax.plot(range(start, stop + 1), result_history[start - 1:])
    ax.yaxis.set_major_formatter(modules.tick_format.formatter)
    plt.show()

def plot_hist(weighted_attempts, start, stop, finish_rate):
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    fig.set_figheight(7)
    plt.xlabel("Time")
    plt.ylabel("Weighted Frequency")
    plt.title(f"Attempt time distribution (Finish rate: {finish_rate * 100:.2f}%)")
    attempts = list(map(lambda x: x[2], weighted_attempts))[:stop - start + 1]
    weights = list(map(lambda x: x[1], weighted_attempts))[:stop - start + 1]
    ax.hist(attempts, weights=weights)
    ax.xaxis.set_major_formatter(modules.tick_format.formatter)
    plt.show()