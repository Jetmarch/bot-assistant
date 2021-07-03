from re import L
import time
from bot_module import BotModule

class EchoModule(BotModule):
    def __init__(self, vk, db) -> None:
        super().__init__(vk, db)
        self.module_name = 'EchoModule'

    def update(self):
        pass

    def process_request(self, event):
        self.vk.send_message(event.user_id, event.text)
        return super().process_request(event)
        



