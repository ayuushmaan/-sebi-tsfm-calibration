"""Quick check of breaks and data fetch."""
import sys
sys.path.insert(0, "src")
from regchange.breaks.sebi_reforms import SEBI_REFORMS
from regchange.data.fetch import fetch_indices
from regchange.data.index_universe import TREATED, CONTROL
print([r.name for r in SEBI_REFORMS])
try:
    data = fetch_indices([TREATED[0], CONTROL[0]], "2024-01-01", "2025-12-31")
    print(list(data.keys()))
    for k, v in data.items():
        print(k, len(v))
except Exception as e:
    print(e)
