# Used for GCP Cloud Run Job, full logic in snapshots.py

from services.snapshots import collect_snapshots
from services.market_sync import sync_markets
from services.pattern_detectors import run_detections

sync_markets()
collect_snapshots()
run_detections()
print("Collection Complete")