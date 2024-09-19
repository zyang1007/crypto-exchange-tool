from src.strategy.abstract_strategy import AbstractStrategy


class OtherStrategy(AbstractStrategy):
    def __init__(self, symbol, exchange):
        super().__init__(symbol, exchange)

    def execute(self):
        # Implement another trading strategy
        print(f"Executing other strategy for {self.symbol}")
