from datetime import date
from logger import Logger
from bot_module import BotModule

import sys
import datetime
import dateutil.parser as dparser
from threading import Timer


class AlarmModule(BotModule):

    def __init__(self, vk, db) -> None:
        super().__init__(vk, db)
        self.keywords.extend(['будильник', 'таймер', 'напоминание', 'напомни'])
        self.alarms = list()
        self.module_name = 'AlarmModule'
        #Пусть каждый отдельный модуль будет беспокоиться о своих таблицах
        self.db.execute_and_commit('CREATE TABLE IF NOT EXISTS "Alarms" ("id" INTEGER,"user_id" TEXT NOT NULL,"alarm_date" TEXT NOT NULL,"is_repeat" TEXT NOT NULL,PRIMARY KEY("id" AUTOINCREMENT));')

        #Подгружаем из базы данных все ранее заданные будильники, если они не просрочены
        #Инициализируем их и заносим в список
        alarm_list = self.db.get_data('Alarms', '*')
        for row in alarm_list:
            alarm_date = dparser.parse(row[2], fuzzy=True)
            if alarm_date > datetime.datetime.now():
                self.alarms.append(AlarmObject(self.vk, row[1], alarm_date))

    def update(self):
        return super().update()

    def process_request(self, event):
        #Попытка получить из строки пользователя дату и время
        #Если нет даты, то по умолчанию будильник рассчитывается на сегодня/завтра, в зависимости от текущего времени
        #Если нет времени, то по умолчанию уведомление придёт в указанную дату, но в 10 утра
        try:
            alarm_date = dparser.parse(event.text, fuzzy=True)
            if(alarm_date.hour < datetime.datetime.now().hour):
                current_day = alarm_date.day
                alarm_date = alarm_date.replace(day=current_day + 1)

            alarm_object = AlarmObject(self.vk, event.user_id, alarm_date)
            self.db.execute_and_commit('INSERT INTO Alarms(user_id, alarm_date, is_repeat) VALUES ("{0}", "{1}", "N")'.format(event.user_id, alarm_date))

            self.alarms.append(alarm_object)

            self.vk.send_message(event.user_id, 'Будильник будет установлен на ' + str(alarm_date))
        except ValueError as e:
            Logger.log('MODULE WARNING', '{0} \n User text: {1}'.format(sys.exc_info()[0], event.text))
            self.vk.send_message(event.user_id, 'Не нашёл дату в строке :(')
        except:
            Logger.log('MODULE WARNING', '{0} \n User text: {1}'.format(sys.exc_info()[0], event.text))
            self.vk.send_message(event.user_id, 'Упс, что-то пошло не так!')
        

class AlarmObject(object):
    def __init__(self, vk, user_id, alarm_date) -> None:
        self.vk = vk
        self.user_id = user_id
        self.alarm_date = alarm_date

        current_time = datetime.datetime.now()
        delta_in_seconds = (alarm_date - current_time).total_seconds()
        
        self.timer = Timer(delta_in_seconds, self.alarm_action)
        self.timer.start()

    def alarm_action(self):
        self.vk.send_message(self.user_id, 'Напоминалка!')
        