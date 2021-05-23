from modules.echo_module import EchoModule

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Application:
    modules = []
    

    def __init__(self) -> None:
        file = open("token.txt")
        token_from_file = file.read()
        file.close()

        #Инициализируем vk_api
        vk_session = vk_api.VkApi(token=token_from_file)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

        modules = list()
        #Инициализация каждого нового модуля должна быть здесь
        #modules.append(EchoModule(self.vk, self.longpoll))

        self.default_module = EchoModule(self.vk, self.longpoll)


    def launch_bot(self) -> None:
        #Слушаем longpoll
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                if event.from_user:
                    
                    #TODO: обработка запроса пользователя. Прогоняемся по всем модулям бота, пока не находим тот, который готов обработать запрос
                    is_request_processed = False
                    for module in self.modules:
                        if module.is_keyword_exists_in_module(""" Keyword here """) == True:
                            #Вызываем метод для обработки запроса пользователя, передавая полную строку в качестве аргумента
                            is_request_processed = True
                            break
                        
                    if is_request_processed == False:
                        self.default_module.process_request(event)