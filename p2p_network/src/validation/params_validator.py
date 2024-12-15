class WrongParamError(Exception):
    """Raised when some parameter are not valid."""

    def __init__(self, param_name: str, param_value: str):
        super().__init__(f"Parameter {param_name} with value {param_value} is not valid.")

class WrongModelTypeError(Exception):
    """Raised when the model type is not valid."""

    def __init__(self, model_type: str):
        super().__init__(f"Model type {model_type} is not valid.")



class ParamsValidator:
    """
    A class that validates the parameters for the node.
    """
    def __init__(self, possible_models_and_params: dict):
        self.possible_models_and_params: dict = possible_models_and_params
    
    def validate_params(self, params: list[dict]) -> bool:
        """Validates the given parameters.

        Args:
            params (list[dict]): given parameters
            structure of an example params list:
            [{"name": "param1", type="int" "value": 5},
            {"name": "param2", type="float", "value": 0.3},
            {"name": "param3", type="string", "value": "value"}]

        Returns:
            bool: True if the parameters are valid
        """
        for param in params:
            if param["name"] not in self.possible_models_and_params[param["type"]]:
                raise WrongParamError(param["name"], param["value"])
        return True
    
    def validate_model_type(self, model_type: str) -> bool:
        """Validates the given model type.

        Args:
            model_type (str): given model type

        Returns:
            bool: True if the model type is valid
        """
        if model_type not in self.possible_models_and_params.keys():
            raise WrongModelTypeError(model_type)
        return True