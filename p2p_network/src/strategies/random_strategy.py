from typing import Any
from p2p_network.src.strategies.base_strategy import BaseStrategy, Grid, UserInput
import random

class RandomGridSearch(BaseStrategy):

    def _get_params_using_heuristic(self, grid: Grid) -> dict[str, Any]:

        hyperparameters = random.choice(grid.grid_data)
        grid.grid_data.remove(hyperparameters)
        return hyperparameters

