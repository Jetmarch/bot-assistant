from re import L
import time
from bot_module import BotModule

class EchoModule(BotModule):
    def __init__(self, vk, longpoll) -> None:
        super().__init__(vk, longpoll)

    def update(self):
        pass

    def process_request(self, event):
        random_id = int(round(time.time() * 1000))
        self.vk.messages.send(user_id=event.user_id, message=event.text, random_id=random_id)
        return super().process_request(event)
        



