import unittest
import bisect

from src.grid_trader import GridTrader


class TestTrading(unittest.TestCase):

    def setUp(self):
        # Define self-defined grid_prices and other necessary parameters
        self.grid_prices = [2635.71, 2656.8665, 2678.1929, 2699.6904, 2721.3605, 2743.2045, 2765.2239, 2787.42]
        self.initial_price = 2699.6904
        self.initial_price_index = 3

        self.trading = GridTrader(
            symbol='ETH/USDT',
            api_key="",
            api_secret="",
            price_min=2635.71,
            price_max=2787.42,
            num_grids=8,
            position=0,
            max_position=10,

            grid_prices=self.grid_prices,
            initial_price=self.initial_price,
            initial_price_idx=self.initial_price_index
        )
        print("--- Initialization Completed ---")
        print(f"initial price={self.trading.previous_price}")
        print(f"initial price idx ={self.trading.previous_price_idx}")
        print(self.trading.grid_prices)

    def test_initialization(self):
        # Verify the initialization
        self.assertEqual(self.trading.grid_prices, self.grid_prices)
        self.assertEqual(self.trading.previous_price_idx, 3)

    def test_trade_amount(self):
        # Note: calculate_trade_amount compute trade amount = (pre_price_idx - curr_price_idx) / 10,
        # And the function does not update the pre_price_idx.
        index = self.trading.calculate_trade_amount(2660)  # trading 1
        self.assertEqual(2, index)
        self.assertEqual(0.1, self.trading.trade_amount)

        index = self.trading.calculate_trade_amount(2710)  # trading 2
        self.assertEqual(3, index)
        self.assertEqual(0, self.trading.trade_amount)

        index = self.trading.calculate_trade_amount(2780)  # trading 3
        self.assertEqual(6, index)
        self.assertEqual(0.3, self.trading.trade_amount)

        index = self.trading.calculate_trade_amount(2725)  # trading 4
        self.assertEqual(4, index)
        self.assertEqual(0.1, self.trading.trade_amount)

        # TODO: adds more cases to test...


if __name__ == '__main__':
    unittest.main()
