import pytest
from unittest.mock import MagicMock, patch
from services.calibration import _derive_resolution, sync_resolved_market

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
            "outcomePrices": ["0", "0"],
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