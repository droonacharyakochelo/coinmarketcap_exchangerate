# Coinmarketcap Exchangerate API

A Python module to fetch cryptocurrency prices from CoinMarketCap API and forex prices from ExchangeRate API.

## Features

- Fetch cryptocurrency prices from CoinMarketCap API
- Fetch forex prices from ExchangeRate API
- Automatic detection of cryptocurrency vs forex tickers
- Support for API keys via environment variables or direct assignment
- Easy to use and integrate into your projects

## Installation

```bash
pip install coinmarketcap-exchangerate
```

## Usage

### Basic Usage

```python
from coinmarketcap_exchangerate import PriceFetcher

# Initialize the fetcher
fetcher = PriceFetcher()

# Provide tickers as a list
tickers = ['BTC', 'ETH', 'EUR', 'JPY', 'DOT']

# Fetch prices
prices = fetcher.fetch_prices(tickers)

# Print results
for ticker, price in prices:
    print(f"{ticker}: {name}: {price}")
```

### Using API Keys

You can provide API keys in two ways:

#### Method 1: Environment Variables (.env file)

Create a `.env` file in your project root:

```env
CMC_API_KEY=your_coinmarketcap_api_key
ER_API_KEY=your_exchangerate_api_key
```

Then use as:

```python
import os
from dotenv import load_dotenv
from coinmarketcap_exchangerate import PriceFetcher

# Load environment variables
load_dotenv()
cmc_api_key = os.getenv('CMC_API_KEY')
er_api_key = os.getenv('ER_API_KEY')

fetcher = PriceFetcher(cmc_api_key, er_api_key)
prices = fetcher.fetch_prices(['BTC', 'EUR'])
```

#### Method 2: Direct Assignment - not recommended

```python
from coinmarketcap_exchangerate import PriceFetcher

# Provide API key as variable
cmc_api_key = 'your api key'
er_api_key = 'your api key'

fetcher = PriceFetcher(cmc_api_key, er_api_key)
prices = fetcher.fetch_prices(['BTC', 'EUR'])
```

### Without API Keys (Default)

If no API keys are provided, the module will use:

- CoinMarketCap sandbox API (with limited requests)
- Default ExchangeRate API endpoint

```python
from coinmarketcap_exchangerate import PriceFetcher

fetcher = PriceFetcher()
prices = fetcher.fetch_prices(['BTC', 'EUR'])
```

## Return Format

The `fetch_prices()` method returns a list of tuples in the format:

```python
[
    ('EUR', 'Euro', 0.980),
    ('JPY', 'Japanese Yen', 0.005),
    ('BTC', 'Bitcoin', 78000.0),
    ('ETH', 'Ethereum', 3500.0),
    ('DOT', 'Polkadot', 7.5)
]
```

Each tuple contains the ticker symbol, currency name and its price in USD.

## Requirements

- Python 3.10+
- requests

## API Documentation

- [CoinMarketCap API Documentation](https://coinmarketcap.com/api/documentation/v1/)
- [ExchangeRate API Documentation](https://www.exchangerate-api.com/docs)

## License

MIT License
