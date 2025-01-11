import json
import socket
from p2p_network.src.commands.command import Command
from p2p_network.src.managers.message_manager import MessageManager


class ExitNetworkCommand(Command):
    def __init__(self, message_manager: MessageManager):
        self.message_manager = message_manager

    def execute(self):
        self.message_manager.stop_listening()
        exiting_peer = self.message_manager.get_current_node()

        payload = {"peer_removal": exiting_peer}
        encoded_payload = json.dumps(payload).encode()

        known_peers = self.message_manager.get_peers()

        for peer in known_peers:  
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(encoded_payload)
            except ConnectionRefusedError:
                print(f"Failed to notify peer {peer} about the removal of {exiting_peer}.")   