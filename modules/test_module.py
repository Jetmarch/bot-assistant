import time
from bot_module import BotModule


class TestModule(BotModule):
    def __init__(self, vk, db) -> None:
        super().__init__(vk, db)
        self.module_name = 'TestModule'
        self.keywords.append("test")
        self.keywords.append("qq")
        self.keywords.append("hello")

    def process_request(self, event):
        self.vk.send_message(event.user_id, "test module is active!")

    def update(self):
        pass