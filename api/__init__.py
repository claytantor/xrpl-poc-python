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

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

import logging


from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

def create_app():
    app = FastAPI(title="xurlpay API",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version=config['API_VERSION'],)
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "hello world again"}




