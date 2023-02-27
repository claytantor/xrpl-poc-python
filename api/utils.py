import logging
from logging.handlers import RotatingFileHandler

from api.schema import SubjectType, VerbType, Xurl
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


def parse_xurl(xurl: str)->Xurl:

    assert xurl.startswith("xurl://")
    xurl = xurl[7:]
    xurl = xurl.split("?")
    subject = xurl[0]
    subject = subject.split("/")
    subject_type = subject[0]
    subject_id = subject[1]
    verb_type = subject[2]
    parameters = xurl[1]
    parameters = parameters.split("&")
    parameters = [parameter.split("=") for parameter in parameters]
    parameters = [{"name": parameter[0], "value": parameter[1]} for parameter in parameters]

    return Xurl(
        subject_type=SubjectType(subject_type), 
        subject_id=subject_id, 
        verb_type=VerbType(verb_type), 
        parameters=parameters)
