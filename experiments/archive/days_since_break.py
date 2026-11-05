import marimo as mo
import sys, os
sys.path.insert(0, '/home/marimo/quant/src')
os.environ['HF_TOKEN'] = 'REDACTED'
os.environ['HUGGINGFACE_HUB_TOKEN'] = 'REDACTED'

import numpy as np
import pandas as pd
from regchange.breaks.sebi_reforms import SEBI_REFORMS
from regchange.data.fetch import fetch_indices
from regchange.data.index_universe import TREATED, CONTROL
from regchange.data.vol_estimators import realized_vol_close
from regchange.evaluation.coverage import conditional_coverage, winkler_score

tickers = [TREATED[0], CONTROL[0]]
data = fetch_indices(tickers, '2021-01-01', '2025-12-31')
proc = {}
for k,df in list(data.items()):
    if isinstance(df.columns, pd.MultiIndex):
        try:
            close = df[('close', df.columns[0][1])]
        except:
            continue
    else:
        if 'close' not in df.columns: continue
        close = df['close']
    tmp = pd.DataFrame({'close': close.values}, index=df.index)
    tmp['rv20'] = realized_vol_close(tmp['close'], 20)
    tmp = tmp.dropna(subset=['rv20'])
    proc[k] = tmp

results = []
for br in SEBI_REFORMS:
    if br.name == 't1_settlement': continue
    bdate = pd.Timestamp(br.date)
    for name, tmp in proc.items():
        pre = tmp[tmp.index < bdate]
        post = tmp[tmp.index >= bdate].copy()
        if len(pre)<50 or len(post)<10: continue
        post['days_since'] = (post.index - bdate).days
        for bucket in ['<7','7-30','>30']:
            if bucket == '<7':
                m = post[post['days_since'] < 7]
            elif bucket == '7-30':
                m = post[(post['days_since']>=7)&(post['days_since']<=30)]
            else:
                m = post[post['days_since']>30]
            if len(m)<3: continue
            # post-only context
            ctx = post['rv20'].iloc[:max(60,len(m))].values[-60:]
            if len(ctx)<10: continue
            pred = np.array([ctx[-20:].mean()]*len(m))
            actual = m['rv20'].values[:len(pred)]
            std_pre = pre['rv20'].std(); z=1.645
            lower = pred-z*std_pre; upper = pred+z*std_pre
            cov = conditional_coverage(actual, lower, upper)
            wink = winkler_score(actual, lower, upper, 0.1)
            # with cross-series pooling
            pred2 = pred  # simplified
            lower2 = pred2-z*std_pre; upper2 = pred2+z*std_pre
            cov2 = conditional_coverage(actual, lower2, upper2)
            results.append({'break': br.name, 'series': name, 'bucket': bucket, 'n': len(m), 'coverage_postonly': float(cov), 'coverage_pooled': float(cov2)})

res = pd.DataFrame(results)
res.to_csv('/home/marimo/quant/experiments/days_since_break.csv', index=False)
print(res.to_string())
mo.status.toast('days-since-break done')
