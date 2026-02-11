import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock
from services.pattern_detectors import detect_volume_spikes, detect_price_momentum

class MockMarket:
    def __init__(self, id, title, status="open"):
        self.id = id
        self.title = title
        self.status = status

class MockSnapshot:
    def __init__(self, ts, market_id, volume, price=0.5):
        self.ts = ts
        self.market_id = market_id
        self.volume = volume
        self.price = price

@pytest.fixture
def db():
    return MagicMock()

@pytest.fixture
def market():
    return MockMarket("m1", "Test Market")

@pytest.fixture
def now():
    return datetime.now(timezone.utc)

class TestVolumeSpikes:
    def test_no_snapshots_return_empty(self, db, market):
        db.query.return_value.filter.return_value.all.return_value = [market]
        db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        assert detect_volume_spikes(db) == []

    def test_less_than_10_snapshots_returns_empty(self, db, market, now):
        db.query.return_value.filter.return_value.all.return_value = [market]
        snapshots = [MockSnapshot(now, "m1", 1000 * i) for i in range(5)]
        db.query.return_value.filter.return_value.order_by.return_value.all.return_value = snapshots

        assert detect_volume_spikes(db) == []

    def test_detect_spike_when_delta_exceeds_threshold(self, db, market, now):
        snapshots = []
        volume = 100000
        for i in range(15):
            snapshots.append(MockSnapshot(now - timedelta(hours=15-i),"m1", volume))
            volume += 1000
        snapshots.append(MockSnapshot(now, "m1", volume + 50000))

        db.query.return_value.filter.return_value.all.return_value = [market]
        db.query.return_value.filter.return_value.order_by.return_value.all.return_value = snapshots

        signals = detect_volume_spikes(db)

        assert len(signals) == 1
        assert signals[0]["market_id"] == "m1"
        assert signals[0]["signal_type"] == "volume_spike"

    def test_no_spike_when_delta_is_normal(self, db, market, now):
        snapshots = []
        volume = 100000
        for i in range(15):
            snapshots.append(MockSnapshot(now - timedelta(hours=15-i),"m1", volume))
            volume += 1000

        db.query.return_value.filter.return_value.all.return_value = [market]
        db.query.return_value.filter.return_value.order_by.return_value.all.return_value = snapshots

        assert detect_volume_spikes(db) == []

    def test_no_spike_when_variance_too_low(self, db, market, now):
        snapshots = []
        volume = 100000
        for i in range(15):
            snapshots.append(MockSnapshot(now - timedelta(hours=15-i), "m1", volume))
            volume += 5

        db.query.return_value.filter.return_value.all.return_value = [market]
        db.query.return_value.filter.return_value.order_by.return_value.all.return_value = snapshots

        assert detect_volume_spikes(db) == []


class TestPriceMomentum:
    def test_no_snapshots_returns_empty(self, db, market):
        db.query.return_value.filter.return_value.all.return_value = [market]
        db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

        assert detect_price_momentum(db) == []

    def test_detect_momentum_when_price_change_exceeds_threshold(self, db, market, now):
        latest = MockSnapshot(now, "m1", 100000, price=0.75)
        earlier = MockSnapshot(now - timedelta(hours=7), "m1", 100000, price=0.50)

        db.query.return_value.filter.return_value.all.return_value = [market]
        db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [latest, earlier]

        signals = detect_price_momentum(db)
        assert len(signals) == 1
        assert signals[0]["signal_type"] == "price_momentum"
        assert signals[0]["details"]["direction"] == "up"

    def test_no_momentum_when_price_stable(self, db, market, now):
        latest = MockSnapshot(now, "m1", 100000, price=0.50)
        earlier = MockSnapshot(now - timedelta(hours=7), "m1", 100000, price=0.48)

        db.query.return_value.filter.return_value.all.return_value = [market]
        db.query.return_value.filter.return_value.order_by.return_value.first.side_effect = [latest, earlier]

        assert detect_price_momentum(db) == []
