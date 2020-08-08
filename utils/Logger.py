import logging

class Logger:
    """
    Permet d'afficher bien les logs
    """


    # create logger
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


    @classmethod
    def debug(self, arg):
        self.logger.debug(arg)

    @classmethod
    def info(self, arg):
        self.logger.info(arg)

    @classmethod
    def error(self, arg):
        self.logger.error(arg)

    @classmethod
    def warn(self, arg):
        self.logger.warn(arg)
