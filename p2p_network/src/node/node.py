import json
import threading
import time
from p2p_network.src.managers.message_manager import MessageManager
from p2p_network.src.node.node_interface import NodeInterface
from p2p_network.src.validation.params_validator import ParamsValidator
from p2p_network.src.validation.params_validator import WrongParamError, WrongModelTypeError
from p2p_network.src.strategies.base_strategy import UserInput
from p2p_network.src.strategies.random_strategy import RandomGridSearch


class WrongUserInputError(Exception):
    """Raised when some user input is not valid."""
    def __init__(self, message: str):
        super().__init__(message)

class Node(NodeInterface):
    """A class that represents a node in the network.

    Attributes:
        possible_models_and_params (dict): The possible models and their parameters.
        Example structure of the possible_models_and_params:
        {
            "model1": [{"name": "param1", "type": "int", "value": 5},
                       {"name": "param2", "type": "float", "value": {
                           "min": 0.1,
                           "max": 0.5}},
                       {"name": "param3", "type": "string", "value": "value"}],
            "model2": [{"name": "param1", "type": "int", "value": {
                           "min": 1,
                           "max": 10}},
                       {"name": "param2", "type": "float", "value": 0.3},
                       {"name": "param3", "type": "string", "value": "value"}]
        }
        
        possible_heuristics (list): The possible heuristics.
        Example structure of the possible_heuristics:
        {"heuristics":[
        {"name": "heuristic1", "description": "description1"},
        {"name": "heuristic2", "description": "description2"}
        ]}}

        model_type (str): type of the model

        initial_params (dict): initial parameters for the model
        structure of an example initial params list:
        [{"name": "param1", type="int" "value": 5},
        {"name": "param2", type="float", "value": 0.3},
        {"name": "param3", type="string", "value": "value"}]

        port (int): port on which the node will run
        other_peer_port (int or None): port of the other peer node

        params_validator (ParamsValidator): an instance of the ParamsValidator class
    """
    def __init__(self, model_type: str, initial_params: list[dict], socket_port: int, other_peer_port: int = None):
        with open("p2p_network/available_models_and_params.json", encoding="utf-8") as f:
            self.possible_models_and_params: dict = json.load(f)
        with open("p2p_network/available_heuristics.json", encoding="utf-8") as f:
            self.possible_heuristics: dict = json.load(f)
        self.model_type: str = model_type
        self.initial_params: dict = initial_params

        self.params_validator = ParamsValidator(self.possible_models_and_params)
        self.message_manager = MessageManager(socket_port, other_peer_port)

        try:
            #self.params_validator.validate_model_type(model_type)
            #self.params_validator.validate_params(initial_params)
            pass
        except WrongModelTypeError as e:
            raise WrongUserInputError(str(e)) from e
        except WrongParamError as e:
            raise WrongUserInputError(str(e)) from e

    def run_node(self):
        threading.Thread(target=self.message_manager.initialize).start()

        user_input = UserInput(
        model_name="RandomForest",
        hyperparameters={
            "n_estimators": [10, 50, 100],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5, 10],
        },
        num_trials=5,
    )
        random_strategy = RandomGridSearch()
        
        while(True):
            hyperparams = random_strategy.grid_search(user_input).grid_search_output
            params, score = max(hyperparams.items(), key=lambda x: x[1])
            self.message_manager.publish_message(f"Node found best hyperparameters: {params} with score: {score}")
            time.sleep(10)
        

    def stop_node(self):
        pass

    def get_possible_model_types(self) -> list[str]:
        return self.possible_models_and_params.keys()

    def get_possible_params(self, model_type: str) -> list[dict]:
        return self.possible_models_and_params[model_type]

    def get_possible_heuristics(self) -> dict:
        return self.possible_heuristics
