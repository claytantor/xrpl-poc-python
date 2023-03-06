
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
import base64
from datetime import datetime as dt, timedelta
import xumm
import asyncio
from PIL import Image

from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import JSONResponse, Response, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from api.schema import MessageSchema, ApiInfoSchema, OAuth2AuthSchema, OAuth2TokenSchema, PaymentItemSchema, PaymentRequestSchema, XurlSubjectType, XurlVerbType, WalletCreateSchema, WalletSchema, XrpCurrencyRateSchema, XummPayloadSchema, XurlVersion
from api.models import InventoryItem, InventoryItemImage, Message, ApiInfo, PaymentItem, Wallet, XrpCurrencyRate, XummPayload
from api.decorators import verify_user_jwt_scopes
from api.jwtauth import make_signed_token, get_token_body
from api.dao import InventoryItemDao, PaymentItemDao, XummPayloadDao, get_db, WalletDao
from api.utils import parse_xurl
from api.xrpcli import get_account_info, get_rpc_network_from_wss, get_rpc_network_type, get_xrp_network_from_jwt, xrp_to_drops, get_xapp_tokeninfo, get_wss_network_type, get_rpc_network_from_jwt

import logging
ulogger = logging.getLogger("uvicorn.error")

router = APIRouter()


from api.xqr import generate_qr_code
from api.serializers import PaymentItemDetailsSerializer
from api.s3utils import save_image

from dotenv import dotenv_values
config = {
    # load shared development variables
    **dotenv_values(os.getenv("APP_CONFIG")),
    **os.environ,  # override loaded values with environment variables
}

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

@router.get("/info",tags=["ApiInfo"], response_model=ApiInfoSchema,status_code=200)
def get_api_info():
    ulogger.info(f"get_api_info {ApiInfo().to_dict()}")
    return ApiInfo().to_dict()

@router.post("/token",tags=["Auth"], response_model=OAuth2TokenSchema,status_code=200)
def auth_token(username: str = Form(), password: str = Form()):
    ulogger.info(f"get_spoof_token {username} {password}")
    jwt_token = make_signed_token(password, {'sub':username, 'net':config['XRP_WS_NET']})
    return {"access_token":jwt_token}

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
@verify_user_jwt_scopes(scopes['wallet_owner'])
def xrp_price_from_currency(fiat_i8n_currency:str, request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)

    # wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    # if wallet is None:
    #     return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})
    
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
    payloadRequest:XummPayloadSchema,
    request: Request,
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)

    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    # ulogger.info(f"update_wallet_payload {payloadRequest}")
    payload_exists = XummPayloadDao.fetch_by_wallet_payload_uuidv4(db=db, wallet_id=wallet.id, payload_uuidv4=payloadRequest.payload_uuidv4)

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
    paymentRequest:PaymentRequestSchema,
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
        'address':wallet.classic_address,
        'network_endpoint':get_rpc_network_from_jwt(jwt_body),
        'network_type': get_rpc_network_type(get_rpc_network_from_jwt(jwt_body)),
        'memo':paymentRequest.memo,
        'request_hash':pr_hash,
    }

    # json_str = json.dumps(payment_request_dict)
    # base64_message, base_64_sig = self.sign_msg(json_str)
    # payment_request=f"{base64_message}:{base_64_sig}"
    # return payment_request_dict, payment_request

    create_payload = {
        'txjson': {
                'TransactionType' : 'Payment',
                'Destination' : wallet.classic_address,
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


def save_images(db: Session, images_list:dict, inventory_item:InventoryItem):
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
def get_payment_items_by_user_address(user_address:str, request: Request, db: Session = Depends(get_db)):
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
def delete_payment_item_by_id(id:int, 
    request: Request, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_item = PaymentItemDao.fetch_single_by_wallet_id(db, payment_item_id=id, wallet_id=wallet.id)
    if payment_item is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})

    PaymentItemDao.delete(db, payment_item)

    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "payment item deleted"})


@router.get('/payment_item/{id}') 
def get_payment_item_by_id(id:int, 
    request: Request, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_item = PaymentItemDao.fetch_single_by_wallet_id(db, wallet_id=wallet.id, payment_item_id=id)
    # payment_item = PaymentItemDao.fetch_by_id(db, payment_item_id=id)
    
    if payment_item is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})

    return JSONResponse(status_code=HTTPStatus.OK, content=PaymentItemDetailsSerializer(payment_item, shop_id=wallet.shop_id).serialize())



def make_payment_item_payload(payment_item:PaymentItem, wallet:Wallet, verb:str, qty:int=1):

    ulogger.info(f"get_xrp_price {payment_item.fiat_i8n_currency} {payment_item.fiat_i8n_price}")
    rates = sdk.get_rates(payment_item.fiat_i8n_currency).to_dict()
    ulogger.info(f"rates: {rates}")
    xrp_price = rates['XRP']
    xrp_amount = (payment_item.fiat_i8n_price / xrp_price)*qty
    
    payment_request_dict = {
        'type': 'payment_item',
        'payment_item_id': payment_item.id,       
        'xrp_quote': xrp_price,
        'fiat_i8n_currency': payment_item.fiat_i8n_currency,
        'fiat_i8n_price': payment_item.fiat_i8n_price,
        'request_hash': shortuuid.uuid(),
        'network_endpoint': config['XRP_NETWORK_ENDPOINT'],
        'network_type': config['XRP_NETWORK_TYPE'], 
        'verb': verb     
    }

    if qty > 1:
        payment_request_dict['qty'] = qty

    return {
        'txjson': {
            'TransactionType' : 'Payment',
            'Destination' : wallet.classic_address,
            'Amount': str(xrp_to_drops(xrp_amount)),
        },
        "custom_meta": {
            "identifier": f"payment_item:{shortuuid.uuid()[:12]}",
            "blob": json.dumps(payment_request_dict),
            "instruction": f"Pay {payment_item.fiat_i8n_price} {payment_item.fiat_i8n_currency} each for {qty} {payment_item.inventory_item.name}"
        }
    }


def make_xumm_payment_item_payload_response(payment_item:PaymentItem, verb:XurlVerbType, db: Session):

    # # get the wallet for this payment item
    wallet = db.query(Wallet).filter_by(wallet_id=payment_item.wallet_id).first()
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "payment item wallet not found"})

    created = sdk.payload.create(make_payment_item_payload(payment_item=payment_item, wallet=wallet, verb=verb))
    xumm_payload = created.to_dict()
    p_xumm_payload = XummPayload(payload_body=json.dumps(xumm_payload),
                            wallet_id=wallet.id,
                            payload_uuidv4=xumm_payload['uuid'])

    db.add(p_xumm_payload)
    db.commit()

    # return xumm_payload
    ulogger.info(f"xumm_payload:{xumm_payload}")
    return RedirectResponse(xumm_payload['next']['always'])


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


    images_list = [{'id': image.id, 'data_url': image.data_url} for image in paymentItem.images]
    save_images(db=db, images_list=images_list, inventory_item=inventory_item)
    
    # save the inventory item
    inventory_item = InventoryItemDao.create(db=db, inventory_item=inventory_item)

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
    
    payment_item = PaymentItemDao.fetch_single_by_wallet_id(db, paymentItem.id, wallet.id)
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
  
    images_list = [{'id': image.id, 'data_url': image.data_url} for image in paymentItem.images]
    save_images(db=db, images_list=images_list, inventory_item=payment_item.inventory_item)

    payload = PaymentItemDao.update(db=db, payment_item=payment_item)
    return JSONResponse(status_code=HTTPStatus.OK, content=PaymentItemDetailsSerializer(payload, shop_id=wallet.shop_id).serialize())

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
            _process_payload_verb(payload=payload, db=db)
    
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

def _process_payload_verb(payload: XummPayload,
    db: Session = Depends(get_db)):

    ulogger.info(f"==== _process_payload_verb from payload.")

    # get the payload body
    payload_body = json.loads(payload.webhook_body)

    # determine the verb type from the payload custom_meta
    custom_meta = json.loads(payload_body['custom_meta']['blob'])
    verb = XurlVerbType(custom_meta['verb'])
    # ignore no_op verbs
    if(verb != XurlVerbType.no_op):
        ulogger.info(f"==== do something with the verb: {verb}")
    else:
        ulogger.info(f"==== no_op verb, ignoring")


def _make_xurl_payload(version:XurlVersion,
    subject:XurlSubjectType,
    subjectid:int,
    verb:XurlVerbType,
    request: Request,
    db: Session = Depends(get_db)):

    """
    will return a xrp native payload suitable for signing this can also be injected 
    into a xumm payload via the txjson field
    """

    ulogger.info(f"==== query params: {request.query_params}")

    if subject == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {subjectid}")
        payment_item = db.query(PaymentItem).filter_by(payment_item_id=int(subjectid)).first()
        # # get the wallet for this payment item
        wallet = db.query(Wallet).filter_by(wallet_id=payment_item.wallet_id).first()
        if wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "payment item wallet not found"})
        
        qty=1
        if 'qty' in request.query_params:
            qty = int(request.query_params['qty'])
        
        return make_payment_item_payload(payment_item=payment_item, wallet=wallet, verb=verb, qty=qty)
        
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="invalid xurl")

@router.get("/xumm/xapp")
def xumm_xapp(xAppStyle:str, 
    xAppToken:str,
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
        ulogger.error(f"==== xapp_session nodewss network type {get_wss_network_type(xapp_session['nodewss'])} does not match config {config['XRP_NETWORK_TYPE']}")
        
        # return jsonify({"message": f"wrong network was expecting {config['XRP_NETWORK_TYPE']}, please switch and scan again"}), HTTPStatus.BAD_REQUEST
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": f"wrong network was expecting {config['XRP_NETWORK_TYPE']}, please switch and scan again"})

    if 'xAppNavigateData' not in xapp_session:
        return RedirectResponse(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}')

    xAppNavigateData = xapp_session['xAppNavigateData']
    if xAppNavigateData is None:
        return RedirectResponse(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}')
    
    ulogger.info(f"==== xAppNavigateData:\n{xAppNavigateData}")

    # now get the xurl
    if xAppNavigateData['xurl'] is None:
        # not an xurlpay transaction
        return RedirectResponse(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}')
    
    ulogger.info(f"==== xurl:{xAppNavigateData['xurl']}")
    xurl = parse_xurl(xAppNavigateData['xurl'])
    xumm_payload = _make_xurl_payload(
        version=xurl.version, 
        subject=xurl.subject_type, 
        subjectid=xurl.subject_id, 
        verb=xurl.verb_type, 
        request=request, db=db)
    
    # look up the wallet based on the destination address
    wallet = db.query(Wallet).filter_by(classic_address=xumm_payload['txjson']['Destination']).first()
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "wallet not found"})
    
    created = sdk.payload.create(xumm_payload)
    xumm_payload = created.to_dict()
    p_xumm_payload = XummPayload(payload_body=json.dumps(xumm_payload),
                            wallet_id=wallet.id,
                            payload_uuidv4=xumm_payload['uuid'])

    db.add(p_xumm_payload)
    db.commit()

    # return xumm_payload
    ulogger.info(f"xumm_payload:{xumm_payload}")
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

