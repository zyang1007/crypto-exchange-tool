import unittest
from unittest.mock import MagicMock, patch
from src.strategy.grid_strategy import GridStrategy


class TestGridStrategy(unittest.TestCase):

    def setUp(self):
        """Set up the test environment for both spot and futures markets."""
        grid_levels = [1800 + (i * (3600 - 1800) / 99) for i in range(100)]  # Example grid levels

        # Mock ExchangeManager to avoid actual ccxt usage
        with patch('src.strategy.abstract_strategy.ExchangeManager') as MockExchangeManager:
            # Mock the create_exchange_instance method to return a mock exchange instance
            mock_exchange_spot = MagicMock()
            mock_exchange_future = MagicMock()

            MockExchangeManager.return_value.create_exchange_instance.side_effect = [
                mock_exchange_spot,  # For spot market
                mock_exchange_future  # For futures market
            ]

            # Mock the necessary methods and attributes for both exchanges
            mock_exchange_spot.fetch_ticker = MagicMock()
            mock_exchange_spot.create_order = MagicMock()
            mock_exchange_future.fetch_ticker = MagicMock()
            mock_exchange_future.create_order = MagicMock()

            # Initialize GridStrategy for both spot and futures markets
            grid_strategy_instance = GridStrategy(
                exchange_name=None,  # Use a valid exchange name for the test
                exchange_config=None,
                symbol='ETH/USDT',
                starting_price=2700,
                grid_levels=grid_levels,
            )
            self.grid_strategy_spot = grid_strategy_instance.exchange_manager.spot_exchange

            self.grid_strategy_future = grid_strategy_instance.exchange_manager.futures_exchange

            # Mock the ticker fetching and order placing for both strategies
            self.grid_strategy_spot.fetch_ticker = MagicMock()
            self.grid_strategy_spot.place_order = MagicMock()
            self.grid_strategy_future.fetch_ticker = MagicMock()
            self.grid_strategy_future.place_order = MagicMock()

    def test_monitor_and_trade(self):
        """Test the monitor_and_trade method for both spot and futures markets."""
        # Simulate different price scenarios for both markets
        price_changes_spot = [2690, 2710, 2705, 2720, 2700]  # Spot prices
        price_changes_future = [2695, 2705, 2710, 2730, 2720]  # Futures prices

        self.grid_strategy_spot.fetch_ticker.side_effect = price_changes_spot
        self.grid_strategy_future.fetch_ticker.side_effect = price_changes_future

        # Run the monitor_and_trade method in test mode for both strategies
        for i in range(len(price_changes_spot)):
            self.grid_strategy_spot.monitor_and_trade()
            self.grid_strategy_future.monitor_and_trade()

        # Check if the right number of orders were placed for both markets
        self.assertEqual(self.grid_strategy_spot.place_order.call_count, len(price_changes_spot),
                         f"Expected {len(price_changes_spot)} spot orders, but got {self.grid_strategy_spot.place_order.call_count}")
        self.assertEqual(self.grid_strategy_future.place_order.call_count, len(price_changes_future),
                         f"Expected {len(price_changes_future)} futures orders, but got {self.grid_strategy_future.place_order.call_count}")

        # Verify that the correct type of orders were placed (buy/sell) for both markets
        for i in range(len(price_changes_spot)):
            current_price_spot = price_changes_spot[i]
            prev_price_spot = price_changes_spot[i - 1] if i > 0 else self.grid_strategy_spot.price_min - 1
            trade_type_spot = 'buy' if current_price_spot < prev_price_spot else 'sell'

            current_price_future = price_changes_future[i]
            prev_price_future = price_changes_future[i - 1] if i > 0 else self.grid_strategy_future.price_min - 1
            trade_type_future = 'buy' if current_price_future < prev_price_future else 'sell'

            # Assert spot market orders
            self.grid_strategy_spot.place_order.assert_any_call(
                self.grid_strategy_spot.symbol, trade_type_spot, unittest.mock.ANY, current_price_spot, 'limit', 'spot'
            )

            # Assert futures market orders
            self.grid_strategy_future.place_order.assert_any_call(
                self.grid_strategy_future.symbol, trade_type_future, unittest.mock.ANY, current_price_future, 'limit', 'future'
            )

    def test_monitor_and_trade_with_exception_handling(self):
        """Test monitor_and_trade to handle exceptions and edge cases in both spot and futures markets."""
        # Simulate different price scenarios including an exception for both markets
        price_changes_spot = [2690, 2710, 2705, Exception("API Error"), 2700]
        price_changes_future = [2695, 2705, Exception("API Error"), 2730, 2720]

        self.grid_strategy_spot.fetch_ticker.side_effect = price_changes_spot
        self.grid_strategy_future.fetch_ticker.side_effect = price_changes_future

        # Run the monitor_and_trade method with exception handling for both markets
        for i in range(4):  # Simulate up to the exception
            self.grid_strategy_spot.monitor_and_trade()
            self.grid_strategy_future.monitor_and_trade()

        # Check if the right number of orders were placed despite the exception
        self.assertEqual(self.grid_strategy_spot.place_order.call_count, 3, "Expected 3 spot orders")
        self.assertEqual(self.grid_strategy_future.place_order.call_count, 2, "Expected 2 futures orders")

        # Verify that the correct type of orders were placed for both markets
        for i in range(3):
            current_price_spot = price_changes_spot[i]
            prev_price_spot = price_changes_spot[i - 1] if i > 0 else self.grid_strategy_spot.price_min - 1
            trade_type_spot = 'buy' if current_price_spot < prev_price_spot else 'sell'

            if i < 2:  # Ensure not to check after exception
                current_price_future = price_changes_future[i]
                prev_price_future = price_changes_future[i - 1] if i > 0 else self.grid_strategy_future.price_min - 1
                trade_type_future = 'buy' if current_price_future < prev_price_future else 'sell'

                # Assert spot market orders
                self.grid_strategy_spot.place_order.assert_any_call(
                    self.grid_strategy_spot.symbol, trade_type_spot, unittest.mock.ANY, current_price_spot, 'limit', 'spot'
                )

                # Assert futures market orders
                self.grid_strategy_future.place_order.assert_any_call(
                    self.grid_strategy_future.symbol, trade_type_future, unittest.mock.ANY, current_price_future, 'limit', 'future'
                )


if __name__ == '__main__':
    unittest.main()
