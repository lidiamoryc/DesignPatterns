import json
import socket
import threading

LOCALHOST = '127.0.0.1'

class MessageManager:
    peers: list[tuple[str, int]]
    socket_port: int
    messaging_socket: socket.socket
    is_running: bool

    def __init__(self, socket_port: int):
        self.peers = []

        self.socket_port = socket_port
        self.messaging_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.is_running = False

    def initialize(self):
        self.messaging_socket.bind((LOCALHOST, self.socket_port))
        self.messaging_socket.listen()

        self.is_running = True

        while self.is_running:
            try:
                client, _ = self.messaging_socket.accept()
                threading.Thread(target=self.handle_client, args=(client,)).start()
            except socket.error:
                break
        
    def handle_client(self, connection: socket.socket):
        with connection:
            data = connection.recv(1024)
            
            if data:
                message = json.loads(data.decode())
                print(f"Received message: {message}")
                
                if "request" in message and message["request"] == "peers":
                    payload = {"peers": self.peers}
                    encoded_payload = json.dumps(payload).encode()
                    connection.send(encoded_payload)
                elif "new_peer" in message:
                    new_peer = tuple(message["new_peer"])
                    current_node = self.get_current_node()
                    if new_peer not in self.peers and new_peer != current_node:
                        self.peers.append(new_peer)
                elif "peer_removal" in message:
                        removed_peer = tuple(message["peer_removal"])
                        if removed_peer in self.peers:
                            self.peers.remove(removed_peer)
                            print(f"Peer {removed_peer} has been removed.")
            
    def add_peers(self, peers: list[tuple[str, int]]):
        for peer in peers:
            self.peers.append(peer)

    def get_peers(self) -> list[tuple[str, int]]:
        return self.peers

    def get_current_node(self) -> tuple[str, int]:
        return (LOCALHOST, self.socket_port)
    
    def stop_listening(self):
        self.is_running = False
        self.messaging_socket.close()        