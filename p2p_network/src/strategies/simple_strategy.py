from typing import Any
from p2p_network.src.strategies.base_strategy import BaseStrategy, Grid, UserInput


class SimpleGridSearch(BaseStrategy):

    def _get_params_using_heuristic(self, grid: Grid) -> dict[str, Any]:

        hyperparameters = grid.grid_data.pop(0)
        return hyperparameters


if __name__ == '__main__':
    gs = SimpleGridSearch()

    user_input = UserInput(model_name='NotExistingModelXD',
                           hyperparameters={"batch_size": [x for x in range(100)], "lr": [x / 1000 for x in range(10)]},
                           # TODO: This should be parsed from a JSON file ; P
                           num_trials=5000)

    gs.grid_search(user_input)
