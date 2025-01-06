# import random
# from p2p_network.src.strategies.base_strategy import BaseStrategy
# # TODO: delete?
# class RandomCombinationSearcher(BaseStrategy):
#     """A class for a random search of the best combination of parameters.
#
#     Methods:
#         calculate_new_params: calculate the new parameters based on the
#         top k parameters and the number of combinations
#     """
#
#     def __init__(self, possible_models_and_params: dict):
#         self.possible_models_and_params = possible_models_and_params
#
#     def calculate_new_params(self, top_k_params: list[dict], comb_num: int) -> list[dict]:
#         """Calculate the new parameters based on the top k parameters and the number of combinations
#
#         Args:
#             top_k_params (list[dict]): top k sets of already used parameters
#             comb_num (int): How many combinations should the function return
#
#         Returns:
#             list[dict]: list of comb_num sets of new parameters
#         """
#         new_params = []
#         for _ in range(comb_num):
#             new_params.append(self._generate_random_params())
#
#         return new_params
#
#     def _generate_random_params(self) -> dict:
#         """Generate random parameters based on the possible models and their parameters
#
#         Returns:
#             dict: random set of parameters
#         """
#         random_params = {}
#         for param in self.possible_models_and_params:
#             if param["type"] == "int":
#                 random_params[param["name"]] = random.randint(param["values"]["min"],
#                                                               param["values"]["max"])
#             elif param["type"] == "float":
#                 random_params[param["name"]] = random.uniform(param["values"]["min"],
#                                                               param["values"]["max"])
#             elif param["type"] == "string":
#                 random_params[param["name"]] = random.choice(param["values"])
#         return random_params
