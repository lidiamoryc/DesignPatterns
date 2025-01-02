class WrongParamError(ValueError):
    """Raised when some parameter are not valid."""

    def __init__(self, param_name: str, param_value: str):
        super().__init__(f"Parameter {param_name} with value {param_value} is not valid.")

class WrongModelTypeError(ValueError):
    """Raised when the model type is not valid."""

    def __init__(self, model_type: str):
        super().__init__(f"Model type {model_type} is not valid.")



class ParamsValidator:
    """
    A class that validates the parameters for the node.

    Args:
        possible_models_and_params (dict): The possible models and their parameters.
        Example structure of the _possible_models_and_params:
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

    Methods:
        validate_model_type: validates the given model type
        validate_params: validates the given parameters
    """
    def __init__(self, possible_models_and_params: dict):
        self._possible_models_and_params: dict = possible_models_and_params

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
            self._validate_param_name(param["name"], param["value"], possible_params)
            param_conditions = self._get_param_conditions(param["name"], possible_params)
            self._validate_param_type(param["name"], param["value"], param_conditions["type"])
            self._validate_param_values(param["name"], param["value"], param_conditions.get("values"))
        return True


    def _validate_param_name(self, name: str, value, possible_params: list[dict]) -> None:
        """
        Validates if the parameter name exists in the possible parameters.
        """
        if not any(x["name"] == name for x in possible_params):
            raise WrongParamError(name, value)


    def _get_param_conditions(self, name: str, possible_params: list[dict]) -> dict:
        """
        Retrieves the conditions for a specific parameter name.
        """
        for param in possible_params:
            if param["name"] == name:
                return param
        raise ValueError(f"Parameter conditions not found for {name}")


    def _validate_param_type(self, name: str, value, expected_type: str) -> None:
        """
        Validates the type of the parameter value.
        """
        if expected_type == "string":
            if not isinstance(value, str):
                raise WrongParamError(name, value)
        elif expected_type == "int":
            if not (isinstance(value, int) or (isinstance(value, float) and value.is_integer())):
                raise WrongParamError(name, value)
        elif expected_type == "float":
            if not isinstance(value, float):
                raise WrongParamError(name, value)
        else:
            raise ValueError(f"Unsupported parameter type: {expected_type}")


    def _validate_param_values(self, name: str, value, values) -> None:
        """
        Validates the parameter value against a predefined set of possible values or a range.
        """
        if values is None:
            return
        if isinstance(values, list):
            if value not in values:
                raise WrongParamError(name, value)
        elif isinstance(values, dict):
            if not values["min"] <= value <= values["max"]:
                raise WrongParamError(name, value)
        else:
            raise ValueError(f"Unsupported values type: {type(values)}")
