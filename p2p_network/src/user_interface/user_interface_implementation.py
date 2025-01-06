from p2p_network.src.node.node_interface import NodeInterface
from p2p_network.src.node.node import Node

class WrongUserInputError(Exception):
    """Raised when some user input is not valid."""
    def __init__(self, message: str):
        super().__init__(message)


class UserInterface:
    """
    A class that implements the UserInterfaceInterface. This class is responsible for 
    starting, stopping of the node and giving user the possible models and parameters.
    """
    def __init__(self, model_type: str, initial_params: list[dict]):
        """Initializes the UserInterfaceImplementation.

        Attributes:
            model_type (str): type of the model
            initial_params (dict): initial parameters for the model
            structure of an example initial params list:
            [{"name": "param1", type="int" "value": 5},
            {"name": "param2", type="float", "value": 0.3},
            {"name": "param3", type="string", "value": "value"}]

        Methods:
            start_training: starts the node
            stop_training: stops the node
        """
        self.node: NodeInterface = Node(model_type, initial_params)
        self.is_stopped = False
        self.model_type = model_type
        self.initial_params = initial_params

    def start_training(self) -> None:
        #todo exception handling
        """
        Starts the node.
        """
        self.node.run_node()

    def stop_training(self) -> None:
        """Stops the node.
        """
        self.node.stop_node()
