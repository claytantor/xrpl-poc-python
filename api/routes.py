import io
import uuid
from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask import current_app as app
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
import os
import sys
import shortuuid
import json
import base64
from datetime import datetime as dt, timedelta
import jwt
import xumm
import asyncio
from PIL import Image


from api.exchange_rates import xrp_price
from api.xrpcli import XUrlWallet, verify_msg, drops_to_xrp
from api.models import PaymentItemImage, Wallet, XummPayload, PaymentItem
from api.serializers import PaymentItemDetailsSerializer
from api.xrpcli import xrp_to_drops, XummWallet, get_rpc_network


from . import db
from .decorators import log_decorator, verify_user_jwt_scopes
from .jwtauth import is_token_valid, has_all_scopes, get_token_body, get_token_sub
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


@app.route("/")
def hello_world():
    return jsonify({'message': "Hello xURL"}), 200


@app.route("/version", methods=['GET'])
@cross_origin()
@log_decorator(app.logger)
def api_version():
    app.logger.info(f"version: {config['APP_VERSION']}")
    return jsonify({'version': config['APP_VERSION']}), 200


@app.route("/xrp/price/<fiat_i8n_currency>", methods=['GET'])
@cross_origin()
@log_decorator(app.logger)
def xrp_price_from_currency(fiat_i8n_currency):
    xrp_quote = asyncio.run(xrp_price(fiat_i8n_currency))
    return jsonify({'price': xrp_quote}), 200


@app.route('/auth/access_token', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['*', 'https://rapaygo.com', 'https://dev.rapaygo.com/'])
@log_decorator(app.logger)
def post_access_token():

    if request.method == 'OPTIONS':
        return jsonify({'message': "OK"}), 200, {'Access-Control-Allow-Origin': '*',
                                                 'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                                                 'Access-Control-Allow-Methods': 'POST, OPTIONS'}
    if request.method == 'POST':
        json_body = request.json
        # app.logger.info(json.dumps(json_body, indent=4))
        if json_body is None:
            return jsonify({"message": "empty body not allowed"}), HTTPStatus.BAD_REQUEST

        if 'classic_address' not in list(json_body.keys()):
            return jsonify({"message": "Missing required body element classic_address"}), HTTPStatus.BAD_REQUEST
        if 'private_key' not in list(json_body.keys()):
            return jsonify({"message": "Missing required body element private_key"}), HTTPStatus.BAD_REQUEST

        classic_address = json_body['classic_address']
        private_key = json_body['private_key']
        app.logger.debug(f"auth body: {json_body}")
        wallet = db.session.query(Wallet).filter_by(
            classic_address=classic_address, private_key=private_key).first()

        # dont let them know the wallet_id is wrong
        if wallet is None:
            return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

        return get_auth(wallet, classic_address, private_key, wallet.private_key,
                        scopes['wallet_owner'], scopes_refresh=scopes['wallet_owner_refresh'])


def get_auth_base(wallet, username, scopes, scopes_refresh):

    exp_time = dt.utcnow()+timedelta(hours=24)
    exp_time_refresh = dt.utcnow()+timedelta(days=30)

    jwt_body = {"sid": username,
                'scopes': scopes,
                "exp": int(exp_time.timestamp())}

    token = jwt.encode(
        jwt_body,
        wallet.private_key,
        algorithm="HS256")

    refresh_body = {"sid": username,
                    'scopes': scopes_refresh,
                    "exp": int(exp_time_refresh.timestamp())}

    refresh_token = jwt.encode(
        refresh_body,
        wallet.private_key,
        algorithm="HS256")

    return token, refresh_token


def get_auth(wallet, username, test_phrase, pass_phrase, scopes, scopes_refresh):

    token, refresh_token = get_auth_base(
        wallet, username, scopes, scopes_refresh)

    return jsonify({'access_token': token,
                    'refresh_token': refresh_token,
                    "wallet_id": wallet.wallet_id}), 200, {'subject': token}


def make_wallet(classic_address):
    wallet = Wallet(classic_address=classic_address)
    db.session.add(wallet)
    db.session.commit()
    return wallet


@app.route("/wallet", methods=['GET'])
# @verify_user_jwt_scopes(scopes['wallet_owner'])
@cross_origin()
@log_decorator(app.logger)
def get_wallet():
    # lookup the wallet by the classic address in the jwt
    jwt_body = get_token_body(dict(request.headers)[
                              "Authorization"].replace("Bearer ", ""))

    wallet = db.session.query(Wallet).filter_by(
        classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message": "wallet not found"}), HTTPStatus.NOT_FOUND
        # create a new wallet
        # wallet = make_wallet(classic_address=jwt_body['sub']) # create a new wallet

    # {'client_id': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'scope': 'XummPkce', 'aud': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'sub': 'rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y', 'email': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce+rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y@xumm.me', 'app_uuidv4': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'app_name': 'dev-xurlpay', 'payload_uuidv4': 'a9d8f45a-16ff-48ee-8ef1-163ce3b10f7c', 'usertoken_uuidv4': '4de21968-8c2f-4fb3-9bb6-94b589a13a8c', 'network_type': 'TESTNET', 'network_endpoint': 'wss://s.altnet.rippletest.net:51233', 'iat': 1668223704, 'exp': 1668310104, 'iss': 'https://oauth2.xumm.app'}
    xumm_wallet = XummWallet(
        network_endpoint=get_rpc_network(jwt_body['network_type']),
        classic_address=wallet.classic_address)

    return jsonify({
        'classic_address': wallet.classic_address,
        'wallet_info': wallet.serialize(),
        'wallet_user_info': jwt_body,
        'account_data': xumm_wallet.account_data}), 200


@app.route("/wallet", methods=['POST'])
@cross_origin()
@log_decorator(app.logger)
def create_wallet():
    jwt_body = get_token_body(dict(request.headers)[
                              "Authorization"].replace("Bearer ", ""))

    wallet = db.session.query(Wallet).filter_by(
        classic_address=jwt_body['sub']).first()
    if wallet is None:
        # create a new wallet
        wallet = make_wallet(classic_address=jwt_body['sub'])

    xumm_wallet = XummWallet(
        network_endpoint=get_rpc_network(jwt_body['network_type']),
        classic_address=wallet.classic_address)

    return jsonify({
        'classic_address': wallet.classic_address,
        'wallet_info': jwt_body,
        'account_data': xumm_wallet.account_data}), 200


@app.route("/pay_request", methods=['POST'])
@cross_origin()
@log_decorator(app.logger)
def create_pay_request():
    json_body = request.get_json()

    # lookup the wallet by the classic address in the jwt
    #classic_address = get_token_sid(dict(request.headers)["Authorization"])

    jwt_body = get_token_body(dict(request.headers)[
                              "Authorization"].replace("Bearer ", ""))

    wallet = db.session.query(Wallet).filter_by(
        classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

    if 'amount' not in list(json_body.keys()):
        return jsonify({"message": "Missing required body element amount"}), HTTPStatus.BAD_REQUEST
    xrp_amount = float(json_body['amount'])

    memo = f"xURL payment request {shortuuid.uuid()[:8]}"
    if 'memo' in list(json_body.keys()):
        memo = json_body['memo']

    # receiving_wallet = XUrlWallet(network=config['JSON_RPC_URL'], seed=wallet.seed)
    # payment_request_dict, payment_request = receiving_wallet.generate_payment_request(amount=xrp_amount, memo=memo)

    xumm_wallet = XummWallet(
        network_endpoint=get_rpc_network(jwt_body['network_type']),
        classic_address=wallet.classic_address)

    xumm_payload = xumm_wallet.generate_payment_request(
        xrp_amount=xrp_amount, memo=memo)

# {
#   "uuid": "9112991f-c106-4311-9aca-857bff640c15",
#   "next": {
#     "always": "https://xumm.app/sign/9112991f-c106-4311-9aca-857bff640c15"
#   },
#   "refs": {
#     "qr_png": "https://xumm.app/sign/9112991f-c106-4311-9aca-857bff640c15_q.png",
#     "qr_matrix": "https://xumm.app/sign/9112991f-c106-4311-9aca-857bff640c15_q.json",
#     "qr_uri_quality_opts": [
#       "m",
#       "q",
#       "h"
#     ],
#     "websocket_status": "wss://xumm.app/sign/9112991f-c106-4311-9aca-857bff640c15"
#   },
#   "pushed": false
# }

    app.logger.info(f"Xumm payload: {xumm_payload} {json.dumps(xumm_payload)}")
    m_payload = XummPayload(payload_body=json.dumps(xumm_payload),
                            wallet_id=wallet.wallet_id,
                            payload_uuidv4=xumm_payload['uuid'])

    db.session.add(m_payload)
    db.session.commit()

    return jsonify(xumm_payload), 200


# @app.route("/send_payment", methods=['POST'])
# @cross_origin()
# @log_decorator(app.logger)
# def send_payment():
#     json_body = request.get_json()
#     # json_body = json.loads(json_body['data'])
#     # print("==== send payment",json.loads(json_body['data']))

#     # lookup the wallet by the classic address in the jwt
#     classic_address = get_token_sub(dict(request.headers)["Authorization"])
#     wallet = db.session.query(Wallet).filter_by(
#         classic_address=classic_address).first()
#     if wallet is None:
#         return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

#     # ok now lets pay it with a faucet
#     # decode the payment request
#     pr_parts = json_body['payment_request'].split(":")
#     # print("==== send payment",pr_parts)

#     # # verify the signed message

#     message_payload = json.loads(base64.b64decode(pr_parts[0]))
#     print("==== send payment", message_payload)

#     # use the public key to verify
#     try:
#         # this is a faucet wallet
#         sending_wallet = XUrlWallet(
#             network=config['JSON_RPC_URL'], seed=wallet.seed)

#         # this will throw an exception if the signature is not valid
#         verify_msg(pr_parts[0], pr_parts[1], message_payload['public_key'])

#         tx_response_status, tx_response_result = sending_wallet.send_payment(
#             amount_xrp=message_payload['amount'],
#             destination_address=message_payload['address']
#         )

#         print(tx_response_status, tx_response_result)
#         return jsonify(tx_response_result), 200

#     except Exception as e:
#         print("=== COULD NOT VERIFY SIG", e)
#         return jsonify({'error': 'could not verify'}), 400


@app.route("/payload", methods=['GET'])
@cross_origin()
@log_decorator(app.logger)
def get_wallet_payloads():
    # lookup the wallet by the classic address in the jwt
    jwt_body = get_token_body(dict(request.headers)[
                              "Authorization"].replace("Bearer ", ""))

    wallet = db.session.query(Wallet).filter_by(
        classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

    print(wallet.serialize())
    payloads = db.session.query(XummPayload).filter_by(
        wallet_id=wallet.wallet_id).all()
    print(payloads)

    return jsonify([p.serialize() for p in payloads]), 200


def save_images(images_dict, payment_item, app):
    for image in images_dict:
        app.logger.info(image)
        # {'data_url': 'https://s3.us-west-2.amazonaws.com/dev.rapaygo.com/uploaded_images/c053789c-4d0a-4dc2-a175-39eb0d694d6f.png', 'id': 28}
        if 'id' not in image or image['id'] is None:

            im = Image.open(io.BytesIO(base64.b64decode(
                image['data_url'].split(',')[1])))
            file_name = f"{uuid.uuid4()}.png"

            url_saved = save_image(im, app.config["AWS_BUCKET_NAME"],
                                   f"{app.config['AWS_UPLOADED_IMAGES_PATH']}/{file_name}")

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

        db.session.commit()


def save_images_for_request(request, payment_item, app):

    if 'images' in request.json:
        save_images(request.json['images'], payment_item, app)


@app.route('/payment_item', methods=['GET'])  # depricated
@cross_origin()
def get_payment_items():

    # lookup the wallet by the classic address in the jwt
    jwt_body = get_token_body(dict(request.headers)[
                              "Authorization"].replace("Bearer ", ""))

    wallet = db.session.query(Wallet).filter_by(
        classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

    # get all the payment items for this wallet
    payment_items = db.session.query(PaymentItem).filter_by(
        wallet_id=wallet.wallet_id).all()
    return jsonify([p.serialize() for p in payment_items]), 200


@app.route('/payment_item/<id>', methods=['GET'])  # depricated
@cross_origin()
def get_payment_item_by_id(id):

    # lookup the wallet by the classic address in the jwt
    jwt_body = get_token_body(dict(request.headers)[
                              "Authorization"].replace("Bearer ", ""))

    wallet = db.session.query(Wallet).filter_by(
        classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

    # get all the payment items for this wallet
    payment_item = db.session.query(PaymentItem).filter_by(
        wallet_id=wallet.wallet_id, payment_item_id=id).first()
    
    if payment_item is None:
        return jsonify({"message": "payment item not found"}), HTTPStatus.NOT_FOUND


    pi_m = payment_item.serialize()
    pi_m['xurl'] = f'{config["APP_BASEURL_API"]}/payment_item/xumm/payload/{payment_item.payment_item_id}'
    # pi_m['images'] = [i.serialize() for i in payment_item.images]

    return jsonify(pi_m), 200


@app.route('/payment_item/xumm/payload/<id>', methods=['GET'])  # depricated
@cross_origin()
def get_payment_item_payload_by_id(id):

    payment_item = db.session.query(PaymentItem).filter_by(payment_item_id=id).first()
    
    if payment_item is None:
        return jsonify({"message": "payment item not found"}), HTTPStatus.NOT_FOUND

    # get the wallet for this payment item
    wallet = db.session.query(Wallet).filter_by(wallet_id=payment_item.wallet_id).first()

    # convert the payment item to a xumm payload
    xrp_quote = asyncio.run(xrp_price(payment_item.fiat_i8n_currency))
    xrp_amount = payment_item.fiat_i8n_amount / xrp_quote
    
    payment_request_dict = {
        'type': 'payment_item',
        'payment_item_id': payment_item.payment_item_id,       
        'xrp_quote': xrp_quote,
        'fiat_i8n_currency': payment_item.fiat_i8n_currency,
        'fiat_i8n_price': payment_item.fiat_i8n_price,
        'request_hash':shortuuid.uuid(),
    }

    create_payload = {
        'txjson': {
                'TransactionType' : 'Payment',
                'Destination' : wallet.classic_address,
                'Amount': str(xrp_to_drops(xrp_amount)),
        },
        "custom_meta": {
            "blob": json.dumps(payment_request_dict),
            "instruction": f"Pay {payment_item.fiat_i8n_amount} {payment_item.fiat_i8n_currency} for item {payment_item.name}"
        }
    }   

    created = sdk.payload.create(create_payload)

    return redirect(created.to_dict()['next']['always'], code=302)    



@app.route('/payment_item', methods=['POST'])  # depricated
@cross_origin()
def create_payment_item():
    app.logger.info("create payment item")

    # lookup the wallet by the classic address in the jwt
    jwt_body = get_token_body(dict(request.headers)[
                              "Authorization"].replace("Bearer ", ""))

    wallet = db.session.query(Wallet).filter_by(
        classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message": "wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED

    # print(json.dumps(wallet.serialize(), indent=4))
    payment_item_name = request.json.get('name')
    description = request.json.get('description')
    price = float(request.json.get('price'))
    sku_id = str(uuid.uuid4()).replace("-", "")[:10]

    payment_item = PaymentItem(
        wallet_id=wallet.wallet_id, 
        name=payment_item_name,
        description=description,
        fiat_i8n_price=price, 
        fiat_i8n_currency='USD', 
        sku_id=sku_id)

    save_images_for_request(request, payment_item, app)

    db.session.add(payment_item)
    db.session.commit()
    response = {'full_messages': ['PaymentItem updated successfully']}
    response.update(PaymentItemDetailsSerializer(payment_item).data)
    return jsonify(response)


@app.route("/xumm/deeplink/payment/basic", methods=['GET'])
@cross_origin()
@log_decorator(app.logger)
def xumm_deeplink_payment_basic():
    # lookup the wallet by the classic address in the jwt
    classic_address = request.args.get('classic_address')
    if classic_address is None:
        return jsonify({"message": "wallet address not found, requires classic_address"}), HTTPStatus.BAD_REQUEST

    amount = request.args.get('amount')
    if amount is None:
        return jsonify({"message": "amount not found, requires amount"}), HTTPStatus.BAD_REQUEST

    memo = request.args.get('memo')
    if memo is None:
        memo = "xURL payment request"

    # classic_address = get_token_sub(dict(request.headers)["Authorization"])
    wallet = db.session.query(Wallet).filter_by(
        classic_address=classic_address).first()
    if wallet is None:
        return jsonify({"message": "wallet not found, bad request"}), HTTPStatus.BAD_REQUEST

    create_payload = {
        'txjson': {
            'TransactionType': 'Payment',
            'Destination': classic_address,
            'Amount': str(xrp_to_drops(float(amount))),
        }
    }

    created = sdk.payload.create(create_payload)

    # return jsonify(created.to_dict()), 200
    return redirect(created.to_dict()['next']['always'], code=302)


# @app.route("/xumm/ping", methods=['GET'])
# @cross_origin()
# @log_decorator(app.logger)
# def xumm_ping():
#     try:
#         app_details = sdk.ping()
#         a_m = app_details.to_dict()
#         a_m['xapp_deeplink'] = config['XUMM_APP_DEEPLINK']
#         return jsonify(a_m), 200
#     except Exception as e:
#         app.logger.error(e)
#         return jsonify({'error':'could not ping'}), 400

# @app.route("/xumm/app", methods=['GET','POST', 'OPTIONS'])
# @cross_origin()
# @log_decorator(app.logger)
# def xumm_app():

#     app.logger.info("==== xumm app")

#     if request.method == 'OPTIONS':
#         return jsonify({'message':"OK"}), 200, {'Access-Control-Allow-Origin':'*',
#                                                 'Access-Control-Allow-Headers':'Content-Type, Authorization',
#                                                 'Access-Control-Allow-Methods':'POST, OPTIONS'}

#     return jsonify({'message':'xumm_app'}), 200

# https://devapi.xurlpay.org/v1/xumm/webhook
@app.route("/xumm/webhook", methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
@log_decorator(app.logger)
def xumm_webhook():

    app.logger.info("==== xumm webhook")

    if request.method == 'OPTIONS':
        return jsonify({'message': "OK"}), 200, {'Access-Control-Allow-Origin': '*',
                                                 'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                                                 'Access-Control-Allow-Methods': 'POST, OPTIONS'}

    #  {
    #     "meta": {
    #         "url": "https://devapi.xurlpay.org/v1/xumm/webhook",
    #         "application_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
    #         "payload_uuidv4": "62d7bc46-3e46-45ed-8358-e87812f15a6e",
    #         "opened_by_deeplink": true
    #     },
    #     "custom_meta": {
    #         "identifier": null,
    #         "blob": "{\"amount\": 1.25, \"amount_drops\": 1250000, \"address\": \"rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y\", \"network_endpoint\": \"https://s.altnet.rippletest.net:51234/\", \"network_type\": \"testnet\", \"memo\": \"its for the kids man 2\", \"request_hash\": \"M97R6EEXdgXxyKd9myFgD8\"}",
    #         "instruction": "its for the kids man 2"
    #     },
    #     "payloadResponse": {
    #         "payload_uuidv4": "62d7bc46-3e46-45ed-8358-e87812f15a6e",
    #         "reference_call_uuidv4": "11b36850-eaaf-406d-bf3d-622e3882c678",
    #         "signed": true,
    #         "user_token": true,
    #         "return_url": {
    #             "app": null,
    #             "web": null
    #         },
    #         "txid": "8340735242F2B65392F5734A49209A13BD4BC77DAED4CC99B5ACFB8C67BE9E76"
    #     },
    #     "userToken": {
    #         "user_token": "83234d7d-54d6-4240-89a3-e86cb97603cd",
    #         "token_issued": 1668293195,
    #         "token_expiration": 1670986728
    #     }
    # }

    json_body = request.get_json()

    # get the xumm payload by the payload_uuidv4
    payload = XummPayload.get_by_payload_uuidv4(
        json_body['payloadResponse']['payload_uuidv4'])
    if payload is None:
        return jsonify({'message': 'payload not found'}), 404
    payload.set_is_signed_bool(json_body['payloadResponse']['signed'])
    payload.txid = json_body['payloadResponse']['txid']
    payload.webhook_body = json.dumps(json_body)
    db.session.commit()

    app.logger.info(json.dumps(json_body, indent=4))
    return jsonify({'message': 'xumm_webhook'}), 200

# https://devapi.xurlpay.org/v1/xumm/webhook


@app.route("/xumm/app", methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
@log_decorator(app.logger)
def xumm_app():

    app.logger.info("==== xumm app")

    if request.method == 'OPTIONS':
        return jsonify({'message': "OK"}), 200, {'Access-Control-Allow-Origin': '*',
                                                 'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                                                 'Access-Control-Allow-Methods': 'POST, OPTIONS'}
    app.logger.info(
        f"{request} {request.args} {request.headers} {request.environ} {request.method} {request.url}")

    # lookup the wallet by the classic address in the jwt
    xAppStyle = request.args.get('xAppStyle')
    if xAppStyle is None:
        xAppStyle = "LIGHT"

    xAppToken = request.args.get('xAppToken')
    if xAppToken is None:
        return jsonify({"xAppToken": "token not found unauthorized"}), HTTPStatus.UNAUTHORIZED

    create_payload = {
        'txjson': {
            'TransactionType': 'Payment',
            'Destination': 'rNDtp9V6MUnbb14fPtVrCqR2Ftd6V17RLw',
            'Amount': str(xrp_to_drops(9.23)),
        }
    }

    created = sdk.payload.create(create_payload)

    # return jsonify(created.to_dict()), 200
    return redirect(created.to_dict()['next']['always'], code=302)


# @app.route("/xumm/pay", methods=['POST', 'OPTIONS'])
# @cross_origin()
# @log_decorator(app.logger)
# def xumm_pay():

#     app.logger.info("==== xumm pay")

#     if request.method == 'OPTIONS':
#         return jsonify({'message':"OK"}), 200, {'Access-Control-Allow-Origin':'*',
#                                                 'Access-Control-Allow-Headers':'Content-Type, Authorization',
#                                                 'Access-Control-Allow-Methods':'POST, OPTIONS'}


#     # const request = {
#     #     "TransactionType": "Payment",
#     #     "Destination": "rwietsevLFg8XSmG3bEZzFein1g8RBqWDZ",
#     #     "Amount": "10000",
#     #     "Memos": [
#     #     {
#     #         "Memo": {
#     #         "MemoData": "F09F988E20596F7520726F636B21"
#     #         }
#     #     }
#     #     ]
#     # }

#     # const payload = await Sdk.payload.create(request, true)
#     # console.log(payload)

#     json_body = request.get_json()
#     # app.logger.info(json_body, list(json_body.keys(), 'amount' not in list(json_body.keys()))
#     if 'amount' not in list(json_body.keys()):
#         return jsonify({"message":"Missing required body element amount"}), HTTPStatus.BAD_REQUEST

#     if 'classic_address' not in list(json_body.keys()):
#         return jsonify({"message":"Missing required body element classic_address"}), HTTPStatus.BAD_REQUEST

#     create_payload = {
#         'txjson': {
#             'TransactionType' : 'Payment',
#             'Destination' : json_body['classic_address'],
#             'Amount': str(json_body['amount']),
#         }
#     }

#     created = sdk.payload.create(create_payload)

#     return jsonify(created.to_dict()), 200
