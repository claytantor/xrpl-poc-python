from typing import Optional, Any
from pydantic import BaseModel
from enum import Enum, IntEnum


# ===== xurl schemas
class XurlVersion(str, Enum):
    v1 = 'v1'

class NameValue(BaseModel):
    name: str
    value: str

    def __init__(self, **data: Any) -> None: 
        super().__init__(**data)

class XurlSubjectType(str, Enum):
    payment_item = 'paymentitem'
    order_invoice = 'orderinvoice'
    customer_account = 'customeraccount'
    postal_address = 'postaladdress'

class XurlSubject(BaseModel):
    type: XurlSubjectType
    uri: str

    def __init__(self, **data: Any) -> None: 
        super().__init__(**data)

class XurlVerbType(str, Enum):
    NOOP = 'NOOP'
    NOTIFY = 'NOTIFY'
    CARRY = 'CARRY'
    SHIP = 'SHIP'
    CREATEACCOUNT = 'CREATEACCOUNT'
    SHARE = 'SHARE'

class XurlVerb(BaseModel):
    type: XurlVerbType
    uri: Optional[str]
    description: Optional[str]

    def __init__(self, **data: Any) -> None: 
        super().__init__(**data)

class XurlType(str, Enum):
    payload = 'payload'
    verb = 'verb'
    subject = 'subject'

class Xurl(BaseModel):
    xurl_type: XurlType
    base_url: str
    version: XurlVersion
    subject_type: XurlSubjectType
    subject_id: str
    verb_type: XurlVerbType 
    parameters: Optional[list[NameValue]]   

    def __init__(self, **data: Any) -> None: 
        super().__init__(**data)

    def to_xurl(self)->str:
        if self.xurl_type == XurlType.payload:
            xurl = f"xurl://{self.xurl_type}/{self.subject_type}/{self.subject_id}/{self.verb_type}"
            if self.parameters:
                r_parameters = [f"{p.name}={p.value}" for p in self.parameters]
                r_parameters = "&".join(r_parameters)
                xurl = f"{xurl}?{r_parameters}"
            return xurl
        elif self.xurl_type == XurlType.verb:
            return f"xurl://{self.xurl_type}/{self.verb_type}"
        elif self.xurl_type == XurlType.subject:
            return f"xurl://{self.xurl_type}/{self.subject_type}/{self.subject_id}"
        else:
            raise Exception(f"Unknown xurl type: {self.xurl_type}")

class XurlClient(BaseModel):
    # https://rapaygo.com/.well-known/xurl.json?name=b9bcd
    well_known_domain: str
    name: str
    description: Optional[str]
    account_id: Optional[str]

class XurlCustomer(BaseModel):
    customer_id: int
    classic_address: str
    name: Optional[str]
    description: Optional[str]
    supported_verbs: Optional[list[XurlVerb]]

class XurlInfoSchema(BaseModel):
    version: str
    commit_sha: str
    api_branch: str
    endpoint: Optional[str]
    well_known_domain: Optional[str]
    shop_id: Optional[str]
    shop_name: Optional[str]
    shop_description: Optional[str]
    shop_logo: Optional[str]
    shop_url: Optional[str]
    shop_email: Optional[str]
    xurl_user: Optional[str]
    xurl_customer: Optional[XurlCustomer]


# ===== base schemas
class MessageSchema(BaseModel):
    message: str

class ApiInfoSchema(BaseModel):
    version: str
    commit_sha: str
    api_branch: str
    endpoint: Optional[str]
    shop_id: Optional[str]
    shop_name: Optional[str]
    shop_description: Optional[str]
    shop_logo: Optional[str]
    shop_url: Optional[str]
    shop_email: Optional[str]
    customer_account_id: Optional[str]

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

class WalletCreateSchema(BaseModel):
    # seed = Optional[str]
    # private_key = Optional[str]
    # public_key = Optional[str]
    classic_address: str

    def __init__(self, **data: Any) -> None: 
        super().__init__(**data)
        self.classic_address = data['classic_address']
        print("WalletCreateSchema.__init__", self.__dict__)
        

# class XurlVersion(str, Enum):
#     v1 = 'v1'

# class NameValue(BaseModel):
#     name: str
#     value: str

#     def __init__(self, **data: Any) -> None: 
#         super().__init__(**data)


# class XurlSubjectType(str, Enum):
#     payment_item = 'paymentitem'
#     order_invoice = 'orderinvoice'


# class XurlSubject(BaseModel):
#     subject_type: XurlSubjectType
#     uri: str

#     def __init__(self, **data: Any) -> None: 
#         super().__init__(**data)



# class Xurl(BaseModel):
#     base_url: str
#     version: XurlVersion
#     subject_type: XurlSubjectType
#     subject_id: str
#     verb_type: XurlVerbType 
#     parameters: Optional[list[NameValue]]   

#     def __init__(self, **data: Any) -> None: 
#         super().__init__(**data)



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

class ImageSchema(BaseModel):
    id: Optional[int]
    data_url: str
    file: Optional[dict]

class PaymentItemSchema(BaseModel):
    """
    {
        "images": [{
            "id": 3,
            "data_url": "https://s3.us-west-2.amazonaws.com/dev.xurlpay.org/uploaded_images/65c74114-c2c9-444b-9c6f-a579123fa77e.png"
        }],
        "id": 3,
        "name": "Tootsie Roll Chocolate Midgees",
        "description": "Tootsie Roll Chocolatey Twist Midgees Resealable Standup Bag, Peanut Free, Gluten Free original, Allergy Friendly, Mini Midgees",
        "sku_id": "bd209ac51b",
        "fiat_i8n_price": 0.19,
        "fiat_i8n_currency": "USD",
        "xurl": "https://xumm.app/detect/xapp:sandbox.32849dc99872?TransactionType=Payment&LookupType=PaymentItem&LookupRef=3"
    }
    """

    id: Optional[int] # update
    name: str
    description: str
    sku_id: Optional[str]
    fiat_i8n_price: float
    fiat_i8n_currency: str
    xurl: Optional[str]
    images: list[ImageSchema]
    verb: Optional[str]
    in_shop: Optional[bool]
    is_xurl_item: Optional[bool]
    is_stocked_item: Optional[bool]
    in_stock_count: Optional[int]
    on_backorder_count: Optional[int]

    def to_dict(self):
        return self.dict()
    

class TrustlineConversion(BaseModel):
    token_currency: str
    i8n_currency: str
    issuerAccount: str
    receiverAccount: str
    rate: float
    datetime: str
    txid: Optional[str]

class CustomerSchema(BaseModel):
    """
    {
        "customer_id": 1,
        "classic_address": "
        "created_at": "2021-12-22T19:10:25",
        "updated_at": "2021-12-22T19:10:25"
    }
    """
    id: Optional[int]
    classic_address: str
    shop_id: Optional[str]
    # created_at: str
    # updated_at: str

# 'id': self.id,
# 'name': self.name,
# 'first_name': self.first_name,
# 'last_name': self.last_name,
# 'street_address': self.street_address,
# 'street_address_2': self.street_address_2,
# 'zip_code': self.zip_code,
# 'city': self.city,
# 'state': self.state,
# 'country': self.country,
# 'phone_number': self.phone_number,
# 'postal_code': self.postal_code,
# 'created_at': str(self.created_at),
# 'updated_at': str(self.updated_at)
class AddressSchema(BaseModel):
    id: Optional[int]
    name: Optional[str]
    first_name: str
    last_name: str
    street_address: str
    street_address_2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str
    phone_number: str

# id = Column(Integer, primary_key=True)
#     wallet_id = Column(Integer, ForeignKey('wallet.id'))
#     address_id = Column(Integer, ForeignKey('address.id'))
#     shop_id = Column(String)
#     well_known_uri = Column(String)
class PostalAddressSchema(BaseModel):
    id: Optional[int]
    wallet_id: Optional[int]
    address_id: Optional[int]
    shop_id: Optional[str]
    well_known_uri: Optional[str]

    
