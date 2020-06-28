import numpy as np
import math

np.warnings.filterwarnings('ignore')


def min_path_length(model):
    return np.nanmin([np.nanmin(ant.path_lengths) for ant in model.schedule.agents])


def mean_min_path_length(model):
    return np.nanmean([np.nanmin(ant.path_lengths) for ant in model.schedule.agents])
