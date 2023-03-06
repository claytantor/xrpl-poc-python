import logging
from logging.handlers import RotatingFileHandler

from api.schema import XurlSubjectType, XurlVerbType, Xurl, XurlVersion

logger = logging.getLogger(__name__)

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

    logger.info(f"PARSING XURL: {xurl}")

    assert xurl.startswith("xurl://")
    xurl = xurl[7:]
    xurl = xurl.split("?")
    xurl_path = xurl[0]

    xurl_parts = xurl_path.split("/")
    base_url = "/".join(xurl_parts[0:-4])
    api_version = xurl_parts[-4:-3][0]
    subject_type = xurl_parts[-3:-2][0]
    subject_id = xurl_parts[-2:-1][0]
    verb_type = xurl_parts[-1:][0]

    logger.info(f"base_url: {base_url} api_version: {api_version} subject_type: {subject_type} subject_id: {subject_id} verb_type: {verb_type}")

    parameters = []
    if len(xurl) == 2:
        parameters = xurl[1]
        parameters = parameters.split("&")
        parameters = [parameter.split("=") for parameter in parameters]
        parameters = [{"name": parameter[0], "value": parameter[1]} for parameter in parameters]

    return Xurl(
        base_url=base_url,
        version=XurlVersion(api_version),
        subject_type=XurlSubjectType(subject_type), 
        subject_id=subject_id, 
        verb_type=XurlVerbType(verb_type), 
        parameters=parameters)
