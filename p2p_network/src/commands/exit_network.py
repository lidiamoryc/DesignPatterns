import json
from p2p_network.src.commands.command import Command
from p2p_network.src.managers.message_manager import MessageManager


class ExitNetworkCommand(Command):
    def __init__(self, message_manager: MessageManager):
        self.message_manager = message_manager

    def execute(self):
        self.message_manager.exit_network()