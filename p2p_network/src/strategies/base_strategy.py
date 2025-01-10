from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import Any
import json

import structlog
from tqdm import tqdm

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score


from p2p_network.src.strategies.models import UserInput, Grid, GridSearchOutput

logger = structlog.get_logger()

MODEL_MAP = {
    "RandomForest": RandomForestClassifier,
    "SVC": SVC,
    "LogisticRegression": LogisticRegression,
    "DecisionTree": DecisionTreeClassifier,
}

class BaseStrategy(ABC):
    def grid_search(self,
                    user_input: UserInput) -> tuple[str, Any]:  # TODO: What is the prefered output? Score? Best model weights?

        iris = load_iris() # TODO: which dataset?
        X_train, X_test, y_train, y_test = train_test_split(
            iris.data, iris.target, test_size=0.2, random_state=42)

        # TODO: how many different models? When to switch them?
        model_class = MODEL_MAP.get(user_input.model_name)
        if model_class is None:
            raise ValueError(f"Unsupported model: {user_input.model_name}")

        grid = self.get_grid(user_input)

        hyperparams = self._get_params_using_heuristic(grid)

        # Filter valid hyperparameters
        # valid_params = {k: v for k, v in hyperparams.items() if k in model().get_params()}
        model = model_class(**hyperparams)

        # Train model
        model.fit(X_train, y_train)

        # Log score for this hyperparameters
        predictions = model.predict(X_test)

        # TODO: one choosen metric or more?
        scores = cross_val_score(model, X_train, y_train, cv=5)
        score = scores.mean()
        # score = accuracy_score(y_test, predictions)

        #logger.info("Trial complete!", model=str(model), score=score, hyperparams=hyperparams)

        hyperparams_string = json.dumps(hyperparams)

        return hyperparams_string, score

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