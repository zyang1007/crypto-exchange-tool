import ccxt

try:
    # Initialize the Binance exchange
    exchange = ccxt.binance()

    # Fetch the ticker for BTC/USDT
    ticker = exchange.fetch_ticker('BTC/USDT')

    # Print the ticker information
    print(ticker)
except Exception as e:
    print(f"An error occurred: {e}")
