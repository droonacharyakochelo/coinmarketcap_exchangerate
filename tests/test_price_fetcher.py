#!/usr/bin/env python3
import unittest
from coinmarketcap_exchangerate import PriceFetcher

class TestPriceFetcher(unittest.TestCase):
    
    def setUp(self):
        self.fetcher = PriceFetcher()
    
    def test_ticker_filtering(self):
        """Test that tickers are correctly filtered into forex and crypto"""
        # Mixed tickers
        tickers = ['BTC', 'EUR', 'ETH', 'JPY', 'DOT']
        forex_tickers, crypto_tickers = self.fetcher._filter_tickers(tickers)
        
        # Check that we have the right tickers in each list
        self.assertIn('EUR', forex_tickers)
        self.assertIn('JPY', forex_tickers)
        self.assertIn('BTC', crypto_tickers)
        self.assertIn('ETH', crypto_tickers)
        self.assertIn('DOT', crypto_tickers)
    
    def test_invalid_input(self):
        """Test that invalid input raises appropriate error"""
        with self.assertRaises(ValueError):
            # Testing with invalid input type
            self.fetcher.fetch_prices("not a list")  # type: ignore
    
    def test_empty_input(self):
        """Test that empty input returns empty list"""
        result = self.fetcher.fetch_prices([])
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()