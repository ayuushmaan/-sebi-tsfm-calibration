"""Rule-keyed in-context retrieval for TSFMs."""

import numpy as np
import pandas as pd


class RuleKeyedRetrieval:
    def __init__(self, max_context: int = 60):
        self.max_context = max_context

    def get_context(self, df: pd.DataFrame, current_date: pd.Timestamp, break_date: pd.Timestamp, treated_pool: dict = None):
        """Retrieve context using rule-keyed logic: prefer post-break same-regime history, else cross-series treated pool."""
        # post-break only context
        post = df[df.index >= break_date]
        if len(post) >= self.max_context:
            return post.iloc[-self.max_context:]
        # if short, try cross-series pool
        if treated_pool:
            combined = []
            for name, tdf in treated_pool.items():
                p2 = tdf[(tdf.index >= break_date) & (tdf.index <= current_date)]
                combined.append(p2)
            if combined:
                allp = pd.concat(combined)
                allp = allp[~allp.index.duplicated(keep='first')]
                allp = allp.sort_index()
                ctx = pd.concat([post, allp])
                ctx = ctx[~ctx.index.duplicated(keep='first')]
                return ctx.iloc[-self.max_context:]
        return post.iloc[-self.max_context:] if len(post) > 0 else df.iloc[-self.max_context:]
