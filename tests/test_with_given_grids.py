import unittest
from unittest.mock import patch, MagicMock

from src.strategy.grid_strategy import GridStrategy


class TestTrading(unittest.TestCase):

    def setUp(self):
        # Define self-defined grid_prices and other necessary parameters
        self.grid_prices = [2635.71, 2656.8665, 2678.1929, 2699.6904, 2721.3605, 2743.2045, 2765.2239, 2787.42]
        self.initial_price = 2699.6904
        self.initial_price_index = 3

        self.grid_strategy = GridStrategy(
            exchange_name=None,
            config=None,
            symbol=None,
            starting_price=self.initial_price,
            grid_levels=self.grid_prices,
        )
        print("--- Initialization Completed ---")
        print(f"initial price={self.grid_strategy.grid_levels[self.grid_strategy.previous_price_idx]}")
        print(f"initial price idx ={self.grid_strategy.previous_price_idx}")
        print(self.grid_strategy.grid_levels)

    def test_initialization(self):
        # Verify the initialization
        self.assertEqual(self.grid_strategy.grid_levels, self.grid_prices)
        self.assertEqual(self.grid_strategy.previous_price_idx, 3)
        initial_price = self.grid_strategy.grid_levels[self.grid_strategy.previous_price_idx]
        self.assertEqual(initial_price, self.initial_price)

    def test_trade_amount(self):
        # Note: calculate_trade_amount compute trade amount = (pre_price_idx - curr_price_idx) / 100,
        # And the pre_price_idx starts at 3
        index = self.grid_strategy.calculate_trade_amount(2660, 3)  # trading 1
        self.assertEqual(2, index)
        self.assertEqual(0.01, self.grid_strategy.trade_amount)

        index = self.grid_strategy.calculate_trade_amount(2710, 2)  # trading 2
        self.assertEqual(3, index)
        self.assertEqual(0.01, self.grid_strategy.trade_amount)

        index = self.grid_strategy.calculate_trade_amount(2780, 3)  # trading 3
        self.assertEqual(6, index)
        self.assertEqual(0.03, self.grid_strategy.trade_amount)

        index = self.grid_strategy.calculate_trade_amount(2725, 6)  # trading 4
        self.assertEqual(5, index)
        self.assertEqual(0.01, self.grid_strategy.trade_amount)

    @patch.object(GridStrategy, 'fetch_ticker', return_value=None)  # Patch fetch_ticker method
    @patch('time.sleep', return_value=None)  # Patch sleep to speed up tests
    def test_monitor_and_trade(self, mock_sleep, mock_fetch_ticker):
        """Test the monitor_and_trade method for price changes and trading."""
        # Mock the place_order method
        self.grid_strategy.place_order = MagicMock()

        # Define the sequence of prices and set it as side_effect
        mock_fetch_ticker.side_effect = [2660, 2660, 2710, 2710, 2780, 2780, 2725, 2725]

        # Execute the trading logic
        max_iterations = 5  # Limit to avoid excessive looping
        iterations = 0

        while iterations < max_iterations:
            self.grid_strategy.monitor_and_trade()
            iterations += 1
        """self.grid_strategy.monitor_and_trade()
        self.grid_strategy.monitor_and_trade()
        self.grid_strategy.monitor_and_trade()"""

        # Print out the call arguments to help debug
        print("Calls to place_order:")
        for call in self.grid_strategy.place_order.call_args_list:
            print(call)

        # Assertions to check if the correct orders were placed
        # Verify if place_order was called with correct parameters for spot market
        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'buy', 0.01, 2660, 'limit', 'spot'
        )
        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'buy', 0.01, 2660, 'limit', 'future'
        )

        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.01, 2710, 'limit', 'spot'
        )

        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.01, 2710, 'limit', 'future'
        )

        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.03, 2780, 'limit', 'spot'
        )
        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.03, 2780, 'limit', 'future'
        )

        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'buy', 0.01, 2725, 'limit', 'spot'
        )
        self.grid_strategy.place_order.assert_any_call(
            'ETH/USDT', 'buy', 0.01, 2725, 'limit', 'future'
        )

        # Verify the total number of calls to place_order
        self.assertEqual(self.grid_strategy.place_order.call_count, 8)


if __name__ == '__main__':
    unittest.main()