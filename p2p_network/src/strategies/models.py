from typing import Any
from dataclasses import dataclass

@dataclass
class UserInput:  # TODO: How map a JSON file from user to python class?
    model_name: str
    hyperparameters: dict[str, list[Any]]
    # num_trials: int


@dataclass
class Grid:
    """Grid based on what the user requested."""
    grid_data: list[dict[str, Any]]


@dataclass
class GridSearchOutput:
    """The structured that is returned by the grid_search method.

   Attributes:
    grid_search_output (dict[dict[str, Any], float]):
        A dictionary where:
        - The keys are strings representing combinations of hyperparameters choosen by the _get_params_using_heuristic method (e.g., {"lr": 0.01, "batch_size": 32}).
        - The values are floats representing the corresponding metric scores (e.g., accuracy, loss).
    """

    grid_search_output: dict[str, float | int]