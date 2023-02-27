# content of test_sample.py
from api.schema import SubjectType, VerbType, XurlVersion
from api.utils import parse_xurl
import logging

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4

def test_parse_xurl(caplog):
    caplog.set_level(logging.DEBUG)
    xurl="xurl://devapi.xurlpay.org/v1/xurl/v1/paymentitem/3/buynow?qty=3"
    logger.info(f"XURL: {xurl}")
    xurl_p = parse_xurl(xurl=xurl)
    logger.info(f"XURL parsed: {xurl_p}")
    assert xurl_p.base_url == "devapi.xurlpay.org/v1/xurl"
    assert xurl_p.version == XurlVersion("v1")
    assert xurl_p.subject_type == SubjectType.payment_item
    assert xurl_p.subject_id == "3"
    assert xurl_p.verb_type == VerbType.buy_now
    assert xurl_p.parameters[0].name == "qty"
    assert xurl_p.parameters[0].value == "3"
