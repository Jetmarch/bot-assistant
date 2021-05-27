import time
from bot_module import BotModule


class TestModule(BotModule):
    def __init__(self, vk, longpoll) -> None:
        super().__init__(vk, longpoll)
        self.keywords.append("test")
        self.keywords.append("qq")
        self.keywords.append("hello")

    def process_request(self, event):
        random_id = int(round(time.time() * 1000))
        self.vk.messages.send(user_id=event.user_id, message="test module is active!", random_id=random_id)


    def update(self):
        pass