import os
import uvicorn

from fastapi import FastAPI
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import PlainTextResponse

import logging

from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional


import logging

from api.routes import base
from api.routes import xurl


logging.basicConfig(level=logging.DEBUG)
ulogger = logging.getLogger("uvicorn.error")
ulogger.info("APP START")
log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
ulogger.info("APP CONFIG PATH: " + os.getenv("APP_CONFIG"))

from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}


class ApiMiddleware:
    def __init__(
            self,
            some_attribute: str,
    ):
        self.some_attribute = some_attribute

    async def __call__(self, request: Request, call_next):
        # do something with the request object
        content_type = request.headers.get('Content-Type')
        ulogger.info(f'ApiMiddleware {content_type}')
        
        # process the request and get the response    
        response = await call_next(request)
        
        return response


def create_app():
    app = FastAPI(title="xurlpay API",
    description="Durable payment automation for XRP",
    version=config['API_VERSION'],
    openapi_url=config['API_OPENAPI_URL'],
    root_path=config['API_ROOT_PATH'])
    return app

app = create_app()
app.include_router(base.router)
app.include_router(xurl.router)

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
    headers_cors["Access-Control-Allow-Headers"] = "Content-Type, Authorization, x-xurl-user, x-xurl-shopid"
    headers_cors["Access-Control-Max-Age"] = "86400"
    headers_cors["Access-Control-Allow-Credentials"] = "true"
    headers_cors["Access-Control-Expose-Headers"] = "Content-Length, Content-Range"
    
    
    if request.method == "OPTIONS":
        return PlainTextResponse("OK", status_code=200, headers=headers_cors)

    response = await call_next(request) 

    response.headers.update(headers_cors)
    return response






