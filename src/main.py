from grid_trader import GridTrader
import config


def main():
    try:
        trader = GridTrader(
            api_key = config.API_KEY,
            api_secret = config.API_SECRET,
            symbol = 'ETH/USDT',
            initial_price = 2700,
            price_min = 1800,
            price_max = 3600,
            grids = 100,
            fixed_trade_volume = 0.1,
            max_amount = 10
        )
        trader.monitor_and_trade()

    except KeyboardInterrupt:
        print("\n\nTrading process interrupted by user. Exiting...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Ensure any necessary cleanup is done here
        print("Exiting program.")


if __name__ == "__main__":
    main()
