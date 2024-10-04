from src.strategy.abstract_strategy import AbstractStrategy


class OtherStrategy(AbstractStrategy):
    def __init__(self, exchange, strategy_config, tracking_symbol):
        super().__init__(exchange, strategy_config, tracking_symbol)

    def execute(self, time_interval):
        # Implement another trading strategy
        print(f"Executing other strategy...")
