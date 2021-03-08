import logging
import sys , time
from logging.handlers import TimedRotatingFileHandler
import import_ipynb

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
    print("Getting custom logger . Wait!")
    logging.setLoggerClass(SeparateLogger)
    if name:
        return SeparateLogger.manager.getLogger(name)
    else:
        return logging.root
    
    
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
        time.sleep(10)

"""PROPAGATE:
 - If this attribute evaluates to true, events logged to this logger will be passed to the handlers of 
   higher level (ancestor) loggers, in addition to any handlers attached to this logger. Messages are
   passed directly to the ancestor loggers’ handlers - neither the level nor filters of the ancestor
   loggers in question are considered.
 - If this evaluates to false, logging messages are not passed to the handlers of ancestor loggers.
 - The constructor sets this attribute to True.
Note : 
If you attach a handler to a logger and one or more of its ancestors, it may emit the same record multiple times.
In general, you should not need to attach a handler to more than one logger - if you just attach it to the
appropriate logger which is highest in the logger hierarchy, then it will see all events logged by all
descendant loggers, provided that their propagate setting is left set to True. A common scenario is to attach 
handlers only to the root logger, and to let propagation take care of the rest.
"""
