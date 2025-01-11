
import json
import socket
from p2p_network.src.commands.command import Command
from p2p_network.src.managers.message_manager import MessageManager


class NotifyAboutResultsCommand(Command):
    def __init__(self, message_manager: MessageManager):
        self.message_manager = message_manager

    def execute(self, params: str, score: int | float):
        payload = {"results": f"params: {params} -> score: {score}"}
        encoded_payload = json.dumps(payload).encode()

        known_peers = self.message_manager.get_peers()

        for peer in known_peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(encoded_payload)
            except ConnectionRefusedError:
                print(f"Failed to notify peer {peer} about results.")       
                    