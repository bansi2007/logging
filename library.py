import logging
import sys
from logging.handlers import TimedRotatingFileHandler

class SeparateLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, level)
    
    def callHandlers(self, record):
        """
        Pass a record to all relevant handlers.

        Loop through all handlers for this logger and its parents in the
        logger hierarchy. If no handler was found, output a one-off error
        message to sys.stderr. Stop searching up the hierarchy whenever a
        logger with the "propagate" attribute set to zero is found - that
        will be the last logger whose handlers are called.
        """
        c = self
        found = 0
        while c:
            for hdlr in c.handlers:
                found = found + 1
                if record.levelno == hdlr.level:
                    hdlr.handle(record)
            if not c.propagate:
                c = None    #break out
            else:
                c = c.parent
        if (found == 0):
            if logging.lastResort:
                if record.levelno == logging.lastResort.level:
                    logging.lastResort.handle(record)
            elif logging.raiseExceptions and not self.manager.emittedNoHandlerWarning:
                sys.stderr.write("No handlers could be found for logger"
                                 " \"%s\"\n" % self.name)
                self.manager.emittedNoHandlerWarning = True


def getLogger(name=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    print("Getting Custom Logger.Wait!")
    logging.setLoggerClass(SeparateLogger)
    if name:
        return SeparateLogger.manager.getLogger(name)
    else:
        return logging.root

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


