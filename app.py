import argparse
import sys
from p2p_network.src.user_interface.user_interface_implementation import UserInterface
import numpy as np


def main():
    parser = argparse.ArgumentParser(description="P2P Node with Peer Discovery")
    parser.add_argument('--port', type=int, required=True, help="Port for this node to listen on")
    parser.add_argument('--other', type=int, required=False, help="Other argument")
    args = parser.parse_args()
    node = UserInterface("RandomForest", {
            "n_estimators": list(np.arange(10, 15, 1, dtype=int)),
            "max_depth": list(np.arange(10, 50, 1, dtype=int)),
            "min_samples_split": list(np.arange(2, 5, 1, dtype=int)),
        }, "random", args.port, args.other)
    node.start_training()

    while True:
        user_input = input("Press 'q' to terminate: \n").strip().lower()
        if user_input == 'q':
            print("Termination key 'q' pressed.")
            node.stop_training()
            sys.exit(0)

if __name__ == '__main__':
    main()