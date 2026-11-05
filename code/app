import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title='SEBI F&O Breaks - Calibration Dashboard', layout='wide')
st.title('Do Foundation Models Notice When the Rules Change?')
st.caption('Calibration across SEBI F&O reforms | Testbed of documented exogenous interventions')

exp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'experiments')
files = sorted([f for f in os.listdir(exp_dir) if f.endswith('.csv')])
if not files:
    st.warning('No CSV files found')
else:
    tabs = st.tabs(files)
    for tab,f in zip(tabs,files):
        with tab:
            df = pd.read_csv(os.path.join(exp_dir,f))
            st.dataframe(df, use_container_width=True)
