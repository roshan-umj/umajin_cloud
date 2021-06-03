import logging
import time


class Logger:

    def __init__(self, logger, file_level=logging.INFO):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        format = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] [%(levelname)s] %(message)s')

        curr_time = time.strftime("%Y-%m-%d")
        self.LogFileName = "logs\\log" + curr_time + '.txt'
        # "a" to append the logs in same file, "w" to generate new logs and delete old one
        fh = logging.FileHandler(self.LogFileName, mode="w+")
        fh.setFormatter(format)
        fh.setLevel(file_level)
        self.logger.addHandler(fh)
