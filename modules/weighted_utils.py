import random

class WeightedUtils():
    """Calcualte weighted statistics from an array of (index, weight, value) tuples."""
    def __init__(self, arr):
        self.__arr = arr
        self.__sorted_arr = sorted(self.__arr, key=lambda x: x[2])

    def weighted_percentile(self, percentile, w_sum, min_index = 0, max_index = -1):
        sum = 0
        for i, elem in enumerate(self.__sorted_arr):
            original_i = elem[0]
            w = elem[1]
            if original_i < min_index or (max_index >= 0 and original_i >= max_index):
                continue
            sum += w
            if round(sum / w_sum, 5) == round(percentile, 5):
                # If we're at the last element we can't take the average of two.
                if i == len(self.__sorted_arr) - 1:
                    return self.__sorted_arr[i][2]
                return ((self.__sorted_arr[i][2] + self.__sorted_arr[i + 1][2]) / 2)
            elif round(sum / w_sum, 5) > round(percentile, 5):
                return self.__sorted_arr[i][2]
        return None
    
    def weighted_average(self, w_sum, min_index, max_index = -1):
        sum = 0
        for elem in self.__arr:
            original_i = elem[0]
            w = elem[1]
            v = elem[2]
            if original_i < min_index or (max_index >= 0 and original_i >= max_index):
                continue
            sum += w * v
        return sum / w_sum

    def simulate(self, n, min_index = 0, max_index = -1):
        """Return an arrary of n simulations from the weighted array."""
        w_sum = sum(map(lambda x: x[1], self.__arr[min_index:max_index]))
        sim_results = []
        for _ in range(n):
            sim_results.append(self.weighted_percentile(random.random(), w_sum, min_index, max_index))
        return sim_results
