from modules.echo_module import EchoModule
import time
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

        #Инициализация каждого нового модуля должна быть здесь
        modules = EchoModule()


    def launch_bot(self) -> None:
        #Слушаем longpoll
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                if event.from_user:
                    random_id = int(round(time.time() * 1000))
                    #TODO: обработка запроса пользователя. Прогоняемся по всем модулям бота, пока не находим тот, который готов обработать запрос
                    self.vk.messages.send(user_id=event.user_id, message=event.text, random_id=random_id)