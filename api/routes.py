from flask import Flask, jsonify, request
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

from . import db
from .decorators import log_decorator, verify_user_jwt_scopes
from .jwtauth import is_token_valid, has_all_scopes, get_token_sid


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
def api_version():
    return jsonify({'version':"0.1.2"}), 200


@app.route('/auth/access_token', methods=['POST','OPTIONS'])
@cross_origin(origins=['*','https://rapaygo.com','https://dev.rapaygo.com/'])
def post_access_token():
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

@app.route("/wallet", methods=['GET'])
@verify_user_jwt_scopes(scopes['wallet_owner'])
@cross_origin()
def get_wallet():
    wallet = Wallet.query.first()

    # now get account info
    xurl_wallet = XUrlWallet(seed=wallet.seed)
    account_info = xurl_wallet.get_account_info()
    wallet_model = wallet.serialize()
    wallet_model['account_info'] = account_info

    return jsonify(wallet_model), 200

@app.route("/wallet", methods=['POST'])
@cross_origin()
def create_wallet():
    json_body = request.get_json()
    seed = None
    # generate a new wallet
    if 'seed' in json_body.keys():
        seed = json_body['seed']

    xurl_wallet_n = XUrlWallet(network=config['JSON_RPC_URL'], isFaucet=True)
    wallet = Wallet(seed=xurl_wallet_n.seed,
                  private_key=xurl_wallet_n.private_key,
                  public_key=xurl_wallet_n.public_key,
                  classic_address=xurl_wallet_n.wallet.classic_address) # create a new wallet

    # save wallet to database
    db.session.add(wallet)
    db.session.commit()

    # n_w = wallet.serialize() # serialize the wallet with all the fields
    # n_w['seed'] = wallet.seed # add the seed to the wallet
    # n_w['private_key'] = wallet.private_key # add the private key to the wallet
    # n_w['public_key'] = wallet.public_key # add the public key to the wallet
    
    return jsonify(xurl_wallet_n.serialize()), 200


@app.route("/pay_request", methods=['POST'])
@cross_origin()
def create_pay_request():
    json_body = request.get_json()


    # lookup the wallet by the classic address in the jwt
    classic_address = get_token_sid(dict(request.headers)["Authorization"])    
    wallet = db.session.query(Wallet).filter_by(classic_address=classic_address).first()
    if wallet is None:
        return jsonify({"message":"wallet not found, unauthorized"}), HTTPStatus.UNAUTHORIZED


    if 'amount' not in list(json_body.keys()):
        return jsonify({"message":"Missing required body element amount"}), HTTPStatus.BAD_REQUEST
    xrp_amount = float(json_body['amount'])

    memo=f"xURL payment request {shortuuid.uuid()[:8]}"
    if 'memo' in list(json_body.keys()):
        memo = json_body['memo']
    
    receiving_wallet = XUrlWallet(network=config['JSON_RPC_URL'], seed=wallet.seed)
    payment_request_dict, payment_request = receiving_wallet.generate_payment_request(amount=xrp_amount, memo=memo)

    return jsonify({'body':payment_request_dict, 'payment_request':payment_request}), 200

@app.route("/send_payment", methods=['POST'])
@cross_origin()
def send_payment():
    json_body = request.get_json()
    # json_body = json.loads(json_body['data'])
    # print("==== send payment",json.loads(json_body['data']))

    # lookup the wallet by the classic address in the jwt
    classic_address = get_token_sid(dict(request.headers)["Authorization"])    
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

