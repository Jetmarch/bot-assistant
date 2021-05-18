from abc import abstractmethod
from abc import ABC


"""
Базовый класс модуля для бота.
Каждый модуль должен наследовать его.
Это должно исключить случаи отсутствия реализации основных методов
"""
class BotModule(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def update(self):
        pass


