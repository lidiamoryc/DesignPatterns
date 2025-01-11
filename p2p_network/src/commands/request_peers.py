import json
import socket
from p2p_network.src.commands.command import Command
from p2p_network.src.managers.message_manager import MessageManager


class RequestPeersCommand(Command):
    def __init__(self, message_manager: MessageManager):
        self.message_manager = message_manager

    def execute(self, other_peer: tuple[str, int]):
        payload = {"request": "peers"}
        encoded_payload = json.dumps(payload).encode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(other_peer)
            client_socket.send(encoded_payload)
                
            response = json.loads(client_socket.recv(1024).decode())
                    
            peers = [tuple(peer) for peer in response["peers"]] + [other_peer]
            self.message_manager.add_peers(peers)    