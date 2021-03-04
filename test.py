import logging
import time
from logging.handlers import TimedRotatingFileHandler

from mylogging import SeparateLogger, getLogger


logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)


def add_handlers(logger):
    rcount = 3
    formatter = logging.Formatter(
                fmt="%(asctime)s - %(levelname)s [%(name)s] -  %(filename)s:%(lineno)d - %(message)s "
            )
    debugLogHandler = TimedRotatingFileHandler('logs/debug.log', when='S', interval=5, backupCount=rcount)
    debugLogHandler.setLevel(logging.DEBUG)
    debugLogHandler.setFormatter(formatter)
    logger.addHandler(debugLogHandler)
    
    infoLogHandler = logging.handlers.TimedRotatingFileHandler('logs/info.log', when='S', interval=5, backupCount=rcount)
    infoLogHandler.setLevel(logging.INFO)
    infoLogHandler.setFormatter(formatter)
    logger.addHandler(infoLogHandler)
    
    warningLogHandler = logging.handlers.TimedRotatingFileHandler('logs/warning.log', when='S', interval=5, backupCount=rcount)
    warningLogHandler.setLevel(logging.WARNING)
    warningLogHandler.setFormatter(formatter)
    logger.addHandler(warningLogHandler)
    
    errorLogHandler = logging.handlers.TimedRotatingFileHandler('logs/error.log', when='S', interval=5, backupCount=rcount)
    errorLogHandler.setLevel(logging.ERROR)
    errorLogHandler.setFormatter(formatter)
    logger.addHandler(errorLogHandler)

add_handlers(logger)


if __name__ == "__main__":
    print("started")
    while True:
        logger.warning("warning message")
        logger.info("info message")
        logger.error("error message")
        logger.debug("debug message")
        time.sleep(0.1)
