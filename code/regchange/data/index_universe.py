"""Treated vs control index definitions."""

# Treated: indices that lost weekly options / affected by weekly expiry changes
TREATED = ["^NSEBANK", "NIFTY_FIN_SERVICE.NS", "NIFTY_MIDCAP_SELECT.NS", "BANKNIFTY.NS"]  # Bank Nifty/FinNifty/Midcap Select variants

# Control: indices that never had weeklies (or less directly affected) - use as counterfactual
CONTROL = ["^NSEI", "NIFTYIT.NS", "NIFTYPHARMA.NS", "^CNX100"]

# Map common names
INDEX_MAP = {
    "banknifty": "^NSEBANK",
    "finnifty": "NIFTY_FIN_SERVICE.NS",
    "midcap_select": "NIFTY_MIDCAP_SELECT.NS",
    "nifty": "^NSEI",
}
