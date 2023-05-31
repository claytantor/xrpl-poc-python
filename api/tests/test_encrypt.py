# content of test_sample.py
from api.pinatautils import pinata_pin_dict
from api.schema import XurlSubjectType, XurlType, XurlVerbType, XurlVersion
from api.utils import parse_xurl, parse_shop_url
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_public_key
from cryptography.hazmat.primitives.asymmetric import rsa

import json
import base64
import traceback
import asyncio

from api.rsa_encrypt import extract_public_key, rsa_encrypt


# FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


jwk = {
        "alg": "RS256",
        "kty": "RSA",
        "use": "sig",
        "x5c": [
            "MIIC+DCCAeCgAwIBAgIJBIGjYW6hFpn2MA0GCSqGSIb3DQEBBQUAMCMxITAfBgNVBAMTGGN1c3RvbWVyLWRlbW9zLmF1dGgwLmNvbTAeFw0xNjExMjIyMjIyMDVaFw0zMDA4MDEyMjIyMDVaMCMxITAfBgNVBAMTGGN1c3RvbWVyLWRlbW9zLmF1dGgwLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMnjZc5bm/eGIHq09N9HKHahM7Y31P0ul+A2wwP4lSpIwFrWHzxw88/7Dwk9QMc+orGXX95R6av4GF+Es/nG3uK45ooMVMa/hYCh0Mtx3gnSuoTavQEkLzCvSwTqVwzZ+5noukWVqJuMKNwjL77GNcPLY7Xy2/skMCT5bR8UoWaufooQvYq6SyPcRAU4BtdquZRiBT4U5f+4pwNTxSvey7ki50yc1tG49Per/0zA4O6Tlpv8x7Red6m1bCNHt7+Z5nSl3RX/QYyAEUX1a28VcYmR41Osy+o2OUCXYdUAphDaHo4/8rbKTJhlu8jEcc1KoMXAKjgaVZtG/v5ltx6AXY0CAwEAAaMvMC0wDAYDVR0TBAUwAwEB/zAdBgNVHQ4EFgQUQxFG602h1cG+pnyvJoy9pGJJoCswDQYJKoZIhvcNAQEFBQADggEBAGvtCbzGNBUJPLICth3mLsX0Z4z8T8iu4tyoiuAshP/Ry/ZBnFnXmhD8vwgMZ2lTgUWwlrvlgN+fAtYKnwFO2G3BOCFw96Nm8So9sjTda9CCZ3dhoH57F/hVMBB0K6xhklAc0b5ZxUpCIN92v/w+xZoz1XQBHe8ZbRHaP1HpRM4M7DJk2G5cgUCyu3UBvYS41sHvzrxQ3z7vIePRA4WF4bEkfX12gvny0RsPkrbVMXX1Rj9t6V7QXrbPYBAO+43JvDGYawxYVvLhz+BJ45x50GFQmHszfY3BR9TPK8xmMmQwtIvLu1PMttNCs7niCYkSiUv2sc2mlq1i3IashGkkgmo="
        ],
        "n": "yeNlzlub94YgerT030codqEztjfU_S6X4DbDA_iVKkjAWtYfPHDzz_sPCT1Axz6isZdf3lHpq_gYX4Sz-cbe4rjmigxUxr-FgKHQy3HeCdK6hNq9ASQvMK9LBOpXDNn7mei6RZWom4wo3CMvvsY1w8tjtfLb-yQwJPltHxShZq5-ihC9irpLI9xEBTgG12q5lGIFPhTl_7inA1PFK97LuSLnTJzW0bj096v_TMDg7pOWm_zHtF53qbVsI0e3v5nmdKXdFf9BjIARRfVrbxVxiZHjU6zL6jY5QJdh1QCmENoejj_ytspMmGW7yMRxzUqgxcAqOBpVm0b-_mW3HoBdjQ",
        "e": "AQAB",
        "kid": "NjVBRjY5MDlCMUIwNzU4RTA2QzZFMDQ4QzQ2MDAyQjVDNjk1RTM2Qg",
        "x5t": "NjVBRjY5MDlCMUIwNzU4RTA2QzZFMDQ4QzQ2MDAyQjVDNjk1RTM2Qg"
    }


def inc(x):
    return x + 1

def test_answer():
    logger.info("========= test_answer")
    assert inc(3) == 4

def test_eggs():
    logger.debug('eggs debug')
    logger.info('eggs info')
    logger.warning('eggs warning')
    logger.error('eggs error')
    logger.critical('eggs critical')
    assert True

def test_encrypt():
    
    public_key = extract_public_key(jwk)
    logger.info(f"public key:{public_key}")
    print("public key:",public_key)

    pa_d = {
        "id": 1,
        "name": "Homeworld",
        "first_name": "Clayton",
        "last_name": "Graham",
        "street_address": "6310 SOUTHEAST REDDPUTX STREET",
        "street_address_2": "Mariloara 2",
        "zip_code": "97206",
        "city": "Portland",
        "state": "OR",
        "country": "USA",
        "phone_number": "510-406-4414",
        "postal_code": "97206"
    }

    json_str = f'{pa_d["first_name"]}|{pa_d["last_name"]}|{pa_d["street_address"]}|{pa_d["street_address_2"]}|{pa_d["zip_code"]}|{pa_d["city"]}|{pa_d["state"]}|{pa_d["country"]}|{pa_d["phone_number"]}|{pa_d["postal_code"]}'

    encrypted_data = rsa_encrypt(json_str, public_key)
    logger.info(f"encrypted_data:{encrypted_data}")


    assert True

def test_encrypt_and_pin():

    public_key = extract_public_key(jwk)
    logger.info(f"public key:{public_key}")
    print("public key:",public_key)

    pa_d = {
        "id": 1,
        "name": "Homeworld",
        "first_name": "Clayton",
        "last_name": "Graham",
        "street_address": "6310 SOUTHEAST REDDPUTX STREET",
        "street_address_2": "Mariloara 2",
        "zip_code": "97206",
        "city": "Portland",
        "state": "OR",
        "country": "USA",
        "phone_number": "510-406-4414",
        "postal_code": "97206"
    }

    json_str = f'{pa_d["first_name"]}|{pa_d["last_name"]}|{pa_d["street_address"]}|{pa_d["street_address_2"]}|{pa_d["zip_code"]}|{pa_d["city"]}|{pa_d["state"]}|{pa_d["country"]}|{pa_d["phone_number"]}|{pa_d["postal_code"]}'

    encrypted_data = rsa_encrypt(json_str, public_key)

    # now base64 encode the encrypted data
    encrypted_data_b64 = base64.b64encode(encrypted_data)

    # now make the base64 encoded data a string
    encrypted_data_b64_str = encrypted_data_b64.decode('utf-8')

    pin_postal_address_data = {
        'encrypted_data': encrypted_data_b64_str,
        'shop_id': '18f67a8d',
        'well_known_uri': 'http://18f67a8d.localhost:5005/.well-known/xurl-shop-jwks.json?shop_id=18f67a8d',
        'customer_classic_address': "rscvr9YsZA5fK4rTNMvSeVHpRVgQddsnkS",
    }

    pin_response = asyncio.run(pinata_pin_dict(
        dict=pin_postal_address_data)) 
    
    logger.info(f"pin_response:{pin_response}")

    assert True