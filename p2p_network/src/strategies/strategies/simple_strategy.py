from typing import Any

from p2p_network.src.strategies.base_strategy import BaseStrategy, Grid, UserInput


class SimpleGridSearch(BaseStrategy):

    def _get_params_using_heuristic(self, grid: Grid) -> dict[str, Any]:
        if not grid:
            raise ValueError("No hyperparameters available for selection.")

        hyperparameters = grid.grid_data.pop(0)
        return hyperparameters


if __name__ == '__main__':
    gs = SimpleGridSearch()
    #
    # grid_data = [{'lr': 0.1, "batch_size": 32},
    #              {'lr': 0.1, "batch_size": 64},
    #              {"lr": 0.2, "batch_size": 32},
    #              {'lr': 0.2, "batch_size": 64}],

    user_input = UserInput(model_name='NotExistingModelXD',
                           hyperparameters=[{"batch_size": [x for x in range(100)]}, {"lr": [x / 1000 for x in range(10)]}],
                           num_trials=3)

    gs.grid_search(user_input)

