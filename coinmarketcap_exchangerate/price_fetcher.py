import os
import json
import requests
from typing import List, Tuple, Dict, Any, Union


class PriceFetcher:
    """
    Fetch cryptocurrency prices from CoinMarketCap API 
    and forex prices from ExchangeRate API
    """
    
    def __init__(self, cmc_api_key=None, er_api_key=None):
        # Get API keys from environment variables or use defaults
        self.cmc_api_key = cmc_api_key
        self.er_api_key = er_api_key
        
        # Set default URLs
        self._set_default_urls()
        
        # Load forex symbols
        self.forex_symbols = self._load_forex_symbols()


    def _set_default_urls(self):
        """
        Set default URLs based on API keys
        @TODO change the hardcoded url to more robust once later to support CMC v2 and v3 APIs
        @TODO keep eye on Exchangerate API to see if v4 are still supported and update it accordingly
        """
        # CMC API URLs
        if not self.cmc_api_key:
            # CMC Sandbox API
            self.cmc_api_key = "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c"
            self.cmc_url = "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        else:
            # CMC Main API
            self.cmc_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        
        # ER API URLs
        if not self.er_api_key:
            # Default API, no need for user account for v4 yet
            self.er_url = "https://api.exchangerate-api.com/v4/latest/USD"
        else:
            self.er_url = f"https://v6.exchangerate-api.com/v6/{self.er_api_key}/latest/USD"


    def _load_forex_symbols(self) -> Dict[str, str]:
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', 'db', 'exchange_rate_currencies.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return "File not found!"


    def fetch_prices(self, tickers: List[str]) -> List[Tuple[str, float]]:
        """
        Fetch prices for given tickers
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            List of tuples containing (ticker, price)
            
        Raises:
            ValueError: If tickers is not a list
        """
        if not isinstance(tickers, list):
            raise ValueError("Tickers must be provided as a list")
        
        if not tickers:
            return []
        
        # Filter tickers into forex and crypto
        forex_tickers, crypto_tickers = self._filter_tickers(tickers)
        
        # Fetch prices
        prices = []
        
        # Fetch forex prices
        if forex_tickers:
            forex_prices = self._fetch_forex_prices(forex_tickers)
            prices.extend(forex_prices)
        
        # Fetch crypto prices
        if crypto_tickers:
            crypto_prices = self._fetch_crypto_prices(crypto_tickers)
            prices.extend(crypto_prices)
        
        return prices


    def _filter_tickers(self, tickers: List[str]) -> Tuple[List[str], List[str]]:
        """
        Filter tickers into forex and crypto lists
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            Tuple of (forex_tickers, crypto_tickers)
        """
        forex_tickers = []
        crypto_tickers = []
        
        for ticker in tickers:
            if ticker.upper() in self.forex_symbols:
                forex_tickers.append(ticker.upper())
            else:
                crypto_tickers.append(ticker.upper())
        
        return forex_tickers, crypto_tickers

    
    def _fetch_forex_prices(self, tickers: List[str]) -> List[Tuple[str, float]]:
        """
        Fetch forex prices from ExchangeRate API
        
        Args:
            tickers: List of forex ticker symbols
            
        Returns:
            List of tuples containing (ticker, price)
        """
        prices = []
        
        try:           
            response = requests.get(self.er_url)
            response.raise_for_status()
            
            data = response.json()
            if not self.er_api_key:
                rates = data.get('rates', {})
            else:
                rates = data.get('conversion_rates', {})
            
            # Get USD as base rate (1.0)
            if 'USD' in tickers:
                prices.append(('USD', 1.0))
            
            # Get other requested rates
            for ticker in tickers:
                if ticker != 'USD' and ticker in rates:
                    prices.append((ticker, rates[ticker]))
                    
        except Exception as e:
            print(f"Error fetching forex prices: {e}")
        
        return prices


    def _fetch_crypto_prices(self, tickers: List[str]) -> List[Tuple[str, float]]:
        """
        Fetch cryptocurrency prices from CoinMarketCap API
        
        Args:
            tickers: List of cryptocurrency ticker symbols
            
        Returns:
            List of tuples containing (ticker, price)
        """
        prices = []
        
        if not tickers:
            return prices
        
        try:
            # Prepare symbols for CMC API
            symbol_list = ','.join(tickers)
            
            # Endpoint for latest quotes
            url = f"{self.cmc_url}"
            
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': self.cmc_api_key,
            }
            
            parameters = {
                'symbol': symbol_list,
            }
            
            response = requests.get(url, headers=headers, params=parameters)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract prices
            if 'data' in data:
                for ticker in tickers:
                    if ticker in data['data']:
                        price = data['data'][ticker]['quote']['USD']['price']
                        prices.append((ticker, price))
                        
        except Exception as e:
            print(f"Error fetching crypto prices: {e}")
        
        return prices
