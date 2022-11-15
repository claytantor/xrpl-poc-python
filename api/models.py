from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Float, and_, desc, event, or_, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import uuid
from datetime import datetime as dt
import json

from api import db

class Wallet(db.Model):
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

    def serialize(self):
        return {
            "wallet_id": self.wallet_id,
            "public_key": self.public_key,
            "classic_address": self.classic_address,
            "fiat_i8n_currency": self.fiat_i8n_currency,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


    @staticmethod
    def get_wallet_by_classic_address(classic_address):
        wallet = db.session.query(Wallet).filter_by(classic_address=classic_address).first()
        return wallet
    
class XummPayload(db.Model):
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

    @property
    def is_signed_bool(self):
        return False if self.is_signed == 0 else True

    def set_is_signed_bool(self, is_signed_bool=False):
        self.is_signed = 1 if is_signed_bool else 0

    def serialize(self):
        is_signed = False if self.is_signed == 0 else True

        s_m = {
            "xumm_payload_id": self.xumm_payload_id,
            "is_signed": is_signed,
            "payload_uuidv4": self.payload_uuidv4,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "txid": self.txid,
        }

        if self.body:
            s_m["body"] = json.loads(self.body)

        if self.webhook_body:
            s_m["webhook_body"] = json.loads(self.webhook_body)

        return s_m

    @staticmethod
    def get_by_payload_uuidv4(payload_uuidv4):
        payload = db.session.query(XummPayload).filter_by(payload_uuidv4=payload_uuidv4).first()
        return payload 


    @staticmethod
    def get_page_by_wallet(wallet_id, page=1, page_size=10): 
        return db.session.query(XummPayload).filter_by(wallet_id=str(wallet_id)) \
        .order_by(desc(XummPayload.created_at)).paginate(page=page,per_page=page_size)


class PaymentItem(db.Model):
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

class FileUpload(db.Model):
    __tablename__ = 'file_uploads'
    file_upload_id = db.Column('id', db.Integer, primary_key=True)
    type = db.Column('type', db.String(32))  # this will be our discriminator

    file_path = db.Column(db.String, nullable=False)
    file_name = db.Column(db.String, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    original_name = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=dt.utcnow, onupdate=dt.utcnow)
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'FileUpload'
    }

class PaymentItemImage(FileUpload):
    payment_item_id = db.Column(db.Integer, db.ForeignKey('payment_item.payment_item_id'), nullable=True)
    product = relationship('PaymentItem', backref='images', cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'PaymentItemImage'
    }
