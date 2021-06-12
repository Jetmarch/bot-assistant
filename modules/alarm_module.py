from datetime import date
from logger import Logger
from bot_module import BotModule

import sys
import datetime
import dateutil.parser as dparser
from threading import Timer


class AlarmModule(BotModule):
    alarms = []
    def __init__(self, vk) -> None:
        super().__init__(vk)
        self.keywords.extend(['будильник', 'таймер', 'напоминание', 'напомни'])
        #Подгружаем из базы данных все ранее заданные будильники, если они не просрочены
        #Инициализируем их и заносим в список

    
    def update(self):
        return super().update()

    #Метод, срабатывающий по таймеру
    def alarm_action(self, alarm_object):
        #Посылаем напоминание пользователю
        self.vk.send_message(alarm_object.vk_event, 'Напоминалка!')

    def process_request(self, event):
        #Попытка получить из строки пользователя дату и время
        #Если нет даты, то по умолчанию будильник рассчитывается на сегодня/завтра, в зависимости от текущего времени
        #Если нет времени, то по умолчанию уведомление придёт в указанную дату, но в 10 утра
        try:
            alarm_date = dparser.parse(event.text, fuzzy=True)
            if(alarm_date.hour < datetime.datetime.now().hour):
                current_day = alarm_date.day
                alarm_date = alarm_date.replace(day=current_day + 1)

            alarm_object = AlarmObject(event, alarm_date)

            self.vk.send_message(event.user_id, 'Будильник будет установлен на ' + str(alarm_date))
        except:
            Logger.log('MODULE WARNING', '{0} \n User text: {1}'.format(sys.exc_info()[0], event.text))
            self.vk.send_message(event.user_id, 'Дата для будильника в строке не найдена')
        

class AlarmObject:
    def __init__(self, vk_event, alarm_date) -> None:
        self.user_id = vk_event.user_id
        self.alarm_date = alarm_date

        current_time = datetime.datetime.now()
        delta_in_seconds = (alarm_date - current_time).total_seconds()
        