import time
from src.strategy.grid_strategy import GridStrategy


class Launcher:

    def __init__(self):
        # Initialize the strategy, exchanges, or other configurations
        self.my_strategy = GridStrategy(exchange_name=None, config=None, symbol=None,
                                        starting_price=None, grid_levels=None)  # use default grid strategy

    @staticmethod
    def show_menu():
        print("\n--- Trading Tool Menu ---")
        print("1. Manually Trading")
        print("2. Auto Trading")
        print("3. Exit")
        print("-------------------------")

    def manual_trading(self):
        # Handle the logic for manually trading
        while True:
            print("-------------------------")
            print("1. Check Balance")
            print("2. Check specific Asset")
            print("3. Create an order")
            print("4. Check order status")
            print("5. Cancel an order")
            print("0. Back to main menu")
            choice = input("Enter your choice: ")
            print("-------------------------")

            if choice == '1':  # retrieve all balance
                market_type = input("Enter market type (spot/futures): ")
                balance = self.my_strategy.fetch_balance(market_type)
                print(balance)

            elif choice == '2':  # check specific asset balance on an exchange
                market_type = input("Enter market type (spot/futures): ")
                asset_symbol = input("Enter asset symbol(e.g. ETH/BTC): ")
                balance = self.my_strategy.fetch_specific_balance(market_type, asset_symbol)
                print(balance)

            elif choice == '3':
                self.ask_for_order_info()

            elif choice == '4':  # check order status
                market_type = input("Enter market type (spot/futures): ")
                order_id = input("Enter order_id: ")
                order = self.my_strategy.fetch_order(order_id, 'ETH/USDT', market_type)
                print(f"Order status: {order['status']}")

            elif choice == '5':  # cancel an order
                market_type = input("Enter market type (spot/futures): ")
                order_id = input("Enter order_id: ")
                symbol = input("Enter order symbol(e.g. ETH/USDT) ")
                order = self.my_strategy.exchange_manager.cancel_order(order_id, symbol, market_type)
                print(f"Canceled order {order_id}, status: {order['status']}")

            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

    def auto_trading(self, strategy_type: str):
        # Handle the logic for auto trading (e.g., start grid strategy)
        print(f"Auto Trading Mode: {strategy_type} strategy starts...")
        self.my_strategy.execute(time_interval=60)

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter your choice (1/2/3): ")
            if choice == '1':
                self.manual_trading()
            elif choice == '2':
                self.auto_trading('gird')
            elif choice == '3':
                print("Exiting Trading Tool.")
                break
            else:
                print("Invalid choice. Please try again.")

    def ask_for_order_info(self):
        print("Manual Trading Mode")
        market_type = input("Enter market type (spot/futures): ")
        # symbol = input("Enter trading symbol (e.g., ETH/USDT): ")
        trade_type = input("Enter trade type (buy/sell): ")
        order_type = input("Enter order type (market/limit/ect): ")
        amount = float(input("Enter amount: "))

        if order_type == 'limit':   # Limit orders require a price
            price = float(input("Enter price: "))
            man_order = self.place_order_dynamically(market_type, order_type, trade_type, 'ETH/USDT', amount, price)
            # print(f"Placed {trade_type} order for {amount} ETH at {price} in {market_type} market.")
            print(man_order)

        elif order_type == 'market':  # Market orders don't require a price
            man_order = self.place_order_dynamically(market_type, order_type, trade_type, 'ETH/USDT', amount, None)
            # print(f"Placed {trade_type} order for {amount} ETH in {market_type} market.")
            print(man_order)
        else:
            raise ValueError("Invalid order type")
        print("-------------------------")

    def place_order_dynamically(self, market_type, order_type, side, symbol, amount, price=None):
        # Select the exchange based on market type
        if market_type == 'spot':
            exchange = self.my_strategy.exchange_manager.spot_exchange
        else:
            exchange = self.my_strategy.exchange_manager.futures_exchange

        # Build the method name dynamically
        if order_type == 'market':
            method_name = f'create_market_{side}_order'  # e.g., 'create_market_sell_order'
        else:
            method_name = f'create_limit_{side}_order'  # e.g., 'create_limit_order'

        try:
            # Retrieve the method dynamically
            method = getattr(exchange, method_name)
            print(f"Calling method: {method_name} with parameters: {symbol}, {amount}, {price}")
            print(f"Method: {method} for {method_name}")

            if order_type == 'market':
                # Call the market order method
                print(f"Preparing to {order_type} {amount} {symbol} on the {market_type} market...")
                order = method(symbol, amount)  # Market order
            else:
                # Call the limit order method
                print(f"Preparing to {order_type} {amount} {symbol} at {price} on the {market_type} market...")
                order = method(symbol, amount, price)  # Limit order

            return order

        except Exception as e:
            print(f"Failed to place {order_type} order: {str(e)}")
            return None
