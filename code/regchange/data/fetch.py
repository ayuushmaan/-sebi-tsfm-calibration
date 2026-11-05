"""Fetch OHLCV for Indian indices."""

import os
import numpy as np
import pandas as pd
import yfinance as yf


def fetch_indices(tickers: list, start: str, end: str) -> dict:
    out = {}
    for t in tickers:
        try:
            df = yf.download(t, start=start, end=end, progress=False)
            if df.empty:
                continue
            df = df.rename(columns=str.lower)
            df.index = pd.to_datetime(df.index)
            df["ret"] = np.log(df["close"] / df["close"].shift(1))
            out[t] = df
        except Exception:
            continue
    return out


def save_parquet(data: dict, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    for t, df in data.items():
        safe = t.replace("^", "").replace(".", "_")
        df.to_parquet(os.path.join(out_dir, f"{safe}.parquet"))
