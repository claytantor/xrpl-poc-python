import functools
from http.client import HTTPException
from http import HTTPStatus
from typing import Tuple
from uuid import uuid4
from fastapi.responses import JSONResponse

import logging
import inspect

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# def get_dict_ignore_case(key, dict):
#     dictlower = {k.lower(): v for k, v in dict.iteritems()}
#     return dictlower.get(key.lower())


# def verify_user_jwt_scopes(func):
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         # print(f"=== verify_user_jwt_scopes {args} {kwargs}")
#         # starlette.requests.Request
#         # logger.debug(f"=== verify_user_jwt_scopes {args} {kwargs}")
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


def determine_xurl_wallet(method_or_name):
    def decorator(method):
        if callable(method_or_name):
            # print("CALL method_or_name",method_or_name)
            method.gw_method = method.__name__
        else:
            # print("method_or_name",method_or_name)
            method.gw_method = method_or_name
        
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            print(f"=== wrapper determine_xurl_wallet 2 {args} {kwargs} {'request' in kwargs}")

            # right now we are not using scopes
            if 'request' in kwargs:
                request = kwargs['request']

                logger.debug(f"=== request.headers {request.headers}")
                if 'x-xurl-shopid' not in request.headers:
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="x-xurl-shopid header missing")
                
                if 'x-xurl-user' in request.headers:
                    logger.debug(f"=== x-xurl-user {request.headers['x-xurl-user']}")

                id_header: Tuple[bytes] = "x-request-id".encode(), str(uuid4()).encode()
                xurl_pay_wallet: Tuple[bytes] = "x-xurl-shopid".encode(), "707d6cb060".encode()
                request.headers.__dict__["_list"].append(id_header)
                request.headers.__dict__["_list"].append(xurl_pay_wallet)

                if inspect.iscoroutinefunction(method):
                    return await method(*args, **kwargs)
                else:
                    return method(*args, **kwargs)


                # if 'headers' in request:
                #     # can expect lower case
                #     if 'authorization' in request.headers:
                #         authorization = request.headers['authorization']
                #         # print(f"=== authorization {authorization}")
                #         # dont do anything with it yet
                #         # print(f"=== method type {type(method)} {inspect.iscoroutinefunction(method)}")
                #         if inspect.iscoroutinefunction(method):
                #             return await method(*args, **kwargs)
                #         else:
                #             return method(*args, **kwargs)
                #     else:                   
                #         return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "auth headers, invalid or missing"})
                # else:
                #     return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "request headers, invalid or missing"})
            else:
                return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "request, invalid or missing"})



        return wrapper

    if callable(method_or_name):
        return decorator(method_or_name)

    return decorator