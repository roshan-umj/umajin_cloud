import logging
import time


class Logger:

    def __init__(self, logger, file_level=logging.INFO):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        format = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] [%(levelname)s] %(message)s')

        curr_time = time.strftime("%Y-%m-%d")
        self.LogFileName = "logs/log" + curr_time + '.txt'
        # "a" to append the logs in same file, "w" to generate new logs and delete old one
        file_handler = logging.FileHandler(self.LogFileName, mode="w+")
        file_handler.setFormatter(format)
        file_handler.setLevel(file_level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(format)


        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
