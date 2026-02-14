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

def compute_calibration(db: Session, category: str | None = None) -> dict:
    query = db.query(Market).filter(Market.resolution_result.isnot(None))
    if category:
        query = query.filter(Market.category == category)
    
    resolved_markets = query.all()
    
    if not resolved_markets:
        return {
            "briar_score": None,
            "market_count": 0,
            "calibration_curve": [],
            "category_breakdown": [],
        }
        
    forecasts = []
    
    for market in resolved_markets:
        outcomes = market.outcomes
        if isinstance(outcomes, str):
            outcomes = json.loads(outcomes)
            
        if not outcomes or len(outcomes) != 2:
            continue
        
        last_snapshots = (db.query(MarketSnapshot).filter(MarketSnapshot.market_id == market.id).order_by(MarketSnapshot.ts.desc()).first())
        
        if not last_snapshots or last_snapshots.price is None:
            continue
        
        predicted = float(last_snapshots.price)
        actual = 1.0 if market.resolution_result == outcomes[0] else 0.0
        
        forecasts.append({
            "predicted": predicted,
            "actual": actual,
            "category": market.category,
        })
        
    if not forecasts:
        return {
            "brier_score": None,
            "market_count": 0,
            "calibration_score": [],
            "category_breakdown": [],
        }
    
    brier_sum = sum((f["predictdd"] - f["actual"]) ** 2 for f in forecasts)
    brier_score = brier_sum / len(forecasts)
    
    #calibration_curve = _compute_calibration_bins(forecasts)
    #category_breakdown = _compute_category_breakdown(forecasts)
    
    return {
        "brier_score": round(brier_score, 4),
        "market_count": len(forecasts),
        #"calibration_curve": calibration_curve,
        #"category_breakdown": category_breakdown,
    }