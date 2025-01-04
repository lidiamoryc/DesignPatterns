# TODO: rename file to base_strategy.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import Any

from pydantic import BaseModel
import structlog
from tqdm import tqdm

from sklearn.ensemble import RandomForestClassifier

# GridSearchItem = dict[str, int | float | str]  # GridSearchItem -> {'lr': 0.01, 'barch_size': 32}
# #  list[GridSearchItem] -> [{'lr': 0.2, 'barch_size': 64}, {'lr': 0.01, 'barch_size': 32}, ...]
# GridType = dict[str, list[int | float | str]]

logger = structlog.get_logger()


@dataclass
class UserInput:  # TODO: How map a JSON file from user to python class?
    model_name: str
    hyperparameters: list[dict[str, list[Any]]]
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
        Transform user friendly input into a parameter grid contaning all posible combinations of requested hyperparameters.
        """

        # hyperparameters = user_input.hyperparameters
        grid = Grid(
            grid_data=[{'lr': 0.1, "batch_size": 32},
                       {'lr': 0.1, "batch_size": 64},
                       {"lr": 0.2, "batch_size": 32},
                       {'lr': 0.2, "batch_size": 64}],
        )

        return grid

    @abstractmethod
    def _get_params_using_heuristic(self, grid: Grid) -> dict[str, Any]:
        """Take a single set of parameters chosen form the grid (one item from the grid)."""
        raise NotImplementedError("calculation method is not implemented")
