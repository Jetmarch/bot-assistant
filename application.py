import asyncio, sys
import os
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
        #token_from_file = self.db.get_config_value('token')
        token_from_env = os.environ.get('TOKEN', None)
        self.vk = VKWrapper(token_from_env)

        self.modules = list()
        # Инициализация каждого нового модуля должна быть здесь
        self.modules.append(TestModule(self.vk, self.db))
        self.modules.append(AlarmModule(self.vk, self.db))
        self.modules.append(AlchemyHelperModule(self.vk, self.db))
        self.default_module = EchoModule(self.vk, self.db)
        

    async def launch_bot(self) -> None:
        try:
            # Слушаем longpoll
            for event in self.vk.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.from_user:

                        #TODO: проверка на незавершенные действия от пользователя.
                        #Если в таблице с состояниями модулей есть запись с user_id пользователя
                        #То вызываем тот модуль, состояние которого не было закрыто пользователем
                        #Каждый модуль должен быть ответственен за закрытие состояния

                        module_name_with_unfinished_state = self.db.get_unfinished_state_by_user_id(event.user_id)
                        if module_name_with_unfinished_state:
                            for module in self.modules:
                                if module.module_name == module_name_with_unfinished_state:
                                    module.process_request(event)
                        else:
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
