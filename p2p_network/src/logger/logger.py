from p2p_network.src.singleton_meta import SingletonMeta
from datetime import datetime

class Logger(metaclass=SingletonMeta):
    def __init__(self, log_file: str):
        self.log_file = log_file
    
    def log(self, node_id: str, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{node_id}]: {message}\n"

        with open(self.log_file, 'a') as file:
            file.write(log_entry)