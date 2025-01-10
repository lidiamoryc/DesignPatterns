import argparse
from p2p_network.src.user_interface.user_interface_implementation import UserInterface



def main():
    parser = argparse.ArgumentParser(description="P2P Node with Peer Discovery")
    parser.add_argument('--port', type=int, required=True, help="Port for this node to listen on")
    parser.add_argument('--other', type=int, required=False, help="Other argument")
    args = parser.parse_args()
    node = UserInterface("model_type", [{"name": "param1", "type": "int", "value": 5}], args.port, args.other)
    node.start_training()


if __name__ == '__main__':
    main()