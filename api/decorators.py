import functools
from flask import jsonify, request, make_response
from flask import current_app as app

from .jwtauth import is_token_valid, has_all_scopes, get_token_sub
from .models import Wallet
import logging

def log_decorator(logger, log_enabled=True, log_level=logging.INFO):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if log_enabled:
                # print("Calling Function: " + func.__name__))
                logger.log(log_level, f"{request.method} {request.path} {func.__name__}")
            try:
                return func(*args, **kwargs)     
            except Exception as e:
              if log_enabled:
                logger.exception(e)
                
        return wrapper
    return actual_decorator


def verify_user_jwt_scopes(method_or_name):

    def decorator(method):
        if callable(method_or_name):
            # print("CALL method_or_name",method_or_name)
            method.gw_method = method.__name__
        else:
            # print("method_or_name",method_or_name)
            method.gw_method = method_or_name
        
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            # method(*args, **kwargs)

            print("==== CALL method.gw_method", method.gw_method)

            headers = dict(request.headers)
            scopes = method.gw_method
          
            if request.method == 'OPTIONS':
              return method(*args, **kwargs)

            if 'Authorization' not in headers:
                return make_response(jsonify({"error": "Invalid request missing authorization header."}), 401)

            user_id = get_token_sub(dict(request.headers)["Authorization"].replace("Bearer ", ""))

            if user_id is None:
              return make_response(jsonify({"error": "Authorization is missing"}), 401)

            wallet = Wallet.get_wallet_by_classic_address(user_id)

            if 'Authorization' in headers \
              and is_token_valid(headers["Authorization"]) \
              and has_all_scopes(headers["Authorization"], scopes):

              return method(*args, **kwargs)
              
            else:
              return make_response(jsonify({"error": "Invalid token."}), 401)

        return wrapper

    if callable(method_or_name):
        return decorator(method_or_name)

    return decorator


def verify_user_jwt(f):
  @functools.wraps(f)
  def decorated_function(*args, **kwargs):
    headers = dict(request.headers)
  
    if request.method == 'OPTIONS':
      return f(*args, **kwargs)

    if 'Authorization' in headers and is_token_valid(headers["Authorization"]):
      return f(*args, **kwargs)
    else:
      return make_response(jsonify({"error": "Invalid token"}), 401)    

  return decorated_function
