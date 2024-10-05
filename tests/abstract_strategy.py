from abc import ABC, abstractmethod
from src.exchange_manager import ExchangeManager

""" Base class for all strategies that defines common behavior(trades and others)"""


class AbstractStrategy(ABC):
    def __init__(self, exchange_name: str, config, symbol: str):
        self.exchange_manager = ExchangeManager(exchange_name, config, symbol)

    @abstractmethod
    def execute(self, time_interval):
        """Execute the trading strategy."""
        pass

    def fetch_balance(self, market_type: str):
        """Fetch the balance from the specified market."""
        return self.exchange_manager.fetch_balance(market_type)

    def fetch_specific_balance(self, market_type: str, asset_symbol: str):
        """Fetch the specific balance of an asset from the specified market."""
        return self.exchange_manager.fetch_specific_balance(market_type, asset_symbol)

    def fetch_ticker(self, market_type: str, asset_symbol: str):
        """Fetch the specific balance of an asset from the specified market."""
        try:
            return self.exchange_manager.fetch_specific_balance(market_type, asset_symbol)
        except Exception as e:
            print(f"Failed to fetch specific balance for {asset_symbol} in {market_type} market")
            return None

    def place_order(self, symbol: str, side: str, amount: float, price: float, order_type: str, market_type: str):
        """Place an order on the specified market."""
        base_currency = symbol.split('/')[0]

        if side.lower() == 'buy' and not self.check_balance(market_type, 'USDT', amount, price):
            print("Cannot place buy order. Insufficient USDT balance.")
            return None

        if side.lower() == 'sell' and not self.check_balance(market_type, base_currency, amount):
            print(f"Cannot place sell order. Insufficient {base_currency} balance.")
            return None


    def cancel_order(self, order_id: str, symbol: str, market_type: str):
        """Cancel an order on the specified market."""
        return self.exchange_manager.cancel_order(order_id, symbol, market_type)

    def fetch_order(self, order_id: str, symbol: str, market_type: str):
        """Fetch an order from the specified market."""
        return self.exchange_manager.fetch_order(order_id, symbol, market_type)

    def fetch_open_orders(self, symbol: str, market_type: str):
        """Fetch open orders from the specified market."""
        return self.exchange_manager.fetch_open_orders(symbol, market_type)

    def fetch_closed_orders(self, symbol: str, market_type: str):
        """Fetch closed orders from the specified market."""
        return self.exchange_manager.fetch_closed_orders(symbol, market_type)

    def check_balance(self, market_type: str, asset_symbol: str, required_amount: float, current_price: float = None):
        """Check if the balance is sufficient for a given trade."""
        balance = self.fetch_specific_balance(market_type, asset_symbol)
        if balance is None:
            print(f"Failed to fetch {asset_symbol} balance.")
            return False

        required_amount = required_amount * current_price if asset_symbol.upper() == 'USDT' and current_price else required_amount

        if balance < required_amount:
            print(f"Insufficient {asset_symbol} balance. Required: {required_amount}, Available: {balance}")
            return False

        return True


