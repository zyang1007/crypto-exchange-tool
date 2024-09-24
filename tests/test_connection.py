import time
import unittest

from src.exchange_manager import ExchangeManager


class TestBinanceTestnetConnection(unittest.TestCase):
    def setUp(self):
        self.exchange_manager = ExchangeManager(exchange_name=None, config=None, symbol='ETH/USDT')
        print("Initialization Completed!")

    def test_fetch_balance(self):
        print("> Fetching spot spot_balance...")
        spot_balance = self.exchange_manager.fetch_balance('spot')
        for asset, data in spot_balance['total'].items():
            if data > 0:
                pass
                # print(f"Asset: {asset}, Free: {spot_balance['free'][asset]}, Locked: {spot_balance['used'][asset]}")

        self.assertIsNotNone(spot_balance)
        self.assertIsNotNone(spot_balance['total']['ETH'])

        print("> Fetching future spot_balance...")
        future_balance = self.exchange_manager.fetch_balance('futures')
        self.assertIsNotNone(future_balance)

        print(f"futures ETH: {future_balance['total']['ETH']}")
        free_eth = future_balance['total'].get('ETH', 0)
        print(f"Free ETH: {free_eth}")

        self.assertEqual(0, future_balance['total']['ETH'])

    # Example of transferring from spot to futures
    def test_transfer_spot_to_futures(self):
        usdt_spot = self.exchange_manager.fetch_balance('spot')
        free_usdt_spot = usdt_spot['total'].get('USDT', 0)
        print(f"Initial free USDT in Spot: {free_usdt_spot}")

        usdt_future = self.exchange_manager.fetch_balance('futures')
        free_usdt_future = usdt_future['total'].get('USDT', 0)
        print(f"Initial free USDT in Future: {free_usdt_future}")

        before_transfer = free_usdt_future

        transfer_amount = 10
        try:
            self.exchange_manager.futures_exchange.futures_transfer('USDT', transfer_amount, 1)
            print(f"Transferred {transfer_amount} USDT from Spot to Futures.")
        except Exception as e:
            print(f"Transfer failed: {str(e)}")

        usdt_future = self.exchange_manager.fetch_balance('futures')
        after_transfer_usdt = usdt_future['total'].get('USDT', 0)
        print(f"Initial free USDT in Future: {after_transfer_usdt}")

        self.assertEqual(before_transfer + transfer_amount, after_transfer_usdt)

    """ def transfer_in(self, code: str, amount, params={}):
            # transfer from spot wallet to usdm futures wallet
            return self.futuresTransfer(code, amount, 1, params)
            
        def transfer_out(self, code: str, amount, params={}):
            # transfer from usdm futures wallet to spot wallet
            return self.futuresTransfer(code, amount, 2, params)"""


if __name__ == "__main__":
    print("--- Tests main  ---")

    binance_testnet = TestBinanceTestnetConnection()

    # binance_testnet.test_fetch_balance()
    binance_testnet.test_transfer_spot_to_futures()

    print("---All tests completed ---")

