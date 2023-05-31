
from dotenv import dotenv_values
from api.rsa_encrypt import extract_public_key, rsa_encrypt
from api.s3utils import save_image
from api.serializers import PaymentItemDetailsSerializer, PostalAddressSerializer
from api.xqr import generate_qr_code
import io
from pydoc import describe
from typing import Union
import uuid
from http import HTTPStatus
import os
import requests
import json
import shortuuid
import json
import xrpl
import base64
from datetime import datetime as dt, timedelta
import xumm
import asyncio
from PIL import Image

from xrpl.models.requests import Ledger, Tx
from xrpl.models.transactions import NFTokenMintFlag


from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import JSONResponse, Response, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session



from api.schema import AddressSchema, CustomerSchema, MessageSchema, ApiInfoSchema, OAuth2AuthSchema, OAuth2TokenSchema, PaymentItemSchema, PaymentRequestSchema, PostalAddressSchema, Xurl, XurlSubjectType, XurlVerbType, WalletCreateSchema, WalletSchema, XrpCurrencyRateSchema, XummPayloadSchema, XurlVersion
from api.models import Address, CustomerAccount, InventoryItem, InventoryItemImage, Message, ApiInfo, PaymentItem, PostalAddress, Wallet, XrpCurrencyRate, XummPayload
from api.decorators import verify_user_jwt_scopes
from api.jwtauth import make_signed_token, get_token_body
from api.dao import AddressDao, CustomerAccountDao, InventoryItemDao, PaymentItemDao, PostalAddressDao, XummPayloadDao, get_db, WalletDao
from api.utils import parse_shop_url, parse_xurl
from api.xrpcli import get_account_info, get_rpc_network_from_wss, get_rpc_network_type, get_xrp_network_from_jwt, xrp_to_drops, get_xapp_tokeninfo, get_wss_network_type, get_rpc_network_from_jwt
from api.pinatautils import pinata_get_pin, pinata_pin_dict


import logging
ulogger = logging.getLogger("uvicorn.error")

router = APIRouter()


config = {
    # load shared development variables
    **dotenv_values(os.getenv("APP_CONFIG")),
    **os.environ,  # override loaded values with environment variables
}


xrpl_url = config['XRP_NETWORK_ENDPOINT']
client = xrpl.clients.JsonRpcClient(xrpl_url)

sdk = xumm.XummSdk(config['XUMM_API_KEY'], config['XUMM_API_SECRET'])

scopes = {
    'wallet_owner': [
        'wallet.view',
        'wallet.transfer',
        'wallet.sign',
        'wallet.receive',
        'wallet.request'],
    'wallet_owner_refresh': ['wallet.refresh'],
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config['API_TOKEN_PATH'])


@router.get("/xurl-shop-jwks.json")
def get_api_info():
    # ulogger.info(f"get_api_info {ApiInfo().to_dict()}")
    # return ApiInfo().to_dict()

    key = {
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
    return JSONResponse(key)


@router.get("/info", tags=["ApiInfo"], response_model=ApiInfoSchema, status_code=200)
def get_api_info():
    ulogger.info(f"get_api_info {ApiInfo().to_dict()}")
    return ApiInfo().to_dict()


@router.post("/token", tags=["Auth"], response_model=OAuth2TokenSchema, status_code=200)
def auth_token(username: str = Form(), password: str = Form()):
    ulogger.info(f"get_spoof_token {username} {password}")
    jwt_token = make_signed_token(
        password, {'sub': username, 'net': config['XRP_WS_NET']})
    return {"access_token": jwt_token}


@router.get("/wallet", tags=["Wallet"], response_model=WalletSchema, status_code=200)
@verify_user_jwt_scopes(scopes['wallet_owner'])
async def get_wallet(request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # ulogger.info(f"get_wallet {token}")
    jwt_body = get_token_body(token)
    ulogger.info(f"body {json.dumps(jwt_body, indent=4)}")

    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        # return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})
        ulogger.error(f"get_wallet wallet not found")
        create_item = WalletCreateSchema(classic_address=jwt_body['sub'])
        wallet = WalletDao.create(db, create_item)

    ulogger.info(f"get_wallet {wallet.to_dict()}")

# {
#     "client_id": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#     "scope": "XummPkce",
#     "aud": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#     "sub": "r9DvujRNfGrZr4nBjudEJJWFBNfkDfcwNA",
#     "email": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce+r9DvujRNfGrZr4nBjudEJJWFBNfkDfcwNA@xumm.me",
#     "app_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#     "app_name": "dev-xurlpay",
#     "payload_uuidv4": "4dbbb16e-d651-47c5-ba24-c9b90237964c",
#     "usertoken_uuidv4": "4de21968-8c2f-4fb3-9bb6-94b589a13a8c",
#     "network_type": "TESTNET",
#     "network_endpoint": "wss://testnet.xrpl-labs.com",
#     "iat": 1674590544,
#     "exp": 1674676944,
#     "iss": "https://oauth2.xumm.app"
# }
    try:
        xrp_network = get_xrp_network_from_jwt(jwt_body)
        account_info = await get_account_info(jwt_body['sub'], xrp_network.json_rpc)

        wallet_dict = wallet.to_dict()
        wallet_dict['account_data'] = account_info['account_data']
        wallet_dict['xrp_network'] = xrp_network.to_dict()
        return JSONResponse(status_code=HTTPStatus.OK, content=wallet_dict)

    except Exception as e:
        ulogger.error(f"get_wallet {e}")
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": str(e)})


@router.get("/xrp/price/{fiat_i8n_currency}", tags=["XRP"], response_model=XrpCurrencyRateSchema, status_code=200)
# @verify_user_jwt_scopes(scopes['wallet_owner'])
def xrp_price_from_currency(fiat_i8n_currency: str, request: Request, db: Session = Depends(get_db)):

    ulogger.info(f"get_xrp_price {fiat_i8n_currency}")
    rates = sdk.get_rates(fiat_i8n_currency).to_dict()
    ulogger.info(f"rates: {rates}")

    rate_dict = XrpCurrencyRate(
        fiatCurrencyI8NCode=fiat_i8n_currency,
        fiatCurrencyName=rates['__meta']['currency']['en'],
        fiatCurrencySymbol=rates['__meta']['currency']['symbol'],
        fiatCurrencyIsoDecimals=rates['__meta']['currency']['isoDecimals'],
        xrpRate=rates['XRP'],
    ).to_dict()

    return rate_dict


@router.post("/wallet", tags=["Wallet"], response_model=WalletSchema, status_code=200)
@verify_user_jwt_scopes(scopes['wallet_owner'])
def post_create_wallet():
    pass
#     jwt_body = get_token_body(dict(request.headers)[
#                               "Authorization"].replace("Bearer ", ""))

#     wallet = db.session.query(Wallet).filter_by(
#         classic_address=jwt_body['sub']).first()
#     if wallet is None:
#         # create a new wallet
#         wallet = make_wallet(classic_address=jwt_body['sub'])


#     rpc_network = get_rpc_network_from_wss(jwt_body['net'])
#     account_info = get_account_info(wallet.classic_address, rpc_network)

#     return jsonify({
#         'classic_address': wallet.classic_address,
#         'wallet_info': jwt_body,
#         'account_data': account_info}), 200


@router.get("/payload", tags=["Xumm"], response_model=list[XummPayloadSchema], status_code=200)
@verify_user_jwt_scopes(scopes['wallet_owner'])
def get_wallet_payloads(request: Request,
                        db: Session = Depends(get_db),
                        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)

    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payloads = XummPayloadDao.fetch_by_wallet_id(db=db, wallet_id=wallet.id)
    return JSONResponse(status_code=HTTPStatus.OK, content=[p.to_dict() for p in payloads])


@router.put("/payload", tags=["Xumm"], response_model=XummPayloadSchema, status_code=200)
@verify_user_jwt_scopes(scopes['wallet_owner'])
def update_wallet_payload(
        payloadRequest: XummPayloadSchema,
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)

    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    # ulogger.info(f"update_wallet_payload {payloadRequest}")
    payload_exists = XummPayloadDao.fetch_by_wallet_payload_uuidv4(
        db=db, wallet_id=wallet.id, payload_uuidv4=payloadRequest.payload_uuidv4)

    if payload_exists is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "payload does not belong to wallet"})

    py_r = payloadRequest.dict()
    ulogger.info(f"update_wallet_payload {py_r}")
    payload_exists.from_dict(py_r)
    payload_exists.set_is_signed_bool(py_r['is_signed'])
    payload = XummPayloadDao.update(db=db, payload=payload_exists)

    return payload.to_dict()


@router.post("/pay_request", tags=["Xumm"], response_model=XummPayloadSchema, status_code=200)
@verify_user_jwt_scopes(scopes['wallet_owner'])
def create_pay_request(
        paymentRequest: PaymentRequestSchema,
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    pr_hash = shortuuid.uuid()[:12]
    payment_request_dict = {
        'xrp_amount': paymentRequest.xrp_amount,
        'amount_drops': int(xrp_to_drops(paymentRequest.xrp_amount)),
        'address': wallet.classic_address,
        'network_endpoint': get_rpc_network_from_jwt(jwt_body),
        'network_type': get_rpc_network_type(get_rpc_network_from_jwt(jwt_body)),
        'memo': paymentRequest.memo,
        'request_hash': pr_hash,
    }

    # json_str = json.dumps(payment_request_dict)
    # base64_message, base_64_sig = self.sign_msg(json_str)
    # payment_request=f"{base64_message}:{base_64_sig}"
    # return payment_request_dict, payment_request

    create_payload = {
        'txjson': {
            'TransactionType': 'Payment',
            'Destination': wallet.classic_address,
            'Amount': str(xrp_to_drops(paymentRequest.xrp_amount)),
        },
        "custom_meta": {
            "identifier": f"payment_request:{pr_hash}",
            "blob": json.dumps(payment_request_dict),
            "instruction": paymentRequest.memo
        }
    }

    created = sdk.payload.create(create_payload)
    xumm_payload = created.to_dict()
    m_payload = XummPayload(payload_body=json.dumps(xumm_payload),
                            wallet_id=wallet.id,
                            payload_uuidv4=xumm_payload['uuid'])

    db.add(m_payload)
    db.commit()

    return m_payload.to_dict()


def save_images(db: Session, images_list: dict, inventory_item: InventoryItem):
    for image in images_list:
        ulogger.info(f"SAVING IMAGE {image}")
        # {'data_url': 'https://s3.us-west-2.amazonaws.com/dev.rapaygo.com/uploaded_images/c053789c-4d0a-4dc2-a175-39eb0d694d6f.png', 'id': 28}
        if 'id' not in image or image['id'] is None:

            im = Image.open(io.BytesIO(base64.b64decode(
                image['data_url'].split(',')[1])))
            file_name = f"{uuid.uuid4()}.png"

            url_saved = save_image(im, config["AWS_BUCKET_NAME"],
                                   f"{config['AWS_UPLOADED_IMAGES_PATH']}/{file_name}")

            url_saved = f'https://s3.us-west-2.amazonaws.com/{config["AWS_BUCKET_NAME"]}/uploaded_images/{file_name}'

            inventory_item_image = InventoryItemImage(
                type="InventoryItemImage", file_path=url_saved, file_name=file_name, file_size=0, original_name=file_name)

            db.add(inventory_item_image)
            inventory_item.images = [inventory_item_image]

            db.commit()

        elif 'file_path' in image:
            payment_item_image = InventoryItemImage.query.filter_by(
                id=image['id']).first()
            payment_item_image.file_path = image['file_path']
            payment_item_image.file_name = image['file_name']
            payment_item_image.original_name = image['original_name']
            payment_item_image.file_size = image['file_size']

            db.commit()


@router.get('/payment_item/shop/{user_address}')
def get_payment_items_by_user_address(user_address: str, request: Request, db: Session = Depends(get_db)):
    wallet = WalletDao.fetch_by_classic_address(db, user_address)
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_items = PaymentItemDao.fetch_all_by_wallet_id(db, wallet.id)

    return JSONResponse(status_code=HTTPStatus.OK, content=[PaymentItemDetailsSerializer(payment_item, shop_id=wallet.shop_id).serialize() for payment_item in payment_items])


@router.get('/payment_item')
@verify_user_jwt_scopes(scopes['wallet_owner'])
def get_payment_items(request: Request,
                      db: Session = Depends(get_db),
                      token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_items = PaymentItemDao.fetch_all_by_wallet_id(db, wallet.id)

    return JSONResponse(status_code=HTTPStatus.OK, content=[PaymentItemDetailsSerializer(payment_item, shop_id=wallet.shop_id).serialize() for payment_item in payment_items])


@router.delete('/payment_item/{id}')
@verify_user_jwt_scopes(scopes['wallet_owner'])
def delete_payment_item_by_id(id: int,
                              request: Request,
                              db: Session = Depends(get_db),
                              token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_item = PaymentItemDao.fetch_single_by_wallet_id(
        db, id=id, wallet_id=wallet.id)
    if payment_item is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})

    PaymentItemDao.delete(db, payment_item)

    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "payment item deleted"})


@router.get('/payment_item/{id}')
def get_payment_item_by_id(id: int,
                           request: Request,
                           db: Session = Depends(get_db),
                           token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_item = PaymentItemDao.fetch_single_by_wallet_id(
        db, wallet_id=wallet.id, payment_item_id=id)

    if payment_item is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})

    return JSONResponse(status_code=HTTPStatus.OK, content=PaymentItemDetailsSerializer(payment_item, shop_id=wallet.shop_id).serialize())


def make_create_account_payload(xurl: Xurl, shop_wallet: Wallet, verb: str):

    return {
        'txjson': {
            'TransactionType': 'Payment',
            'Destination': shop_wallet.classic_address,
            'Amount': str(xrp_to_drops(0.1)),
        },
        "custom_meta": {
            "identifier": f"create_account:{shortuuid.uuid()[:12]}",
            "blob": json.dumps({'shop_id': shop_wallet.shop_id, 'xurl': xurl.to_xurl()}),
            "instruction": f"Sign payment of 0.1 XRP to create a customer account with shop {shop_wallet.shop_id}"
        }
    }

def make_share_postal_address_payload(xurl: Xurl, shop_wallet: Wallet, customer_wallet: Wallet, ipfsHash: str, postal_address: PostalAddress):

    address_memo = xrpl.models.transactions.Memo(
        memo_format=xrpl.utils.str_to_hex("application/json"), 
        memo_data=xrpl.utils.str_to_hex(json.dumps({
            "type":"PostalAddressHandle",
            "body":{
                'postalAddressId':postal_address.id
            }
        })))

    tx_memos = [address_memo]

    nft_uri = f"ipfs://{ipfsHash}"
    ulogger.info(f"nft uri {nft_uri}")

    flags=[NFTokenMintFlag.TF_BURNABLE, NFTokenMintFlag.TF_TRANSFERABLE],

    # lets mint the nft

    # mint_nft_tx = xrpl.models.transactions.NFTokenMint(
    #         nftoken_taxon=0,
    #         account=issuer.get_wallet().classic_address,
    #         uri=uri.encode(
    #             'utf-8').hex().upper(),
    #         flags=[NFTokenMintFlag.TF_BURNABLE, NFTokenMintFlag.TF_TRANSFERABLE]
    #     )
    nft_mint_tx = xrpl.models.transactions.NFTokenMint(
        account=customer_wallet.classic_address,
        uri=xrpl.utils.str_to_hex(nft_uri),
        flags=NFTokenMintFlag.TF_BURNABLE,
        # transfer_fee=1000,
        nftoken_taxon=0,
        memos=tx_memos
    )

    create_payload = {
        'uuid': uuid.uuid4().hex,
        'txjson': nft_mint_tx.to_xrpl(),
        'custom_meta': {
            'identifier': f'mintPostalAddressNft_{uuid.uuid4().hex[:8]}',
            'instruction':'Please sign this transaction to mint and share the postal address NFT.'
        }
    }

    return create_payload


def make_payment_item_payload(
        xurl: Xurl,
        payment_item: PaymentItem,
        wallet: Wallet):

    # @TODO: support qty
    qty = 1

    ulogger.info(
        f"get_xrp_price {payment_item.fiat_i8n_currency} {payment_item.fiat_i8n_price}")
    rates = sdk.get_rates(payment_item.fiat_i8n_currency).to_dict()
    ulogger.info(f"rates: {rates}")
    xrp_price = rates['XRP']
    xrp_amount = (payment_item.fiat_i8n_price / xrp_price)*qty

    payment_request_dict = {
        'type': 'payment_item',
        'id': payment_item.id,
        'xrp_quote': xrp_price,
        'fiat_i8n_currency': payment_item.fiat_i8n_currency,
        'fiat_i8n_price': payment_item.fiat_i8n_price,
        'request_hash': shortuuid.uuid(),
        'network_endpoint': config['XRP_NETWORK_ENDPOINT'],
        'network_type': config['XRP_NETWORK_TYPE'],
        'xurl': xurl.to_xurl()
    }

    if qty > 1:
        payment_request_dict['qty'] = qty

    return {
        'txjson': {
            'TransactionType': 'Payment',
            'Destination': wallet.classic_address,
            'Amount': str(xrp_to_drops(xrp_amount)),
        },
        "custom_meta": {
            "identifier": f"payment_item:{shortuuid.uuid()[:12]}",
            "blob": json.dumps(payment_request_dict),
            "instruction": f"Pay {payment_item.fiat_i8n_price} {payment_item.fiat_i8n_currency} each for {qty} {payment_item.inventory_item.name}"
        }
    }


# def make_xumm_payment_item_payload_response(xurl:Xurl, payment_item:PaymentItem, db: Session):

#     # # get the wallet for this payment item
#     wallet = db.query(Wallet).filter_by(id=payment_item.wallet_id).first()
#     if wallet is None:
#         return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "payment item wallet not found"})

#     created = sdk.payload.create(
#         make_payment_item_payload(
#         xurl=xurl, payment_item=payment_item, wallet=wallet))
#     xumm_payload = created.to_dict()
#     p_xumm_payload = XummPayload(payload_body=json.dumps(xumm_payload),
#                             wallet_id=wallet.id,
#                             payload_uuidv4=xumm_payload['uuid'])

#     db.add(p_xumm_payload)
#     db.commit()

#     # return xumm_payload
#     ulogger.info(f"xumm_payload:{xumm_payload}")
#     return RedirectResponse(xumm_payload['next']['always'])


@router.post('/payment_item')
@verify_user_jwt_scopes(['wallet_owner'])
def create_payment_item(
        paymentItem: PaymentItemSchema,
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    inventory_item = InventoryItem()
    inventory_item.sku_id = shortuuid.uuid()[:12]
    inventory_item.wallet_id = wallet.id
    inventory_item.name = paymentItem.name
    inventory_item.description = paymentItem.description
    inventory_item.is_stocked_item = 1
    inventory_item.in_stock_count = 0
    inventory_item.on_backorder_count = 0
    inventory_item.created_at = dt.now()

    images_list = [{'id': image.id, 'data_url': image.data_url}
                   for image in paymentItem.images]
    save_images(db=db, images_list=images_list, inventory_item=inventory_item)

    # save the inventory item
    inventory_item = InventoryItemDao.create(
        db=db, inventory_item=inventory_item)

    payment_item = PaymentItem()
    payment_item.inventory_item = inventory_item
    payment_item.wallet_id = wallet.id
    payment_item.inventory_item.name = paymentItem.name
    payment_item.inventory_item.description = paymentItem.description
    payment_item.fiat_i8n_currency = paymentItem.fiat_i8n_currency
    payment_item.fiat_i8n_price = paymentItem.fiat_i8n_price
    payment_item.verb = paymentItem.verb
    payment_item.in_shop = 0
    payment_item.inventory_item.is_stocked_item = paymentItem.is_stocked_item
    payment_item.inventory_item.in_stock_count = paymentItem.in_stock_count
    payment_item.inventory_item.on_backorder_count = paymentItem.on_backorder_count
    payment_item.inventory_item.sku_id = paymentItem.sku_id
    payment_item.inventory_item.updated_at = dt.now()
    payment_item.inventory_item.created_at = dt.now()

    pi = PaymentItemDao.create(db=db, payment_item=payment_item)
    return JSONResponse(status_code=HTTPStatus.OK, content=PaymentItemDetailsSerializer(pi, shop_id=wallet.shop_id).serialize())


@router.put('/payment_item')
@verify_user_jwt_scopes(['wallet_owner'])
def update_payment_item(
        paymentItem: PaymentItemSchema,
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_item = PaymentItemDao.fetch_single_by_wallet_id(
        db, paymentItem.id, wallet.id)
    if payment_item is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})

    # update the inventory item also
    payment_item.inventory_item.name = paymentItem.name
    payment_item.inventory_item.description = paymentItem.description
    payment_item.fiat_i8n_currency = paymentItem.fiat_i8n_currency
    payment_item.fiat_i8n_price = paymentItem.fiat_i8n_price
    payment_item.verb = paymentItem.verb
    payment_item.in_shop = paymentItem.in_shop
    # payment_item.is_xurl_item = paymentItem.is_xurl_item
    payment_item.inventory_item.is_stocked_item = paymentItem.is_stocked_item
    payment_item.inventory_item.in_stock_count = paymentItem.in_stock_count
    payment_item.inventory_item.on_backorder_count = paymentItem.on_backorder_count
    payment_item.inventory_item.sku_id = paymentItem.sku_id
    payment_item.inventory_item.updated_at = dt.now()

    if paymentItem.is_xurl_item:
        payment_item.is_xurl_item = 1
    else:
        payment_item.is_xurl_item = 0

    images_list = [{'id': image.id, 'data_url': image.data_url}
                   for image in paymentItem.images]
    save_images(db=db, images_list=images_list,
                inventory_item=payment_item.inventory_item)

    payload = PaymentItemDao.update(db=db, payment_item=payment_item)
    return JSONResponse(status_code=HTTPStatus.OK, content=PaymentItemDetailsSerializer(payload, shop_id=wallet.shop_id).serialize())

# ADDRESS


@router.post('/address')
@verify_user_jwt_scopes(['wallet_owner'])
def create_address(addressInfo: AddressSchema,
                   request: Request,
                   db: Session = Depends(get_db),
                   token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    address = Address(
        wallet_id=wallet.id,
        name=addressInfo.name,
        first_name=addressInfo.first_name,
        last_name=addressInfo.last_name,
        street_address=addressInfo.street_address,
        street_address_2=addressInfo.street_address_2,
        city=addressInfo.city,
        state=addressInfo.state,
        country=addressInfo.country,
        postal_code=addressInfo.postal_code,
        phone_number=addressInfo.phone_number)

    payload = AddressDao.create(db=db, address=address)

    return JSONResponse(status_code=HTTPStatus.OK, content=payload.serialize())


@router.get('/address')
def get_address(
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payload = AddressDao.fetch_by_wallet_id(db=db, wallet_id=wallet.id)

    return JSONResponse(status_code=HTTPStatus.OK, content=[address.serialize() for address in payload])


@router.get('/address/{id}')
def get_address_by_id(id: int,
                      request: Request,
                      db: Session = Depends(get_db),
                      token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payload = AddressDao.fetch_by_id(db=db, address_id=id)

    if payload is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "address not found"})

    address_s = payload.serialize()
    address_s['postal_addresses'] = [PostalAddressSerializer(
        pa).serialize() for pa in payload.postal_addresses]

    # ulogger.info(f"get_address_by_id {payload.serialize()}")
    return JSONResponse(status_code=HTTPStatus.OK,
                        content=address_s)


# PostalAddress =============================================================================================

@router.post('/postal_address')
@verify_user_jwt_scopes(['wallet_owner'])
def create_postal_address(postalAddress: PostalAddressSchema,
                          request: Request,
                          db: Session = Depends(get_db),
                          token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    well_known_uri = f"http://{postalAddress.shop_id}.localhost:5005/.well-known/xurl-shop-jwks.json?shop_id={postalAddress.shop_id}"

    postalAddress = PostalAddress(
        wallet_id=wallet.id,
        address_id=postalAddress.address_id,
        shop_id=postalAddress.shop_id,
        well_known_uri=well_known_uri)

    payload = PostalAddressDao.create(db=db, postal_address=postalAddress)

    return JSONResponse(status_code=HTTPStatus.OK, content=payload.serialize())


# @router.get('/postal_address')
# @verify_user_jwt_scopes(['wallet_owner'])
# def get_postal_addresses(
#     request: Request,
#     db: Session = Depends(get_db),
#     token: str = Depends(oauth2_scheme)):

#     jwt_body = get_token_body(token)
#     wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
#     if wallet is None:
#         return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})


#     well_known_uri=f"http://{postalAddress.shop_id}.localhost:5005/.well-known/xurl-shop-jwks.json?shop_id={postalAddress.shop_id}"

#     postalAddress = PostalAddress(
#         wallet_id=wallet.id,
#         address_id=postalAddress.address_id,
#         shop_id=postalAddress.shop_id,
#         well_known_uri=well_known_uri)

#     payload = PostalAddressDao.create(db=db, postal_address=postalAddress)

#     return JSONResponse(status_code=HTTPStatus.OK, content=payload.serialize())


# CUSTOMER =============================================================================================
@router.post("/l/customer_account")
@verify_user_jwt_scopes(['wallet_owner'])
def create_customer(
        customer: CustomerSchema,
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    ulogger.info(f"create_customer: {customer}")

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_shopid(db, shop_id=customer.shop_id)
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    customer_wallet = WalletDao.fetch_by_classic_address(
        db, customer.classic_address)
    if customer_wallet is None:
        wallet_c = WalletCreateSchema(classic_address=customer.classic_address)
        account_wallet = WalletDao.create(db=db, item=wallet_c)
    else:
        account_wallet = customer_wallet

    # see if the customer already exists
    customer = CustomerAccountDao.fetch_by_account_wallet_id(
        db, account_wallet.id)
    if customer is not None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "customer already exists"})

    customer_account = CustomerAccount()
    customer_account.account_wallet_id = account_wallet.id
    customer_account.wallet_id = wallet.id
    customer_account = CustomerAccountDao.create(
        db=db, customer_account=customer_account)
    return JSONResponse(status_code=HTTPStatus.OK, content=customer_account.serialize())


@router.post("/customer_account")
@verify_user_jwt_scopes(['wallet_owner'])
def create_customer(
        customer: CustomerSchema,
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    customer_wallet = WalletDao.fetch_by_classic_address(
        db, customer.classic_address)
    if customer_wallet is None:
        wallet_c = WalletCreateSchema(classic_address=customer.classic_address)
        # wallet_c.classic_address = customer.classic_address
        account_wallet = WalletDao.create(db=db, item=wallet_c)
    else:
        account_wallet = customer_wallet

        # see if the customer already exists
    customer = CustomerAccountDao.fetch_by_account_wallet_id(
        db, account_wallet.id)
    if customer is not None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "customer already exists"})

    customer_account = CustomerAccount()
    customer_account.account_wallet_id = account_wallet.id
    customer_account.wallet_id = wallet.id
    customer_account = CustomerAccountDao.create(
        db=db, customer_account=customer_account)
    return JSONResponse(status_code=HTTPStatus.OK, content=customer_account.serialize())


# get customer accounts for a wallet
@router.get("/customer_account")
@verify_user_jwt_scopes(['wallet_owner'])
def get_customer_accounts(
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    customer_accounts = CustomerAccountDao.fetch_by_wallet_id(
        db, wallet_id=wallet.id)
    ulogger.info(f"customer_accounts: {customer_accounts} {wallet.id}")
    if customer_accounts is None:
        customer_accounts = []
    return JSONResponse(status_code=HTTPStatus.OK, content=[customer_account.serialize() for customer_account in customer_accounts])

# get customer accounts for a wallet


@router.get("/customer_shop")
@verify_user_jwt_scopes(['wallet_owner'])
def get_customer_shop(
        request: Request,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    # customer_accounts = CustomerAccountDao.fetch_by_account_wallet_id(db, account_wallet_id=wallet.id)
    # ulogger.info(f"customer_accounts: {customer_accounts} {wallet.id}")
    # shop_wallets = []
    # if customer_accounts is not None:
    #     for customer_account in customer_accounts:
    #         ulogger.info(f"customer_account: {customer_account.serialize()}")
    #         shop_wallet = WalletDao.fetch_by_id(db, _id=customer_account.wallet_id)
    #         shop_wallets.append(shop_wallet)
    customer_account = CustomerAccountDao.fetch_by_account_wallet_id(
        db, account_wallet_id=wallet.id)
    shop_wallet = WalletDao.fetch_by_id(db, _id=customer_account.wallet_id)

    return JSONResponse(status_code=HTTPStatus.OK, content=[shop_wallet.serialize()])


# XUMM =================================================================================================


@router.post("/xumm/webhook")
async def xumm_webhook(request: Request, db: Session = Depends(get_db)):

    json_body = await request.json()

    if json_body['payloadResponse']['signed'] == True:
        ulogger.info("==== xumm webhook payload is signed")

        # get the xumm payload by the payload_uuidv4
        payload = XummPayloadDao.fetch_by_payload_uuidv4(db=db,
                                                         payload_uuidv4=json_body['payloadResponse']['payload_uuidv4'])

        if payload is None:
            # return jsonify({'message': 'payload not found'}), 404
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payload not found"})

        # dont run this if the payload is already processed
        if not payload.is_signed:
            payload.set_is_signed_bool(json_body['payloadResponse']['signed'])
            payload.txid = json_body['payloadResponse']['txid']
            payload.webhook_body = json.dumps(json_body)
            db.commit()

            # now take the payload and process it
            ulogger.info("==== xumm webhook payload is signed, processing")
            await _process_payload_verb(payload=payload, db=db)

    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "ok"})


# def send_slack_message(message):
#     """Send a message to slack"""
#     ulogger.info(f"==== send_slack_message: {message} to {app.config['SLACK_WEBHOOK_URL']}")
#     try:
#         slack_data = {'text': message}
#         response = requests.post(
#             app.config['SLACK_WEBHOOK_URL'], data=json.dumps(slack_data),
#             headers={'Content-Type': 'application/json'}
#         )
#         if response.status_code != 200:
#             ulogger.error(f"==== slack webhook error: {response.status_code}")
#     except Exception as e:
#         app.log_exception(f"==== slack webhook error: {e}")

async def _process_payload_verb(payload: XummPayload,
                                db: Session = Depends(get_db)):

    ulogger.info(f"==== _process_payload_verb from payload.")

    # get the payload body
    payload_body = json.loads(payload.webhook_body)

    ulogger.info(f"==== payload_body: {payload_body}")

    # determine the verb type from the payload custom_meta
    custom_meta = json.loads(payload_body['custom_meta']['blob'])
    tx_id = payload_body['payloadResponse']['txid']

    # get the xurl
    xurl = custom_meta['xurl']
    shop_id = custom_meta['shop_id']
    uri_base = f'{config["XURL_BASEURL"].replace("{shop_id}", shop_id)}'
    xurl_p = parse_xurl(base_url=uri_base, xurl=xurl)

    if xurl_p.verb_type.lower() == XurlVerbType.NOOP.lower():
        ulogger.info(f"==== no_op verb, ignoring")
        return
    elif xurl_p.verb_type.lower() == XurlVerbType.CREATEACCOUNT.lower():
        ulogger.info(f"==== create_account verb, processing")
        # _process_create_account_verb(payload=payload, xurl=xurl_p, db=db)

        # get the tx from the blockchain
        onchain_r = await client.request_impl(Tx(
            transaction=tx_id
        ))
        onchain_tx = onchain_r.to_dict()

        ulogger.info(f"==== onchain_tx: {onchain_tx}")

        # get the destination address
        customer_account_address = onchain_tx['result']['Account']
        shop_wallet = WalletDao.fetch_by_classic_address(
            db=db, classic_address=onchain_tx['result']['Destination'])
        if onchain_tx['status'] == 'success' and shop_wallet is not None:
            pass
            customer_wallet = WalletDao.fetch_by_classic_address(
                db, customer_account_address)
            if customer_wallet is None:
                wallet_c = WalletCreateSchema(
                    classic_address=customer_account_address)
                account_wallet = WalletDao.create(db=db, item=wallet_c)
            else:
                account_wallet = customer_wallet

            # see if the customer already exists
            customer = CustomerAccountDao.fetch_by_account_wallet_id(
                db, account_wallet.id)
            if customer is None:
                customer_account = CustomerAccount()
                customer_account.account_wallet_id = account_wallet.id
                customer_account.wallet_id = shop_wallet.id
                customer_account = CustomerAccountDao.create(
                    db=db, customer_account=customer_account)


def _make_xurl_payload(
        xurl: Xurl,
        request: Request,
        db: Session = Depends(get_db)):
    """
    will return a xrp native payload suitable for signing this can also be injected 
    into a xumm payload via the txjson field
    """

    ulogger.info(f"==== query params: {request.query_params}")

    if xurl.subject_type == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {xurl.subject_id}")
        payment_item = db.query(PaymentItem).filter_by(
            id=int(xurl.subject_id)).first()
        # # get the wallet for this payment item
        wallet = db.query(Wallet).filter_by(id=payment_item.wallet_id).first()
        if wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "payment item wallet not found"})

        # qty=1
        # if 'qty' in request.query_params:
        #     qty = int(request.query_params['qty'])

        return make_payment_item_payload(
            xurl=xurl, payment_item=payment_item, wallet=wallet)

    elif xurl.subject_type == XurlSubjectType.customer_account and xurl.verb_type == XurlVerbType.CREATEACCOUNT.lower():

        # get the shop id from the xurl
        shop_id = parse_shop_url(shop_url=xurl.base_url)
        shop_wallet = db.query(Wallet).filter_by(shop_id=shop_id).first()

        if shop_wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "shop wallet not found"})

        # wallet:Wallet, verb:str
        return make_create_account_payload(xurl=xurl, shop_wallet=shop_wallet, verb=xurl.verb_type)

    elif xurl.subject_type == XurlSubjectType.postal_address and xurl.verb_type == XurlVerbType.SHARE.lower():
        # get the postal address
        ulogger.info(f"==== xurl postal_address id: {xurl.subject_id}")
        postal_address = PostalAddressDao.fetch_by_id(
            db=db, postal_address_id=xurl.subject_id)
        
        if postal_address is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "postal address not found"})
        
        # # get the wallet for this payment item
        customer_wallet = db.query(Wallet).filter_by(id=postal_address.wallet_id).first()
        if customer_wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "payment customer_wallet wallet not found"})

        # get the shop id from the xurl
        shop_id = parse_shop_url(shop_url=xurl.base_url)
        shop_wallet = db.query(Wallet).filter_by(shop_id=shop_id).first()

        if shop_wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "shop wallet not found"})
        
        # lookup the key for encryption
        well_known_jks = postal_address.well_known_uri
        ulogger.info(f"==== SHOP well_known_jks: {well_known_jks}")
        
        # get the public key from the well known jwks
        response = requests.get(well_known_jks)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response as JSON and return it
            # return response.json()
            jwks = response.json()
            ulogger.info(f"==== SHOP jwks: {jwks}")
            public_key = extract_public_key(jwks)

            pa_d = postal_address.address.serialize()
            json_str = f'{pa_d["first_name"]}|{pa_d["last_name"]}|{pa_d["street_address"]}|{pa_d["street_address_2"]}|{pa_d["zip_code"]}|{pa_d["city"]}|{pa_d["state"]}|{pa_d["country"]}|{pa_d["phone_number"]}|{pa_d["postal_code"]}'
            encrypted_data = rsa_encrypt(json_str, public_key)

            # now base64 encode the encrypted data
            encrypted_data_b64 = base64.b64encode(encrypted_data)

            # now make the base64 encoded data a string
            encrypted_data_b64_str = encrypted_data_b64.decode('utf-8')

            pin_postal_address_data = {
                'encrypted_data': encrypted_data_b64_str,
                'shop_id': shop_id,
                'well_known_uri': well_known_jks,
                'customer_classic_address': customer_wallet.classic_address,
            }

            pin_response = asyncio.run(pinata_pin_dict(
                dict=pin_postal_address_data)) 
                      
            ulogger.info(f"==== pin_response: {pin_response}")

            # xurl: Xurl, shop_wallet: Wallet, customer_wallet: Wallet, ipfsHash: str, postal_address: PostalAddress
            return make_share_postal_address_payload(xurl=xurl, postal_address=postal_address, shop_wallet=shop_wallet, customer_wallet=customer_wallet, ipfsHash=pin_response['IpfsHash'])


        else:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                        detail="could nopt load shop jwks")
        

    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                        detail="invalid xurl")


@router.get("/xumm/xapp")
def xumm_xapp(xAppStyle: str,
              xAppToken: str,
              request: Request,
              db: Session = Depends(get_db)):

    xapp_session = asyncio.run(get_xapp_tokeninfo(xAppToken))
    if xapp_session is None:
        # return jsonify({"xAppToken": "cannot create payload"}), HTTPStatus.UNAUTHORIZED
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"xAppToken": "cannot create payload"})

    ulogger.info(f"==== xapp_session: {xapp_session}")

    # lookup the action by the xAppNavigateData
    # make sure they are using the correct network
    if get_wss_network_type(xapp_session['nodewss']).lower() != str(config['XRP_NETWORK_TYPE']).lower():
        ulogger.error(
            f"==== xapp_session nodewss network type {get_wss_network_type(xapp_session['nodewss'])} does not match config {config['XRP_NETWORK_TYPE']}")

        # return jsonify({"message": f"wrong network was expecting {config['XRP_NETWORK_TYPE']}, please switch and scan again"}), HTTPStatus.BAD_REQUEST
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": f"wrong network was expecting {config['XRP_NETWORK_TYPE']}, please switch and scan again"})

    if 'xAppNavigateData' not in xapp_session:
        return RedirectResponse(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}')

    xAppNavigateData = xapp_session['xAppNavigateData']
    if xAppNavigateData is None:
        return RedirectResponse(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}')

    ulogger.info(f"==== xAppNavigateData:\n{xAppNavigateData}")

    # now get the xurl
    if xAppNavigateData['uri'] is None:
        # not an xurlpay transaction
        return RedirectResponse(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}')

    ulogger.info(f"==== xurl: {xAppNavigateData['uri']}")
    xurl = parse_xurl(xAppNavigateData['uri_base'], xAppNavigateData['uri'])
    xumm_payload = _make_xurl_payload(xurl=xurl,
                                      request=request,
                                      db=db)
    ulogger.info(f"==== xumm_payload: {xumm_payload}")

    # look up the wallet based on the destination address if the verb is a payment
    if xurl.subject_type == XurlSubjectType.payment_item:
        wallet = db.query(Wallet).filter_by(
            classic_address=xumm_payload['txjson']['Destination']).first()
        if wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "wallet not found"})

        created = sdk.payload.create(xumm_payload)
        xumm_payload = created.to_dict()
        p_xumm_payload = XummPayload(payload_body=json.dumps(xumm_payload),
                                     wallet_id=wallet.id,
                                     payload_uuidv4=xumm_payload['uuid'])

        db.add(p_xumm_payload)
        db.commit()
    elif xurl.subject_type == XurlSubjectType.customer_account and xurl.verb_type.lower() == XurlVerbType.CREATEACCOUNT.lower():
        # get the shop id from the xurl
        shop_id = parse_shop_url(shop_url=xurl.base_url)
        wallet = db.query(Wallet).filter_by(shop_id=shop_id).first()

        if wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "wallet not found"})

        created = sdk.payload.create(xumm_payload)
        xumm_payload = created.to_dict()
        p_xumm_payload = XummPayload(payload_body=json.dumps(xumm_payload),
                                     wallet_id=wallet.id,
                                     payload_uuidv4=xumm_payload['uuid'])

        db.add(p_xumm_payload)
        db.commit()
    elif xurl.subject_type == XurlSubjectType.postal_address and xurl.verb_type.lower() == XurlVerbType.SHARE.lower():


        postal_address = PostalAddressDao.fetch_by_id(
            db=db, postal_address_id=xurl.subject_id)
        
        # get the shop id from the xurl
        created = sdk.payload.create(xumm_payload)
        xumm_payload = created.to_dict()
        p_xumm_payload = XummPayload(payload_body=json.dumps(xumm_payload),
                                     wallet_id=postal_address.wallet_id,
                                     payload_uuidv4=xumm_payload['uuid'])

        db.add(p_xumm_payload)
        db.commit()

    else:
        return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "invalid xurl, not implemented"})

    # return xumm_payload
    ulogger.info(f"xumm_payload: {xumm_payload}")
    return RedirectResponse(xumm_payload['next']['always'])


@router.get('/xumm/qr')
def serve_qr_img(url: str):
    # lookup the wallet by the classic address in the jwt
    # url = request.args.get('url')
    if url is None:
        url = 'https://dev.xurlpay.org/xapp'

    ulogger.info(f"==== making qr for {url}")

    img = generate_qr_code({'url': url})
    return serve_pil_image(img)


def serve_pil_image(pil_img, type='PNG', mimetype='image/png'):
    img_io = io.BytesIO()
    pil_img.save(img_io, type, quality=70)
    img_io.seek(0)
    return Response(content=img_io.getvalue(), media_type="image/png")
