import socket
import threading
import argparse
import json
import time

class NetworkNode:
    peers: list[tuple[str, int]]

    server_port: int
    initial_peer_port: int

    def __init__(self, server_port: int, initial_peer_port: int):
        self.peers = []

        self.server_port = server_port
        self.initial_peer_port = initial_peer_port if initial_peer_port is not None else None
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.running = True

    def _get_hostname(self, port: int) -> tuple[str, int]:
        return ('127.0.0.1', port)


    def start_server(self):
        self.server_socket.bind(self._get_hostname(self.server_port))
        self.server_socket.listen()
        self.connect_to_peer()

        print(f"Node listening on port {self.server_port}")
        
        while self.running:
            conn, _ = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn,)).start()

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
                    
                    if new_peer not in self.peers and new_peer != self._get_hostname(self.server_port):
                        self.peers.append(new_peer)
                        print(f"New peer added: {new_peer}")

    def connect_to_peer(self):
        if self.initial_peer_port:
            peer = self._get_hostname(self.initial_peer_port)
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(json.dumps({"request": "peers"}).encode())
                    response = json.loads(client_socket.recv(1024).decode())
                    
                    self.peers = [tuple(peer) for peer in response["peers"]]
                    self.peers.append(peer)
                    
                    print(f"Discovered peers: {self.peers}")
                    
                    self.connect_to_discovered_peers()
            except ConnectionRefusedError:
                print(f"Unable to connect to peer {peer}")

    def connect_to_discovered_peers(self):
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(json.dumps({"new_peer": self._get_hostname(self.server_port)}).encode())
                    
                    print(f"Notified {peer} of this node.")
            except ConnectionRefusedError:
                print(f"Failed to connect to discovered peer {peer}.")
    
    def send_message(self, message):
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(peer)
                    client_socket.send(json.dumps({"message": message}).encode())
            except ConnectionRefusedError:
                print(f"Failed to send message to peer {peer}.")

    def stop(self):
        self.running = False
        self.server_socket.close()

def main():
    parser = argparse.ArgumentParser(description="P2P Node with Peer Discovery")
    parser.add_argument('--port', type=int, required=True, help="Port for this node to listen on")
    parser.add_argument('--peer-port', type=int, help="Port of a peer node to connect to (optional)")
    args = parser.parse_args()

    node = Node(server_port=args.port, initial_peer_port=args.peer_port)

    server_thread = threading.Thread(target=node.start_server, daemon=True)
    server_thread.start()

    if args.peer_port:
        node.connect_to_peer()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Shutting down node...")
        node.stop()

if __name__ == "__main__":
    main()
