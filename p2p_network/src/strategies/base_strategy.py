from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import Any

import structlog
from tqdm import tqdm

from sklearn.ensemble import RandomForestClassifier

logger = structlog.get_logger()


@dataclass
class UserInput:  # TODO: How map a JSON file from user to python class?
    model_name: str
    hyperparameters: dict[str, list[Any]]
    num_trials: int


@dataclass
class Grid:
    """Grid based on what the user requested."""
    grid_data: list[dict[str, Any]]


class BaseStrategy(ABC):
    def grid_search(self,
                    user_input: UserInput) -> float:  # TODO: What is the prefered output? Score? Best model weights?
        grid = self.get_grid(user_input)

        for _ in tqdm(range(user_input.num_trials), desc="Running Grid Search"):
            hyperparams = self._get_params_using_heuristic(grid)
            # model = RandomForestClassifier(**hyperparams)
            model = RandomForestClassifier() # Dummy model
            # print(model)
            # TODO: Train model
            # TODO: Log score for this hyperparameters

            score = 2137  # TODO: Compute actual score

            logger.info("Trial complete!", model=str(model), score=score, hyperparams=hyperparams)

        return score

    def get_grid(self, user_input: UserInput) -> Grid:
        """
        Transform user friendly input into a parameter grid containing all possible combinations of requested hyperparameters.
        """
        keys = user_input.hyperparameters.keys()
        values = user_input.hyperparameters.values()
        assert len(keys) > 0, f"Number of hyperparameters to choose from must be greater than 0."
        assert len(values) > 0, f"Number of hyperparameters to choose from must be greater than 0."

        all_possible_combinations = [dict(zip(keys, combination)) for combination in product(*values)]

        grid = Grid(all_possible_combinations)

        return grid

    @abstractmethod
    def _get_params_using_heuristic(self, grid: Grid) -> dict[str, Any]:
        """Take a single set of parameters chosen form the grid (one item from the grid)."""
        raise NotImplementedError("calculation method is not implemented")
