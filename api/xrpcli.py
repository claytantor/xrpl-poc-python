
import os, sys
from tkinter import W
import shortuuid


from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.wallet import generate_faucet_wallet
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.transaction import send_reliable_submission
from xrpl.models.requests.account_info import AccountInfo
from xrpl.wallet import Wallet
from xrpl.core.keypairs import derive_classic_address, derive_keypair, generate_seed

from xrpl.constants import CryptoAlgorithm
from xrpl.core import addresscodec
from xrpl.core.keypairs.crypto_implementation import CryptoImplementation
from xrpl.core.keypairs.ed25519 import ED25519
from xrpl.core.keypairs.ed25519 import PREFIX as ED_PREFIX
from xrpl.core.keypairs.exceptions import XRPLKeypairsException
from xrpl.core.keypairs.helpers import get_account_id
from xrpl.core.keypairs.secp256k1 import SECP256K1
from typing_extensions import Final
from typing import Dict, Optional, Tuple, Type

_ALGORITHM_TO_MODULE_MAP: Final[Dict[CryptoAlgorithm, Type[CryptoImplementation]]] = {
    CryptoAlgorithm.ED25519: ED25519,
    CryptoAlgorithm.SECP256K1: SECP256K1,
}

import base64
import json
from datetime import datetime as dt, timedelta
import bech32

# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.
from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

DROPS_IN_XRP=1000000

class XUrlWallet:
    def __init__(self, network="https://s.altnet.rippletest.net:51234/", seed=None, isFaucet=False):
        print("network:", network)
        self.client = JsonRpcClient(network)
        if seed is None:
            if isFaucet:
                self.wallet = self.create_faucet_wallet()
                self.seed = self.wallet.seed          
                self.public_key = self.wallet.public_key
                self.private_key = self.wallet.private_key
                self.classic_address = self.wallet.classic_address
            else:
                self.seed = generate_seed(algorithm=CryptoAlgorithm.SECP256K1)
                self.wallet = Wallet(seed=self.seed, sequence=16237283)
                self.wallet.create()
                self.pub_key, self.private_key  = derive_keypair(self.seed)    
                self.classic_address = self.wallet.classic_address
        else:
            self.seed = seed
            self.wallet = Wallet(seed=seed, sequence=16237283)
            self.wallet.create()
            self.pub_key, self.private_key  = derive_keypair(seed)
            self.classic_address = self.wallet.classic_address


    def get_account_info(self, address=None):
        if address is None:
            address = self.wallet.classic_address

        acct_info = AccountInfo(
            account=address,
            ledger_index="current",
            queue=True,
            strict=True,
        )
        response = self.client.request(acct_info)
        result = response.result
        return result
    
    def create_faucet_wallet(self):
        wallet = generate_faucet_wallet(self.client, debug=True)
        return wallet

    def serialize(self):
        return {
            'seed': self.seed,
            'public_key': self.public_key,
            'private_key': self.private_key,
            'classic_address': self.classic_address,
            'account_info': self.get_account_info(),
        }

    def send_payment(self, amount_xrp, destination_address):
        # Prepare payment
        print(f"sending xrp:{amount_xrp} drops:{xrp_to_drops(xrp=amount_xrp)} to:{destination_address}")
        tx_payment = Payment(
            account=self.wallet.classic_address,
            # amount=xrp_to_drops(xrp=amount_xrp),
            amount=xrp_to_drops(amount_xrp),
            destination=destination_address,
        ) # send to my testnet xumm wallet

        # Sign the transaction
        tx_payment_signed = safe_sign_and_autofill_transaction(tx_payment, self.wallet, self.client)

        tx_response = send_reliable_submission(tx_payment_signed, self.client)
        # print(tx_response)
        return tx_response.status, tx_response.result  

    def sign_msg(self, message, encoding='utf-8'):
        """Sign the message to be sent
        private_key: must be hex
        """

        base64_message, base64_signature =  sign_message(message, self.private_key)

        return base64_message, base64_signature


    def generate_payment_request(self, amount, memo="generated payment request"):
        """Generate a payment request
        """

        expires = dt.now()+timedelta(minutes=60)

        payment_request_dict = {
            'amount': amount,
            'public_key':self.pub_key,
            'address':self.wallet.classic_address,
            'expires':expires.timestamp(),
            'memo':memo,
            'request_hash':shortuuid.uuid(),
        }
        json_str = json.dumps(payment_request_dict)
        print(json_str)
        base64_message, base_64_sig = self.sign_msg(json_str)
        payment_request=f"{base64_message}:{base_64_sig}"
        return payment_request_dict, payment_request


"""
==========================
functional methods
==========================
"""

def drops_to_xrp(drops):
    return int(drops/DROPS_IN_XRP)

def sign_message(message, private_key, encoding='utf-8'):
    """
    sign the message to be sent
    private_key: must be hex
    message: must be encoded
    """
    module = _ALGORITHM_TO_MODULE_MAP[CryptoAlgorithm.ED25519]
    message_bytes = message.encode(encoding)
    sig = module.sign(message_bytes, private_key)

    return base64.b64encode(message_bytes).decode(encoding), base64.b64encode(sig).decode(encoding)

def verify_msg(base64_message, base64_signature, public_key):
    sig = base64.b64decode(base64_signature)
    message = base64.b64decode(base64_message)
    module = _ALGORITHM_TO_MODULE_MAP[CryptoAlgorithm.ED25519]
    if not module.is_valid_message(message, sig, public_key):
        raise XRPLKeypairsException(
            "Derived keypair did not generate verifiable signature",
        )

def send_payment_from_request():
    receiving_wallet = XUrlWallet(network=config['JSON_RPC_URL'], seed=config['WALLET_SECRET_R'])
    
    payment_request = receiving_wallet.generate_payment_request(amount=120)
    print(payment_request)


    # ok now lets pay it with a faucet
    # decode the payment request
    pr_parts = payment_request.split(":")

    # verify the signed message
    message_payload = json.loads(base64.b64decode(pr_parts[0].encode('utf-8')))
    sig = base64.b64decode(pr_parts[1].encode('utf-8'))
    print(message_payload, sig)

    # use the public key to verify

    try:
        sending_wallet = XUrlWallet(network=config['JSON_RPC_URL']) #this is a faucet wallet
        account_info = sending_wallet.get_account_info()
        print(account_info)
        
        # this will throw an exception if the signature is not valid
        verify_msg(pr_parts[0].encode('utf-8'), sig, message_payload['public_key'])

        # Memos": [
        # {
        #     "Memo": {
        #         "MemoType": "687474703a2f2f6578616d706c652e636f6d2f6d656d6f2f67656e65726963",
        #         "MemoData": "72656e74"
        #     }
        #     }
        # ],

        tx_response_status, tx_response_result = sending_wallet.send_payment(
            amount_xrp=message_payload['amount'],
            destination_address=message_payload['address']
        )

        print(tx_response_status, tx_response_result)


    except Exception as e:
        print("=== COULD NOT VERIFY", e)


# def create_new_wallet(network=config['JSON_RPC_URL']):
#     client = JsonRpcClient(network)
#     seed = generate_seed(algorithm=CryptoAlgorithm.SECP256K1)
#     wallet = Wallet(seed=seed, sequence=16237283)
#     wallet.create()
    
#     pub_key, private_key  = derive_keypair(seed) 

#     print(f"wallet created public key:{pub_key} {wallet.classic_address}")
    
#     from xrpl.models.requests.account_info import AccountInfo
#     acct_info = AccountInfo(
#         account=wallet.classic_address,
#         ledger_index="current",
#         queue=True,
#         strict=True,
#     )
#     response = client.request(acct_info)
#     result = response.result
#     print(result)


def sign_basic():
    client = JsonRpcClient(config['JSON_RPC_URL'])
    wallet = generate_faucet_wallet(client, debug=True)
    seed = wallet.seed          
    public_key = wallet.public_key
    private_key = wallet.private_key
    classic_address = wallet.classic_address     
    base64_message, base64_signature = sign_message("message", private_key, encoding='utf-8') 
    print(f"message: {base64_message} signature: {base64_signature}") 
    try:
        verify_msg(base64_message, base64_signature, public_key) 
        print("message verified")
    except Exception as e:
        print("=== COULD NOT VERIFY", e)



# Defining main function
def main():

    import argparse

    parser = argparse.ArgumentParser(description='XURL cli.')
    parser.add_argument('--keypair', '-k', type=str, help='generate a keypair from seed')
    parser.add_argument('--wallet', '-w', type=str, help='action on wallet ["create", "info", "payment"]')
    parser.add_argument('--faucet', '-f', type=str, help='is this a faucet wallet True/False')
    parser.add_argument('--sign', '-s', type=str, help='message to sign, returns base64 signature')
    parser.add_argument('--verify', '-v', type=str, help='base4 message to verify')
    parser.add_argument('--signature', '-g', type=str, help='base4 signature for message verification')
    parser.add_argument('--private_key', '-sk', type=str, help='private key')
    parser.add_argument('--public_key', '-pk', type=str, help='public key')
    
    
    args = parser.parse_args()

    if args.keypair:
        seed = args.keypair
        public_key, private_key = derive_keypair(seed)
        print(f"public_key: {public_key}, private_key: {private_key}")

    # wallet from seed
    if 'wallet' in args and args.wallet == 'create' and 'faucet' in args and args.faucet == 'True':
        wallet = XUrlWallet(network=config['JSON_RPC_URL'], isFaucet=True)
        print(json.dumps(wallet.serialize(), indent=4))

    # sign a message
    if 'sign' in args and args.sign and 'private_key' in args and args.private_key:
        message = args.sign
        private_key = args.private_key
        message,signature = sign_message(message, private_key)
        print(f"message: {message} signature: {signature}")

    # verify a message
    if 'verify' in args and args.verify and 'public_key' in args and args.public_key and 'signature' in args and args.signature:
        message = args.verify
        pk = args.public_key
        sig = args.signature
        try:
            verify_msg(message.encode('utf-8'), sig.encode('utf-8'), pk)
            print("message verified")
        except Exception as e:
            print("=== COULD NOT VERIFY", e)   

   

  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()