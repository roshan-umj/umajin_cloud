import logging
import os
from utilities import config_reader



class Logger:

    def __init__(self, logger_name, file_level=logging.DEBUG):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(file_level)

        # create logs folder if doesn't exist in the root
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # get the name of the log file form the configurations file
        log_file_name = config_reader.read(section="settings", key="log_file_name")

        log_line_format = logging.Formatter('%(name)s [%(levelname)s] %(message)s')

        # file handler is for the log file stored in 'logs' folder
        file_handler = logging.FileHandler(filename=f"logs/{log_file_name}", mode="a")
        file_handler.setFormatter(log_line_format)
        file_handler.setLevel(logging.DEBUG)

        # stream handler is for the console/jenkins logs
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_line_format)
        stream_handler.setLevel(logging.DEBUG)  # change the logging level to logging.WARNING if you want only
        # errors/warning in the console/jenkins logs

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def debug(self, log_message, driver=None):
        if driver:
            self.logger.debug(msg=f"{driver.name}: {log_message}")
        else:
            self.logger.debug(msg=log_message)

    def info(self, log_message, driver=None):
        if driver:
            self.logger.info(msg=f"{driver.name}: {log_message}")
        else:
            self.logger.info(msg=log_message)

    def warning(self, log_message, driver=None):
        if driver:
            self.logger.warning(msg=f"{driver.name}: {log_message}")
        else:
            self.logger.warning(msg=log_message)

    def error(self, log_message, driver=None):
        if driver:
            self.logger.error(msg=f"{driver.name}: {log_message}")
        else:
            self.logger.error(msg=log_message)

    def critical(self, log_message, driver=None):
        if driver:
            self.logger.critical(msg=f"{driver.name}: {log_message}")
        else:
            self.logger.critical(msg=log_message)

    def exception(self, log_message, driver=None):
        if driver:
            self.logger.exception(msg=f"{driver.name}: {log_message}")
        else:
            self.logger.exception(msg=log_message)
