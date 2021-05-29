


class Logger:

    @staticmethod
    def log(logtype, message):
        log_file = open('log.txt', 'a+')

        print(" [" + logtype + "] " + str(message))
        log_file.write(" [" + logtype + "] " + str(message) + "\n")