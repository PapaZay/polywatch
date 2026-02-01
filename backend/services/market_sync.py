#from sqlalchemy.orm import Session
from database import SessionLocal
from models.market import Market
from services.polymarket_service import PolyMarketClient

def sync_markets():
    client = PolyMarketClient()
    db = SessionLocal()
    try:
        events = client.get_events(limit=100)
        count = 0
        for event in events:
            tags = event.get("tags", [])
            category = tags[0]["label"].title() if tags else None

            for market_data in event.get("markets", []):
                count += 1
                market_id = market_data.get("id")
                existing = db.query(Market).filter(Market.id == market_id).first()

                if existing:
                    existing.status = "closed" if market_data.get("closed") else "open"
                    existing.outcomes = market_data.get("outcomes")
                    existing.category = category
                    existing.title = market_data.get("question", "")
                else:
                    market = Market(
                        id=market_id,
                        title=market_data.get("question", ""),
                        category=category,
                        status="closed" if market_data.get("closed") else "open",
                        outcomes=market_data.get("outcomes")
                    )
                    db.add(market)
        db.commit()
        print(f"Synced {count} markets from {len(events)} events")

    except Exception as e:
        db.rollback()
        print(f"Error syncing markets: {e}")
    finally:
        client.close()
        db.close()

if __name__ == "__main__":
    sync_markets()