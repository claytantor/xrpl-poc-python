from typing import Optional
from pydantic import BaseModel

# ===== schemas
class MessageSchema(BaseModel):
    message: str

class ApiInfoSchema(BaseModel):
    version: str


class OAuth2AuthSchema(BaseModel):
    grant_type: str
    username: str
    password: str

class OAuth2TokenSchema(BaseModel):
    access_token: str
    # token_type: str
    # expires_in: int



class XrpAccountDataSchema(BaseModel):

#   "account_data": {
#     "Account": "rGsFLmyy5gggTV2MtaYua7sGXoHa7z5HAG",
#     "Balance": "1055560000",
#     "Flags": 0,
#     "LedgerEntryType": "AccountRoot",
#     "OwnerCount": 0,
#     "PreviousTxnID": "C1CCC88ACF57CA7B449C51717516A79E087F9BE4CC832D78B49731C1A7475CD1",
#     "PreviousTxnLgrSeq": 30742316,
#     "Sequence": 30687688,
#     "index": "65BFF5E8BB98C59AFC7A8ADAC3129524FD8CABC9BD033FD4F1F6DE0DAC77E751"
#   },
    Account: str
    Balance: str
    Flags: int
    LedgerEntryType: str
    OwnerCount: int
    PreviousTxnID: str
    PreviousTxnLgrSeq: int
    Sequence: int
    index: str

class XrpNetworkSchema(BaseModel):
    # 's.devnet.rippletest.net':{  
    #     'json_rpc':'https://s.devnet.rippletest.net:51234',
    #     'websocket':'wss://s.devnet.rippletest.net:51233',
    #     'type':'devnet',
    # },
    json_rpc: str
    websocket: str
    type: str
    domain: str

class PaymentRequestSchema(BaseModel):
    xrp_amount: float
    memo: str


# 'txjson': {
#                 'TransactionType' : 'Payment',
#                 'Destination' : wallet.classic_address,
#                 'Amount': str(xrp_to_drops(paymentRequest.xrp_amount)),
#         },
#         "custom_meta": {
#             "identifier": f"payment_request:{pr_hash}",
#             "blob": json.dumps(payment_request_dict),
#             "instruction": paymentRequest.memo
#         }

# class XummTxJsonSchema(BaseModel):
#     TransactionType: str
#     Destination: str
#     Amount: str

# class XummCustomMetaSchema(BaseModel):
#     identifier: str
#     blob: str
#     instruction: str

# class XummPayloadSchema(BaseModel):
#     txjson: XummTxJsonSchema
#     custom_meta: XummCustomMetaSchema



class XummPayloadSchema(BaseModel):

    """
    {
  "payload_uuidv4": "22af42a9-8f62-4246-8000-9ff84f00d2c6",
  "is_signed": true,
  "txid": "FFF142299675D6D56AB83E4FE18C7366336BA0EB1DC044288B24DEC516336A38",
  "body": "{\"xrp_amount\": 36.30234668741087, \"amount_drops\": 36302346, \"address\": \"rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y\", \"network_endpoint\": \"https://s.altnet.rippletest.net:51234\", \"network_type\": \"testnet\", \"memo\": \"uppo\", \"request_hash\": \"hX5t3YXTThPr\"}"
}
    """
    xumm_payload_id: Optional[int]
    is_signed: bool
    payload_uuidv4: str
    created_at: Optional[str]
    updated_at: Optional[str]
    txid: Optional[str]
    body: Optional[dict]
    webhook_body: Optional[dict]

class WalletSchema(BaseModel):

    """
    {
    "wallet_id": 1,
    "classic_address": "rGsFLmyy5gggTV2MtaYua7sGXoHa7z5HAG",
    "created_at": "2021-12-22T19:10:25",
    "updated_at": "2021-12-22T19:10:25"
    }    
    """
    wallet_id: int
    classic_address: str
    created_at: str
    updated_at: str
    account_data: XrpAccountDataSchema
    xrp_network: XrpNetworkSchema

class XrpCurrencyRateSchema(BaseModel):

    fiatCurrencyI8NCode: str
    fiatCurrencyName: str
    fiatCurrencySymbol: str
    fiatCurrencyIsoDecimals: int
    xrpRate: float

