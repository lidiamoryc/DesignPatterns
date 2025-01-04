# TODO: rename file to base_strategy.py
from abc import ABC, abstractmethod
from typing import Any

GridSearchItem = dict[str, Any]  # GridSearchItem -> {'lr': 0.01, 'barch_size': 32}
#  list[GridSearchItem] -> [{'lr': 0.2, 'barch_size': 64}, {'lr': 0.01, 'barch_size': 32}, ...]
AvailableHyperparameterValuesType = dict[str, list[int | float | str]]


class UserInput:  # TODO: How map a JSON file from user to python class?
    model_name: str
    hyperparameters: list[AvailableHyperparameterValuesType]
    num_trials: int


class BaseStrategy(ABC):
    def grid_search(self, user_input: UserInput):
        """
        Input: Grid of hyperparameters sets
        Output: Best model
        """
        grid = self.get_grid(user_input)
        # TODO: Sklearn grid search here?

    @abstractmethod
    def get_grid(self, user_input: UserInput) -> list[GridSearchItem]:  # TODO: top_k_params?
        # TODO: Update docstring
        raise NotImplementedError("calculation method is not implemented")

    @abstractmethod
    def _get_params_using_heuristic(self, available_hyperparameters: dict) -> GridSearchItem:
        """Generate a single set of parameters (one item of gridsearch)"""
        raise NotImplementedError("calculation method is not implemented")


class SimpleGridSearch(BaseStrategy):
    def grid_search(self, user_input):
        grid = self.get_grid()

        for _ in range(user_input.num_trials):
            output, updated_grid = self._get_params_using_heuristic(grid)
            # output: new gridsearch (without the hyperparameters we've tested out in this step) + acc + model?

        return best_model, best_score


    def get_grid(self, user_input: UserInput) -> list[GridSearchItem]:

        hyperparameters = user_input.hyperparameters
        grid = []

        # for _ in range(user_input.num_trials): # Generate a list of N hyperparameter sets to try out
        #     grid.append(self._get_params_using_heuristic(hyperparameters))

        return grid

    def _get_params_using_heuristic(self,
                                    available_hyperparameters: AvailableHyperparameterValuesType) -> GridSearchItem:
        """Sample parameters based on the available hyperparameters"""

        chosen_parameters: GridSearchItem = {}

        for name, value in available_hyperparameters.items():
            pass

        return chosen_parameters


class BayesianGridSearchStrategy(BaseStrategy):
    """In contrast to GridSearchCV, not all parameter values are tried out, but rather a fixed number of parameter
     settings is sampled from the specified distributions. The number of parameter settings that
     are tried is given by n_iter."""

    def __init__(self, n_iter: int, available_hyperparameters: dict):
        """
        Initialize the BayesianGridSearchStrategy with the number of iterations for sampling.

        Args:
            n_iter (int): The number of parameter settings to try.
            available_hyperparameters (dict): Dictionary with hyperparameter names as keys and ranges or choices as values.
        """
        self.n_iter = n_iter
        self.available_hyperparameters = available_hyperparameters

    def get_grid(self, user_input: UserInput) -> list[GridSearchItem]:
        """Generate grid (sampled parameters) using Bayesian optimization approach."""
        n_iter = user_input.num_trials
        grid = []

        for _ in range(self.n_iter):
            grid.append(self._get_params_using_heuristic(self.available_hyperparameters))

        return grid

    def _get_params_using_heuristic(self, available_hyperparameters: dict) -> GridSearchItem:
        """Sample parameters based on the available hyperparameters"""

        chosen_parameters: GridSearchItem = {}

        for name, value in available_hyperparameters.items():
            pass

        return chosen_parameters


class RandomSearchStrategy(BaseStrategy):
    """A strategy for hyperparameter search that selects random combinations of parameters
    from the specified parameter space."""
    pass
