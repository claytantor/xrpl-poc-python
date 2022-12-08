import os

from http.client import HTTPException
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
# from fastapi.logger import logger as fastapi_logger
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

import functools
import re
import typing

from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send
import logging



from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

import logging

from api import routes
# from api.models import Message
# from api.schema import MessageSchema

from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

logging.basicConfig(level=logging.DEBUG)
ulogger = logging.getLogger("uvicorn.error")



# formatter = logging.Formatter('%(levelname)s\t%(asctime)s - %(name)s - %(message)s')
# stream = logging.StreamHandler()
# stream.setFormatter(formatter)
# logger.addHandler(stream)

# logging.warning('Watch out!')  # will print a message to the console
# logging.info('I told you so')  # will not print anything

class MyMiddleware:
    def __init__(
            self,
            some_attribute: str,
    ):
        self.some_attribute = some_attribute

    async def __call__(self, request: Request, call_next):
        # do something with the request object
        content_type = request.headers.get('Content-Type')
        ulogger.info(f'MyMiddleware {content_type}')
        
        # process the request and get the response    
        response = await call_next(request)
        
        return response




def create_app():
    app = FastAPI(title="xurlpay API",
    description="Durable payment automation for XRP",
    version=config['API_VERSION'],
    openapi_url=config['API_OPENAPI_URL'],)

    return app


app = create_app()
app.include_router(routes.router)


# my_middleware = MyMiddleware(some_attribute="some_attribute_here_if_needed")
# app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.middleware("http")
async def CorsSupportMiddleware(request: Request, call_next):
    ulogger.info("CorsSupportMiddleware was called")

    headers_cors = {}
    headers_cors["Access-Control-Allow-Origin"] = "*"
    headers_cors["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    headers_cors["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    headers_cors["Access-Control-Max-Age"] = "86400"
    headers_cors["Access-Control-Allow-Credentials"] = "true"
    headers_cors["Access-Control-Expose-Headers"] = "Content-Length, Content-Range"

    if request.method == "OPTIONS":
        #return JSONResponse(status_code=204, headers=headers_cors, content={})
        return PlainTextResponse("OK", status_code=200, headers=headers_cors)

    response = await call_next(request) 

    response.headers.update(headers_cors)
    return response






