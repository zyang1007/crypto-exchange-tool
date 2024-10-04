import unittest
from unittest.mock import MagicMock, patch
from src.strategy.grid_strategy import GridStrategy


class TestGridStrategy(unittest.TestCase):

    def setUp(self):
        """Set up the test environment for future market."""
        print("--- Initializing SetUp() ---")
        # Mock ExchangeManager to avoid actual ccxt usage
        with patch('src.service.exchange') as MockExchange:
            # Mock the create_exchange_instance method to return a mock exchange instance
            mock_exchange = MagicMock()

            MockExchange.return_value.create_exchange_instance.side_effect = [
                mock_exchange  # For futures market
            ]

            # Mock the necessary methods and attributes
            mock_exchange.fetch_ticker = MagicMock()
            mock_exchange.place_order = MagicMock()

            # Initialize GridStrategy for both spot and futures markets
            config = {
                "symbol": "ETH/USDT",
                "min_price": 1800,
                "max_price": 3600,
                "num_grids": 100,
                "max_position": 10,
                "security_deposit": 0,
                "fixed_trade_amount": 0.1,
                "starting_price": 2700
            }
            grid_strategy_instance = GridStrategy(
                exchange=mock_exchange,  # Use a valid exchange name for the test
                dev_config=config
            )

            self.grid_strategy_instance = grid_strategy_instance
            self.prev_price_for_test = self.grid_strategy_instance.previous_price
            self.prev_price_idx_for_test = self.grid_strategy_instance.previous_price_idx
            print("--- Completed SetUp() ---")

    def test_monitor_and_trade(self):
        """Test the monitor_and_trade method for future markets."""
        # Simulate different price scenarios for the market
        price_changes_future = [2682, 2705, 2720.6597, 2740, 2701.6775]  # Futures prices
        self.grid_strategy_instance.exchange.fetch_ticker.side_effect = price_changes_future

        # Run the monitor_and_trade method in test mode for both strategies
        print(f"grid_strategy_instance: starting price = {self.grid_strategy_instance.previous_price}, "
              f"index = {self.grid_strategy_instance.previous_price_idx}")

        # [56]:2664.1097, 2682.8278, 2701.6775, 2720.6597, 2739.7752, 2759.025, 2778.41, [63]2797.9313
        for i in range(len(price_changes_future)):
            self.grid_strategy_instance.monitor_and_trade()

        # Check if the right number of orders were placed for the market
        self.assertEqual(self.grid_strategy_instance.exchange.place_order.call_count, 6,
                         f"Expected 6 futures orders, but got "
                         f"{self.grid_strategy_instance.exchange.place_order.call_count}")

        # Verify that the correct type of orders were placed (buy/sell) for both markets
        for i in range(len(price_changes_future)):
            current_price_future = price_changes_future[i]
            trade_type_future = 'buy' if current_price_future < self.prev_price_for_test else 'sell'
            self.prev_price_for_test = current_price_future

            # Assert futures market orders
            self.grid_strategy_instance.exchange.place_order.assert_any_call(
                self.grid_strategy_instance.tracking_symbol, trade_type_future, unittest.mock.ANY,
                current_price_future, 'limit')


if __name__ == '__main__':
    unittest.main()
