


class Logger:

    @staticmethod
    def log(logtype, *args):
        log_file = open('log.txt', 'a+')
        result_string = ""
        for arg in args:
            result_string += arg

        print(" [" + logtype + "] " + result_string)
        log_file.write(" [" + logtype + "] " + result_string + "\n")