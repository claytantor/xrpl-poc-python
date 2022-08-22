
import os, sys

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

import ecdsa
import base64
import json
import time
from datetime import datetime as dt, timedelta
import bech32

from dotenv import load_dotenv
DROPS_IN_XRP=1000000

load_dotenv()  # take environment variables from .env.


def make_wallet(secret_seed):
    
    # Address: rU32wptoF4YPK3USvuYipUeDMqjF371B9J
    # Secret: ssZTE9S5fcphbVbcwnNd6RjbTkzA1
    # Balance: 1,000 XRP

    return Wallet(seed=secret_seed, sequence=16237283)
    # print(test_wallet.classic_address) # "rMCcNuTcajgw7YTgBy1sys3b89QqjUrMpH"

def drops_to_xrp(drops):
    return int(drops/DROPS_IN_XRP)


def get_account_info(address, client):
    acct_info = AccountInfo(
        account=address,
        ledger_index="current",
        queue=True,
        strict=True,
    )
    response = client.request(acct_info)
    result = response.result
    return result
    

def sign_msg(message, private_key, encoding='utf-8'):
    """Sign the message to be sent
    private_key: must be hex
    """
    # Get timestamp, round it, make it into a string and encode it to bytes
    # message = str(round(time.time()))
    # bmessage = message.encode()
    # SECP256K1
    # sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    # signature = base64.b64encode(sk.sign(message))
    # return signature, message 

    module = _ALGORITHM_TO_MODULE_MAP[CryptoAlgorithm.SECP256K1]
    message_bytes = message.encode(encoding)
    base64_bytes = base64.b64encode(message_bytes)
    base64_signature =  base64.b64encode(module.sign(base64_bytes, private_key))

    return base64_bytes.decode(encoding),base64_signature.decode(encoding)


def verify_msg(message, signature, public_key):
    module = _ALGORITHM_TO_MODULE_MAP[CryptoAlgorithm.SECP256K1]
    if not module.is_valid_message(message, signature, public_key):
        raise XRPLKeypairsException(
            "Derived keypair did not generate verifiable signature",
        )

def send_payment(wallet, amount_xrp, destination_address, client):
    # Prepare payment
    print(f"sending xrp:{amount_xrp} drops:{xrp_to_drops(xrp=amount_xrp)} to:{destination_address}")
    tx_payment = Payment(
        account=wallet.classic_address,
        # amount=xrp_to_drops(xrp=amount_xrp),
        amount=xrp_to_drops(amount_xrp),
        destination=destination_address,
    ) # send to my testnet xumm wallet

    # Sign the transaction
    tx_payment_signed = safe_sign_and_autofill_transaction(tx_payment, wallet, client)

    tx_response = send_reliable_submission(tx_payment_signed, client)
    # print(tx_response)
    return tx_response.status, tx_response.result

def generate_payment_request(amount, requesting_wallet, wallet_pub_key, wallet_private_key):
    # wallet_pub_key, wallet_private_key  = derive_keypair(os.getenv('WALLET_SECRET_R'))
    # print(len(wallet_private_key))

    expires = dt.now()+timedelta(minutes=60)

    payment_request = {
        'amount': amount,
        'public_key':wallet_pub_key,
        'address':requesting_wallet.classic_address,
        'expires':expires.timestamp()
    }
    json_str = json.dumps(payment_request)
    base64_message,base_64_sig  = sign_msg(json_str, wallet_private_key)
    payment_request=f"{base64_message}:{base_64_sig}"
    return payment_request

# Defining main function
def main():
    print("xrpl demo")
    # Define the network client
    # from xrpl.clients import JsonRpcClient

    # JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(os.getenv('JSON_RPC_URL'))
    receiving_wallet = Wallet(seed=os.getenv('WALLET_SECRET_R'), sequence=16237283)

    wallet_pub_key, wallet_private_key  = derive_keypair(os.getenv('WALLET_SECRET_R'))
    payment_request=generate_payment_request(212, receiving_wallet, 
        wallet_pub_key, wallet_private_key)
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
        account_info = get_account_info(receiving_wallet.classic_address, client=client)
        print(account_info)
        verify_msg(pr_parts[0].encode('utf-8'), sig, message_payload['public_key'])
        sender_wallet = generate_faucet_wallet(client, debug=True)
        # send from test wallet to the dest
        tx_response_status, tx_response_result = send_payment(
            wallet=sender_wallet, 
            amount_xrp=message_payload['amount'], 
            destination_address=message_payload['address'], 
            client=client)
        print(tx_response_status, tx_response_result)




    except Exception as e:
        print("=== COULD NOT VERIFY", e)


    # sender_wallet = generate_faucet_wallet(client, debug=True)
    # account_info = get_account_info(sender_wallet.classic_address, client=client)
   



    # print(receiving_wallet.public_key, wallet_private_key)
    # account_info = get_account_info(receiving_wallet.classic_address, client=client)
    # print(account_info)



    
    # Create a wallet using the testnet faucet:
    # https://xrpl.org/xrp-testnet-faucet.html
    # from xrpl.wallet import generate_faucet_wallet
    # test_wallet = generate_faucet_wallet(client, debug=True)
    # account_info = get_account_info(test_wallet.classic_address, client=client)


    # # account_addr = 'rBtXmAdEYcno9LWRnAGfT9qBxCeDvuVRZo'
    # account_info = get_account_info(test_wallet.classic_address, client=client)
    # # print(account_info)
    # xrp_in_account = drops_to_xrp(int(account_info['account_data']['Balance']))-10
    # print(f"===  {xrp_in_account} XRP in account: {test_wallet.classic_address}")

    # # {'account_data': {'Account': 'rBtXmAdEYcno9LWRnAGfT9qBxCeDvuVRZo', 'Balance': '2146000000', 'Flags': 0, 'LedgerEntryType': 'AccountRoot', 'OwnerCount': 0, 'PreviousTxnID': '9F533FF9355580D65A527E11E5CC6856372CF68317AFE4EB20B53E1C8DED454E', 'PreviousTxnLgrSeq': 23472630, 'Sequence': 16233962, 'index': 'FD66EC588B52712DCE74831DCB08B24157DC3198C29A0116AA64D310A58512D7'}, 'ledger_current_index': 30520694, 'queue_data': {'txn_count': 0}, 'validated': False}
    # # amount_xrp_to_send = int((int(account_info['account_data']['Balance'])-1000)/DROPS_IN_XRP)
    # # print(f"== sending {amount_xrp_to_send} XRP")
    
    # # send from test wallet to the dest
    # tx_response_status, tx_response_result = send_payment(wallet=test_wallet, amount_xrp=xrp_in_account,destination_address=os.getenv('WALLET_ADDRESS_1'), client=client)

    # # # now get the destination wallet account info
    # dest_account = get_account_info(os.getenv('WALLET_ADDRESS_1'), client)
    # xrp_in_account_dest = drops_to_xrp(int(dest_account['account_data']['Balance']))
    # print(f"===  {xrp_in_account_dest} XRP in account: {os.getenv('WALLET_ADDRESS_1')}")

  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()