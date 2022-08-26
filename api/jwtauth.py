import jwt
from . import db
from datetime import datetime as dt
from .models import Wallet


def get_token_sid(token):
    try:
        jwt_body = jwt.decode(token, options={"verify_signature": False})
        return jwt_body['sid']
    except:
        return None

def get_token_pos_id(token):
    try:
        jwt_body = jwt.decode(token, options={"verify_signature": False})
        return jwt_body['pos_id']
    except:
        return None

def has_all_scopes(token, scopes):
    try:
        jwt_body = jwt.decode(token, options={"verify_signature": False})
        if 'scopes' in jwt_body:
            for scope in scopes:
                if scope not in jwt_body['scopes']:
                    return False
            return True
            
    except jwt.ExpiredSignatureError as e:
        print(e)
        return False
    except jwt.InvalidTokenError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False

def is_token_valid(token):

    try:
        jwt_body = jwt.decode(token, options={"verify_signature": False})
        sid = jwt_body['sid']
        wallet = db.session.query(Wallet).filter_by(classic_address=sid).first()
        if wallet is None:
            return False
        else:
            jwt.decode(token, wallet.private_key, algorithms=["HS256"])
            return True
            
    except jwt.ExpiredSignatureError as e:
        print(e)
        return False
    except jwt.InvalidTokenError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False

def is_signed_token_valid(token, secret):

    try:
        jwt.decode(token, secret, algorithms=["HS256"])
        return True
            
    except jwt.ExpiredSignatureError as e:
        print(e)
        return False
    except jwt.InvalidTokenError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False

