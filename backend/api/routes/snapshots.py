from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.market import MarketSnapshot
from datetime import datetime, timedelta, timezone
router = APIRouter()

@router.get("/markets/{market_id}/snapshots")
def snapshot_history(market_id: str, db: Session= Depends(get_db)):
    five_days_ago = datetime.now(timezone.utc) - timedelta(days=5)
    query = db.query(MarketSnapshot).filter(MarketSnapshot.market_id == market_id, MarketSnapshot.ts >= five_days_ago).order_by(MarketSnapshot.ts.desc()).all()
    
    snapshots = []
    for snapshot in query:
        snapshots.append({
            "timestamp": snapshot.ts,
            "price": snapshot.price,
            "volume": snapshot.volume,
            "liquidity": snapshot.liquidity,
        })
    return snapshots