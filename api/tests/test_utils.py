# content of test_sample.py
from api.schema import XurlSubjectType, XurlType, XurlVerbType, XurlVersion
from api.utils import parse_xurl, parse_shop_url
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
    base_url = "https://391a919a.shops.xurlpay.org/v1/xurl"
    xurl="xurl://payload/paymentitem/1/noop?qty=3"
    logger.info(f"XURL: {xurl}")
    xurl_p = parse_xurl(base_url=base_url,xurl=xurl)
    logger.info(f"XURL parsed: {xurl_p}")

    shop_id = parse_shop_url(shop_url=base_url)

    assert xurl_p.base_url == "https://391a919a.shops.xurlpay.org/v1/xurl"
    assert xurl_p.xurl_type == XurlType.payload
    assert xurl_p.version == XurlVersion("v1")
    assert xurl_p.subject_type == XurlSubjectType.payment_item
    assert xurl_p.subject_id == "1"
    assert xurl_p.verb_type == XurlVerbType.NOOP.lower()
    assert xurl_p.parameters[0].name == "qty"
    assert xurl_p.parameters[0].value == "3"
    assert shop_id == "391a919a"
    assert xurl_p.to_xurl() == "xurl://payload/paymentitem/1/noop?qty=3"
