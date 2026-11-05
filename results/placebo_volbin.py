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
from regchange.evaluation.coverage import conditional_coverage

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
    tmp['rv5'] = realized_vol_close(tmp['close'], 5)
    tmp = tmp.dropna(subset=['rv20'])
    proc[k] = tmp

np.random.seed(123)
results = []
for br in SEBI_REFORMS:
    if br.name == 't1_settlement': continue
    bdate = pd.Timestamp(br.date)
    for name, tmp in proc.items():
        pre = tmp[tmp.index < bdate]
        if len(pre) < 200: continue
        for i in range(30):
            pdate = pre.index[np.random.randint(50, len(pre)-50)]
            pre2 = tmp[tmp.index < pdate]
            post2 = tmp[tmp.index >= pdate]
            if len(pre2)<50 or len(post2)<10: continue
            pred = pre2['rv20'].rolling(20).mean().iloc[-len(post2):].values
            if len(pred)!=len(post2): continue
            actual = post2['rv20'].values[:len(pred)]
            std_pre = pre2['rv20'].std()
            z=1.645
            lower = pred-z*std_pre; upper = pred+z*std_pre
            cov = conditional_coverage(actual, lower, upper)
            results.append({'break': br.name, 'series': name, 'type': 'placebo', 'coverage': float(cov)})

for br in SEBI_REFORMS:
    if br.name == 't1_settlement': continue
    bdate = pd.Timestamp(br.date)
    for name, tmp in proc.items():
        pre = tmp[tmp.index < bdate]
        post = tmp[tmp.index >= bdate]
        if len(pre)<50 or len(post)<10: continue
        qs = pre['rv5'].quantile([0,0.2,0.4,0.6,0.8,1.0])
        for ql, qu in zip(qs.values[:-1], qs.values[1:]):
            mpost = post[(post['rv5']>=ql)&(post['rv5']<qu)]
            if len(mpost)<3: continue
            pred = np.array([pre['rv20'].tail(20).mean()]*len(mpost))
            actual = mpost['rv20'].values
            std_pre = pre['rv20'].std(); z=1.645
            lower = pred-z*std_pre; upper = pred+z*std_pre
            cov = conditional_coverage(actual, lower, upper)
            results.append({'break': br.name, 'series': name, 'type': 'volbin', 'coverage': float(cov), 'qbin': int((ql/qu) if qu!=0 else 0)})

res = pd.DataFrame(results)
res.to_csv('/home/marimo/quant/experiments/placebo_volbin.csv', index=False)
print(res[res['type']=='placebo'].groupby(['break','series'])['coverage'].mean())
print(res[res['type']=='volbin'].groupby(['break','series'])['coverage'].mean())
mo.status.toast('done')
