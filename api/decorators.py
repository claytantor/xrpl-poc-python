import functools
from http.client import HTTPException
from http import HTTPStatus
from fastapi.responses import JSONResponse

import logging
import inspect

logging.basicConfig(level=logging.DEBUG)
ulogger = logging.getLogger("uvicorn.error")

# def get_dict_ignore_case(key, dict):
#     dictlower = {k.lower(): v for k, v in dict.iteritems()}
#     return dictlower.get(key.lower())


# def verify_user_jwt_scopes(func):
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         # print(f"=== verify_user_jwt_scopes {args} {kwargs}")
#         # starlette.requests.Request
#         # ulogger.debug(f"=== verify_user_jwt_scopes {args} {kwargs}")
#         if 'request' in kwargs:
#             request = kwargs['request']
#             if 'headers' in request:
#                 # can expect lower case
#                 if 'authorization' in request.headers:
#                     authorization = request.headers['authorization']
#                     print(f"=== authorization {authorization}")
#                 else:                   
#                     return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "auth headers, invalid or missing"})
#             else:
#                 return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "request headers, invalid or missing"})
#         else:
#           return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "request, invalid or missing"})

#         return func(*args, **kwargs)
#     return wrapper


def verify_user_jwt_scopes(method_or_name):
    def decorator(method):
        if callable(method_or_name):
            # print("CALL method_or_name",method_or_name)
            method.gw_method = method.__name__
        else:
            # print("method_or_name",method_or_name)
            method.gw_method = method_or_name
        
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
        #   print(f"=== verify_user_jwt_scopes 2 {args} {kwargs}")
        #   print("==== CALL method.gw_method", method.gw_method)          
          scopes = method.gw_method

          # right now we are not using scopes
          if 'request' in kwargs:
            request = kwargs['request']
            if 'headers' in request:
                # can expect lower case
                if 'authorization' in request.headers:
                    authorization = request.headers['authorization']
                    # print(f"=== authorization {authorization}")
                    # dont do anything with it yet
                    # print(f"=== method type {type(method)} {inspect.iscoroutinefunction(method)}")
                    if inspect.iscoroutinefunction(method):
                        return await method(*args, **kwargs)
                    else:
                        return method(*args, **kwargs)
                else:                   
                    return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "auth headers, invalid or missing"})
            else:
                return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "request headers, invalid or missing"})
          else:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "request, invalid or missing"})



        return wrapper

    if callable(method_or_name):
        return decorator(method_or_name)

    return decorator


# def log_decorator(logger, log_enabled=True, log_level=logging.INFO):
#     def actual_decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             if log_enabled:
#                 # print("Calling Function: " + func.__name__))
#                 logger.log(log_level, f"{request.method} {request.path} {func.__name__}")
#             try:
#                 return func(*args, **kwargs)     
#             except Exception as e:
#               if log_enabled:
#                 logger.exception(e)
                
#         return wrapper
#     return actual_decorator


# def verify_user_jwt_scopes(method_or_name):

#     def decorator(method):
#         if callable(method_or_name):
#             # print("CALL method_or_name",method_or_name)
#             method.gw_method = method.__name__
#         else:
#             # print("method_or_name",method_or_name)
#             method.gw_method = method_or_name
        
#         @functools.wraps(method)
#         async def wrapper(*args, **kwargs):
#             # method(*args, **kwargs)

#             logger.info("==== CALL method.gw_method", method.gw_method)
          
#             scopes = method.gw_method

#             if 'request' in kwargs:
#               request = kwargs['request']
#               headers = dict(request.headers)

#               if request.method == 'OPTIONS':
#                 return await method(*args, **kwargs)

#               if 'Authorization' not in headers:
#                   raise HTTPException(status_code=400, detail="Authorization header invalid missing")
#               else:
#                 return await method(*args, **kwargs)

#               # user_id = get_token_sub(dict(request.headers)["Authorization"].replace("Bearer ", ""))

#               # if user_id is None:
#               #   return make_response(jsonify({"error": "Authorization is missing"}), 401)

#               # wallet = Wallet.get_wallet_by_classic_address(user_id)

#               # if 'Authorization' in headers \
#               #   and is_token_valid(headers["Authorization"]) \
#               #   and has_all_scopes(headers["Authorization"], scopes):

#               #   return method(*args, **kwargs)
                
#               # else:
#               #   return make_response(jsonify({"error": "Invalid token."}), 401)

#         return wrapper

#     if callable(method_or_name):
#         return decorator(method_or_name)

#     return decorator


# def verify_user_jwt(f):
#   @functools.wraps(f)
#   def decorated_function(*args, **kwargs):
#     headers = dict(request.headers)
  
#     if request.method == 'OPTIONS':
#       return f(*args, **kwargs)

#     if 'Authorization' in headers and is_token_valid(headers["Authorization"]):
#       return f(*args, **kwargs)
#     else:
#       return make_response(jsonify({"error": "Invalid token"}), 401)    

#   return decorated_function
