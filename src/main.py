from grid_trader import GridTrader
import config


def main():
    try:
        trader = GridTrader(  # Trading parameters
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            symbol='ETH/USDT',
            price_min=1800,
            price_max=3600,
            num_grids=100,
            position=0,
            max_position=10,
            initial_price=2700,
            initial_price_idx=None,
            grid_prices=None
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
