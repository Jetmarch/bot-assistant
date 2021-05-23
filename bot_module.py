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


    def is_keyword_exists_in_module(self) -> bool:
        #Перебираем все keywords. Если находим, то возвращаем true
        #Пока ещё не придумал лаконичный способ передачи функционала vk_api в каждый модуль
        #Поэтому это простая заглушка на данный момент
        return False


