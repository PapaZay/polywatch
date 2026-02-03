import json
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from database import SessionLocal
from models.market import Market, MarketSnapshot, Signal

def detect_volume_spikes(db, sigma_threshold: float = 2.0):
    signals = []
    week_ago = datetime.now(timezone.utc) - timedelta(days=7) # about a week ago, week ago!

    markets = db.query(Market).filter(Market.status == "open").all()

    for market in markets:
        stats = db.query(
            func.avg(MarketSnapshot.volume).label("avg_vol"),
            func.stddev(MarketSnapshot.volume).label("std_vol"),
        ).filter(
            MarketSnapshot.market_id == market.id,
            MarketSnapshot.ts >= week_ago,
        ).first()

        if not stats or not stats.avg_vol or not stats.std_vol:
            continue

        avg_vol = float(stats.avg_vol)
        std_vol = float(stats.std_vol)

        if std_vol == 0:
            continue

        latest = (db.query(MarketSnapshot).filter(
            MarketSnapshot.market_id == market.id
        ).order_by(MarketSnapshot.ts.desc()).first())

        if not latest:
            continue

        current_vol = float(latest.volume)
        z_score = (current_vol - avg_vol) / std_vol

        if z_score > sigma_threshold:
            confidence = min(z_score / 5.0, 1.0)
            signals.append({
                "market_id": market.id,
                "title": market.title,
                "signal_type": "volume_spike",
                "confidence": round(confidence, 2),
                "details": {
                    "current_volume": current_vol,
                    "avg_volume": round(avg_vol, 2),
                    "std_dev": round(std_vol, 2),
                    "z_score": round(z_score, 2),
                }
            })
    return signals

