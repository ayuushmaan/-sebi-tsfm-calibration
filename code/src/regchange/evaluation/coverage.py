"""Coverage metrics."""

import numpy as np


def conditional_coverage(y, lower, upper):
    covered = ((y >= lower) & (y <= upper)).astype(float)
    return covered.mean()


def winkler_score(y, lower, upper, alpha=0.1):
    score = np.zeros_like(y)
    covered = (y >= lower) & (y <= upper)
    score[covered] = upper[covered] - lower[covered]
    score[~covered] = (upper[~covered] - lower[~covered]) + (2 / alpha) * (lower[~covered] - y[~covered])
    # upper violation
    viol_upper = y > upper
    if viol_upper.any():
        score[viol_upper] = (upper[viol_upper] - lower[viol_upper]) + (2 / alpha) * (y[viol_upper] - upper[viol_upper])
    return score.mean()
