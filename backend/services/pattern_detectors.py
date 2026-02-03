from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from database import SessionLocal
from models.market import Market, MarketSnapshot, Signal

def detect_volume_spikes(db, sigma_threshold: float = 3.0):
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

        if current_vol < 100000:
            continue

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

def detect_price_momentum(db, threshold: float = 0.15):
    signals = []
    six_hours_ago = datetime.now(timezone.utc) - timedelta(hours=6)
    markets = db.query(Market).filter(Market.status == "open").all()

    for market in markets:
        latest = db.query(MarketSnapshot).filter(
            MarketSnapshot.market_id == market.id
        ).order_by(MarketSnapshot.ts.desc()).first()

        earlier = db.query(MarketSnapshot).filter(
            MarketSnapshot.market_id == market.id,
            MarketSnapshot.ts <= six_hours_ago,
        ).order_by(MarketSnapshot.ts.desc()).first()

        if not latest or not earlier or not latest.price or not earlier.price:
            continue

        current_price = float(latest.price)
        earlier_price = float(earlier.price)

        if earlier_price == 0:
            continue

        diff = abs(current_price - earlier_price)

        if diff > threshold:
            direction = "up" if current_price > earlier_price else "down"
            confidence = min(diff / 0.3, 1.0)

            signals.append({
                "market_id": market.id,
                "title": market.title,
                "signal_type": "price_momentum",
                "confidence": round(confidence, 2),
                "details": {
                    "current_price": current_price,
                    "earlier_price": earlier_price,
                    "change": round(diff, 4),
                    "direction": direction,
                }
            })

    return signals

def save_signals(db, signals):
    count = 0
    for s in signals:
        signal = Signal(
            market_id=s["market_id"],
            signal_type=s["signal_type"],
            confidence=s["confidence"],
            signal_metadata=s["details"],
        )
        db.add(signal)
        count += 1
    db.commit()
    return count

def run_detections():
    db = SessionLocal()
    try:
        print("Running pattern detectors...")

        volume_signals = detect_volume_spikes(db)
        print(f"Volume spikes: {len(volume_signals)}")

        momentum_signals = detect_price_momentum(db)
        print(f"Price momentum: {len(momentum_signals)}")

        all_signals = volume_signals + momentum_signals

        if all_signals:
            saved = save_signals(db, all_signals)
            print(f"Saved {saved} signals to database")

            for s in all_signals:
                print(f"[{s['signal_type']} {s['title'][:50]}]"
                      f"(confidence: {s['confidence']})")
        else:
            print("No signals detected")
    except Exception as e:
        db.rollback()
        print(f"Error in pattern detection: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_detections()