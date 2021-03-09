import logging
import time
from logging.handlers import TimedRotatingFileHandler

from library import SeparateLogger, getLogger, add_handlers


logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
add_handlers(logger)


def hypotenuse(a, b):
    """Compute the hypotenuse"""
    return (a**2 + b**2)**0.5

if __name__ == "__main__":
    print("started")
    while True:
        x = 3
        y = 4
        c = hypotenuse(x,y)
        logger.info("Hypotenuse of {}, {} is {}".format(x, y,c))
        time.sleep(10)

