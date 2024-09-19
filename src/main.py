
from src.exchange_manager import ExchangeManager
from src.strategy.grid_strategy import GridStrategy
from src.strategy.strategy_manager import StrategyManager


def main():
    try:
        config = {
            'apiKey': 'your-api-key',
            'secret': 'your-secret',
            'baseURL': 'https://testnet.binancefuture.com'
        }

        # Initialize the Strategy Manager
        strategy_manager = StrategyManager()

        grid_strategy = GridStrategy()  # Creates and adds grid strategies into manager
        strategy_manager.add_strategy(grid_strategy)
        strategy_manager.execute_strategy('GridStrategy', 'BTC/USDT', market_type='futures')  # Run a specific strategy

        # another_strategy = AnotherStrategy(exchange_manager, config)  # Assuming have another class
        # strategy_manager.add_strategy(another_strategy)  # add new strategy into manager

        # strategy_manager.execute_all_strategies()  # Run all strategies

    except KeyboardInterrupt:
        print("\n\nTrading process interrupted by user. Exiting...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Ensure any necessary cleanup is done here
        print("Exiting program.")


if __name__ == "__main__":
    main()
