import sqlite3
import atexit
from logger import Logger

class DB_Wrapper:
    def __init__(self) -> None:
        self.con = sqlite3.connect('bot_memory.db')
        self.cur = self.con.cursor()
        atexit.register(self.cleanup)
    
    def cleanup(self):
        if self.con:
            self.con.commit()
            self.cur.close()
            self.con.close()

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
    
    def get_data(self, table, columns):
        query = 'SELECT {0} FROM {1}'.format(columns, table)
        res = self.cur.execute(query)
        return res.fetchall()

    def create_database_for_a_bot(self):
        try:
            self.execute_and_commit('CREATE TABLE IF NOT EXISTS CONFIG(id integer PRIMARY KEY AUTOINCREMENT, config_field text NOT NULL, config_value text)')
        except Exception as e:
            Logger.log('ERROR', e)
    
    def get_config_value(self, config_field) -> str:
        try:
            res = self.execute('SELECT config_value FROM CONFIG WHERE config_field = "' + str(config_field) + '"')
            return res.fetchone()[0]
        except Exception as e:
            Logger.log('ERROR', e)
