import pytest
from unittest.mock import MagicMock, patch
from services.calibration import _derive_resolution, sync_resolved_market, _compute_calibration_bins, _compute_category_breakdown, compute_calibration

class TestDeriveResolution:
    def test_yes_wins(self):
        market_data = {
            "outcomePrices": '["0.9999995", "0.0000005"]',
            "outcomes": '["Yes", "No"]',
        }
        assert _derive_resolution(market_data) == "Yes"
        
    def test_no_wins(self):
        market_data = {
            "outcomePrices": '["0.0000005", "0.9999995"]',
            "outcomes": ['Yes', 'No'],
        }
        assert _derive_resolution(market_data) == "No"
    
    def test_ambiguous_returns_none(self):
        market_data = {
            "outcomePrices": ["0.5", "0.5"],
            "outcomes": '["Yes", "No"]',
        }
        assert _derive_resolution(market_data) is None
    
    def test_zeroed_prices_return_none(self):
        market_data = {
            "outcomePrices": '["0", "0"]',
            "outcomes": '["Yes", "No"]',
        }
        assert _derive_resolution(market_data) is None
    
    def test_handles_list_format(self):
        market_data = {
            "outcomePrices": [0.999999, 0.000001],
            "outcomes": ["Yes", "No"],
        }
        assert _derive_resolution(market_data) == "Yes"
        
    def test_single_outcome_returns_none(self):
        market_data = {
            "outcomePrices": '["0.95"]',
            "outcomes": '["Yes"]',
        }
        assert _derive_resolution(market_data) is None
    
    def test_barely_above_threshold(self):
        market_data = {
            "outcomePrices": '["0.91", "0.09"]',
            "outcomes": '["Yes", "No"]',
        }
        assert _derive_resolution(market_data) == "Yes"
        
    def test_barely_below_threshold(self):
        market_data = {
            "outcomePrices": '["0.89", "0.11"]',
            "outcomes": '["Yes", "No"]',
        }
        assert _derive_resolution(market_data) is None
        
    def test_invalid_json_returns_none(self):
        market_data = {
            "outcomePrices": "not json",
            "outcomes": '["Yes"]',
        }
        assert _derive_resolution(market_data) is None

class MockMarket:
    def __init__(self, id, resolution_result=None, status="open"):
        self.id = id
        self.resolution_result = resolution_result
        self.status = status
        self.outcome_prices = None

class TestSyncResolvedMarket:
    @patch("services.calibration.SessionLocal")
    @patch("services.calibration.PolyMarketClient")
    def test_updated_resolved_market(self, MockClient, MockSession):
        db = MockSession.return_value
        client = MockClient.return_value
        
        client.get_events.return_value = [{
            "markets": [{
                "id": "m1",
                "closed": True,
                "outcomePrices": '["0.999", "0.001"]',
                "outcomes": '["Yes", "No"]',
            }]
        }]
        
        existing = MockMarket("m1")
        db.query.return_value.filter.return_value.first.return_value = existing
        
        sync_resolved_market()
        
        assert existing.resolution_result == "Yes"
        assert existing.status == "closed"
        db.commit.assert_called_once()
    
    @patch("services.calibration.SessionLocal")
    @patch("services.calibration.PolyMarketClient")
    def test_skips_unknown_market(self, MockClient, MockSession):
        db = MockSession.return_value
        client = MockClient.return_value
        
        client.get_events.return_value = [{
            "markets": [{
                "id": "unknown",
                "closed": True,
                "outcomePrices": '["0.999", "0.001"]',
                "outcomes": '["Yes", "No"]',
            }]
        }]
        
        db.query.return_value.filter.return_value.first.return_value = None
        sync_resolved_market()
        db.commit.assert_called_once()
        
    @patch("services.calibration.SessionLocal")
    @patch("services.calibration.PolyMarketClient")
    def test_skips_unsettled_market(self, MockClient, MockSession):
        db = MockSession.return_value
        client = MockClient.return_value
        
        client.get_events.return_value = [{
            "markets": [{
                "id": "m1",
                "closed": True,
                "outcomePrices": '["0.5", "0.5"]',
                "outcomes": '["Yes", "No"]',
            }]
        }]
        
        existing = MockMarket("m1")
        db.query.return_value.filter.return_value.first.return_value = existing
        sync_resolved_market()
        
        assert existing.resolution_result is None

class TestCalibrationBins:
    def test_empty_forcasts(self):
        bins = _compute_calibration_bins([])
        assert len(bins) == 10
        assert all(b["count"] == 0 for b in bins)
        assert all(b["actual_frequency"] is None for b in bins)
        
    def test_perfect_calibrations(self):
        forecasts = [
            {"predicted": 0.95, "actual": 1.0, "category": "Sports"},
            {"predicted": 0.05, "actual": 0.0, "category": "Sports"},
        ]
        bins = _compute_calibration_bins(forecasts)
        assert bins[0]["count"] == 1
        assert bins[0]["actual_frequency"] == 0.0
        assert bins[9]["count"] == 1
        assert bins[9]["actual_frequency"] == 1.0
        
    def test_all_in_one_bin(self):
        forecasts = [
            {"predicted": 0.51, "actual": 1.0, "category": None},
            {"predicted": 0.55, "actual": 0.0, "category": None},
            {"predicted": 0.59, "actual": 1.0, "category": None},
        ]
        bins = _compute_calibration_bins(forecasts)
        assert bins[5]["count"] == 3
        assert round(bins[5]["actual_frequency"], 4) == round(2 / 3, 4)
    
    def test_price_one_goes_in_all_bin(self):
        forecasts = [{"predicted": 1.0, "actual": 1.0, "category": None}]
        bins = _compute_calibration_bins(forecasts)
        assert bins[9]["count"] == 1
        
    def test_bin_boundaries(self):
        forecasts = [
            {"predicted": 0.0, "actual": 0.0, "category": None},
            {"predicted": 0.1, "actual": 0.0, "category": None},
        ]
        bins = _compute_calibration_bins(forecasts)
        assert bins[0]["count"] == 1
        
class TestCategoryBreakdown:
    def test_single_category(self):
        forecasts = [
            {"predicted": 0.9, "actual": 1.0, "category": "Sports"},
            {"predicted": 0.8, "actual": 1.0, "category": "Sports"},
        ]
        breakdown = _compute_category_breakdown(forecasts)
        assert len(breakdown) == 1
        assert breakdown[0]["category"] == "Sports"
        assert breakdown[0]["count"] == 2
    
    def test_multiple_categories_sorted_by_brier(self):
        forecasts = [
            {"predicted": 0.9, "actual": 1.0, "category": "Good"},
            {"predicted": 0.5, "actual": 1.0, "category": "Bad"},
        ]
        breakdown = _compute_category_breakdown(forecasts)
        assert breakdown[0]["category"] == "Good"
        assert breakdown[1]["category"] == "Bad"
        assert breakdown[0]["brier_score"] < breakdown[1]["brier_score"]
        
    def test_none_category_becomes_uncategorized(self):
        forecasts = [{"predicted": 0.5, "actual": 1.0, "category": None}]
        breakdown = _compute_category_breakdown(forecasts)
        assert breakdown[0]["category"] == "Uncategorized"