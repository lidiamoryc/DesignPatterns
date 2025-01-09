import json
import socket
import threading

LOCALHOST = '127.0.0.1'

class MessageManager:
    peers: list[tuple[str, int]]
    socket_port: int
    other_peer_port: int
    messaging_socket: socket.socket
    is_running: bool

    def __init__(self, socket_port: int, other_peer_port: int):
        self.peers = []

        self.socket_port = socket_port
        self.other_peer_port = other_peer_port if other_peer_port is not None else None
        self.messaging_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.is_running = False

    def initialize(self):
        self.messaging_socket.bind((LOCALHOST, self.socket_port))
        self.messaging_socket.listen()

        self.is_running = True

        self.connect_to_other_peer()

        while self.is_running:
            client, _ = self.messaging_socket.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, connection: socket.socket):
        with connection:
            data = connection.recv(1024)
            
            if data:
                message = json.loads(data.decode())
                print(f"Received message: {message}")
                
                if "request" in message and message["request"] == "peers":
                    connection.send(json.dumps({"peers": self.peers}).encode())
                elif "new_peer" in message:
                    new_peer = tuple(message["new_peer"])
                    
                    if new_peer not in self.peers and new_peer != (LOCALHOST, self.socket_port):
                        self.peers.append(new_peer)

    def connect_to_other_peer(self):
        if self.other_peer_port:
            peer = (LOCALHOST, self.other_peer_port)
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(json.dumps({"request": "peers"}).encode())
                    response = json.loads(client_socket.recv(1024).decode())
                    
                    self.peers = [tuple(peer) for peer in response["peers"]]
                    self.peers.append(peer)                
                    self.connect_to_discovered_peers()
            except ConnectionRefusedError:
                print(f"Unable to connect to peer {peer}")

    def connect_to_discovered_peers(self):
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(json.dumps({"new_peer": (LOCALHOST, self.socket_port)}).encode())
            except ConnectionRefusedError:
                print(f"Failed to connect to discovered peer {peer}.")
    
    def publish_message(self, message: str):
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(json.dumps({"message": message}).encode())
            except ConnectionRefusedError:
                print(f"Failed to send message to peer {peer}.")

        