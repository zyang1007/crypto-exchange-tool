import unittest
from unittest.mock import patch, MagicMock

from src.strategy.grid_strategy import GridStrategy


class TestTrading(unittest.TestCase):

    def setUp(self):
        with patch('src.service.exchange') as MockExchange:
            # Mock the create_exchange_instance method to return a mock exchange instance
            mock_exchange = MagicMock()

            MockExchange.return_value.create_exchange_instance.side_effect = [
                mock_exchange  # For futures market
            ]

            # Mock the necessary methods and attributes
            mock_exchange.fetch_ticker = MagicMock()
            mock_exchange.place_order = MagicMock()

        # Define self-defined grid_prices and other necessary parameters
        self.grid_prices = [2635.71, 2656.8665, 2678.1929, 2699.6904, 2721.3605, 2743.2045, 2765.2239, 2787.42]
        self.initial_price = 2699.6904

        config = {
            "symbol": "ETH/USDT",
            "min_price": 1800,
            "max_price": 3600,
            "num_grids": 100,
            "max_position": 10,
            "security_deposit": 0,
            "fixed_trade_amount": 0.1,
            "starting_price": 2699.6904
        }
        self.grid_strategy = GridStrategy(
            exchange=mock_exchange,  # Use a valid exchange name for the test
            dev_config=config,
            grid_levels=self.grid_prices
        )

        print("--- Initialization Completed ---")
        print(f"initial price={self.grid_strategy.grid_levels[self.grid_strategy.previous_price_idx]}")
        print(f"initial price idx ={self.grid_strategy.previous_price_idx}")
        print(self.grid_strategy.grid_levels)

    def test_initialization(self):
        # Verify the initialization
        self.assertEqual(self.grid_strategy.grid_levels, self.grid_prices)
        self.assertEqual(3, self.grid_strategy.previous_price_idx)
        initial_price = self.grid_strategy.grid_levels[self.grid_strategy.previous_price_idx]
        self.assertEqual(initial_price, self.initial_price)

    def test_monitor_and_trade(self):
        """Test the monitor_and_trade method for price changes and trading."""
        # Mock the place_order method
        self.grid_strategy.exchange.place_order = MagicMock()

        # Define the sequence of prices and set it as side_effect
        market_prices = [2660, 2710, 2780, 2725]
        self.grid_strategy.exchange.fetch_ticker.side_effect = market_prices

        # Execute the trading logic
        max_iterations = 4  # Limit to avoid excessive looping
        iterations = 0

        while iterations < max_iterations:
            self.grid_strategy.monitor_and_trade()
            iterations += 1

        # Print out the call arguments to help debug
        print("Calls to place_order:")
        for call in self.grid_strategy.exchange.place_order.call_args_list:
            print(call)

        # Assertions to check if the correct orders were placed
        # Verify if place_order was called with correct parameters for spot market

        self.grid_strategy.exchange.place_order.assert_any_call(
            'ETH/USDT', 'buy', 0.1, 2660, 'limit'
        )

        self.grid_strategy.exchange.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.1, 2710, 'limit'
        )

        self.grid_strategy.exchange.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.1, 2780, 'limit'
        )
        self.grid_strategy.exchange.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.1, 2780, 'limit'
        )
        self.grid_strategy.exchange.place_order.assert_any_call(
            'ETH/USDT', 'sell', 0.1, 2780, 'limit'
        )

        self.grid_strategy.exchange.place_order.assert_any_call(
            'ETH/USDT', 'buy', 0.1, 2725, 'limit'
        )

        # Verify the total number of calls to place_order
        self.assertEqual(self.grid_strategy.exchange.place_order.call_count, 6)


if __name__ == '__main__':
    unittest.main()
