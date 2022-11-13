from flask import Flask, jsonify, request,redirect,render_template,url_for
from flask import current_app as app
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
import os, sys
import shortuuid
import json
import base64
from api.xrpcli import XUrlWallet, verify_msg, drops_to_xrp
from api.models import Wallet
from datetime import datetime as dt, timedelta
import jwt

from api.serializers import XummApplicationDetailsSerializer
from api.xrpcli import xrp_to_drops, XummWallet, get_rpc_network



from . import db
from .decorators import log_decorator, verify_user_jwt_scopes
from .jwtauth import is_token_valid, has_all_scopes, get_token_body, get_token_sub


from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}


scopes = {
        'wallet_owner': [
                    'wallet.view',
                    'wallet.transfer',
                    'wallet.sign',
                    'wallet.receive',
                    'wallet.request'],
        'wallet_owner_refresh':['wallet.refresh'],
    }

@app.route("/")
def hello_world():
    return jsonify({'message':"Hello xURL"}), 200

@app.route("/version", methods=['GET'])
@cross_origin()
@log_decorator(app.logger)
def api_version():
    app.logger.info(f"version: {config['APP_VERSION']}")
    return jsonify({'version':config['APP_VERSION']}), 200


@app.route('/auth/access_token', methods=['POST','OPTIONS'])
@cross_origin(origins=['*','https://rapaygo.com','https://dev.rapaygo.com/'])
@log_decorator(app.logger)
def post_access_token():

    if request.method == 'OPTIONS':
        return jsonify({'message':"OK"}), 200, {'Access-Control-Allow-Origin':'*',
                                                'Access-Control-Allow-Headers':'Content-Type, Authorization',
                                                'Access-Control-Allow-Methods':'POST, OPTIONS'}
    if request.method == 'POST':
        json_body = request.json
        # app.logger.info(json.dumps(json_body, indent=4))
        if json_body is None:
            return jsonify({"message":"empty body not allowed"}), HTTPStatus.BAD_REQUEST
        

        if 'classic_address' not in list(json_body.keys()):
            return jsonify({"message":"Missing required body element classic_address"}), HTTPStatus.BAD_REQUEST
        if 'private_key' not in list(json_body.keys()):
            return jsonify({"message":"Missing required body element private_key"}), HTTPStatus.BAD_REQUEST 
    
        classic_address = json_body['classic_address']
        private_key = json_body['private_key']
        app.logger.debug(f"auth body: {json_body}")
        wallet = db.session.query(Wallet).filter_by(classic_address=classic_address, private_key=private_key).first()
        
        # dont let them know the wallet_id is wrong
        if wallet is None:
            return jsonify({"message":"wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED
        

        return get_auth(wallet, classic_address, private_key, wallet.private_key,  
                scopes['wallet_owner'], scopes_refresh=scopes['wallet_owner_refresh'])



def get_auth_base(wallet, username, scopes, scopes_refresh):

    exp_time = dt.utcnow()+timedelta(hours=24)
    exp_time_refresh = dt.utcnow()+timedelta(days=30)

    jwt_body = {"sid": username, 
            'scopes': scopes,
            "exp":int(exp_time.timestamp())}


    
    token = jwt.encode(
            jwt_body,
            wallet.private_key,
            algorithm="HS256")  


    refresh_body = {"sid": username,
            'scopes': scopes_refresh,
            "exp":int(exp_time_refresh.timestamp())} 

    refresh_token = jwt.encode(
            refresh_body,
            wallet.private_key,
            algorithm="HS256")

    return token, refresh_token

def get_auth(wallet, username, test_phrase, pass_phrase, scopes, scopes_refresh):

    token, refresh_token = get_auth_base(wallet, username, scopes, scopes_refresh)

    return jsonify({'access_token':token, 
                        'refresh_token':refresh_token,
                        "wallet_id":wallet.wallet_id}), 200, {'subject':token} 

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
    jwt_body = get_token_body(dict(request.headers)["Authorization"].replace("Bearer ",""))    

    wallet = db.session.query(Wallet).filter_by(classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message":"wallet not found"}), HTTPStatus.NOT_FOUND
        # create a new wallet
        # wallet = make_wallet(classic_address=jwt_body['sub']) # create a new wallet


    # {'client_id': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'scope': 'XummPkce', 'aud': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'sub': 'rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y', 'email': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce+rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y@xumm.me', 'app_uuidv4': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'app_name': 'dev-xurlpay', 'payload_uuidv4': 'a9d8f45a-16ff-48ee-8ef1-163ce3b10f7c', 'usertoken_uuidv4': '4de21968-8c2f-4fb3-9bb6-94b589a13a8c', 'network_type': 'TESTNET', 'network_endpoint': 'wss://s.altnet.rippletest.net:51233', 'iat': 1668223704, 'exp': 1668310104, 'iss': 'https://oauth2.xumm.app'}
    xumm_wallet = XummWallet(
        network_endpoint=get_rpc_network(jwt_body['network_type']), 
        classic_address=wallet.classic_address)

    return jsonify({
        'classic_address':wallet.classic_address,
        'wallet_info':jwt_body,
        'account_data':xumm_wallet.account_data}), 200

@app.route("/wallet", methods=['POST'])
@cross_origin()
@log_decorator(app.logger)
def create_wallet():
    jwt_body = get_token_body(dict(request.headers)["Authorization"].replace("Bearer ",""))    

    wallet = db.session.query(Wallet).filter_by(classic_address=jwt_body['sub']).first()
    if wallet is None:
        # create a new wallet
        wallet = make_wallet(classic_address=jwt_body['sub'])

    xumm_wallet = XummWallet(
        network_endpoint=get_rpc_network(jwt_body['network_type']), 
        classic_address=wallet.classic_address)

    return jsonify({
        'classic_address':wallet.classic_address,
        'wallet_info':jwt_body,
        'account_data':xumm_wallet.account_data}), 200       

@app.route("/pay_request", methods=['POST'])
@cross_origin()
@log_decorator(app.logger)
def create_pay_request():
    json_body = request.get_json()


    # lookup the wallet by the classic address in the jwt
    #classic_address = get_token_sid(dict(request.headers)["Authorization"])    

    jwt_body = get_token_body(dict(request.headers)["Authorization"].replace("Bearer ",""))    

    wallet = db.session.query(Wallet).filter_by(classic_address=jwt_body['sub']).first()
    if wallet is None:
        return jsonify({"message":"wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED


    if 'amount' not in list(json_body.keys()):
        return jsonify({"message":"Missing required body element amount"}), HTTPStatus.BAD_REQUEST
    xrp_amount = float(json_body['amount'])

    memo=f"xURL payment request {shortuuid.uuid()[:8]}"
    if 'memo' in list(json_body.keys()):
        memo = json_body['memo']
    
    # receiving_wallet = XUrlWallet(network=config['JSON_RPC_URL'], seed=wallet.seed)
    # payment_request_dict, payment_request = receiving_wallet.generate_payment_request(amount=xrp_amount, memo=memo)

    xumm_wallet = XummWallet(
        network_endpoint=get_rpc_network(jwt_body['network_type']), 
        classic_address=wallet.classic_address)

    return jsonify(xumm_wallet.generate_payment_request(xrp_amount=xrp_amount, memo=memo)), 200


@app.route("/send_payment", methods=['POST'])
@cross_origin()
@log_decorator(app.logger)
def send_payment():
    json_body = request.get_json()
    # json_body = json.loads(json_body['data'])
    # print("==== send payment",json.loads(json_body['data']))

    # lookup the wallet by the classic address in the jwt
    classic_address = get_token_sub(dict(request.headers)["Authorization"])    
    wallet = db.session.query(Wallet).filter_by(classic_address=classic_address).first()
    if wallet is None:
        return jsonify({"message":"wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED


    # ok now lets pay it with a faucet
    # decode the payment request
    pr_parts = json_body['payment_request'].split(":")
    # print("==== send payment",pr_parts)
    

    # # verify the signed message

    message_payload = json.loads(base64.b64decode(pr_parts[0]))
    print("==== send payment",message_payload)

    # use the public key to verify
    try:
        sending_wallet = XUrlWallet(network=config['JSON_RPC_URL'], seed=wallet.seed) #this is a faucet wallet
        
        # this will throw an exception if the signature is not valid      
        verify_msg(pr_parts[0], pr_parts[1], message_payload['public_key'])

        tx_response_status, tx_response_result = sending_wallet.send_payment(
            amount_xrp=message_payload['amount'],
            destination_address=message_payload['address']
        )

        print(tx_response_status, tx_response_result)
        return jsonify(tx_response_result), 200


    except Exception as e:
        print("=== COULD NOT VERIFY SIG", e)
        return jsonify({'error':'could not verify'}), 400


@app.route("/xumm/deeplink", methods=['GET'])
@cross_origin()
@log_decorator(app.logger)
def xumm_deeplink():
    # lookup the wallet by the classic address in the jwt
    classic_address = request.args.get('classic_address')
    if classic_address is None:
        return jsonify({"message":"wallet address not found, requires classic_address"}), HTTPStatus.BAD_REQUEST

    amount = request.args.get('amount')
    if amount is None:
        return jsonify({"message":"amount not found, requires amount"}), HTTPStatus.BAD_REQUEST

    memo = request.args.get('memo')
    if memo is None:
        memo = "xURL payment request"

    # classic_address = get_token_sub(dict(request.headers)["Authorization"])    
    wallet = db.session.query(Wallet).filter_by(classic_address=classic_address).first()
    if wallet is None:
        return jsonify({"message":"wallet not found, bad request"}), HTTPStatus.BAD_REQUEST

    # xumm_wallet = XummWallet(
    #     network_endpoint=get_rpc_network(get_token_body(dict(request.headers)["Authorization"])['network_type']), 
    #     classic_address=wallet.classic_address)

    #https://xumm.app/detect/xapp:sandbox.32849dc99872?amount=11.25&memo=hi

    # return jsonify(xumm_wallet.generate_deeplink()), 200
    return redirect(f"https://xumm.app/detect/xapp:sandbox.32849dc99872?amount={amount}&memo={memo}&classic_address={classic_address}", code=302)



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

#https://devapi.xurlpay.org/v1/xumm/webhook
@app.route("/xumm/webhook", methods=['GET','POST', 'OPTIONS'])
@cross_origin()
@log_decorator(app.logger)
def xumm_webhook():

    app.logger.info("==== xumm webhook")

    if request.method == 'OPTIONS':
        return jsonify({'message':"OK"}), 200, {'Access-Control-Allow-Origin':'*',
                                                'Access-Control-Allow-Headers':'Content-Type, Authorization',
                                                'Access-Control-Allow-Methods':'POST, OPTIONS'}
    json_body = request.get_json()
    app.logger.info(json.dumps(json_body, indent=4))
    return jsonify({'message':'xumm_webhook'}), 200

#https://devapi.xurlpay.org/v1/xumm/webhook
@app.route("/xumm/app", methods=['GET','POST', 'OPTIONS'])
@cross_origin()
@log_decorator(app.logger)
def xumm_app():

    app.logger.info("==== xumm app")

    if request.method == 'OPTIONS':
        return jsonify({'message':"OK"}), 200, {'Access-Control-Allow-Origin':'*',
                                                'Access-Control-Allow-Headers':'Content-Type, Authorization',
                                                'Access-Control-Allow-Methods':'POST, OPTIONS'}
    json_body = request.get_json()
    app.logger.info(json.dumps(json_body, indent=4))
    return jsonify({'message':'xumm_webhook'}), 200



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