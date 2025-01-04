from p2p_network.src.strategies.base_strategy import BaseStrategy, UserInput, GridSearchItem, GridType


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


