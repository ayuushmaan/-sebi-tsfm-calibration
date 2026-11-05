"""Volatility estimators for daily data."""

import numpy as np
import pandas as pd


def parkinson_vol(high: pd.Series, low: pd.Series) -> pd.Series:
    rs = (np.log(high / low)) ** 2
    vol = np.sqrt(rs.mean() / (4 * np.log(2)))
    return vol


def garman_klass_vol(open_: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    log_hl = np.log(high / low) ** 2
    log_co = np.log(close / open_) ** 2
    rs = 0.5 * log_hl - (2 * np.log(2) - 1) * log_co
    return np.sqrt(rs)


def realized_vol_close(close: pd.Series, window: int = 20) -> pd.Series:
    ret = np.log(close / close.shift(1))
    return ret.rolling(window).std() * np.sqrt(252)
