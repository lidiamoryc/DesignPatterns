
import json
from p2p_network.src.commands.command import Command
from p2p_network.src.managers.message_manager import MessageManager

class NotifyAboutResultsCommand(Command):
    def __init__(self, message_manager: MessageManager):
        self.message_manager = message_manager

    def execute(self, results: dict[str, any]):
        payload = {"results": f"{results}"}
        encoded_payload = json.dumps(payload).encode()
        self.message_manager.notify_peers(encoded_payload)
                    