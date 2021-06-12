import threading
import datetime

def test():
    print('test')

user_date = datetime.datetime(2021, 6, 12, 21, 35, 0, 0)
current_date = datetime.datetime.now()
delta = (user_date - current_date).total_seconds()


threading.Timer(delta, test).start()
threading.Timer(2.0, test).start()

