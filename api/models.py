from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Float, and_, desc, event, or_, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import os
from datetime import datetime as dt
import json

from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}



Base = declarative_base()



class XrpNetwork():
    def __init__(self,     
        json_rpc: str,
        websocket: str,
        type: str,
        domain: str):
        self.json_rpc = json_rpc
        self.websocket = websocket
        self.type = type
        self.domain = domain

    def __init__(self, data):
        self.from_dict(data)
    

    def from_dict(self, data):
        for field in ['json_rpc', 'websocket', 'type', 'domain']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            "json_rpc": self.json_rpc,
            "websocket": self.websocket,
            "type": self.type,
            "domain": self.domain
        }


class XrpCurrencyRate():
    #   
    def __init__(self, 
        fiatCurrencyI8NCode: str,
        fiatCurrencyName: str,
        fiatCurrencySymbol: str,
        fiatCurrencyIsoDecimals: int,
        xrpRate: float):

        self.fiatCurrencyI8NCode = fiatCurrencyI8NCode
        self.fiatCurrencyName = fiatCurrencyName
        self.fiatCurrencySymbol = fiatCurrencySymbol
        self.fiatCurrencyIsoDecimals = fiatCurrencyIsoDecimals
        self.xrpRate = xrpRate


    def to_dict(self):
        return {
            "fiatCurrencyI8NCode": self.fiatCurrencyI8NCode,
            "fiatCurrencyName": self.fiatCurrencyName,
            "fiatCurrencySymbol": self.fiatCurrencySymbol,
            "fiatCurrencyIsoDecimals": self.fiatCurrencyIsoDecimals,
            "xrpRate": self.xrpRate
        }


class ApiInfo():
    version = config['API_VERSION']
    commit_sha = config['API_GIT_SHA']
    api_branch = config['API_GIT_BRANCH']

    def to_dict(self):
        return {
            'name':'xumm-api',
            'version':self.version,
            'commit_sha':self.commit_sha,
            'api_branch':self.api_branch
        }


class Message():
    message = ""


    def to_dict(self):
        return {
            'message':self.message
        }

class Wallet(Base):
    __tablename__ = "wallet"
    wallet_id = Column(Integer, primary_key=True)
    seed = Column(String())
    private_key = Column(String())
    public_key = Column(String())
    classic_address = Column(String())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    ## adding fiat currency
    fiat_i8n_currency = Column(String(3))

    def __init__(self,
                 seed=None,
                 private_key=None,
                 public_key=None,
                 classic_address=None):
                 
        self.seed = seed
        self.private_key = private_key
        self.public_key = public_key
        self.classic_address = classic_address 
        self.fiat_i8n_currency = "USD" 
        self.created_at = dt.now()
        self.updated_at = dt.now()
    
    def __repr__(self):
        return f"<Wallet(wallet_id={self.wallet_id})>"

    def to_dict(self):
        return {
            "wallet_id": self.wallet_id,
            # "public_key": self.public_key,
            "classic_address": self.classic_address,
            # "fiat_i8n_currency": self.fiat_i8n_currency,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }


    # @staticmethod
    # def get_wallet_by_classic_address(classic_address):
    #     wallet = session.query(Wallet).filter_by(classic_address=classic_address).first()
    #     return wallet
    
class XummPayload(Base):
    __tablename__ = "xumm_payload"

    xumm_payload_id = Column(Integer, primary_key=True)
    body = Column(String(16000))
    webhook_body = Column(String(16000))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    payload_uuidv4 = Column(String(36))
    wallet_id = Column(Integer, ForeignKey('wallet.wallet_id'))

    is_signed = Column(Integer)
    txid = Column(String(64))


    payment_item_id = Column(Integer, ForeignKey('payment_item.payment_item_id'), nullable=True)
    payment_item = relationship('PaymentItem', foreign_keys=[payment_item_id])

    def __init__(self,
                 payload_body=None,
                 wallet_id=None,
                 payload_uuidv4=None):
                 
        self.body = payload_body
        self.wallet_id = wallet_id
        self.payload_uuidv4 = payload_uuidv4
        self.created_at = dt.now()
        self.updated_at = dt.now()
        self.is_signed = 0

    def __repr__(self):
        return f"<XummPayload(xumm_payload_id={self.xumm_payload_id})>"

    def from_dict(self, data):
        for field in ['xumm_payload_id', 'body', 'webhook_body', 'created_at', 'updated_at', 'payload_uuidv4', 'wallet_id', 'is_signed', 'txid']:
            if field in data:
                if data[field] != None:
                    setattr(self, field, data[field])

    @property
    def is_signed_bool(self):
        return False if self.is_signed == 0 else True

    def set_is_signed_bool(self, is_signed_bool=False):
        self.is_signed = 1 if is_signed_bool else 0

    
    def to_dict(self):
        return self.serialize()

        
    def serialize(self):
        is_signed = False if self.is_signed == 0 else True

        s_m = {
            "xumm_payload_id": self.xumm_payload_id,
            "is_signed": is_signed,
            "payload_uuidv4": self.payload_uuidv4,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "txid": self.txid,
        }

        if self.body:
            s_m["body"] = json.loads(self.body)

        if self.webhook_body:
            s_m["webhook_body"] = json.loads(self.webhook_body)

        return s_m



class PaymentItem(Base):
    __tablename__ = "payment_item"   

    payment_item_id = Column(Integer, primary_key=True, nullable=False)

    fiat_i8n_currency = Column(String(3))
    fiat_i8n_price = Column(Float)
    wallet_id = Column(Integer, ForeignKey('wallet.wallet_id'), nullable=False)

    name = Column(String(255))
    description = Column(String(1024))
    sku_id = Column(String(32))

    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    def __init__(self,
            fiat_i8n_currency=None,
            fiat_i8n_price=None,
            name=None,
            description=None,
            sku_id=None,
            wallet_id=None):
                    
            self.fiat_i8n_currency = fiat_i8n_currency
            self.fiat_i8n_price = fiat_i8n_price
            self.name = name
            self.description = description
            self.sku_id = sku_id
            self.wallet_id = wallet_id
            self.created_at = dt.now()
            self.updated_at = dt.now()

    def __repr__(self):
        return f"<PaymentItem(payment_item_id={self.payment_item_id})>"

    def from_dict(self, data):
        for field in ['payment_item_id', 'fiat_i8n_currency', 'fiat_i8n_price', 'name', 'description', 'sku_id', 'created_at', 'updated_at']:
            if field in data:
                if data[field] != None:
                    setattr(self, field, data[field])

    def to_dict(self):
        return self.serialize()

    def serialize(self):
        return {
            "payment_item_id": self.payment_item_id,
            "fiat_i8n_currency": self.fiat_i8n_currency,
            "fiat_i8n_price": self.fiat_i8n_price,
            "name": self.name,
            "description": self.description,
            "sku_id": self.sku_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class FileUpload(Base):
    __tablename__ = 'file_uploads'
    file_upload_id = Column('id', Integer, primary_key=True)
    type = Column('type', String(32))  # this will be our discriminator

    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    original_name = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False, default=dt.utcnow)
    updated_at = Column(DateTime, nullable=False, default=dt.utcnow, onupdate=dt.utcnow)
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'FileUpload'
    }

class PaymentItemImage(FileUpload):
    payment_item_id = Column(Integer, ForeignKey('payment_item.payment_item_id'), nullable=True)
    payment_item = relationship('PaymentItem', backref='images', cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'PaymentItemImage'
    }
