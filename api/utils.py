import logging
from logging.handlers import RotatingFileHandler
#----------------------------------------------------------------------
def create_rotating_log(path, logger, level=logging.INFO, maxBytes=1000000, backupCount=5):
    """
    Creates a rotating log
    """
    # logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    
    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=maxBytes,
                                  backupCount=backupCount)
    logger.addHandler(handler)
    
    # for i in range(10):
    #     logger.info("This is test log line %s" % i)
    #     time.sleep(1.5)