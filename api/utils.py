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


def parse_shop_url(shop_url: str)->str:
    logger.info(f"PARSING SHOP URL: {shop_url}")
    shop_url = shop_url.split("/")
    shop_host = shop_url[2]
    shop_id = shop_host.split(".")[0]
    logger.info(f"shop_id: {shop_id}")
    return shop_id

def parse_xurl(base_url:str, xurl: str)->Xurl:

    logger.info(f"PARSING XURL: {xurl}")

    assert xurl.startswith("xurl://")
    xurl = xurl[7:]
    xurl = xurl.split("?")

    xurl_path = xurl[0]
    xurl_parts = xurl_path.split("/")
    logger.info(f"xurl_parts: {xurl_parts}")
    prefix = xurl_parts[0]
    subject_type = xurl_parts[1]
    subject_id = xurl_parts[2]
    verb_type = xurl_parts[3]

    logger.info(f"base_url: {base_url} prefix: {prefix} subject_type: {subject_type} subject_id: {subject_id} verb_type: {verb_type}")

    parameters = []
    if len(xurl) == 2:
        parameters = xurl[1]
        parameters = parameters.split("&")
        parameters = [parameter.split("=") for parameter in parameters]
        parameters = [{"name": parameter[0], "value": parameter[1]} for parameter in parameters]
    logger.info(f"parameters: {parameters}")

    return Xurl(
        xurl_type=prefix,
        base_url=base_url,
        version=XurlVersion.v1,
        subject_type=XurlSubjectType(subject_type), 
        subject_id=subject_id, 
        verb_type=XurlVerbType(verb_type), 
        parameters=parameters)
