import time
from bot_module import BotModule


class TestModule(BotModule):
    def __init__(self, vk) -> None:
        super().__init__(vk)
        self.keywords.append("test")
        self.keywords.append("qq")
        self.keywords.append("hello")

    def process_request(self, event):
        self.vk.send_message(event, "test module is active!")

    def update(self):
        pass