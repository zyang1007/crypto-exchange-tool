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

    def fetch_ticker(self, market_type: str):
        """Fetch the current ticker price from the specified market."""
        return self.exchange_manager.fetch_ticker(market_type)

    def place_order(self, symbol: str, side: str, amount: float, price: float, order_type: str, market_type: str):
        """Place an order on the specified market."""
        return self.exchange_manager.place_order(symbol, side, amount, price, order_type, market_type)

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
