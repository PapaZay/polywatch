from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from database import SessionLocal
from models.market import Market, MarketSnapshot, Signal

def detect_volume_spikes(db, sigma_threshold: float = 3.0):
    signals = []
    week_ago = datetime.now(timezone.utc) - timedelta(days=7) # about a week ago, week ago!
    markets = db.query(Market).filter(Market.status == "open").all()

    for market in markets:
        snapshots = db.query(MarketSnapshot).filter(
            MarketSnapshot.market_id == market.id,
            MarketSnapshot.ts >= week_ago,
        ).order_by(MarketSnapshot.ts.asc()).all()

        if len(snapshots) < 10:
            continue

        deltas = []
        for i in range(1, len(snapshots)):
            delta = float(snapshots[i].volume) - float(snapshots[i-1].volume)
            if delta > 0:
                deltas.append(delta)

        if len(deltas) < 5:
            continue


        avg_delta = sum(deltas) / len(deltas)
        std_delta = (sum((d - avg_delta) ** 2 for d in deltas) / len(deltas)) ** 0.5

        if std_delta == 0:
            continue

        latest_delta = float(snapshots[-1].volume) - float(snapshots[-2].volume)

        if latest_delta < 1000:
            continue

        z_score = (latest_delta - avg_delta) / std_delta

        if z_score > sigma_threshold:
            confidence = min(z_score / 5.0, 1.0)
            signals.append({
                "market_id": market.id,
                "title": market.title,
                "signal_type": "volume_spike",
                "confidence": round(confidence, 2),
                "details": {
                    "current_volume": latest_delta,
                    "avg_volume": round(avg_delta, 2),
                    "std_dev": round(std_delta, 2),
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
    now = datetime.now(timezone.utc)
    new_count = 0
    updated_count = 0
    for s in signals:
        existing = db.query(Signal).filter(
            Signal.market_id == s["market_id"],
            Signal.signal_type == s["signal_type"],
            Signal.status == "active",
        ).first()
        if existing:
            existing.last_seen = now
            existing.confidence = s["confidence"]
            existing.signal_metadata = s["details"]
            updated_count += 1
        else:

            signal = Signal(
                market_id=s["market_id"],
                signal_type=s["signal_type"],
                confidence=s["confidence"],
                signal_metadata=s["details"],
                status="active",
            )
            db.add(signal)
            new_count += 1
    db.commit()
    print(f"New signals: {new_count}, Updated signals: {updated_count}")
    return new_count

def resolve_old_signals(db, active_market_ids, signal_type):
    db.query(Signal).filter(
        Signal.signal_type == signal_type,
        Signal.status == "active",
        ~Signal.market_id.in_(active_market_ids),
        ).update({"status": "resolved"}, synchronize_session=False)

def run_detections():
    db = SessionLocal()
    try:
        print("Running pattern detectors...")

        volume_signals = detect_volume_spikes(db)
        print(f"Volume spikes: {len(volume_signals)}")

        active_volume_markets = [s["market_id"] for s in volume_signals]
        resolve_old_signals(db, active_volume_markets, "volume_spike")

        momentum_signals = detect_price_momentum(db)
        print(f"Price momentum: {len(momentum_signals)}")

        active_momentum_markets = [s["market_id"] for s in momentum_signals]
        resolve_old_signals(db, active_momentum_markets, "price_momentum")

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