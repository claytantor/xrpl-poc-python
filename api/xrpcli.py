
import os, sys
import shortuuid
import xrpl
import os
import json
import click


from xrpl.clients import JsonRpcClient, WebsocketClient
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
from typing import Dict, Type
# get the token info
import requests
import xumm

from api.models import XrpNetwork

_ALGORITHM_TO_MODULE_MAP: Final[Dict[CryptoAlgorithm, Type[CryptoImplementation]]] = {
    CryptoAlgorithm.ED25519: ED25519,
    CryptoAlgorithm.SECP256K1: SECP256K1,
}

import base64
import json
from datetime import datetime as dt, timedelta
import bech32

import logging
ulogger = logging.getLogger("uvicorn.error")

cli_logger = logging.getLogger("xrpcli")

# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.
from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

DROPS_IN_XRP=1000000

# # Or with manually provided credentials (instead of using dotenv):
# sdk = xumm.XummSdk(config['XUMM_API_KEY'], config['XUMM_API_SECRET'])

# class AppTokenPayloadFactory:
#     def __init__(self, xapp_token):
#         self.xapp_token = xapp_token

#     async def _make_payload(self):
#         xumm_app_session = await self.get_xapp_tokeninfo(self.xapp_token)

#         # print(xumm_app_session)
        
    
#     async def get_xapp_tokeninfo(self, xumm_token):
#         url = f"https://xumm.app/api/v1/platform/xapp/ott/{xumm_token}"

#         headers = {
#             "accept": "application/json",
#             "X-API-Key": f"{config['XUMM_API_KEY']}",
#             "X-API-Secret": f"{config['XUMM_API_SECRET']}",
#         }

#         response = requests.get(url, headers=headers)

#         return json.loads(response.text)
        

#     @staticmethod
#     async def make_payload(xapp_token):
#         factory = AppTokenPayloadFactory(xapp_token)
#         return await factory._make_payload() 

# class XummWallet:

#     """
#     {
#         "client_id": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#         "scope": "XummPkce",
#         "aud": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#         "sub": "rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y",
#         "email": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce+rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y@xumm.me",
#         "app_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#         "app_name": "dev-xurlpay",
#         "payload_uuidv4": "4eb33332-ae57-43bc-82eb-d6d099b26ecb",
#         "usertoken_uuidv4": "4de21968-8c2f-4fb3-9bb6-94b589a13a8c",
#         "network_type": "TESTNET",
#         "network_endpoint": "wss://s.altnet.rippletest.net:51233",
#         "iat": 1668194332,
#         "exp": 1668280732,
#         "iss": "https://oauth2.xumm.app"
#     }
    
#     """
#     def __init__(self, network_endpoint, classic_address):
#         self.network_endpoint = network_endpoint
#         self.classic_address = classic_address
#         self.client = JsonRpcClient(network_endpoint)
        

#         # {
#         #     "id": 5,
#         #     "status": "success",
#         #     "type": "response",
#         #     "result": {
#         #         "account_data": {
#         #             "Account": "rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn",
#         #             "Balance": "999999999960",
#         #             "Flags": 8388608,
#         #             "LedgerEntryType": "AccountRoot",
#         #             "OwnerCount": 0,
#         #             "PreviousTxnID": "4294BEBE5B569A18C0A2702387C9B1E7146DC3A5850C1E87204951C6FDAA4C42",
#         #             "PreviousTxnLgrSeq": 3,
#         #             "Sequence": 6,
#         #             "index": "92FA6A9FC8EA6018D5D16532D7795C91BFB0831355BDFDA177E86C8BF997985F"
#         #         },
#         #         "ledger_current_index": 4,
#         #         "queue_data": {
#         #             "auth_change_queued": true,
#         #             "highest_sequence": 10,
#         #             "lowest_sequence": 6,
#         #             "max_spend_drops_total": "500",
#         #             "transactions": [
#         #                 {
#         #                     "auth_change": false,
#         #                     "fee": "100",
#         #                     "fee_level": "2560",
#         #                     "max_spend_drops": "100",
#         #                     "seq": 6
#         #                 },
#         #                 ... (trimmed for length) ...
#         #                 {
#         #                     "LastLedgerSequence": 10,
#         #                     "auth_change": true,
#         #                     "fee": "100",
#         #                     "fee_level": "2560",
#         #                     "max_spend_drops": "100",
#         #                     "seq": 10
#         #                 }
#         #             ],
#         #             "txn_count": 5
#         #         },
#         #         "validated": false
#         #     }
#         # }

#         account_info_response = self.client.request(AccountInfo(account=self.classic_address))


#         # acct_info = AccountInfo(
#         #     account="rBtXmAdEYcno9LWRnAGfT9qBxCeDvuVRZo",
#         #     ledger_index="current",
#         #     queue=True,
#         #     strict=True,
#         # )
#         # response = client.request(acct_info)
#         result = account_info_response.result
#         self.account_data = result["account_data"]


        
#     @property
#     def balance(self): 
#         return self.account_data['Balance'] / DROPS_IN_XRP


#     def generate_payment_request(self, xrp_amount, memo="generated payment request"):
#         """Generate a payment request
#         """

#         # expires = dt.now()+timedelta(minutes=60)

#         payment_request_dict = {
#             'amount': xrp_amount,
#             'amount_drops': int(xrp_to_drops(xrp_amount)),
#             'address':self.classic_address,
#             'network_endpoint':self.network_endpoint,
#             # 'network_type': get_network_type(self.network_endpoint),
#             'memo':memo,
#             'request_hash':shortuuid.uuid(),
#         }

#         # json_str = json.dumps(payment_request_dict)
#         # base64_message, base_64_sig = self.sign_msg(json_str)
#         # payment_request=f"{base64_message}:{base_64_sig}"
#         # return payment_request_dict, payment_request

#         create_payload = {
#             'txjson': {
#                     'TransactionType' : 'Payment',
#                     'Destination' : self.classic_address,
#                     'Amount': str(xrp_to_drops(xrp_amount)),
#             },
#             "custom_meta": {
#                 "identifier": "payment_request",
#                 "blob": json.dumps(payment_request_dict),
#                 "instruction": memo
#             }
#         }   

#         created = sdk.payload.create(create_payload)

#         return created.to_dict()

# class XUrlWallet:
#     def __init__(self, network="https://s.altnet.rippletest.net:51234/", seed=None, isFaucet=False):
#         print("network:", network)
#         self.client = JsonRpcClient(network)
#         if seed is None:
#             if isFaucet:
#                 self.wallet = self.create_faucet_wallet()
#                 self.seed = self.wallet.seed          
#                 self.public_key = self.wallet.public_key
#                 self.private_key = self.wallet.private_key
#                 self.classic_address = self.wallet.classic_address
#             else:
#                 self.seed = generate_seed(algorithm=CryptoAlgorithm.SECP256K1)
#                 self.wallet = Wallet(seed=self.seed, sequence=16237283)
#                 self.wallet.create()
#                 self.pub_key, self.private_key  = derive_keypair(self.seed)    
#                 self.classic_address = self.wallet.classic_address
#         else:
#             self.seed = seed
#             self.wallet = Wallet(seed=seed, sequence=16237283)
#             self.wallet.create()
#             self.pub_key, self.private_key  = derive_keypair(seed)
#             self.classic_address = self.wallet.classic_address


#     def get_account_info(self, address=None):
#         if address is None:
#             address = self.wallet.classic_address

#         acct_info = AccountInfo(
#             account=address,
#             ledger_index="current",
#             queue=True,
#             strict=True,
#         )
#         response = self.client.request(acct_info)
#         result = response.result
#         return result
    
#     def create_faucet_wallet(self):
#         wallet = generate_faucet_wallet(self.client, debug=True)
#         return wallet

#     def serialize(self):
#         return {
#             'seed': self.seed,
#             'public_key': self.public_key,
#             'private_key': self.private_key,
#             'classic_address': self.classic_address,
#             'account_info': self.get_account_info(),
#         }

#     def send_payment(self, amount_xrp, destination_address):
#         # Prepare payment
#         print(f"sending xrp:{amount_xrp} drops:{xrp_to_drops(xrp=amount_xrp)} to:{destination_address}")
#         tx_payment = Payment(
#             account=self.wallet.classic_address,
#             # amount=xrp_to_drops(xrp=amount_xrp),
#             amount=xrp_to_drops(amount_xrp),
#             destination=destination_address,
#         ) # send to my testnet xumm wallet

#         # Sign the transaction
#         tx_payment_signed = safe_sign_and_autofill_transaction(tx_payment, self.wallet, self.client)

#         tx_response = send_reliable_submission(tx_payment_signed, self.client)
#         # print(tx_response)
#         return tx_response.status, tx_response.result  

#     def sign_msg(self, message, encoding='utf-8'):
#         """Sign the message to be sent
#         private_key: must be hex
#         """

#         # base64_message, base64_signature =  sign_message(message, self.private_key)

#         # return base64_message, base64_signature
#         pass


#     def generate_payment_request(self, amount, memo="generated payment request"):
#         """Generate a payment request
#         """

#         expires = dt.now()+timedelta(minutes=60)

#         payment_request_dict = {
#             'amount': amount,
#             'amount_drops': int(xrp_to_drops(amount)),
#             'public_key':self.pub_key,
#             'address':self.wallet.classic_address,
#             'expires':expires.timestamp(),
#             'memo':memo,
#             'request_hash':shortuuid.uuid(),
#         }
#         json_str = json.dumps(payment_request_dict)
#         print(json_str)
#         base64_message, base_64_sig = self.sign_msg(json_str)
#         payment_request=f"{base64_message}:{base_64_sig}"
#         return payment_request_dict, payment_request


"""
==========================
functional methods
==========================
"""

"""
If you don't run your own rippled server, you can use the following public servers to submit transactions or read data from the ledger.

Operator	Network	JSON-RPC URL	WebSocket URL	Notes
XRP Ledger Foundation	Mainnet	https://xrplcluster.com/
https://xrpl.ws/ ²	wss://xrplcluster.com/
wss://xrpl.ws/ ²	Full history server cluster.
Ripple¹	Mainnet	https://s1.ripple.com:51234/	wss://s1.ripple.com/	General purpose server cluster
Ripple¹	Mainnet	https://s2.ripple.com:51234/	wss://s2.ripple.com/	Full-history server cluster
Sologenic	Mainnet		wss://x1.sologenic.org	Websocket Server
Ripple¹	Testnet	https://s.altnet.rippletest.net:51234/	wss://s.altnet.rippletest.net/	Testnet public server
Ripple¹	Devnet	https://s.devnet.rippletest.net:51234/	wss://s.devnet.rippletest.net/	Devnet public server
"""

xrp_lookup = {
    's.altnet.rippletest.net':{
        'json_rpc':'https://s.altnet.rippletest.net:51234',
        'websocket':'wss://s.altnet.rippletest.net:51233',
        'type':'testnet',
    },
    's.devnet.rippletest.net':{  
        'json_rpc':'https://s.devnet.rippletest.net:51234',
        'websocket':'wss://s.devnet.rippletest.net:51233',
        'type':'devnet',
    },
    's1.ripple.com':{
        'json_rpc':'https://s1.ripple.com:51234',
        'websocket':'wss://s1.ripple.com:51233',
        'type':'mainnet',
    },
    's2.ripple.com':{
        'json_rpc':'https://s2.ripple.com:51234',
        'websocket':'wss://s2.ripple.com:51233',
        'type':'mainnet',
    },
    'xrplcluster.com':{
        'json_rpc':'https://xrplcluster.com',
        'websocket':'wss://xrplcluster.com',
        'type':'mainnet',
    },
    'xrpl.ws':{
        'json_rpc':'https://xrpl.ws',
        'websocket':'wss://xrpl.ws',
        'type':'mainnet',
    },
    'x1.sologenic.org':{
        'json_rpc':'',
        'websocket':'wss://x1.sologenic.org',
        'type':'mainnet',
    },
    'xrpl.link':{
        'json_rpc':'https://xrpl.link',
        'websocket':'wss://xrpl.link',
        'type':'mainnet',
    },
    'testnet.xrpl-labs.com':{
        'json_rpc':'https://testnet.xrpl-labs.com',
        'websocket':'wss://testnet.xrpl-labs.com',
        'type':'testnet',
    },

}

def get_xrp_network_from_jwt(jwt_body)-> XrpNetwork:
    xrp_network = {}
    if 'net' in jwt_body:
        xrp_network['websocket'] = jwt_body['net']
    elif 'network_endpoint' in jwt_body:
        xrp_network['websocket'] = jwt_body['network_endpoint']
    else:
        raise Exception("No network endpoint found in jwt")
    
    xrp_network['json_rpc'] = get_rpc_network_from_wss(xrp_network['websocket'])
    xrp_network['type'] = get_rpc_network_type(xrp_network['json_rpc'])
    xrp_network['domain'] = get_rpc_domain(xrp_network['json_rpc'])

    return XrpNetwork(xrp_network)


def get_wss_from_jwt(jwt_body):
    if 'net' in jwt_body:
        return jwt_body['net']
    elif 'network_endpoint' in jwt_body:
        return jwt_body['network_endpoint']
    else:
        return None


def get_rpc_network_from_jwt(jwt_body):
    rpc_network = xrp_lookup['s.altnet.rippletest.net']['json_rpc']
    if 'net' in jwt_body:
        rpc_network = get_rpc_network_from_wss(jwt_body['net'])
        # app.logger.info(f"rpc_network: {rpc_network} net:{jwt_body['net']}")
    elif 'network_endpoint' in jwt_body:
        rpc_network = get_rpc_network_from_wss(jwt_body['network_endpoint'])
        # app.logger.info(f"rpc_network: {rpc_network} network_endpoint:{jwt_body['network_endpoint']}")
    return rpc_network

def get_rpc_network_from_wss(wss_endpoint):
    for domain in xrp_lookup.keys():
        if xrp_lookup[domain]['websocket'] == wss_endpoint:
            return xrp_lookup[domain]['json_rpc']
    
    return 'none'

def get_rpc_network_type(network):
    for domain in xrp_lookup.keys():
        if xrp_lookup[domain]['json_rpc'] == network:
            return xrp_lookup[domain]['type']
    
    return 'none'

def get_wss_network_type(network):
    for domain in xrp_lookup.keys():
        if xrp_lookup[domain]['websocket'] == network:
            return xrp_lookup[domain]['type']
    
    return 'none'

def get_rpc_domain(network):
    for domain in xrp_lookup.keys():
        if domain in network:
            return domain
    
    return 'none'


async def get_account_info(address, network="https://s.altnet.rippletest.net:51234/"):

    try:
        ulogger.info(f"get_account_info: {address} {network}")
        client = JsonRpcClient(network)
        acct_info = AccountInfo(
            account=address,
            ledger_index="current",
            queue=True,
            strict=True,
        )
        response = await client.request_impl(acct_info)
        result = response.result
        return result
    except Exception as e:
        ulogger.error(f"get_account_info: {e}")
        raise e

def xrp_to_drops(xrp):
    return int(xrp*DROPS_IN_XRP)

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

# def send_payment_from_request():
#     receiving_wallet = XUrlWallet(network=config['JSON_RPC_URL'], seed=config['WALLET_SECRET_R'])
    
#     payment_request = receiving_wallet.generate_payment_request(amount=120)
#     print(payment_request)


#     # ok now lets pay it with a faucet
#     # decode the payment request
#     pr_parts = payment_request.split(":")

#     # verify the signed message
#     message_payload = json.loads(base64.b64decode(pr_parts[0].encode('utf-8')))
#     sig = base64.b64decode(pr_parts[1].encode('utf-8'))
#     print(message_payload, sig)

#     # use the public key to verify

#     try:
#         sending_wallet = XUrlWallet(network=config['JSON_RPC_URL']) #this is a faucet wallet
#         account_info = sending_wallet.get_account_info()
#         print(account_info)
        
#         # this will throw an exception if the signature is not valid
#         verify_msg(pr_parts[0].encode('utf-8'), sig, message_payload['public_key'])

#         # Memos": [
#         # {
#         #     "Memo": {
#         #         "MemoType": "687474703a2f2f6578616d706c652e636f6d2f6d656d6f2f67656e65726963",
#         #         "MemoData": "72656e74"
#         #     }
#         #     }
#         # ],

#         tx_response_status, tx_response_result = sending_wallet.send_payment(
#             amount_xrp=message_payload['amount'],
#             destination_address=message_payload['address']
#         )

#         print(tx_response_status, tx_response_result)


#     except Exception as e:
#         print("=== COULD NOT VERIFY", e)


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
    # base64_message, base64_signature = sign_message("message", private_key, encoding='utf-8') 
    # print(f"message: {base64_message} signature: {base64_signature}") 
    try:
        # verify_msg(base64_message, base64_signature, public_key) 
        print("message verified")
    except Exception as e:
        print("=== COULD NOT VERIFY", e)


async def get_xapp_tokeninfo(xumm_token):


    url = f"https://xumm.app/api/v1/platform/xapp/ott/{xumm_token}"

    headers = {
        "accept": "application/json",
        "X-API-Key": f"{config['XUMM_API_KEY']}",
        "X-API-Secret": f"{config['XUMM_API_SECRET']}",
    }

    response = requests.get(url, headers=headers)

    return json.loads(response.text)



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

    # # wallet from seed
    # if 'wallet' in args and args.wallet == 'create' and 'faucet' in args and args.faucet == 'True':
    #     wallet = XUrlWallet(network=config['JSON_RPC_URL'], isFaucet=True)
    #     print(json.dumps(wallet.serialize(), indent=4))

    # # sign a message
    # if 'sign' in args and args.sign and 'private_key' in args and args.private_key:
    #     message = args.sign
    #     private_key = args.private_key
    #     message,signature = sign_message(message, private_key)
    #     print(f"message: {message} signature: {signature}")

    # # verify a message
    # if 'verify' in args and args.verify and 'public_key' in args and args.public_key and 'signature' in args and args.signature:
    #     message = args.verify
    #     pk = args.public_key
    #     sig = args.signature
    #     try:
    #         verify_msg(message.encode('utf-8'), sig.encode('utf-8'), pk)
    #         print("message verified")
    #     except Exception as e:
    #         print("=== COULD NOT VERIFY", e)   

# CLI helper functions
def save_or_log(out_file=None, dict_out={}):
    s_dict = json.dumps(dict_out, indent=4)
    if out_file == None:
        cli_logger.info(s_dict)
    else:
        # Writing to sample.json
        with open(out_file, "w") as outfile:
            outfile.write(s_dict)

def hydrate_wallet(client:JsonRpcClient, infile):
    # load the wallet file
    click.echo(f'loading wallet: {infile}')
    # Opening JSON file
    with open(infile, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    # get the account info so you cat get the sequence
    acct_info = AccountInfo(
        account=json_object['classic_address'],
        ledger_index="current",
        queue=True,
        strict=True,
    )
    response = client.request(acct_info)
    a_dict = response.result

    h_wallet = Wallet(seed=json_object['seed'], sequence=a_dict['account_data']['Sequence'])
    return h_wallet


# ============================================================
# CLI Functions
# ============================================================
  
@click.group()
def cli():
    pass

@cli.command()
@click.option('--out', help='json outfile')
def create_wallet(out):
    client = JsonRpcClient(config['JSON_RPC_URL'])

    if config['XRP_NETWORK_TYPE'] != 'testnet':
        raise ValueError('cant create faucet on this network')
    cli_logger.info("creating wallet")
    wallet = generate_faucet_wallet(client, debug=True) #issuer
    wallet_info = {
        'public_key':wallet.public_key,
        'private_key':wallet.private_key,
        'classic_address':wallet.classic_address,
        'seed':wallet.seed
    }

    save_or_log(out_file=out, dict_out=wallet_info)

# @cli.command()
# @click.option('--infile', help='json infile')
# def get_account(infile, out):
#     click.echo(f'loading wallet: {infile}')
#     # Opening JSON file
#     with open(infile, 'r') as openfile:
#         # Reading from json file
#         json_object = json.load(openfile)
    
#     logger.debug(json.dumps(json_object, indent=4))
    
#     acct_info = AccountInfo(
#         account=json_object['classic_address'],
#         ledger_index="current",
#         queue=True,
#         strict=True,
#     )
#     response = client.request(acct_info)
#     logger.debug(json.dumps(response, indent=4))

# @cli.command()
# @click.option('--infile', help='issuer wallet infile')
# def issuer_settings_tx(infile):

#     # issuer_wallet = Wallet(seed=json_object['seed'], sequence=a_dict['account_data']['Sequence'])
#     issuer_wallet = hydrate_wallet(infile)

#     # Configure issuer (issuer  address) settings -------------------------------------
#     issuer_settings_tx = xrpl.models.transactions.AccountSet(
#         account=issuer_wallet.classic_address,
#         transfer_rate=0,
#         tick_size=5,
#         domain=bytes.hex(config['XRP_ISSUER_CURRENCY_TRUST_DOMAIN'].encode("ASCII")),
#         set_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE,
#     )
#     cst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
#         transaction=issuer_settings_tx,
#         wallet=issuer_wallet,
#         client=client,
#     )
#     logger.debug("Sending issuer address AccountSet transaction...")
#     response = xrpl.transaction.send_reliable_submission(cst_prepared, client)
#     logger.debug(response)
#     # logger.debug(json.dumps(response, indent=4))

# @cli.command()
# @click.option('--infile', help='receiver wallet infile')
# def receiver_settings_tx(infile):

#     receiver_wallet = hydrate_wallet(infile)

#     # Configure receiver address settings -----------------------------------------------
#     receiver_settings_tx = xrpl.models.transactions.AccountSet(
#         account=receiver_wallet.classic_address,
#         set_flag=xrpl.models.transactions.AccountSetFlag.ASF_REQUIRE_AUTH,
#     )
#     hst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
#         transaction=receiver_settings_tx,
#         wallet=receiver_wallet,
#         client=client,
#     )
#     logger.debug("Sending receiver address AccountSet transaction...")
#     response = xrpl.transaction.send_reliable_submission(hst_prepared, client)
#     logger.debug(response)


# @cli.command()
# @click.option('--issuer', help='issuer wallet infile')
# @click.option('--receiver', help='receiver wallet infile')
# def create_trust_line(issuer, receiver):

#     issuer_wallet = hydrate_wallet(issuer)
#     receiver_wallet = hydrate_wallet(receiver)

#     # Create trust line from receiver to issuer  address -----------------------------------
#     currency_code = config['XRP_CURRENCY_NAME']
#     trust_set_tx = xrpl.models.transactions.TrustSet(
#         account=receiver_wallet.classic_address,
#         limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
#             currency=currency_code,
#             issuer=issuer_wallet.classic_address,
#             value="10000000000", # Large limit, arbitrarily chosen
#         )
#     )
#     ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
#         transaction=trust_set_tx,
#         wallet=receiver_wallet,
#         client=client,
#     )
#     logger.debug("Creating trust line from receiver address to issuer...")
#     response = xrpl.transaction.send_reliable_submission(ts_prepared, client)
#     logger.debug(response)

# @cli.command()
# @click.option('--issuer', help='issuer wallet infile')
# @click.option('--receiver', help='receiver wallet infile')
# @click.option('--amount', help='amount to send')
# def send_tokens(issuer, receiver, amount:int=100):
#     issuer_wallet = hydrate_wallet(issuer)
#     receiver_wallet = hydrate_wallet(receiver)

#     currency_code = config['XRP_CURRENCY_NAME']

#     # issue_quantity = "3840"
#     send_token_tx = xrpl.models.transactions.Payment(
#         account=issuer_wallet.classic_address,
#         destination=receiver_wallet.classic_address,
#         amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
#             currency=currency_code,
#             issuer=issuer_wallet.classic_address,
#             value=amount
#         )
#     )
#     pay_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
#         transaction=send_token_tx,
#         wallet=issuer_wallet,
#         client=client,
#     )
#     logger.debug(f"Sending {amount} {currency_code} to {receiver_wallet.classic_address}...")
#     response = xrpl.transaction.send_reliable_submission(pay_prepared, client)
#     logger.debug(response)    

if __name__ == '__main__':
    cli()
      