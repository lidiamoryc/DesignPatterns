import numpy as np
import json
import numbers

class WrongParamError(ValueError):
    """Raised when some parameter are not valid."""

    def __init__(self, param_name: str, param_value: str):
        super().__init__(f"Parameter {param_name} with value {param_value} is not valid.")

class WrongModelTypeError(ValueError):
    """Raised when the model type is not valid."""

    def __init__(self, model_type: str):
        super().__init__(f"Model type {model_type} is not valid.")

class WrongStrategyError(ValueError):
    """Raised when the strategy is not valid."""

    def __init__(self, strategy: str):
        super().__init__(f"Strategy {strategy} is not valid.")





class ParamsValidator:
    """
    A class that validates the parameters for the node.
    Methods:
        validate_model_type: validates the given model type
        validate_params: validates the given parameters
    """
    def __init__(self):
        with open("p2p_network/src/validation/possible_models_and_params.json", encoding="utf-8") as f:
            self._possible_models_and_params = json.loads(f.read())
        with open("p2p_network/src/validation/possible_strategies.json", encoding="utf-8") as f:
            self._possible_strategies = json.loads(f.read())

    def validate_model_type(self, model_type: str) -> bool:
        """Validates the given model type.

        Args:
            model_type (str): given model type

        Returns:
            bool: True if the model type is valid
        """
        if model_type not in self._possible_models_and_params.keys():
            raise WrongModelTypeError(model_type)
        return True
    
    def validate_strategy(self, strategy: str) -> bool:
        """Validates the given strategy.

        Args:
            strategy (str): given strategy

        Returns:
            bool: True if the strategy is valid
        """
        if strategy not in self._possible_strategies["strategies"]:
            raise WrongStrategyError(strategy)
        return True

    def validate_params(self, model_type: str, params: list[dict]) -> bool:
        """Validates the given parameters.

        Args:
            model_type (str): given model type
            params (list[dict]): given parameters
            structure of an example params list:
            [{"name": "param1", type="int" "value": 5},
            {"name": "param2", type="float", "value": 0.3},
            {"name": "param3", type="string", "value": "value"}]

        Returns:
            bool: True if the parameters are valid
        """
        possible_params = self._possible_models_and_params[model_type]
        for param in params:
            if param not in possible_params:
                raise WrongParamError(param["name"], param["value"])
            minimum = possible_params[param]["limits"]["min"]
            maximum = possible_params[param]["limits"]["max"]
            datatype = possible_params[param]["type"]
            values: list = params[param]
            if datatype == "int":
                for item in values:
                    if not isinstance(item, numbers.Integral):
                        raise WrongParamError(param, item)
            elif datatype == "float":
                for item in values:
                    if not isinstance(item, numbers.Real):
                        raise WrongParamError(param, item)
            if not minimum <= np.min(values):
                raise WrongParamError(param, np.min(values))
            if not maximum >= np.max(values):
                raise WrongParamError(param, np.max(values))
        return True

