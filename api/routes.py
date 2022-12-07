
import io
from pydoc import describe
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
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from api.schema import MessageSchema, ApiInfoSchema, OAuth2AuthSchema, OAuth2TokenSchema, PaymentRequestSchema, WalletSchema, XrpCurrencyRateSchema, XummPayloadSchema
from api.models import Message, ApiInfo, PaymentItem, PaymentItemImage, XrpCurrencyRate, XummPayload
from api.decorators import verify_user_jwt_scopes
from api.jwtauth import make_signed_token, get_token_body
from api.dao import PaymentItemDao, XummPayloadDao, get_db, WalletDao
from api.xrpcli import get_account_info, get_rpc_network_from_wss, get_rpc_network_type, get_xrp_network_from_jwt, xrp_to_drops, get_xapp_tokeninfo, get_wss_network_type, get_rpc_network_from_jwt

import logging
ulogger = logging.getLogger("uvicorn.error")

router = APIRouter()

# from api.exchange_rates import xrp_price
from api.xqr import generate_qr_code
# from api.xrpcli import get_rpc_network_from_jwt, get_rpc_network_type, get_wss_network_type
# from api.models import PaymentItemImage, Wallet, XummPayload, PaymentItem
from api.serializers import PaymentItemDetailsSerializer
# from api.xrpcli import xrp_to_drops, get_xapp_tokeninfo, get_rpc_network_from_wss, get_account_info


# from . import db
# from .decorators import log_decorator, verify_user_jwt_scopes
# from .jwtauth import is_token_valid, has_all_scopes, get_token_body, get_token_sub
from .s3utils import save_image


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/', tags=["ApiInfo"], response_model=MessageSchema,status_code=200)
async def get_index():
    message = Message()
    message.message = "hello xurl"
    return message.to_dict() 


@router.get("/info",tags=["ApiInfo"], response_model=ApiInfoSchema,status_code=200)
def get_api_info():
    # app.logger.info(f"version: {config['APP_VERSION']}")
    # return jsonify({'version': config['APP_VERSION']}), 200
    return ApiInfo().to_dict()

@router.post("/token",tags=["Auth"], response_model=OAuth2TokenSchema,status_code=200)
def auth_token(username: str = Form(), password: str = Form()):
    ulogger.info(f"get_spoof_token {username} {password}")
    jwt_token = make_signed_token(password, {'sub':username, 'net':config['XRP_WS_NET']})
    return {"access_token":jwt_token}

@router.get("/wallet", tags=["Wallet"], response_model=WalletSchema, status_code=200)
# @router.get("/wallet",status_code=200)
@verify_user_jwt_scopes(scopes['wallet_owner'])
async def get_wallet(request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    ulogger.info(f"get_wallet {token}")
    jwt_body = get_token_body(token)

    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    
    try:
        xrp_network = get_xrp_network_from_jwt(jwt_body)
        account_info = await get_account_info(wallet.classic_address, xrp_network.json_rpc)

        wallet_dict = wallet.to_dict()
        wallet_dict['account_data'] = account_info['account_data']
        wallet_dict['xrp_network'] = xrp_network.to_dict()     
        return wallet_dict

    except Exception as e:
        ulogger.error(f"get_wallet {e}")
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": str(e)})

@router.get("/xrp/price/{fiat_i8n_currency}", tags=["XRP"], response_model=XrpCurrencyRateSchema, status_code=200)
@verify_user_jwt_scopes(scopes['wallet_owner'])
def xrp_price_from_currency(fiat_i8n_currency:str, request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)

    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})
    
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

    payloads = XummPayloadDao.fetch_by_wallet_id(db=db, wallet_id=wallet.wallet_id)
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

    ulogger.info(f"update_wallet_payload {payloadRequest}")
    payload_exists = XummPayloadDao.fetch_by_wallet_payload_uuidv4(db=db, wallet_id=wallet.wallet_id, payload_uuidv4=payloadRequest.payload_uuidv4)

    if payload_exists is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "payload does not belong to wallet"})

    payload_exists.from_dict(payloadRequest.__dict__) 
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
                            wallet_id=wallet.wallet_id,
                            payload_uuidv4=xumm_payload['uuid'])

    db.add(m_payload)
    db.commit()

    return m_payload.to_dict()


def save_images(db: Session, images_dict:dict, payment_item:PaymentItem):
    for image in images_dict:
        ulogger.info(image)
        # {'data_url': 'https://s3.us-west-2.amazonaws.com/dev.rapaygo.com/uploaded_images/c053789c-4d0a-4dc2-a175-39eb0d694d6f.png', 'id': 28}
        if 'id' not in image or image['id'] is None:

            im = Image.open(io.BytesIO(base64.b64decode(
                image['data_url'].split(',')[1])))
            file_name = f"{uuid.uuid4()}.png"

            url_saved = save_image(im, config["AWS_BUCKET_NAME"],
                                   f"{config['AWS_UPLOADED_IMAGES_PATH']}/{file_name}")

            url_saved = f'https://s3.us-west-2.amazonaws.com/{app.config["AWS_BUCKET_NAME"]}/uploaded_images/{file_name}'

            payment_item_image = PaymentItemImage(
                type="PaymentItemImage", file_path=url_saved, file_name=file_name, file_size=0, original_name=file_name)

            payment_item.images.append(payment_item_image)

        elif 'file_path' in image:
            payment_item_image = PaymentItemImage.query.filter_by(
                id=image['id']).first()
            payment_item_image.file_path = image['file_path']
            payment_item_image.file_name = image['file_name']
            payment_item_image.original_name = image['original_name']
            payment_item_image.file_size = image['file_size']

        db.commit()


# def save_images_for_request(request, db: Session, payment_item:PaymentItem):

#     if 'images' in request.json:
#         save_images(request.json['images'], payment_item)


@router.get('/payment_item') 
@verify_user_jwt_scopes(scopes['wallet_owner'])
def get_payment_items(request: Request, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_items = PaymentItemDao.fetch_all_by_wallet_id(db, wallet.wallet_id)

    return JSONResponse(status_code=HTTPStatus.OK, content=[PaymentItemDetailsSerializer(payment_item).serialize() for payment_item in payment_items])



#     # get all the payment items for this wallet
#     payment_items = db.session.query(PaymentItem).filter_by(
#         wallet_id=wallet.wallet_id).all()
#     return jsonify([PaymentItemDetailsSerializer(payment_item).serialize() for payment_item in payment_items]), 200


# @router.route('/payment_item/<id>', methods=['DELETE'])  
# @cross_origin()
# def delete_payment_item_by_id(id):
#     # lookup the wallet by the classic address in the jwt
#     jwt_body = get_token_body(dict(request.headers)[
#                               "Authorization"].replace("Bearer ", ""))

#     wallet = db.session.query(Wallet).filter_by(
#         classic_address=jwt_body['sub']).first()
#     if wallet is None:
#         return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

#     # get all the payment items for this wallet
#     payment_item = db.session.query(PaymentItem).filter_by(
#         wallet_id=wallet.wallet_id, payment_item_id=id).first()
    
#     if payment_item is None:
#         return jsonify({"message": "payment item not found"}), HTTPStatus.NOT_FOUND

#     db.session.delete(payment_item)
#     db.session.commit()

#     return jsonify({"message": "payment item deleted"}), HTTPStatus.OK


@router.get('/payment_item/{id}') 
def get_payment_item_by_id(id:int, 
    request: Request, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)):

    jwt_body = get_token_body(token)
    wallet = WalletDao.fetch_by_classic_address(db, jwt_body['sub'])
    if wallet is None:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "wallet not found"})

    payment_item = PaymentItemDao.fetch_single_by_wallet_id(db, wallet_id=wallet.wallet_id, payment_item_id=id)
    
    if payment_item is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})

    return JSONResponse(status_code=HTTPStatus.OK, content=PaymentItemDetailsSerializer(payment_item).serialize())



# @router.route('/payment_item/xumm/payload/<id>', methods=['GET'])  # depricated
# @cross_origin()
# def get_payment_item_payload_by_id(id):

#     payment_item = db.session.query(PaymentItem).filter_by(payment_item_id=id).first()
    
#     if payment_item is None:
#         return jsonify({"message": "payment item not found"}), HTTPStatus.NOT_FOUND

#     app.logger.info(payment_item.serialize())

#     try:
#         return make_payment_item_payload_response(payment_item)
#     except Exception as e:
        
#         app.logger.error(e)
#         app.log_exception(e)
#         return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR




# def make_payment_item_payload_response(payment_item):

#     # get the wallet for this payment item
#     wallet = db.session.query(Wallet).filter_by(wallet_id=payment_item.wallet_id).first()
#     if wallet is None:
#         return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

#     # convert the payment item to a xumm payload
#     xrp_quote = asyncio.run(xrp_price(payment_item.fiat_i8n_currency))
#     xrp_amount = payment_item.fiat_i8n_price / xrp_quote
    
#     payment_request_dict = {
#         'type': 'payment_item',
#         'payment_item_id': payment_item.payment_item_id,       
#         'xrp_quote': xrp_quote,
#         'fiat_i8n_currency': payment_item.fiat_i8n_currency,
#         'fiat_i8n_price': payment_item.fiat_i8n_price,
#         'request_hash':shortuuid.uuid(),
#         'network_endpoint': config['XRP_NETWORK_ENDPOINT'],
#         'network_type': config['XRP_NETWORK_TYPE'],     
#     }

#     create_payload = {
#         'txjson': {
#                 'TransactionType' : 'Payment',
#                 'Destination' : wallet.classic_address,
#                 'Amount': str(xrp_to_drops(xrp_amount)),
#         },
#         "custom_meta": {
#             "identifier": f"payment_item:{shortuuid.uuid()[:12]}",
#             "blob": json.dumps(payment_request_dict),
#             "instruction": f"Pay {payment_item.fiat_i8n_price} {payment_item.fiat_i8n_currency} for item {payment_item.name}"
#         }
#     }   

#     created = sdk.payload.create(create_payload)
#     xumm_payload = created.to_dict()
#     p_xumm_payload = XummPayload(payload_body=json.dumps(xumm_payload),
#                             wallet_id=wallet.wallet_id,
#                             payload_uuidv4=xumm_payload['uuid'])

#     db.session.add(p_xumm_payload)
#     db.session.commit()

#     # return xumm_payload
#     app.logger.info(f"xumm_payload:{xumm_payload}")
#     return redirect(xumm_payload['next']['always'], code=302)



# @router.route('/payment_item', methods=['POST', 'PUT'])  # depricated
# @cross_origin()
# def create_payment_item():
#     app.logger.info("create payment item")

#     # lookup the wallet by the classic address in the jwt
#     jwt_body = get_token_body(dict(request.headers)[
#                               "Authorization"].replace("Bearer ", ""))

#     wallet = db.session.query(Wallet).filter_by(
#         classic_address=jwt_body['sub']).first()
#     if wallet is None:
#         return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

#     if request.method == 'PUT': # update
#             # get all the payment items for this wallet
#         payment_item_id = request.json.get('payment_item_id')
#         if payment_item_id is None:
#             return jsonify({"message": "payment_item_id is required"}), HTTPStatus.BAD_REQUEST

#         payment_item = db.session.query(PaymentItem).filter_by(
#             wallet_id=wallet.wallet_id, payment_item_id=payment_item_id).first()

#         if payment_item is None:
#             return jsonify({"message": "payment item not found"}), HTTPStatus.NOT_FOUND
        
#         payment_item.name = request.json.get('name')
#         payment_item.fiat_i8n_currency = request.json.get('fiat_i8n_currency')
#         payment_item.fiat_i8n_price = float(request.json.get('fiat_i8n_price'))
#         payment_item.description = request.json.get('description')

#         save_images_for_request(request, payment_item, app)


#     elif request.method == 'POST': # create

#         payment_item_name = request.json.get('name')
#         description = request.json.get('description')
#         price = float(request.json.get('fiat_i8n_price'))
#         currency = request.json.get('fiat_i8n_currency')
#         sku_id = str(uuid.uuid4()).replace("-", "")[:10]

#         payment_item = PaymentItem(
#             wallet_id=wallet.wallet_id, 
#             name=payment_item_name,
#             description=description,
#             fiat_i8n_price=price, 
#             fiat_i8n_currency=currency, 
#             sku_id=sku_id)

#         save_images_for_request(request, payment_item, app)
#         db.session.add(payment_item)
    
#     db.session.commit()
#     response = {'full_messages': ['PaymentItem updated successfully']}
#     response.update(PaymentItemDetailsSerializer(payment_item).data)
#     return jsonify(response)




# # https://devapi.xurlpay.org/v1/xumm/webhook
# @router.route("/xumm/webhook", methods=['GET', 'POST', 'OPTIONS'])
# @cross_origin()
# @log_decorator(app.logger)
# def xumm_webhook():

#     app.logger.info("==== xumm webhook")

#     if request.method == 'OPTIONS':
#         return jsonify({'message': "OK"}), 200, {'Access-Control-Allow-Origin': '*',
#                                                  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
#                                                  'Access-Control-Allow-Methods': 'POST, OPTIONS'}

#     # ADHOC PAYMENT
#     #  {
#     #     "meta": {
#     #         "url": "https://devapi.xurlpay.org/v1/xumm/webhook",
#     #         "application_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#     #         "payload_uuidv4": "62d7bc46-3e46-45ed-8358-e87812f15a6e",
#     #         "opened_by_deeplink": true
#     #     },
#     #     "custom_meta": {
#     #         "identifier": null,
#     #         "blob": "{\"amount\": 1.25, \"amount_drops\": 1250000, \"address\": \"rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y\", \"network_endpoint\": \"https://s.altnet.rippletest.net:51234/\", \"network_type\": \"testnet\", \"memo\": \"its for the kids man 2\", \"request_hash\": \"M97R6EEXdgXxyKd9myFgD8\"}",
#     #         "instruction": "its for the kids man 2"
#     #     },
#     #     "payloadResponse": {
#     #         "payload_uuidv4": "62d7bc46-3e46-45ed-8358-e87812f15a6e",
#     #         "reference_call_uuidv4": "11b36850-eaaf-406d-bf3d-622e3882c678",
#     #         "signed": true,
#     #         "user_token": true,
#     #         "return_url": {
#     #             "app": null,
#     #             "web": null
#     #         },
#     #         "txid": "8340735242F2B65392F5734A49209A13BD4BC77DAED4CC99B5ACFB8C67BE9E76"
#     #     },
#     #     "userToken": {
#     #         "user_token": "83234d7d-54d6-4240-89a3-e86cb97603cd",
#     #         "token_issued": 1668293195,
#     #         "token_expiration": 1670986728
#     #     }
#     # }


#     # PAYMENT ITEM
#     # {
#     # "meta": {
#     #     "url": "https://devapi.xurlpay.org/v1/xumm/webhook",
#     #     "application_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
#     #     "payload_uuidv4": "ca14725e-a628-4d16-8a07-99932a916763",
#     #     "opened_by_deeplink": false
#     # },
#     # "custom_meta": {
#     #     "identifier": null,
#     #     "blob": "{\"type\": \"payment_item\", \"payment_item_id\": 1, \"xrp_quote\": 0.37941592, \"fiat_i8n_currency\": \"USD\", \"fiat_i8n_price\": 0.15, \"request_hash\": \"c9qjoB5P4sMhtA7EBgRMSU\"}",
#     #     "instruction": "Pay 0.15 USD for item Tootsie Roll Chocolate Midgee"
#     # },
#     # "payloadResponse": {
#     #     "payload_uuidv4": "ca14725e-a628-4d16-8a07-99932a916763",
#     #     "reference_call_uuidv4": "453f76bd-584e-42d5-bb53-d710e9c2426b",
#     #     "signed": true,
#     #     "user_token": true,
#     #     "return_url": {
#     #         "app": null,
#     #         "web": null
#     #     },
#     #     "txid": "3A2EE5A74AA760C6E40402A11E4416029D97E66F15B58C62987DC0808D4BE011"
#     # },
#     # "userToken": {
#     #     "user_token": "83234d7d-54d6-4240-89a3-e86cb97603cd",
#     #     "token_issued": 1668293195,
#     #     "token_expiration": 1671130384
#     # }
#     # }

    

#     json_body = request.get_json()
#     app.logger.info(f"==== xumm webhook payload:\n{json.dumps(json_body, indent=4)}")
#     if 'signed' in json_body['payloadResponse'] and json_body['payloadResponse']['signed'] == True:
#         app.logger.info("==== xumm webhook payload is signed")

#         # get the xumm payload by the payload_uuidv4
#         payload = XummPayload.get_by_payload_uuidv4(
#             json_body['payloadResponse']['payload_uuidv4'])
        
#         if payload is None:
#             return jsonify({'message': 'payload not found'}), 404

#         # dont run this if the payload is already processed
#         if not payload.is_signed:
#             payload.set_is_signed_bool(json_body['payloadResponse']['signed'])
#             payload.txid = json_body['payloadResponse']['txid']
#             payload.webhook_body = json.dumps(json_body)
#             db.session.commit()

#             # get the custom_meta blob
#             if 'custom_meta' in json_body and json_body['payloadResponse']['txid'] is not None:
#                 custom_meta_blob = json.loads(json_body['custom_meta']['blob'].replace("\\", ''))
#                 app.logger.info(f"==== xumm webhook custom_meta_blob:\n{json.dumps(custom_meta_blob, indent=4)}")
#                 if custom_meta_blob['type'] == 'payment_item':
#                     # get the payment item
#                         # get all the payment items for this wallet
#                     payment_item = db.session.query(PaymentItem).filter_by( payment_item_id=int(custom_meta_blob['payment_item_id'])).first()
#                     if payment_item is not None:
#                         # asyncio.run(send_slack_message(f"Payment Item id:{payment_item.payment_item_id} {payment_item.name} has just been purchased for {payment_item.fiat_i8n_price} {payment_item.fiat_i8n_currency}!"))
#                         send_slack_message(f"Payment Item {payment_item.name} has just been purchased! payment item id:{payment_item.payment_item_id} price:{payment_item.fiat_i8n_price} {payment_item.fiat_i8n_currency} {config['XRP_NETWORK_EXPLORER']}/transactions/{json_body['payloadResponse']['txid']}")
#                         # dont block if this fails

#     return jsonify({'message': 'xumm_webhook'}), 200



# def send_slack_message(message):
#     """Send a message to slack"""
#     app.logger.info(f"==== send_slack_message: {message} to {app.config['SLACK_WEBHOOK_URL']}")
#     try:
#         slack_data = {'text': message}
#         response = requests.post(
#             app.config['SLACK_WEBHOOK_URL'], data=json.dumps(slack_data),
#             headers={'Content-Type': 'application/json'}
#         )
#         if response.status_code != 200:
#             app.logger.error(f"==== slack webhook error: {response.status_code}")
#     except Exception as e:
#         app.log_exception(f"==== slack webhook error: {e}")



# @router.route("/xumm/xapp", methods=['GET', 'OPTIONS'])
# @cross_origin()
# @log_decorator(app.logger)
# def xumm_xapp():

#     app.logger.info("==== xumm xapp")

#     app.logger.info(
#         f"{request} {request.args} {request.headers} {request.environ} {request.method} {request.url}")

#     if request.method == 'OPTIONS':
#         return jsonify({'message': "OK"}), 200, {'Access-Control-Allow-Origin': '*',
#                                                  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
#                                                  'Access-Control-Allow-Methods': 'POST, OPTIONS'}

#     # lookup the wallet by the classic address in the jwt
#     xAppStyle = request.args.get('xAppStyle')
#     if xAppStyle is None:
#         xAppStyle = "LIGHT"

#     xAppToken = request.args.get('xAppToken')
#     if xAppToken is None:
#         return jsonify({"xAppToken": "token not found unauthorized"}), HTTPStatus.UNAUTHORIZED


#     xapp_session = asyncio.run(get_xapp_tokeninfo(xAppToken)) 
#     if xapp_session is None:
#         return jsonify({"xAppToken": "cannot create payload"}), HTTPStatus.UNAUTHORIZED

#     app.logger.info(f"==== xapp_session:\n{xapp_session}")
#     # {
#     #     "version": "2.3.1",
#     #     "locale": "en",
#     #     "currency": "USD",
#     #     "style": "LIGHT",
#     #     "nodetype": "TESTNET",
#     #     "origin": {
#     #         "type": "QR",
#     #         "data": {
#     #         "content": "https://xumm.app/detect/xapp:sandbox.32849dc99872?classic_address=rNDtp9V6MUnbb14fPtVrCqR2Ftd6V17RLw&amount=10.21"
#     #         }
#     #     },
#     #     "classic_address": "rNDtp9V6MUnbb14fPtVrCqR2Ftd6V17RLw",
#     #     "amount": "10.21",
#     #     "account": "rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y",
#     #     "accounttype": "REGULAR",
#     #     "accountaccess": "FULL",
#     #     "nodewss": "wss://testnet.xrpl-labs.com",
#     #     "user": "5cc95aba-7e42-4485-befc-97fe087938eb",
#     #     "user_device": {
#     #         "currency": "USD",
#     #         "platform": "android"
#     #     },
#     #     "account_info": {
#     #         "account": "rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y",
#     #         "name": null,
#     #         "domain": null,
#     #         "blocked": false,
#     #         "source": "",
#     #         "kycApproved": false,
#     #         "proSubscription": false
#     #     },
#     #     "subscriptions": [],
#     #     "xAppNavigateData": {
#     #         "classic_address": "rNDtp9V6MUnbb14fPtVrCqR2Ftd6V17RLw",
#     #         "amount": "10.21"
#     #     }
#     #     }

#     # lookup the action by the xAppNavigateData

#     # make sure they are using the correct network
#     if get_wss_network_type(xapp_session['nodewss']).lower() != str(config['XRP_NETWORK_TYPE']).lower():
#         app.logger.error(f"==== xapp_session nodewss network type {get_wss_network_type(xapp_session['nodewss'])} does not match config {config['XRP_NETWORK_TYPE']}")
#         return jsonify({"message": f"wrong network was expecting {config['XRP_NETWORK_TYPE']}, please switch and scan again"}), HTTPStatus.BAD_REQUEST

#     if 'xAppNavigateData' not in xapp_session:
#         return redirect(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}', code=302)

#     xAppNavigateData = xapp_session['xAppNavigateData']
#     if xAppNavigateData is None:
#         return redirect(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}', code=302)
    
#     app.logger.info(f"==== xAppNavigateData:\n{xAppNavigateData}")
#     if xAppNavigateData['TransactionType'] is None:
#         # not an xurlpay transaction
#         return redirect(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}', code=302)
    
#     if xAppNavigateData['LookupType'] is None:
#         # not an xurlpay transaction
#         return redirect(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}', code=302)

#     lookupType = xAppNavigateData['LookupType']
#     if(lookupType == "PaymentItem"):
#         reference = xAppNavigateData['LookupRef']
#         if reference is None:
#             return jsonify({"xAppNavigateData": "xAppNavigateData LookupRef not found unauthorized"}), HTTPStatus.BAD_REQUEST
#         payment_item = db.session.query(PaymentItem).filter_by(payment_item_id=int(reference)).first()
    
#         if payment_item is None:
#             return jsonify({"message": "payment item not found"}), HTTPStatus.NOT_FOUND

#         return make_payment_item_payload_response(payment_item)

#     else:
#         # not an xurlpay transaction
#         return redirect(f'https://dev.xurlpay.org/xapp?xAppToken={xAppToken}', code=302)


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

# def get_image()
#     image_bytes: bytes = generate_cat_picture()
#     # media_type here sets the media type of the actual response sent to the client.
#     return Response(content=image_bytes, media_type="image/png")