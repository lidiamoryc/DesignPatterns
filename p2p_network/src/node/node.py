import json
import threading
from p2p_network.src.commands.exit_network import ExitNetworkCommand
from p2p_network.src.commands.notify_about_results import NotifyAboutResultsCommand
from p2p_network.src.commands.join_network import JoinNetworkCommand
from p2p_network.src.managers.message_manager import LOCALHOST, MessageManager
from p2p_network.src.node.node_interface import NodeInterface
from p2p_network.src.validation.params_validator import ParamsValidator
from p2p_network.src.validation.params_validator import WrongParamError, WrongModelTypeError
from p2p_network.src.strategies.base_strategy import UserInput, BaseStrategy
from p2p_network.src.strategies.random_strategy import RandomGridSearch
from p2p_network.src.strategies.strategy_mapper import StrategyMapper
from p2p_network.src.strategies.context import Context


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
    def __init__(self, model_type: str, initial_params: list[dict], strategy: str, socket_port: int, other_peer_port: int = None):
        with open("p2p_network/available_models_and_params.json", encoding="utf-8") as f:
            self.possible_models_and_params: dict = json.load(f)
        with open("p2p_network/available_heuristics.json", encoding="utf-8") as f:
            self.possible_heuristics: dict = json.load(f)
        
        self.model_type: str = model_type
        self.initial_params: dict = initial_params
        self.strategy: BaseStrategy = StrategyMapper.map(strategy)
        self.params_validator = ParamsValidator(self.possible_models_and_params)
        self.message_manager = MessageManager(socket_port)
        self.other_peer_port = other_peer_port
        self.context = Context(self.strategy)
        self.is_running = False

        try:
            #self.params_validator.validate_model_type(model_type)
            #self.params_validator.validate_params(initial_params)
            pass
        except WrongModelTypeError as e:
            raise WrongUserInputError(str(e)) from e
        except WrongParamError as e:
            raise WrongUserInputError(str(e)) from e

    def run_node(self):
        self.is_running = True

        self.messaging_thread = threading.Thread(target=self.join_network)
        self.messaging_thread.start()

        self.computation_thread = threading.Thread(target=self.run_computation)
        self.computation_thread.start()

    def join_network(self):
        if self.other_peer_port:
            other_peer = (LOCALHOST, self.other_peer_port)
            
            try:
                self.command = JoinNetworkCommand(self.message_manager)
                self.command.execute(other_peer)
            except ConnectionRefusedError:
                print(f"Unable to join network")

        self.message_manager.initialize()
    
    def run_computation(self):

        while self.is_running:
            hyperparams, score = self.context.executeStrategy(self.initial_params)
            params, score = max(hyperparams.items(), key=lambda x: x[1])
            
            self.command = NotifyAboutResultsCommand(self.message_manager)
            self.command.execute({params, score})

    def stop_node(self):
        self.is_running = False
        
        self.command = ExitNetworkCommand(self.message_manager)
        self.command.execute()
        
        self.messaging_thread.join()
        self.computation_thread.join()
    
    def get_possible_model_types(self) -> list[str]:
        return self.possible_models_and_params.keys()

    def get_possible_params(self, model_type: str) -> list[dict]:
        return self.possible_models_and_params[model_type]

    def get_possible_heuristics(self) -> dict:
        return self.possible_heuristics
