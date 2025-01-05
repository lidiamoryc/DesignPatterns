from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import Any
import json

import structlog
from tqdm import tqdm

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score


from p2p_network.src.strategies.models import UserInput, Grid, GridSearchOutput

logger = structlog.get_logger()


class BaseStrategy(ABC):
    def grid_search(self,
                    user_input: UserInput) -> GridSearchOutput:  # TODO: What is the prefered output? Score? Best model weights?

        iris = load_iris() # TODO: which dataset?
        X_train, X_test, y_train, y_test = train_test_split(
            iris.data, iris.target, test_size=0.2, random_state=42)

        grid = self.get_grid(user_input)

        # TODO: figure out how many results should the function return - is the num_trials correct appriach?
        results = {}

        for _ in tqdm(range(min(user_input.num_trials, len(grid.grid_data))), desc="Running Grid Search"):
            hyperparams = self._get_params_using_heuristic(grid)

            # TODO: how many different models? When to switch them?
            model = RandomForestClassifier(**hyperparams)

            # Train model
            model.fit(X_train, y_train)

            # Log score for this hyperparameters
            predictions = model.predict(X_test)

            scores = cross_val_score(model, X_train, y_train, cv=5)
            score = scores.mean()
            # score = accuracy_score(y_test, predictions)

            logger.info("Trial complete!", model=str(model), score=score, hyperparams=hyperparams)

            hyperparams_string = json.dumps(hyperparams)
            results[hyperparams_string] = score

        hyperparams_with_metrics = GridSearchOutput(results)

        return hyperparams_with_metrics

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