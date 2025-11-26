from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="coinmarketcap-exchangerate",
    version="1.0",
    author="Droonacharya Ko Chelo",
    author_email="droonacharyakohelo@gmail.com",
    description="A Python module to fetch cryptocurrency prices from CoinMarketCap API and forex prices from ExchangeRate API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/droonacharyakochelo/coinmarketcap_exchangerate",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.25.1",
    ],
    package_data={
        'coinmarketcap_exchangerate': ['../db/exchange_rate_currencies.json'],
    },
    include_package_data=True,
)
