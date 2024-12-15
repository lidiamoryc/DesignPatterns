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
  
    @abstractmethod
    def get_possible_model_types(self) -> list[str]:
        """Returns the possible model types.

        Returns:
            models (list[string]): list of possible model types
        """
        raise NotImplementedError("get_possible_model_types method is not implemented")
 
    @abstractmethod
    def get_possible_params(self, model_type: str) -> list[dict]:
        """Returns the possible parameters for the given model type.

        Args:
            model_type (str): type of the model

        Returns:
            params (list[dict]): possible parameters for the given model type
        """
        raise NotImplementedError("get_possible_params method is not implemented")
    
    @abstractmethod
    def get_possible_heuristics(self) -> dict:
        """Returns the possible heuristics.

        Returns:
            heuristics (dict): list of possible heuristics
        """
        raise NotImplementedError("get_possible_heuristics method is not implemented")