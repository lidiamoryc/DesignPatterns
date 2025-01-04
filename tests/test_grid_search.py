from unittest.mock import MagicMock

import pytest

from p2p_network.src.strategies.base_strategy import UserInput
from p2p_network.src.strategies.simple_strategy import SimpleGridSearch


@pytest.fixture
def mock_user_input():
    """Fixture to provide mock UserInput data."""
    return UserInput(
        model_name="NotExistingModelXD",
        hyperparameters={"batch_size": [x for x in range(100)], "lr": [x / 1000 for x in range(10)]},
        num_trials=5000
    )

@pytest.fixture
def simple_grid_search():
    """Fixture to create an instance of SimpleGridSearch."""
    return SimpleGridSearch()

def test_grid_search_execution(simple_grid_search, mock_user_input):
    """
    Test if grid_search runs without errors and logs appropriately.
    """
    gs = simple_grid_search
    user_input = mock_user_input

    # Mock dependent methods if needed
    gs._get_params_using_heuristic = MagicMock(return_value={"batch_size": 32, "lr": 0.001})
    gs._evaluate_model = MagicMock(return_value=("mock_model", 0.9))

    # Run the grid search
    gs.grid_search(user_input)

    # Assertions
    # assert best_model is not None, "Grid search should return a model."
    # assert best_score > 0, "Grid search should return a positive score."

    # Verify mocked methods were called
    gs._get_params_using_heuristic.assert_called()
    # gs._evaluate_model.assert_called()