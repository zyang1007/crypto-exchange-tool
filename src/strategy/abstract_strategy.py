from abc import ABC, abstractmethod
from src.service.exchange import AbstractExchange

""" Base class for all strategies that defines auto trading behavior(trades and others)"""


class AbstractStrategy(ABC):
    def __init__(self, exchange: AbstractExchange):
        self.exchange = exchange

    @abstractmethod
    def execute(self, time_interval):
        """Execute the trading strategy."""
        pass
