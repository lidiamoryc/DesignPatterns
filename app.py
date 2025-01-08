from p2p_network.src.user_interface.user_interface_implementation import UserInterface


def main():
    node = UserInterface("model_type", [{"name": "param1", "type": "int", "value": 5}])
    node.start_training()











if __name__ == '__main__':
    main()