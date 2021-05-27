from re import L
import time
from bot_module import BotModule

class EchoModule(BotModule):
    def __init__(self, vk) -> None:
        super().__init__(vk)

    def update(self):
        pass

    def process_request(self, event):
        self.vk.send_message(event, event.text)
        return super().process_request(event)
        



