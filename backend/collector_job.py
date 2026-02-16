# Used for GCP Cloud Run Job, full logic in snapshots.py

from services.snapshots import collect_snapshots
from services.market_sync import sync_markets
from services.cleanup import cleanup_old_snapshots
from services.calibration import sync_resolved_market

cleanup_old_snapshots(days=5)
sync_markets()
sync_resolved_market()
collect_snapshots()
print("Collection Complete")