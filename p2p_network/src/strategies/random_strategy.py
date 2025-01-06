from typing import Any
from p2p_network.src.strategies.base_strategy import BaseStrategy, Grid, UserInput
import random

class RandomGridSearch(BaseStrategy):

    def _get_params_using_heuristic(self, grid: Grid) -> dict[str, Any]:

        hyperparameters = random.choice(grid.grid_data)
        grid.grid_data.remove(hyperparameters)
        return hyperparameters


if __name__ == "__main__":
    user_input = UserInput(
        model_name="RandomForest",
        hyperparameters={
            "n_estimators": [10, 50, 100],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5, 10],
        },
        num_trials=5,
    )

    random_strategy = RandomGridSearch()
    print(random_strategy.grid_search(user_input))