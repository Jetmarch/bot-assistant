import sqlite3
from logger import Logger

class DB_Wrapper:
    def __init__(self) -> None:
        self.con = sqlite3.connect('bot_memory.db')
        self.cur = self.con.cursor()

    #TODO: Придумать способ не допустить инъекцию
    def execute_and_commit(self, query):
        try:
            res = self.cur.execute(query)
            self.con.commit()
            return res
        except Exception as e:
            Logger.log('ERROR', e)

    def execute(self, query):
        try:
            res = self.cur.execute(query)
            return res
        except Exception as e:
            Logger.log('ERROR', e)