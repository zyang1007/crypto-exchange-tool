from typing import List, Optional

from src.exchange_manager import ExchangeManager
from src.strategy.abstract_strategy import AbstractStrategy


class StrategyManager:
    def __init__(self):
        self.strategies: List[AbstractStrategy] = []

    def add_strategy(self, strategy: AbstractStrategy):
        """Add a strategy to the manager."""
        if not isinstance(strategy, AbstractStrategy):
            raise TypeError("Only AbstractStrategy instances are supported")
        self.strategies.append(strategy)

    def execute_strategy(self, strategy_name: str):
        """Execute a specific strategy by its name."""
        strategy = self._find_strategy_by_name(strategy_name)
        if strategy:
            strategy.execute(time_interval=60)
        else:
            print(f"Strategy '{strategy_name}' not found")

    def execute_all_strategies(self):
        """Execute all strategy"""
        for strategy in self.strategies:
            strategy.execute(time_interval=60)

    def _find_strategy_by_name(self, strategy_name: str) -> Optional[AbstractStrategy]:
        """Find a strategy by its name."""
        for strategy in self.strategies:
            if strategy.__class__.__name__ == strategy_name:
                return strategy
        return None
