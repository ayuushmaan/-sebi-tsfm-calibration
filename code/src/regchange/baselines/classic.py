"""HAR and GARCH baselines."""

import numpy as np


def har_forecast(rv: np.ndarray, lags=(1, 5, 22)) -> float:
    """HAR-RV style forecast using past realized vols."""
    if len(rv) == 0:
        return np.nan
    feats = []
    for l in lags:
        if len(rv) >= l:
            feats.append(np.mean(rv[-l:]))
        else:
            feats.append(np.mean(rv))
    w = [0.3, 0.4, 0.3]
    return float(np.dot(w[: len(feats)], feats))
