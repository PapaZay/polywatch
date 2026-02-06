from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.market import Signal

router = APIRouter()

@router.get("/signals/active")
def get_active_signals(limit: int = Query(20, le=100),
                       signal_type: Optional[str] = Query(None),
                       db: Session = Depends(get_db)):
    query = db.query(Signal).order_by(Signal.detected_at.desc())

    if signal_type:
        query = query.filter(Signal.signal_type == signal_type)

    signals = query.limit(limit).all()
    result = []
    for s in signals:
        result.append({
            "id": str(s.id),
            "market_id": s.market_id,
            "signal_type": s.signal_type,
            "confidence": float(s.confidence) if s.confidence else None,
            "detected_at": s.detected_at.isoformat() if s.detected_at else None,
            "metadata": s.signal_metadata,
        })
    return result

@router.get("/signals/history/{market_id}")
def get_signal_history(market_id: str,
                       limit: int = Query(50, le=200),
                       db: Session = Depends(get_db)):

    signals = (
        db.query(Signal).filter(Signal.market_id == market_id)
        .order_by(Signal.detected_at.desc())
        .limit(limit)
        .all()
    )

    result = []
    for s in signals:
        result.append({
            "id": str(s.id),
            "signal_type": s.signal_type,
            "confidence": float(s.confidence) if s.confidence else None,
            "detected_at": s.detected_at.isoformat() if s.detected_at else None,
            "metadata": s.signal_metadata,
        })
    return result