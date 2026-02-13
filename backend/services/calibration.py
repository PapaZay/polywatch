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
        
def _derive_resolution(market_data: dict) -> str | None:
    raw_prices = market_data.get("outcomePrices")
    raw_outcomes = market_data.get("outcomes")
    
    if not raw_prices or not raw_outcomes:
        return None

    try:
        if isinstance(raw_prices, str):
            prices = json.loads(raw_prices)
        else:
            prices = raw_prices
        
        if isinstance(raw_outcomes, str):
            outcomes = json.loads(raw_outcomes)
        else:
            outcomes = raw_outcomes
            
        float_prices = [float(p) for p in prices]
    except (json.JSONDecodeError, ValueError, TypeError):
        return None

    if len(float_prices) != len(outcomes) or len(float_prices) < 2:
        return None
    
    max_price = max(float_prices)
    if max_price < 0.9:
        return None
    
    winner_index = float_prices.index(max_price)
    return outcomes[winner_index]
    