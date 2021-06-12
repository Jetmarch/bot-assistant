


class Logger:

    @staticmethod
    def log(logtype, message):
        try:
            log_file = open('log.txt', 'a+', encoding='utf-8')
            print('[{0}] {1}\n'.format(logtype, str(message)))
            log_file.write('[{0}] {1}\n'.format(logtype, str(message)))
        except Exception as e:
            print('[ERROR] Logger failed. Text: {0}\n Exception: {1}'.format(message, str(e)))