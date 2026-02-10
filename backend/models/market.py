import uuid
from database import Base
from sqlalchemy import Column, String, Text, Numeric, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func


class Market(Base):
    __tablename__ = "markets"

    id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    category = Column(String, index=True)
    status = Column(String, index=True)
    volume = Column(Numeric(18, 2))
    outcome_prices = Column(JSONB)
    outcomes = Column(JSONB)
    resolution_result = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    ts = Column(DateTime(timezone=True), primary_key=True, server_default=func.now())
    market_id = Column(String, ForeignKey("markets.id"), primary_key=True)
    price = Column(Numeric(10, 4))
    volume = Column(Numeric(18, 2))
    liquidity = Column(Numeric(18, 2))
    bid_ask_spread = Column(Numeric(10, 4))

class Signal(Base):
    __tablename__ = "signals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    market_id = Column(String, ForeignKey("markets.id"), nullable=False)
    signal_type = Column(String, nullable=False)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="active")
    confidence = Column(Numeric(4, 2))
    signal_metadata = Column(JSONB)

# class TraderPerformance(Base):
#   __tablename__ = "trader_performance"