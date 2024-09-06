import ccxt

try:
    # Initialize the Binance.US exchange
    exchange = ccxt.binanceus()

    # Fetch the ticker for BTC/USDT
    ticker = exchange.fetch_ticker('ETH/USDC')

    # Print the ticker information
    print(ticker)
except Exception as e:
    print(f"An error occurred: {e}")
