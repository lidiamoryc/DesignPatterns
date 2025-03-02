import json
import time
import uuid
from p2p_network.src.commands.command import Command
from p2p_network.src.logger.logger import Logger
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
        
        self.node_id = uuid.uuid4()
        self.model_type: str = model_type
        self.initial_params: dict = initial_params
        self.userInput = UserInput(model_name=self.model_type, hyperparameters=self.initial_params)
        self.strategy: BaseStrategy = StrategyMapper.map(strategy)(self.userInput)
        self.context = Context(self.strategy)
        self.is_running = False
        self.command = None
        self.database_path = f"p2p_network/src/database/database{self.node_id}.json"
        self.logger_path = "p2p_network/src/logger/log.text"

        self.logger = Logger(self.logger_path)
        self.database = DatabaseManager(self.database_path, self.model_type)

        
    def set_command(self, command: Command):
        self.command = command

    def log_message(self, message: str):
        self.logger.log(self.node_id, message)

    def get_current_records(self):
        return self.database.read_db()
    
    def store_computed_records(self, records: list[dict]):
        self.database.override_db_with_custom_data(records)
        for record in records["combinations"]:
            results = json.loads(record)
            self.remove_from_grid(results)

    def run_node(self):
        self.is_running = True

        if self.command:
            self.command.execute()
            self.log_message(f"Joined network")

        self.run_computation()
    
    def run_computation(self):
        while self.is_running:
            params = self.context.executeStrategy()
            if params is None:
                print("No more params to compute. Press q to stop the node.")
                self.stop_node()
                break
            self.database.add_to_db(params)
            self.log_message(f"Computed new params: {params}")
            self.command.execute(results={params})
            self.log_message(f"Executed: {self.command}")

    def stop_node(self):
        self.is_running = False
        self.command.execute()
    
    def new_results(self, results: dict):
        if results == "{}":
            return
        results = results[2:-2]
        self.database.add_to_db(results)
        results = json.loads(results)
        self.log_message(f"Received new results: {results}")
        self.remove_from_grid(results)
    
    def remove_from_grid(self, results: dict):
        for grid in self.strategy.grid.grid_data:
            all_match = True
            for key in grid.keys():
                if grid[key] != results[key]:
                    all_match = False
            if all_match:
                self.strategy.grid.grid_data.remove(grid)
                break

        
            
            

