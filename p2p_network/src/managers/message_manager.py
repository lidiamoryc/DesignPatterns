import json
import socket
import threading
from p2p_network.src.node.node import Node
from p2p_network.src.logger.logger import Logger

LOCALHOST = '127.0.0.1'

class MessageManager:
    peers: list[tuple[str, int]]
    socket_port: int
    messaging_socket: socket.socket
    is_running: bool

    def __init__(self, node: Node, socket_port: int, other_peer_port: int = None ):
        self.peers = []

        self.socket_port = socket_port
        self.messaging_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.other_peer_port = other_peer_port
        self.node = node
        self.logger_path = "p2p_network/src/logger/log.text"
        self.logger = Logger(self.logger_path)
        

        self.is_running = False

    def initialize(self):
        try:
            self.messaging_socket.bind((LOCALHOST, self.socket_port))
            self.messaging_socket.listen()
        except OSError as e:
            if e.errno == 10048:
                raise RuntimeError(f"Port {self.socket_port} is already in use.") from e


        self.is_running = True

        while self.is_running:
            try:
                client, _ = self.messaging_socket.accept()
                threading.Thread(target=self.handle_client, args=(client, )).start()
            except socket.error:
                break
        
    def handle_client(self, connection: socket.socket):
        with connection:
            data = connection.recv(65536)

            if not data:
                return
            
            decoded_data = json.loads(data.decode())

            if "results" in decoded_data:
                results = decoded_data["results"]
                self.node.new_results(results) 
            if "request" in decoded_data and decoded_data["request"] == "peers":
                payload = {"peers": self.peers, "records": self.node.get_current_records()}
                encoded_payload = json.dumps(payload).encode()
                    
                json_length = len(encoded_payload)
                connection.sendall(json_length.to_bytes(4, 'big'))
                connection.sendall(encoded_payload)

                self.logger.log(self.node.node_id, "Received request to discover peers.")
            elif "register_peer" in decoded_data:
                new_peer = tuple(decoded_data["register_peer"])
                if new_peer in self.peers or new_peer == self.get_current_node():
                    return
                self.peers.append(new_peer)
                self.logger.log(self.node.node_id, f"Registered new peer {new_peer}.")
            elif "remove_peer" in decoded_data:
                removed_peer = tuple(decoded_data["remove_peer"])
                if removed_peer not in self.peers:
                    return
                self.peers.remove(removed_peer)
                self.logger.log(self.node.node_id, f"Removed peer {removed_peer}")  
            
    def get_current_node(self) -> tuple[str, int]:
        return (LOCALHOST, self.socket_port)
    
    def join_network(self) -> None:
        payload = {"request": "peers"}
        encoded_payload = json.dumps(payload).encode()

        other_peer = (LOCALHOST, self.other_peer_port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(other_peer)
            client_socket.send(encoded_payload)

            json_length_bytes = client_socket.recv(4)
            if not json_length_bytes:
                return None
            
            json_length = int.from_bytes(json_length_bytes, 'big')
            
            json_bytes = bytearray()
            while len(json_bytes) < json_length:
                chunk = client_socket.recv(min(4096, json_length - len(json_bytes)))
                if not chunk:
                    raise ConnectionError("Connection lost while receiving data.")
                
                json_bytes.extend(chunk)
            
            response = json.loads(json_bytes.decode())
            self.peers = [tuple(peer) for peer in response["peers"]] + [other_peer]
            self.node.store_computed_records(response["records"])
        
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

    def check_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((LOCALHOST , self.socket_port))
        if result == 0:
            sock.close()
            return False
        else:
            sock.close()  
            return True
    
    def check_other_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((LOCALHOST , self.other_peer_port))
        if result != 0:
            sock.close()
            return False
        else:
            sock.close()  
            return True
    
                     