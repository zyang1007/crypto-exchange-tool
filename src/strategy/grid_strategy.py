import bisect
import time

from src.strategy.abstract_strategy import AbstractStrategy


class GridStrategy(AbstractStrategy):
    def __init__(self, exchange_name: str, config, symbol: str, starting_price: float, grid_levels: list):
        super().__init__(exchange_name, config, symbol)
        self.symbol = 'ETH/USDT'  # specify trading pair
        self.grid_size = 100   # total number of grids
        self.price_min = 1800   # Lower price boundary
        self.price_max = 3600   # upper price boundary
        self.max_position = 10   # Maximum allowed position size

        self.trade_type = None  # To record whether we are buying or selling
        self.trade_amount = 0  # Total trading amount

        # Grid levels and starting price setup
        self.grid_levels = grid_levels if grid_levels else self.generate_grid_levels()
        self.previous_price_idx = bisect.bisect_left(self.grid_levels, starting_price or 2700)

        # TODO: need to clarify if current position starts with 0? Or fetch real ETH position?
        # Current position (initialize to zero or fetch actual position)
        initial_position = 0  # For now, initialized to 0
        initial_price = self.grid_levels[self.previous_price_idx]

        # Create market instances (spot and futures)
        spot_market = self.create_market_instance('spot', initial_price, self.previous_price_idx, initial_position)
        futures_market = self.create_market_instance('future', initial_price, self.previous_price_idx, initial_position)
        self.markets = [spot_market, futures_market]

    def generate_grid_levels(self):
        """Generate grid prices using a geometric sequence."""
        ratio = self.price_max / self.price_min
        grid_prices = [self.price_min * (ratio ** (i / (self.grid_size - 1))) for i in range(self.grid_size)]

        # Round each price to 4 decimal places
        grid_prices = [round(price, 4) for price in grid_prices]
        return grid_prices

    def calculate_trade_amount(self, current_price, previous_price_idx):
        """ Calculate trade amount based on grids"""
        index = 0
        if self.trade_type == 'buy':
            # Find the next grid level below the current price
            """index = next((i for i in range(previous_price_idx, -1, -1) if self.grid_levels[i] < current_price), 0)"""
            for i in range(previous_price_idx, -1, -1):
                if self.grid_levels[i] < current_price:
                    index = i + 1
                    break
        else:
            # Find the next grid level above the current price
            """index = next((i for i in range(previous_price_idx, len(self.grid_levels)) if
                          self.grid_levels[i] > current_price), len(self.grid_levels) - 1)"""
            for i in range(previous_price_idx, len(self.grid_levels)):
                if self.grid_levels[i] > current_price:
                    index = i - 1
                    break
        self.trade_amount = abs(previous_price_idx - index) / 100  # Note: smaller ratio for test
        return index

    def monitor_and_trade(self):
        # Monitor the price and execute trades based on price changes.
        print("> Starting to monitor and trade ETH...")
        try:
            for market in self.markets:
                current_price = self.fetch_ticker(market.type)
                print(f"\n>{market.type}: current price={current_price}, prev_price={market.previous_price}")

                if current_price is None:
                    print("Failed to retrieve current price.")
                    return

                if current_price <= self.price_min or current_price >= self.price_max:  # check within boundaries
                    print("Price reached the boundary, stopping...")
                    return

                # Trading logic/conditions:
                # Determine whether to buy or sell based on price movement
                index = 0
                if market.previous_price > current_price and market.curr_position < self.max_position:
                    self.trade_type = 'buy'
                    index = self.calculate_trade_amount(current_price, market.previous_price_idx)
                elif current_price > market.previous_price: #and market.curr_position > 0:
                    self.trade_type = 'sell'
                    index = self.calculate_trade_amount(current_price, market.previous_price_idx)
                else:
                    print(f"No trade executed. Current price: {current_price}, "
                          f"Previous price: {market.previous_price}")
                    continue

                # TODO: validate conditions(if any) before place order
                self.place_order(self.symbol, self.trade_type, self.trade_amount,
                                 current_price, 'limit', market.type)

                # TODO: 下单未成交，需识别后再次确认成交条件再下单?

                # if not order['status'] == 'closed':
                # print(f"Order {order_id} not completed, retrying...")
                # TODO: call cancel_order() and then place_order() again? retry 3 times or until price change?

                if self.trade_type == 'buy':  # Update position manually
                    market.curr_position += self.trade_amount
                else:
                    market.curr_position -= self.trade_amount

                # Double check position using ccxt if need to
                # eth_balance = self.fetch_specific_balance('ETH')  # Get position using ccxt
                # if eth_balance:
                    # print("ETH Balances:", eth_balance)
                # else:
                    # print("Asset not found")
                # TODO: double check both two positions are the same if needed?

                market.previous_price = current_price  # Update prev_price and index
                market.previous_price_idx = index

            time.sleep(3)  # Wait for 1 minute

        except Exception as e:
            print(f"Exception in monitor_and_trade: {e}")

    def execute(self):
        # Grid logic:
        print(f"> Executing grid strategy for {self.symbol}")
        while True:
            self.monitor_and_trade()

    def create_market_instance(self, market_type, prev_price, previous_price_idx, position):
        return self.Market(market_type, prev_price, previous_price_idx, position)

    class Market:
        def __init__(self, market_type, previous_price, previous_price_idx, position):
            self.type = market_type
            self.previous_price = previous_price
            self.previous_price_idx = previous_price_idx
            self.curr_position = position
