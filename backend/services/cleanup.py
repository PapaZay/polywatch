from datetime import datetime, timezone, timedelta
from database import SessionLocal
from models.market import Market, MarketSnapshot

def cleanup_old_snapshots(days=5):
    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        deleted = db.query(MarketSnapshot).filter(
            MarketSnapshot.ts < cutoff,
            MarketSnapshot.market_id.in_(
                db.query(Market.id).filter(Market.status == "open")
            )
        ).delete(synchronize_session=False)
        db.commit()
        print(f"Cleanup up {deleted} old snapshots")
    except Exception as e:
        db.rollback()
        print(f"Error cleaning up: {e}")
    finally:
        db.close()