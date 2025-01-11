from __future__ import annotations
from abc import ABC, abstractmethod

from p2p_network.src.strategies.base_strategy import BaseStrategy


class Context:
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: BaseStrategy) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> BaseStrategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseStrategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def executeStrategy(self, params) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        return self._strategy.grid_search(params)