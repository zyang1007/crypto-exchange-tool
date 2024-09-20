import time
import unittest

from src.exchange_manager import ExchangeManager


class TestBinanceTestnetConnection(unittest.TestCase):
    def setUp(self):
        self.test_exchange_manager = ExchangeManager(exchange_name=None, config=None, symbol='ETH/USDT')
        print("Initialization Completed!")

    def test_fetch_balance(self):
        print("> Fetching spot spot_balance...")
        spot_balance = self.test_exchange_manager.fetch_balance('spot')
        for asset, data in spot_balance['total'].items():
            if data > 0:
                pass
                # print(f"Asset: {asset}, Free: {spot_balance['free'][asset]}, Locked: {spot_balance['used'][asset]}")

        self.assertIsNotNone(spot_balance)
        self.assertIsNotNone(spot_balance['total']['ETH'])

        print("> Fetching future spot_balance...")
        future_balance = self.test_exchange_manager.fetch_balance('futures')
        self.assertIsNotNone(future_balance)

        print(f"futures ETH: {future_balance['total']['ETH']}")
        free_eth = future_balance['total'].get('ETH', 0)
        print(f"Free ETH: {free_eth}")


        self.assertEqual(0, future_balance['total']['ETH'])



if __name__ == "__main__":
    print("--- Tests main  ---")

    binance_testnet = TestBinanceTestnetConnection()

    binance_testnet.test_fetch_balance()


    print("---All tests completed ---")
