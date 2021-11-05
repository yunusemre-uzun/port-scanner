from Logger.log_level import LogLevel
from datetime import datetime

import logging

class Logger:
    def __init__(self, componentName: str) -> None:
        self.__component = componentName

    def log(self, logLevel: LogLevel, message: str):
        logMessage = "Time: {} Component: {} Level: {} Message: {}".format(datetime.now().time(), self.__component, logLevel, message)
        if logLevel == LogLevel.info:
            logging.info(logMessage)
        elif logLevel == LogLevel.debug:
            logging.debug(logMessage)
        elif logLevel == LogLevel.fatal:
            logging.critical(logMessage)
        elif logLevel == LogLevel.warning:
            logging.warning(logMessage)
