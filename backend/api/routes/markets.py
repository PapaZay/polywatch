from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.market import Market


router = APIRouter()

@router.get("/markets")
def get_markets(limit: int = 20, db: Session = Depends(get_db)):
    events = db.query(Market).filter(Market.status == "open", Market.volume >= 10000).order_by(Market.updated_at.desc()).limit(limit).all()
    markets = []
    for market in events:
        markets.append({
            "id": market.id,
            "question": market.title,
            "category": market.category,
            "volume": str(market.volume) if market.volume else "0",
            "outcomePrices": market.outcome_prices,
        })
    return markets