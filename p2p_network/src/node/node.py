import json
import time
from p2p_network.src.commands.command import Command
from p2p_network.src.node.node_interface import NodeInterface
from p2p_network.src.validation.params_validator import ParamsValidator
from p2p_network.src.validation.params_validator import WrongParamError, WrongModelTypeError
from p2p_network.src.strategies.base_strategy import UserInput, BaseStrategy
from p2p_network.src.strategies.random_strategy import RandomGridSearch
from p2p_network.src.strategies.strategy_mapper import StrategyMapper
from p2p_network.src.strategies.context import Context
from p2p_network.src.strategies.base_strategy import BaseStrategy
from p2p_network.src.database.database_manager import DatabaseManager


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
    def __init__(self, model_type: str, initial_params: list[dict], strategy: str):
        with open("p2p_network/available_models_and_params.json", encoding="utf-8") as f:
            self.possible_models_and_params: dict = json.load(f)
        with open("p2p_network/available_heuristics.json", encoding="utf-8") as f:
            self.possible_heuristics: dict = json.load(f)
        
        self.model_type: str = model_type
        self.initial_params: dict = initial_params
        self.strategy: BaseStrategy = StrategyMapper.map(strategy)
        self.params_validator = ParamsValidator(self.possible_models_and_params)
        self.context = Context(self.strategy())
        self.is_running = False
        self.command = None
        self.database_path = "p2p_network/src/database/database.json"
        self.database = DatabaseManager(self.database_path, self.model_type)

        try:
            #self.params_validator.validate_model_type(model_type)
            #self.params_validator.validate_params(initial_params)
            pass
        except WrongModelTypeError as e:
            raise WrongUserInputError(str(e)) from e
        except WrongParamError as e:
            raise WrongUserInputError(str(e)) from e
        
    def set_command(self, command: Command):
        self.command = command

    def run_node(self):
        self.is_running = True

        if self.command:
            self.command.execute()

        self.run_computation()
    
    def run_computation(self):
        userInput = UserInput(model_name=self.model_type, hyperparameters=self.initial_params)
        while self.is_running:
            time.sleep(5)
            params = self.context.executeStrategy(userInput)
            self.database.add_to_db(params)
            
            self.command.execute(results={params})

    def stop_node(self):
        self.is_running = False
        self.command.execute()
            
    def get_possible_model_types(self) -> list[str]:
        return self.possible_models_and_params.keys()

    def get_possible_params(self, model_type: str) -> list[dict]:
        return self.possible_models_and_params[model_type]

    def get_possible_heuristics(self) -> dict:
        return self.possible_heuristics
