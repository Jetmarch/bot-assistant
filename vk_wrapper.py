import time
import vk_api
from vk_api.longpoll import VkLongPoll

class VKWrapper:
    def __init__(self, token) -> None:
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

    def send_message(self, event, text):
        random_id = int(round(time.time() * 1000))
        self.vk.messages.send(user_id=event.user_id, message=event.text, random_id=random_id)