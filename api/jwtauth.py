import jwt
from datetime import datetime as dt

# {'client_id': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'scope': 'XummPkce', 'aud': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'sub': 'rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y', 'email': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce+rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y@xumm.me', 'app_uuidv4': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'app_name': 'dev-xurlpay', 'payload_uuidv4': 'a9d8f45a-16ff-48ee-8ef1-163ce3b10f7c', 'usertoken_uuidv4': '4de21968-8c2f-4fb3-9bb6-94b589a13a8c', 'network_type': 'TESTNET', 'network_endpoint': 'wss://s.altnet.rippletest.net:51233', 'iat': 1668223704, 'exp': 1668310104, 'iss': 'https://oauth2.xumm.app'}

def make_signed_token(secret, payload):
    return jwt.encode(payload, secret, algorithm="HS256")

def get_token_sub(token):
    try:
        jwt_body = jwt.decode(token, options={"verify_signature": False})
        return jwt_body['sub']
    except:
        return None

def get_token_body(token):
    try:
        jwt_body = jwt.decode(token, options={"verify_signature": False})
        return jwt_body
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

# def is_token_valid(token):

#     try:
#         jwt_body = jwt.decode(token, options={"verify_signature": False})
#         sid = jwt_body['sid']
#         wallet = db.session.query(Wallet).filter_by(classic_address=sid).first()
#         if wallet is None:
#             return False
#         else:
#             jwt.decode(token, wallet.private_key, algorithms=["HS256"])
#             return True
            
#     except jwt.ExpiredSignatureError as e:
#         print(e)
#         return False
#     except jwt.InvalidTokenError as e:
#         print(e)
#         return False
#     except Exception as e:
#         print(e)
#         return False

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

