import ccxt
from typing import Literal
from src import config_testnet


class ExchangeManager:
    def __init__(self, exchange_name: str = None, config: dict = None, symbol: str = None):
        self.futures_exchange = None
        self.spot_exchange = None
        self.symbol = symbol if symbol else 'ETH/USDT'
        self.create_exchange_instance(exchange_name, config, 'spot')
        self.create_exchange_instance(exchange_name, config, 'futures')

    def create_exchange_instance(self, exchange_name, config, market_type: str):
        # Note: outer if-else statement doesn't cover every case, may need to be filled.
        if exchange_name is None or config is None:
            print(f"Create {market_type} testnet instances...")
            if market_type == 'spot':
                self.spot_exchange = ccxt.binance({  # default exchange is binance, config is testnet
                    'apiKey': config_testnet.SPOT_API_KEY,
                    'secret': config_testnet.SPOT_API_SECRET,
                    'enableRateLimit': True,
                })
                self.spot_exchange.set_sandbox_mode(True)  # Enable testnet mode
            elif market_type == 'futures':
                self.futures_exchange = ccxt.binance({
                    'apiKey': config_testnet.FUTURES_API_KEY,
                    'secret': config_testnet.FUTURES_API_SECRET,
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'future'  # Specify futures
                    }
                })
                self.futures_exchange.set_sandbox_mode(True)  # Enable testnet mode
        else:
            exchange_class = getattr(ccxt, exchange_name)
            if market_type == 'spot':
                self.spot_exchange = exchange_class({
                    'apiKey': config['spot_api_key'],
                    'secret': config['spot_api_secret'],
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'spot'
                    }
                })
            elif market_type == 'futures':
                self.futures_exchange = exchange_class({
                    'apiKey': config['futures_api_key'],
                    'secret': config['futures_api_secret'],
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'future'
                    }
                })

    def get_exchange(self, market_type: str):
        """ Helper function to get the correct exchange instance based on the market type. """
        if market_type == 'spot':
            return self.spot_exchange
        elif market_type == 'futures':
            return self.futures_exchange
        else:
            raise ValueError(f"Unknown market type: {market_type}")

    def fetch_balance(self, market_type: str):
        """Generalized method to fetch the account balance for Spot or Futures markets."""
        exchange = self.get_exchange(market_type)
        try:
            return exchange.fetch_balance()
        except Exception as e:
            raise Exception(f"Failed to fetch balance on {market_type} market: {e}")

    def fetch_specific_balance(self, market_type: str, asset_symbol: str):
        """Check the specific asset balance of the specified market."""
        exchange = self.get_exchange(market_type)
        try:
            balance = exchange.fetch_balance()
            if asset_symbol in balance['total']:
                return {
                    'total_balance': balance['total'][asset_symbol],
                    'free_balance': balance['free'][asset_symbol],
                    'locked_balance': balance['used'][asset_symbol]
                }
            else:
                print(f"Asset {asset_symbol} not found in your {market_type} account.")
                return None
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {str(e)}")

    def fetch_ticker(self, market_type: str):
        """Generalized method to fetch the current price of the trading pair."""
        exchange = self.get_exchange(market_type)
        try:
            ticker = exchange.fetch_ticker(self.symbol)
            return ticker['last']
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {str(e)}")

    def place_order(self, symbol: str, side: Literal['buy', 'sell'], amount: float, price: float, order_type: str,
                    market_type: str):
        """Generalized method to place an order on Spot or Futures markets."""
        exchange = self.get_exchange(market_type)
        try:
            if order_type == 'limit':
                return exchange.create_limit_order(symbol, side, amount, price)
            elif order_type == 'market':
                return exchange.create_market_order(symbol, side, amount)
            else:
                raise ValueError(f"Unknown order type: {order_type}")
        except Exception as e:
            raise Exception(f"Failed to place order on {market_type} market: {e}")

    def cancel_order(self, order_id: str, symbol: str, market_type: str):
        """Generalized method to cancel an order on Spot or Futures markets."""
        exchange = self.get_exchange(market_type)
        try:
            return exchange.cancel_order(order_id, symbol)
        except Exception as e:
            raise Exception(f"Failed to cancel order {order_id} on {market_type} market: {e}")

    def fetch_order(self, order_id: str, symbol: str, market_type: str):
        """Generalized method to fetch an order from Spot or Futures markets."""
        exchange = self.get_exchange(market_type)
        try:
            return exchange.fetch_order(order_id, symbol)
        except Exception as e:
            raise Exception(f"Failed to fetch order {order_id} for {symbol} on {market_type} market: {e}")

    def fetch_open_orders(self, symbol: str, market_type: str):
        """Generalized method to fetch open orders from Spot or Futures markets."""
        exchange = self.get_exchange(market_type)
        try:
            return exchange.fetch_open_orders(symbol)
        except Exception as e:
            raise Exception(f"Failed to fetch open orders for {symbol} on {market_type} market: {e}")

    def fetch_closed_orders(self, symbol: str = 'ETH/USDT', market_type: str = None):
        """Generalized method to fetch closed orders from Spot or Futures markets."""
        exchange = self.get_exchange(market_type)
        try:
            return exchange.fetch_closed_orders(symbol)
        except Exception as e:
            raise Exception(f"Failed to fetch closed orders for {symbol} on {market_type} market: {e}")

    def fetch_recent_ohlcv(self, market_type: str, timeframe='1h', since=None, limit=100):
        """Fetch recent OHLCV data for spot or futures markets."""
        exchange = self.get_exchange(market_type)
        try:
            # Fetch OHLCV data
            ohlcv = exchange.fetch_ohlcv(self.symbol, timeframe, since, limit)
            return ohlcv
        except Exception as e:
            raise Exception(f"Failed to fetch OHLCV data for {self.symbol} on {market_type} market: {e}")
