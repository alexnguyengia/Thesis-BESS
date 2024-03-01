
import numpy as np
import pandas as pd
import time
import numpy as np

def rainflow_counting(soc_time_series):
    # Initialize variables
    cycles = []
    soc_diff = np.diff(soc_time_series)

    # Identify peaks and valleys
    peaks = np.where(soc_diff < 0)[0] + 1
    valleys = np.where(soc_diff > 0)[0] + 1

    # Pair adjacent peaks and valleys
    for peak, valley in zip(peaks, valleys):
        cycles.append((peak, valley))

    # Rainflow counting
    ranges = [soc_time_series[cycle[0]] - soc_time_series[cycle[1]] for cycle in cycles]
    half_ranges = [abs(r) / 2.0 for r in ranges]
    counts = {half_range: half_ranges.count(half_range) for half_range in set(half_ranges)}

    return counts

def calculate_soh(rainflow_counts, total_cycles):
    damage = sum(count * (half_range**3) for half_range, count in rainflow_counts.items())
    soh = 1 - (damage / total_cycles)**(1/3)
    return soh

if _
soc_time_series = np.array([0.2, 0.5, 0.8, 0.3, 0.6, 0.2, 0.9, 0.4, 0.7, 0.1])
total_cycles = len(soc_time_series) - 1  # Total number of cycles is the length of time series minus 1

rainflow_counts = rainflow_counting(soc_time_series)
soh = calculate_soh(rainflow_counts, total_cycles)

print("Rainflow Counts:", rainflow_counts)
print("State of Health (SoH):", soh)


