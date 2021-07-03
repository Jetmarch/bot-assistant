import sqlite3
import atexit
from logger import Logger

class DB_Wrapper:
    def __init__(self) -> None:
        self.con = sqlite3.connect('bot_memory.db')
        self.cur = self.con.cursor()
        self.create_database_for_a_bot()
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
            self.execute_and_commit('CREATE TABLE "ModuleStates" ("id" INTEGER NOT NULL UNIQUE,"module" TEXT NOT NULL UNIQUE,"user_id" TEXT NOT NULL,"state" TEXT NOT NULL,PRIMARY KEY("id" AUTOINCREMENT));')
        except Exception as e:
            Logger.log('ERROR', e)
    
    def get_config_value(self, config_field) -> str:
        try:
            res = self.execute('SELECT config_value FROM CONFIG WHERE config_field = "{0}"'.format(config_field))
            return res.fetchone()[0]
        except Exception as e:
            Logger.log('ERROR', e)

    def create_config_value(self, config_field, config_value):
        try:
            self.execute_and_commit('INSERT INTO CONFIG(config_field, config_value) VALUES ("{0}", "{1}")'.format(config_field, config_value))
        except Exception as e:
            Logger.log('ERROR', e)
    
    def set_config_value(self, config_field, config_value):
        try:
            self.execute_and_commit('UPDATE CONFIG SET config_value = "{0}" WHERE config_field = "{1}"'.format(config_value, config_field))
        except Exception as e:
            Logger.log('ERROR', e)

    def get_user_state(self, module, user_id):
        try:
            res = self.execute('SELECT state FROM ModuleState WHERE module = {0} and user_id = {1}'.format(module, user_id))
            return res.fetchall()
        except Exception as e:
            Logger.log('ERROR', e)

    def set_user_state(self, module, user_id, state):
        try:
            self.execute_and_commit('INSERT OR REPLACE INTO ModuleStates (module, user_id, state) VALUES ("{0}", "{1}", "{2}")'.format(module, user_id, state))
        except Exception as e:
            Logger.log('ERROR', e)
