# content of test_sample.py
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



# FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

RSA_MAX_LEN = 214

def extract_public_key(jwk):
    # Extract the modulus and exponent from the JWK
    n = base64.urlsafe_b64decode(jwk["n"] + '=' * (4 - len(jwk["n"]) % 4))
    e = base64.urlsafe_b64decode(jwk["e"] + '=' * (4 - len(jwk["e"]) % 4))

    # Convert to integers
    n = int.from_bytes(n, byteorder='big')
    e = int.from_bytes(e, byteorder='big')

    # Construct an RSA public key
    public_key = rsa.RSAPublicNumbers(e, n).public_key(default_backend())

    # Convert to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return public_key_pem.decode()

def rsa_encrypt(json_str, public_key_pem):
    try:
        # json_str = f'{pa_d["first_name"]}|{pa_d["last_name"]}|{pa_d["street_address"]}|{pa_d["street_address_2"]}|{pa_d["zip_code"]}|{pa_d["city"]}|{pa_d["state"]}|{pa_d["country"]}|{pa_d["phone_number"]}|{pa_d["postal_code"]}'

        if len(json_str)>RSA_MAX_LEN:
            logger.error(f"json_str too long:{len(json_str)}")
            raise Exception(f"json_str too long:{len(json_str)}")

        # Load the public key
        # logger.info(f"public_key_pem:{public_key_pem}")
        public_key_pem_b64data = '\n'.join(public_key_pem.splitlines()[1:-1])
        logger.info(f"public_key_pem:\n{public_key_pem_b64data}")

        derdata = base64.b64decode(public_key_pem_b64data)

        # cryptography.hazmat.backends.openssl.rsa._RSAPublicKey
        public_key = load_der_public_key(derdata, default_backend())
        logger.debug(public_key)

        # Convert the payload to bytes
        logger.info(f"json_str:{json_str}")
        payload_bytes = json_str.encode('utf-8')

        # Encrypt the payload
        encrypted_payload = public_key.encrypt(
            payload_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_payload

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
        return None

