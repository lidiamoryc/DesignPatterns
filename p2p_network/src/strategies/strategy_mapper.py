from p2p_network.src.strategies.base_strategy import BaseStrategy
from p2p_network.src.strategies.random_strategy import RandomGridSearch
from p2p_network.src.strategies.bayesian_strategy import BayesianGridSearch

class StrategyMapper:
    @classmethod
    def map(cls, strategy: str) -> BaseStrategy:
        if strategy == "random":
            return RandomGridSearch
        elif strategy == "bayesian":
            return BayesianGridSearch
        else:
            raise Exception("Invalid strategy")