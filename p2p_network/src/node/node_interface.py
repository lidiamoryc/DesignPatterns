from abc import ABC, abstractmethod

class NodeInterface(ABC):
    """A class that defines the interface for the Node class.
    """

    @abstractmethod
    def run_node(self):
        raise NotImplementedError("run_node method is not implemented")
 
    @abstractmethod
    def stop_node(self):
        raise NotImplementedError("stop_node method is not implemented")
