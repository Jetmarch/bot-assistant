from abc import abstractmethod
from abc import ABC


"""
Базовый класс модуля для бота.
Каждый модуль должен наследовать его.
"""
class BotModule(ABC):
    keywords = []


    def __init__(self, vk, longpoll) -> None:
        self.vk = vk
        self.longpoll = longpoll
        self.keywords = list()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def process_request(self, event):
        pass


    def is_keyword_exists_in_module(self, user_text) -> bool:
        for word in self.keywords:
            if word in user_text:
                return True

        return False


