import ccxt
import time
import bisect


class GridTrader:
    def __init__(self, api_key, api_secret, symbol, price_min, price_max, num_grids,
                 position, max_position, initial_price, initial_price_idx, grid_prices):

        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        self.exchange.set_sandbox_mode(True)  # Enable testnet mode

        self.symbol = symbol  # Trading pair
        self.previous_price = initial_price  # Track the previous price
        self.price_min = price_min  # Lower price boundary
        self.price_max = price_max  # Upper price boundary
        self.num_grids = num_grids  # number of grids

        self.position = position  # Current position (in ETH)
        self.max_position = max_position  # Maximum allowed position size
        self.trade_type = None  # To record whether we are buying or selling
        self.trade_amount = 0  # Total traded amount

        # Unable passing below parameters for testing
        if grid_prices is not None:
            self.grid_prices = grid_prices
        else:
            print("> Preparing to generate grid prices...")
            self.grid_prices = self.generate_grid_prices()

        if initial_price_idx is not None:
            self.previous_price_idx = initial_price_idx
        else:
            self.previous_price_idx = bisect.bisect_left(self.grid_prices, self.previous_price)

    def generate_grid_prices(self):
        """Generate grid prices using a geometric sequence."""
        ratio = self.price_max / self.price_min
        grid_prices = [self.price_min * (ratio ** (i / (self.num_grids - 1))) for i in
                       range(self.num_grids)]

        # Round each price to 4 decimal places
        grid_prices = [round(price, 4) for price in grid_prices]

        return grid_prices

    def fetch_balance(self):
        """Fetch account balance - all assets"""
        print("> Fetching account balance (all assets)...")
        try:
            balance = self.exchange.fetch_balance()
            for asset, data in balance['total'].items():
                if data > 0:
                    print(f"Asset: {asset}, Free: {balance['free'][asset]}, Locked: {balance['used'][asset]}")
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {str(e)}")

    def fetch_specific_balance(self, asset_symbol):
        """Check the specific asset in the balance data"""
        print(f"> Check {asset_symbol} amount...")
        try:
            balance = self.exchange.fetch_balance()
            if asset_symbol in balance['total']:
                total_balance = balance['total'][asset_symbol]
                free_balance = balance['free'][asset_symbol]
                locked_balance = balance['used'][asset_symbol]

                # Return a dictionary of the balance attributes
                return {
                    'total_balance': total_balance,
                    'free_balance': free_balance,
                    'locked_balance': locked_balance
                }
            else:
                print(f"Asset {asset_symbol} not found in your account.")
                return None
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {str(e)}")

    def fetch_price(self):
        """Fetch the current price of the trading pair."""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            return ticker['last']
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {str(e)}")

    def calculate_trade_amount(self, current_price):
        """ Calculate trade amount based on grids"""
        index = 0
        if self.trade_type == 'buy':
            for i in range(self.previous_price_idx, -1, -1):
                if self.grid_prices[i] < current_price:
                    index = i + 1
                    break
        else:
            for i in range(self.previous_price_idx, len(self.grid_prices)):
                if self.grid_prices[i] > current_price:
                    index = i - 1
                    break

        self.trade_amount = abs(self.previous_price_idx - index) / 10
        return index

    def place_order(self, price, side):
        """Place an order on Binance."""
        # TODO: edge cases, e.g. amount <= 0; position + amount <= max_position; ...
        amount = self.trade_amount / 10  # TODO: ratio for testing, need to change back
        if amount > 0:
            print(f"Preparing to {side} {amount} ETH at {price} USDT.")
            try:
                order = self.exchange.create_order(symbol=self.symbol, type='limit',
                                                   side=side, amount=amount, price=price)
                return order['id']
            except Exception as e:
                print(f"Order failed: {e}")
                return None

    def check_order_status(self, order_id):
        # TODO: handle EXCEPTIONS
        """ Check the status of an order. """
        if order_id:
            time.sleep(5)
            order = self.exchange.fetch_order(order_id, self.symbol)
            return order['status']

    def cancel_order(self, order_id):
        # TODO: handle EXCEPTIONS and edge cases
        """Cancels a specific order if it is still open or partially filled."""
        print(f"Cancelling order {order_id}")
        self.exchange.cancel_order(order_id, self.symbol)

    def monitor_and_trade(self):
        """Monitor the price and execute trades based on price changes."""
        self.fetch_balance()
        self.fetch_specific_balance('ETH')
        self.fetch_specific_balance('USDT')
        print("Starting to monitor ETH price...")

        while True:
            try:
                current_price = self.fetch_price()
                print(f"\n> Current Price: {current_price}, previous price: {self.previous_price}")

                if current_price is None:
                    print("Failed to retrieve current price.")
                    return

                if current_price <= self.price_min or current_price >= self.price_max:  # Set boundary
                    print("Price reached the boundary, stopping...")
                    break

                # Trading logic/conditions:
                # Price drops below the previous grid price -> Buy
                if self.previous_price > current_price and self.position < self.max_position:
                    self.trade_type = 'buy'
                    index = self.calculate_trade_amount(current_price)
                # Price rises above the previous grid price -> Sell
                elif current_price > self.previous_price and self.position > 0:
                    self.trade_type = 'sell'
                    index = self.calculate_trade_amount(current_price)
                elif current_price == self.previous_price:
                    print(f"Current price: {current_price} is equal to previous price: {self.previous_price}")
                    time.sleep(60)  # Wait for 1 minute
                    continue
                else:
                    if current_price > self.previous_price <= 0:
                        print(f"Price rises, would execute \"BUY\", but position = {self.position}")
                    else:
                        print(f"Price drops, would execute \"SELL\", but position = {self.position}")
                    time.sleep(60)  # Wait for 1 minute
                    continue

                # TODO: validate conditions(if any) before place order
                self.place_order(current_price, self.trade_type)

                # TODO: check order status(completed?) after placing order -> replacing order if needed
                """
                    if not order['status'] == 'closed':
                    print(f"Order {order_id} not completed, retrying...")
                    # TODO: call cancel_order() and then place_order() again? retry 3 times or until price change?
                """

                if self.trade_type == 'buy':  # Update position manually
                    self.position += self.trade_amount
                else:
                    self.position -= self.trade_amount

                eth_balance = self.fetch_specific_balance('ETH')  # Get position using ccxt
                if eth_balance:
                    print("ETH Balances:", eth_balance)
                else:
                    print("Asset not found")
                # TODO: double check both two positions are the same if needed

                self.previous_price = current_price  # Update prev_price and index
                self.previous_price_idx = index

                time.sleep(60)  # Wait for 1 minute

            except Exception as e:
                print(f"Exception in monitor_and_trade: {e}")
