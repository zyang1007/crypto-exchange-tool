import time

import ccxt
from src import config


class BinanceTestnet:
    def __init__(self):
        self.api_key = config.API_KEY
        self.secret = config.API_SECRET
        # self.testnet_url = 'https://testnet.binance.vision/api'
        self.exchange = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.secret,
            'enableRateLimit': True,
        })
        self.exchange.set_sandbox_mode(True)  # Enable testnet mode

    def test_fetch_balance(self):
        print("> Fetching account balance...")
        balance = self.exchange.fetch_balance()
        for asset, data in balance['total'].items():
            if data > 0:
                print(f"Asset: {asset}, Free: {balance['free'][asset]}, Locked: {balance['used'][asset]}")

    def test_fetch_ticker(self, symbol):
        print(f"> Fetching ticker price for {symbol}...")
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            print(f"{symbol} Price: {ticker['last']}")
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {str(e)}")

    def test_trading_history(self, symbol):
        """Fetch and display trading history."""
        print("> Fetching trading history...")
        try:
            orders = self.exchange.fetch_orders(symbol)
            for order in orders:
                print(f"Order ID: {order['id']}, Symbol: {order['symbol']}, "
                      f"Status: {order['status']}, Price: {order['price']}")
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {str(e)}")

    def test_place_order(self):
        # Place a test buy order (adjust symbol, price, and amount accordingly)
        print("> Placing a test limit buy order for 0.1 ETH...")
        order = self.exchange.create_order(
            symbol='ETH/USDT',
            type='limit',
            side='buy',
            amount=0.1,  # buy 0.1 ETH
            price=1800  # at $1800 price
        )
        print("Order placed:", order)
        return order['id']

    def test_check_order_status(self, order_id):
        print(f"> Checking order {order_id} status...")
        order_status = self.exchange.fetch_order(order_id, 'ETH/USDT')
        print("Order status:", order_status['status'])

    def test_cancel_order(self, order_id):
        print(f"> Cancel order {order_id}...")
        self.exchange.cancel_order(order_id, 'ETH/USDT')
        order_status = self.exchange.fetch_order(order_id, 'ETH/USDT')
        print("Order status:", order_status['status'])


if __name__ == "__main__":
    pair = 'ETH/USDT'

    binance_test = BinanceTestnet()
    time.sleep(5)

    # Step 1: Fetch account balance
    binance_test.test_fetch_balance()
    time.sleep(5)

    # Step 2: Fetch ticker price
    binance_test.test_fetch_ticker(pair)
    time.sleep(5)

    # Step 3: Fetch trading history
    binance_test.test_trading_history(pair)
    time.sleep(5)

    # Step 4: Place an order
    order_ID = binance_test.test_place_order()
    time.sleep(5)

    # Step 5: Check order status
    binance_test.test_check_order_status(order_ID)
    time.sleep(5)

    # Step 6: Cancel order
    binance_test.test_cancel_order(order_ID)
    time.sleep(5)

    # Step 7: Fetch trading history
    binance_test.test_trading_history(pair)
    time.sleep(5)

    print("---All tests completed ---")
