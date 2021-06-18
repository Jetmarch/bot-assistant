import asyncio, sys
from os import system
from db_wrapper import DB_Wrapper

from logger import Logger
from modules.echo_module import EchoModule
from modules.test_module import TestModule
from modules.alarm_module import AlarmModule
from modules.alchemy_helper_module import AlchemyHelperModule
from vk_wrapper import VKWrapper
from vk_api.longpoll import VkEventType


class Application:
    modules = []

    def __init__(self) -> None:
        self.db = DB_Wrapper()
        token_from_file = self.db.get_config_value('token')

        self.vk = VKWrapper(token_from_file)

        self.modules = list()
        # Инициализация каждого нового модуля должна быть здесь
        self.modules.append(TestModule(self.vk))
        self.modules.append(AlarmModule(self.vk))
        self.modules.append(AlchemyHelperModule(self.vk))
        self.default_module = EchoModule(self.vk)
        

    async def launch_bot(self) -> None:
        try:
            # Слушаем longpoll
            for event in self.vk.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:
                        is_request_processed = False
                        for module in self.modules:
                            if module.is_keyword_exists_in_module(event.text.lower()) == True:
                                # Вызываем метод для обработки запроса пользователя, передавая событие в качестве аргумента
                                module.process_request(event)
                                is_request_processed = True
                                break

                        if is_request_processed == False:
                            self.default_module.process_request(event)
        except Exception as e:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            filename = exc_traceback.tb_frame.f_code.co_filename
            line_number = exc_traceback.tb_lineno
            Logger.log('ERROR', str(e) + '\nFile: ' + str(filename) + '\nLine: ' + str(line_number) )
