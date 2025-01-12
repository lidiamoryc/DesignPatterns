import threading
import sys
from p2p_network.src.commands.exit_network import ExitNetworkCommand
from p2p_network.src.commands.join_network import JoinNetworkCommand
from p2p_network.src.commands.notify_about_results import NotifyAboutResultsCommand
from p2p_network.src.managers.message_manager import MessageManager
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
    def __init__(self, model_type: str, initial_params: list[dict], strategy: str,  socket_port: int = 5001, other_peer_port: int = None):
        """Initializes the UserInterfaceImplementation.

        Attributes:
            model_type (str): type of the model
            initial_params (dict): initial parameters for the model
            structure of an example initial params list:
            [{"name": "param1", type="int" "value": 5},
            {"name": "param2", type="float", "value": 0.3},
            {"name": "param3", type="string", "value": "value"}]
            port (int): port on which the node will run
            other_peer_port (int or None): port of the other peer node
        Methods:
            start_training: starts the node
            stop_training: stops the node
        """
        self.node: NodeInterface = Node(model_type, initial_params, strategy)
        self.is_stopped = False
        self.model_type = model_type
        self.initial_params = initial_params
        self.message_manager = MessageManager(self.node, socket_port, other_peer_port)

        join_network_command = JoinNetworkCommand(self.message_manager) if other_peer_port is not None else None
        
        if join_network_command:
            self.node.set_command(join_network_command)

        if not self.message_manager.check_socket():
            print("Error: Socket is not open. It may be already in use.")
            sys.exit(1)

        if not self.message_manager.check_other_socket():
            print("Error: Other peer port is open. It may not be already in use.")
            sys.exit(1)

    def start_training(self) -> None:
        """
        Starts the node.
        """
        try:
            self.messaging_thread = threading.Thread(target=self.message_manager.initialize)
            self.messaging_thread.start()

            self.computation_thread = threading.Thread(target=self.node.run_node)
            self.computation_thread.start()

            notify_about_results_command = NotifyAboutResultsCommand(self.message_manager)
            self.node.set_command(notify_about_results_command)
        except RuntimeError as e:
            print(f"Error: {e}")
            self.stop_training()
            sys.exit(1)
            
    def stop_training(self) -> None:
        """Stops the node.
        """
        exit_network_command = ExitNetworkCommand(self.message_manager)
        self.node.set_command(exit_network_command)
        self.node.stop_node()

        self.messaging_thread.join()
        self.computation_thread.join(timeout=5)
