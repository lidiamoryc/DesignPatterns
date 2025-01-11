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

            if not data:
                return
            
            decoded_data = json.loads(data.decode())
            print("Received data:", decoded_data)
                 
            if "request" in decoded_data and decoded_data["request"] == "peers":
                payload = {"peers": self.peers}
                encoded_payload = json.dumps(payload).encode()
                connection.send(encoded_payload)
            elif "register_peer" in decoded_data:
                new_peer = tuple(decoded_data["register_peer"])
                if new_peer in self.peers or new_peer == self.get_current_node():
                    return
                self.peers.append(new_peer)    
            elif "remove_peer" in decoded_data:
                removed_peer = tuple(decoded_data["remove_peer"])
                if removed_peer not in self.peers:
                    return
                self.peers.remove(removed_peer)
            
    def get_current_node(self) -> tuple[str, int]:
        return (LOCALHOST, self.socket_port)
    
    def join_network(self, other_peer: tuple[str, int]) -> None:
        payload = {"request": "peers"}
        encoded_payload = json.dumps(payload).encode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(other_peer)
            client_socket.send(encoded_payload)
                
            response = json.loads(client_socket.recv(1024).decode())
            self.peers = [tuple(peer) for peer in response["peers"]] + [other_peer]
        
        payload = {"register_peer": self.get_current_node()}
        encoded_payload = json.dumps(payload).encode()
        self.notify_peers(encoded_payload)
    
    def exit_network(self) -> None:
        self.is_running = False
        self.messaging_socket.close()

        payload = {"remove_peer": self.get_current_node()}
        encoded_payload = json.dumps(payload).encode()
        self.notify_peers(encoded_payload)

    def notify_peers(self, payload: dict) -> None:
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(payload)
            except ConnectionRefusedError:
                print(f"Failed to notify peer {peer}.")               