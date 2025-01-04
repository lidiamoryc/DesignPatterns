from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """An interface for heuristics used to calculate for the best combination of parameters.

    Methods:
        calculate_new_params: calculate the new parameters based on the 
        top k parameters and the number of combinations

    Raises:
        NotImplementedError: the method for search is not implemented
    """

    @abstractmethod
    def get_grid(self, top_k_params: list[dict], gird_items: int) -> list[dict]:
        # TODO: Update docstring
        """Calculate the new parameters based on the top k parameters and the number of combinations

        Args:
            top_k_params (list[dict]): top k sets of already used parameters
            comb_num (int): How many combinations should the function return

        Raises:
            NotImplementedError: method is not implemented

        Returns:
            list[dict]: list of comb_num sets of new parameters
        """
        raise NotImplementedError("calculation method is not implemented")

    @abstractmethod
    def _get_params_using_heuristic(self) -:
    