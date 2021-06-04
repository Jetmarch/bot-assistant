from datetime import date
from bot_module import BotModule

import datetime
import dateutil.parser as dparser


class AlarmModule(BotModule):
    def __init__(self, vk) -> None:
        super().__init__(vk)
        self.keywords.extend(['будильник', 'таймер', 'напоминание', 'напомни'])

    
    def update(self):
        return super().update()


    def process_request(self, event):
        #Попытка получить из строки пользователя дату и время
        #Если нет даты, то по умолчанию будильник рассчитывается на сегодня/завтра, в зависимости от текущего времени
        #Если нет времени, то по умолчанию уведомление придёт в указанную дату, но в 10 утра
        alarm_date = dparser.parse(event.text, fuzzy=True)
        #if(alarm_date.time < datetime.datetime.now()):
        #    pass

        self.vk.send_message(event, 'Будильник будет установлен на ' + str(alarm_date))
        

