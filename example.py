#!/usr/bin/env python3
"""
Example script demonstrating how to use the coinmarketcap_exchangerate module
"""
import os
from dotenv import load_dotenv
from coinmarketcap_exchangerate import PriceFetcher


def main():
    # set the coinmarketcap and exchangerate api key and Initialize the fetcher
    # Using .env file
    # Load environment variables if you are using .env file for API keys
    load_dotenv()
    cmc_api_key = os.getenv('CMC_API_KEY') # change the variable name that you have in your .env file
    er_api_key = os.getenv('ER_API_KEY') # change the variable name that you have in your .env file

    # Plaintext API key -- not recommended
    # cmc_api_key = 'Your Coinmarketcap API key'
    # er_api_key = 'Your Exchangerate API Key'

    fetcher = PriceFetcher(cmc_api_key, er_api_key)
    # fetcher = PriceFetcher()
    
    # Example tickers - mix of cryptocurrencies and forex
    tickers = ['BTC', 'ETH', 'EUR', 'JPY', 'DOT', 'BNB', 'CNY']
    
    print("Fetching prices for:", tickers)
    print("-" * 40)
    
    # Fetch prices
    prices = fetcher.fetch_prices(tickers)
    
    # Display results
    if prices:
        for ticker, name, price in prices:
            print(f"{ticker:>5}:\t{name}:\t{price:>10.6f}")
    else:
        print("No prices fetched. Check your API keys and internet connection.")

if __name__ == "__main__":
    main()
