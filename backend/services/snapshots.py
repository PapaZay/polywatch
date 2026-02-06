import time
from datetime import datetime, timezone

from database import SessionLocal
from models.market import Market, MarketSnapshot
from services.polymarket_service import PolyMarketClient
from services.pattern_detectors import run_detections
import json
def collect_snapshots():
    client = PolyMarketClient()
    db = SessionLocal()

    try:
        events = client.get_events(limit=100)
        count = 0
        now = datetime.now(timezone.utc)

        for event in events:
            for market_data in event.get("markets", []):
                market_id = market_data.get("id")

                exists = db.query(Market).filter(Market.id == market_id).first()
                if not exists:
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
    print(f"Collecting snapshots (every {interval_minutes} mins)")
    while True:
        collect_snapshots()
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    run_collector(interval_minutes=5)