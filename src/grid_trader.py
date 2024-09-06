import ccxt
import time


class GridTrader:
    def __init__(self, api_key, api_secret, symbol, initial_price, price_min, price_max, grids, fixed_trade_volume,
                 max_amount):
        self.exchange = ccxt.binanceus()
        """
        self.exchange = ccxt.binanceus({
            'apiKey': api_key,
            'secret': api_secret,
        })
        """
        self.symbol = symbol
        self.previous_price = initial_price
        self.price_min = price_min
        self.price_max = price_max
        self.grids = grids
        self.fixed_trade_volume = fixed_trade_volume

        self.max_amount = max_amount
        self.grid_prices = self.generate_grid_prices()

    def generate_grid_prices(self):
        """Generate grid prices using a geometric sequence."""
        return [self.price_min * (self.price_max / self.price_min) ** (i / self.grids) for i in
                range(self.grids + 1)]

    def fetch_price(self):
        """Fetch the current market price of the trading pair."""
        ticker = self.exchange.fetch_ticker(self.symbol)
        return ticker['last']

    def place_order(self, order_type, amount):
        """Place a market order to buy or sell ETH."""
        try:
            if order_type == 'buy':
                """self.exchange.create_market_buy_order(self.symbol, amount)"""

            elif order_type == 'sell':
                """self.exchange.create_market_sell_order(self.symbol, amount)"""
            print(f"Order placed: {order_type} {amount} {self.symbol}")
        except Exception as e:
            print(f"Error placing order: {e}")

    def monitor_and_trade(self):
        """Monitor the price and execute trades based on price changes."""
        curr_amount = 0

        while True:
            try:
                current_price = self.fetch_price()
                print(f"Current Price: {current_price}")

                if current_price is None:
                    print("Failed to retrieve current price.")
                    return

                if current_price <= self.price_min or current_price >= self.price_max:
                    print("Price reached the boundary, stopping...")
                    break

                if current_price < self.previous_price and curr_amount < self.max_amount:
                    self.place_order('buy', self.fixed_trade_volume)
                    curr_amount += self.fixed_trade_volume
                elif current_price > self.previous_price and curr_amount > 0:
                    self.place_order('sell', self.fixed_trade_volume)
                    curr_amount -= self.fixed_trade_volume

                self.previous_price = current_price

                time.sleep(60)  # Wait for 1 minute

            except Exception as e:
                print(f"Exception in monitor_and_trade: {e}")