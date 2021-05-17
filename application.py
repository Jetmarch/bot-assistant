import requests
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Application:
    def __init__(self) -> None:
        pass


    def launch_bot(self) -> None:
        file = open("token.txt")
        token_from_file = file.read()
        file.close()

        vk_session = vk_api.VkApi(token=token_from_file)

        longpoll = VkLongPoll(vk_session)
        vk = vk_session.get_api()
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            #listen longpoll
                if event.from_user:
                    random_id = int(round(time.time() * 1000))
                    vk.messages.send(user_id=event.user_id, message=event.text, random_id=random_id)