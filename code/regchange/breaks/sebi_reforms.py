"""SEBI F&O reform dates (documented)."""

from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Reform:
    name: str
    date: date
    description: str
    exchange: str = "NSE"


SEBI_REFORMS: List[Reform] = [
    Reform("weekly_expiry_cut", date(2024, 11, 20), "Weekly expiries cut to one per exchange; index contract sizes raised", "NSE/BSE"),
    Reform("upfront_premium_spread_benefit", date(2025, 2, 1), "Upfront option premium collected; calendar-spread benefit removed on expiry day", "NSE"),
    Reform("intraday_position_monitoring", date(2025, 4, 1), "Intraday monitoring of position limits begins", "NSE"),
    Reform("nifty_weekly_expiry_tue", date(2025, 9, 1), "NSE moves Nifty weekly expiry from Thursday to Tuesday", "NSE"),
]
