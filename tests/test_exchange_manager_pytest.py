import pytest
from unittest.mock import MagicMock
import ccxt

from src.exchange_manager import ExchangeManager


# Create mock exchanges
@pytest.fixture
def mock_exchanges():
    spot_exchange = MagicMock(spec=ccxt.binance)
    futures_exchange = MagicMock(spec=ccxt.binance)
    return spot_exchange, futures_exchange


@pytest.fixture
def exchange_manager(mock_exchanges):
    spot_exchange, futures_exchange = mock_exchanges
    # Mock the methods that should be used in tests
    exchange_manager = ExchangeManager()
    exchange_manager.spot_exchange = spot_exchange
    exchange_manager.futures_exchange = futures_exchange
    return exchange_manager


def test_place_order_spot(exchange_manager, mock_exchanges):
    spot_exchange, _ = mock_exchanges
    spot_exchange.create_limit_order.return_value = {'status': 'success'}

    result = exchange_manager.place_order('BTC/USDT', 'buy', 0.001, 30000, 'limit', 'spot')
    assert result == {'status': 'success'}
    spot_exchange.create_limit_order.assert_called_once_with('BTC/USDT', 'buy', 0.001, 30000)


def test_place_order_futures(exchange_manager, mock_exchanges):
    _, futures_exchange = mock_exchanges
    futures_exchange.create_market_order.return_value = {'status': 'success'}

    result = exchange_manager.place_order('BTC/USDT', 'sell', 0.001, None, 'market', 'futures')
    assert result == {'status': 'success'}
    futures_exchange.create_market_order.assert_called_once_with('BTC/USDT', 'sell', 0.001)


def test_cancel_order_spot(exchange_manager, mock_exchanges):
    spot_exchange, _ = mock_exchanges
    spot_exchange.cancel_order.return_value = {'status': 'cancelled'}

    result = exchange_manager.cancel_order('12345', 'BTC/USDT', 'spot')
    assert result == {'status': 'cancelled'}
    spot_exchange.cancel_order.assert_called_once_with('12345', 'BTC/USDT')


def test_cancel_order_futures(exchange_manager, mock_exchanges):
    _, futures_exchange = mock_exchanges
    futures_exchange.cancel_order.return_value = {'status': 'cancelled'}

    result = exchange_manager.cancel_order('54321', 'BTC/USDT', 'futures')
    assert result == {'status': 'cancelled'}
    futures_exchange.cancel_order.assert_called_once_with('54321', 'BTC/USDT')


def test_fetch_balance_spot(exchange_manager, mock_exchanges):
    spot_exchange, _ = mock_exchanges
    spot_exchange.fetch_balance.return_value = {'total': {'USDT': 1000}}

    result = exchange_manager.fetch_balance('spot')
    assert result == {'total': {'USDT': 1000}}
    spot_exchange.fetch_balance.assert_called_once()


def test_fetch_balance_futures(exchange_manager, mock_exchanges):
    _, futures_exchange = mock_exchanges
    futures_exchange.fetch_balance.return_value = {'total': {'USDT': 500}}

    result = exchange_manager.fetch_balance('futures')
    assert result == {'total': {'USDT': 500}}
    futures_exchange.fetch_balance.assert_called_once()


def test_fetch_order_spot(exchange_manager, mock_exchanges):
    spot_exchange, _ = mock_exchanges
    spot_exchange.fetch_order.return_value = {'id': '12345', 'status': 'open'}

    result = exchange_manager.fetch_order('12345', 'BTC/USDT', 'spot')
    assert result == {'id': '12345', 'status': 'open'}
    spot_exchange.fetch_order.assert_called_once_with('12345', 'BTC/USDT')


def test_fetch_order_futures(exchange_manager, mock_exchanges):
    _, futures_exchange = mock_exchanges
    futures_exchange.fetch_order.return_value = {'id': '54321', 'status': 'open'}

    result = exchange_manager.fetch_order('54321', 'BTC/USDT', 'futures')
    assert result == {'id': '54321', 'status': 'open'}
    futures_exchange.fetch_order.assert_called_once_with('54321', 'BTC/USDT')


if __name__ == "__main__":
    pytest.main()
