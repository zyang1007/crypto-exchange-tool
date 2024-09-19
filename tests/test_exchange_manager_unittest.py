import unittest
from unittest.mock import MagicMock, patch
from src.exchange_manager import ExchangeManager


class TestExchangeManager(unittest.TestCase):

    def setUp(self):
        # Set up test configuration
        self.config = None
        self.manager = ExchangeManager(config=self.config)

    @patch('ccxt.binance')
    def test_create_spot_exchange_instance(self, mock_binance):
        mock_binance.return_value.apiKey = 'test_spot_key'
        self.manager = ExchangeManager(config=self.config)
        self.assertEqual(self.manager.futures_exchange.apiKey, 'test_spot_key')

    @patch('ccxt.binance')
    def test_create_futures_exchange_instance(self, mock_binance):
        mock_binance.return_value.apiKey = 'test_futures_key'
        mock_binance.return_value.secret = 'test_futures_secret'
        self.manager = ExchangeManager(config=self.config)
        self.assertEqual(self.manager.futures_exchange.secret, 'test_futures_secret')

    def test_get_exchange(self):
        spot_exchange = self.manager.get_exchange('spot')
        self.assertEqual(spot_exchange, self.manager.spot_exchange)

        futures_exchange = self.manager.get_exchange('futures')
        self.assertEqual(futures_exchange, self.manager.futures_exchange)

        with self.assertRaises(ValueError):
            self.manager.get_exchange('unknown')

    def test_fetch_balance(self):
        self.manager.spot_exchange.fetch_balance = MagicMock(return_value={'total': {'ETH': 10}})
        balance = self.manager.fetch_balance('spot')
        self.assertEqual(balance['total']['ETH'], 10)

    def test_fetch_ticker(self):
        self.manager.spot_exchange.fetch_ticker = MagicMock(return_value={'last': 2000})
        ticker = self.manager.fetch_ticker('spot')
        self.assertEqual(ticker, 2000)

    def test_place_order(self):
        self.manager.spot_exchange.create_limit_order = MagicMock(return_value={'order_id': '1234'})
        order = self.manager.place_order('ETH/USDT', 'buy', 1, 2000, 'limit', 'spot')
        self.assertEqual(order['order_id'], '1234')

    def test_cancel_order(self):
        self.manager.spot_exchange.cancel_order = MagicMock(return_value={'status': 'canceled'})
        response = self.manager.cancel_order('1234', 'ETH/USDT', 'spot')
        self.assertEqual(response['status'], 'canceled')

    def test_fetch_order(self):
        self.manager.spot_exchange.fetch_order = MagicMock(return_value={'id': '1234'})
        order = self.manager.fetch_order('1234', 'ETH/USDT', 'spot')
        self.assertEqual(order['id'], '1234')

    def test_fetch_open_orders(self):
        self.manager.spot_exchange.fetch_open_orders = MagicMock(return_value=[{'id': '1234'}])
        orders = self.manager.fetch_open_orders('ETH/USDT', 'spot')
        self.assertEqual(orders[0]['id'], '1234')

    def test_fetch_closed_orders(self):
        self.manager.spot_exchange.fetch_closed_orders = MagicMock(return_value=[{'id': '1234'}])
        orders = self.manager.fetch_closed_orders('ETH/USDT', 'spot')
        self.assertEqual(orders[0]['id'], '1234')


if __name__ == '__main__':
    unittest.main()
