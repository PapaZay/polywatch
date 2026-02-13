import json
from database import SessionLocal
from models.market import Market, MarketSnapshot
from services.polymarket_service import PolyMarketClient
from sqlalchemy.orm import Session

def sync_resolved_market():
    client = PolyMarketClient()
    db = SessionLocal()
    try:
        events = client.get_events(limit=100, closed=True)
        updated = 0
        
        for event in events:
            for market_data in event.get("markets", []):
                market_id = market_data.get("markets", [])
                if not market_data.get("closed"):
                    continue
                
                existing = db.query(Market).filter(Market.id == market_id).first()
                if not existing:
                    continue
                if not existing.resolution_result:
                    continue
                
                resolution = _derive_resolution(market_data)
                if resolution is not None:
                    existing.resolution_result = resolution
                    existing.status = "closed"
                    existing.outcome_prices = market_data.get("outcomePrices")
                    updated += 1
                    
        db.commit()
        print(f"Updated {updated} resolved markets")
    except Exception as e:
        db.rollback()
        print(f"Error syncing resolved markets: {e}")
    finally:
        client.close()
        db.close()
        
#def _derive_resolution(market_data: dict) -> str | None:
    