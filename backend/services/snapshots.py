import time
from datetime import datetime, timezone

from database import SessionLocal
from models.market import Market, MarketSnapshot
from services.polymarket_service import PolyMarketClient
from services.pattern_detectors import run_detections
from services.market_sync import sync_markets
from services.calibration import sync_resolved_market
from services.cleanup import cleanup_old_snapshots
import json

def collect_snapshots():
    client = PolyMarketClient()
    db = SessionLocal()

    try:
        events = client.get_events(limit=100)
        count = 0
        now = datetime.now(timezone.utc)

        known_ids = set()
        for m in db.query(Market.id).all():
            known_ids.add(m[0])

        for event in events:
            for market_data in event.get("markets", []):
                market_id = market_data.get("id")

                if market_id not in known_ids:
                    continue

                volume = float(market_data.get("volume", 0))
                if volume < 10000:
                    continue

                prices_str = market_data.get("outcomePrices", "[]")
                try:
                    prices = json.loads(prices_str)
                    price = float(prices[0]) if prices else None
                except (json.JSONDecodeError, IndexError):
                    price = None

                snapshot = MarketSnapshot(
                    ts=now,
                    market_id=market_id,
                    price=price,
                    volume=float(market_data.get("volume", 0)),
                    liquidity=float(event.get("liquidity", 0)),
                )
                db.add(snapshot)
                count += 1

        db.commit()
        print(f"[{now.isoformat()}] Saved {count} snapshots")

        run_detections()
    except Exception as e:
        db.rollback()
        print(f"Error collecting snapshots: {e}")
    finally:
        client.close()
        db.close()

def run_collector(interval_minutes: int = 5):
    sync_interval = 12 * 60
    cycles_to_sync = 0

    print(f"Collecting snapshots (every {interval_minutes} mins)")
    while True:
        if cycles_to_sync <= 0:
            print("Syncing markets...")
            cleanup_old_snapshots(days=5)
            sync_markets()
            sync_resolved_market()
            cycles_to_sync = sync_interval // interval_minutes

        collect_snapshots()
        cycles_to_sync -= 1
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    run_collector(interval_minutes=5)