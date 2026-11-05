# Rule-Change Calibration (SEBI F&O TSFMs)

Calibration of TSFMs/TFMs across SEBI F&O reforms. Studies how rule changes affect probabilistic forecasts for realized volatility and whether rule-keyed retrieval helps under short post-break history.

## Repository layout
- code/src/ — Core library (data, breaks, baselines, retrieval, evaluation)
- code/app/ — Streamlit dashboard
- code/scripts/ — Utility scripts
- code/configs/ — Experiment configs
- esults/tables/ — Main experiment outputs (CSV)
- esults/checks/ — Leakage/sanity checks
- igures/event_study/ — Event-study plots
- docs/results/ — Consolidated results summary
- docs/paper_notes/ — Notes/materials
- data/ — Data (raw/processed/external placeholders)
- experiments/archive/ — Archived scripts/details
- rtifacts/raw_sync/ — Raw sync artifacts (ignored)
- paper/ — Paper draft workspace

## Key artifacts
- esults/tables/days_since_break_width.csv — Coverage/Winkler/width by days-since-break (core)
- esults/tables/master_results.csv — Overall method comparison
- esults/tables/econ_utility_summary.csv — Sizing/shortfall proxy
- esults/tables/paper_table_index.csv — Index of paper tables
- docs/results/RESULTS.md — Summary