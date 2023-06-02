from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Float, and_, desc, event, or_, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import os
from datetime import datetime as dt
import json

import logging
from api.schema import XurlVerbType

from api.serializers import ImageSerializer

logging.basicConfig(level=logging.DEBUG)
ulogger = logging.getLogger("uvicorn.error")
ulogger.info("APP CONFIG PATH: " + os.getenv("APP_CONFIG"))

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
    id = Column(Integer, primary_key=True)
    classic_address = Column(String())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    shop_id = Column(String(10))
    shop_name = Column(String(100))
    shop_description = Column(String(1000))

    # public_key = Column(String(1000))
    # private_key = Column(String(1000))
    
    ## adding fiat currency
    fiat_i8n_currency = Column(String(3))

    def __init__(self,
                 seed=None,
                 private_key=None,
                 public_key=None,
                 classic_address=None,
                 shop_id=None,
                 shop_name=None,
                 shop_description=None):
                 
        self.seed = seed
        # self.private_key = private_key
        # self.public_key = public_key
        self.classic_address = classic_address 
        self.fiat_i8n_currency = "USD" 
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.shop_description = shop_description
        self.created_at = dt.now()
        self.updated_at = dt.now()
    
    def __repr__(self):
        return f"<Wallet(id={self.id})>"

    def to_dict(self):
        return {
            "id": self.id,
            "classic_address": self.classic_address,
            "shop_id": self.shop_id,
            "shop_name": self.shop_name,
            "shop_description": self.shop_description,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
    
    def serialize(self):
        return self.to_dict()

class PaymentItemTx(Base):
    __tablename__ = "payment_item_tx"

    id = Column(Integer, primary_key=True)
    # payment_item_id = Column(Integer, ForeignKey('payment_item.id'))
    # payment_item = relationship('PaymentItem')
    
    # payload_id = Column(Integer, ForeignKey('xumm_payload.id'))
    # payload = relationship('XummPayload')

    tx_hash = Column(String(64))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())


class OrderInvoiceTx(Base):
    __tablename__ = "order_invoice_tx"

    id = Column(Integer, primary_key=True)
    # order_invoice_id = Column(Integer, ForeignKey('order_invoice.id'))
    # order_invoice = relationship('OrderInvoice', foreign_keys=[order_invoice_id])
    
    # payload_id = Column(Integer, ForeignKey('xumm_payload.id'))
    # payload = relationship('XummPayload', foreign_keys=[payload_id])

    tx_hash = Column(String(64))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    
class XummPayload(Base):
    __tablename__ = "xumm_payload"

    id = Column(Integer, primary_key=True)
    body = Column(String(16000))
    webhook_body = Column(String(16000))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    payload_uuidv4 = Column(String(36))
    wallet_id = Column(Integer, ForeignKey('wallet.id'))

    is_signed = Column(Integer)
    txid = Column(String(64))

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
        return f"<XummPayload(id={self.id})>"

    # def from_dict(self, data):
    #     for field in ['xumm_payload_id', 'body', 'webhook_body', 'created_at', 'updated_at', 'payload_uuidv4', 'wallet_id', 'is_signed', 'txid']:
    #         if field in data:
    #             if data[field] != None:
    #                 setattr(self, field, data[field])

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
            "id": self.id,
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

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String(32), nullable=False)
    country = Column(String(3), nullable=False)
    zip_code = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    street_address_2 = Column(String)
    phone_number = Column(String, nullable=True)  # nullable because I have not implemented it
    postal_code = Column(String, nullable=False) 

    wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=True)

    

    created_at = Column(DateTime, nullable=False, default=dt.utcnow)
    updated_at = Column(DateTime, nullable=False, default=dt.utcnow, onupdate=dt.utcnow)

    def __init__(self, wallet_id, name, first_name, last_name, city, state, country, 
        street_address, street_address_2, phone_number, postal_code):
        self.created_at = dt.now()
        self.updated_at = dt.now()
        self.wallet_id = wallet_id
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.zip_code = postal_code
        self.city = city
        self.state = state
        self.country = country
        self.street_address = street_address
        self.street_address_2 = street_address_2 if street_address_2 else ""
        self.phone_number = phone_number
        self.postal_code = postal_code


    def serialize(self, include_wallet=False):
        data = {
            'id': self.id,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'street_address': self.street_address,
            'street_address_2': self.street_address_2,
            'zip_code': self.zip_code,
            'city': self.city,
            'state': self.state, 
            'country': self.country,
            'phone_number': self.phone_number,
            'postal_code': self.postal_code,
            'postal_addresses': [postal_address.serialize() for postal_address in self.postal_addresses],
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

        # if include_wallet:
        #     data['wallet'] = {'id': self.wallet_id, 'username': self.wallet.username}

        return data
    
class PostalAddress(Base):
    __tablename__ = 'postal_address'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallet.id'))

    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship('Address', backref='postal_addresses', cascade="all, delete")
    
    shop_id = Column(String)
    well_known_uri = Column(String)
    status = Column(String(32))
    nft_token_id = Column(String(64))
    nft_token_uri = Column(String(256))
    nft_token_tx_hash = Column(String(64))

    created_at = Column(DateTime, nullable=False, default=dt.utcnow)
    updated_at = Column(DateTime, nullable=False, default=dt.utcnow, onupdate=dt.utcnow)

    def __init__(self, wallet_id, address_id, shop_id, well_known_uri):
        self.created_at = dt.now()
        self.updated_at = dt.now()
        self.wallet_id = wallet_id
        self.address_id = address_id
        self.shop_id = shop_id
        self.well_known_uri = well_known_uri
        self.status = "CREATED"



    def serialize(self, include_wallet=False):
        data = {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'address_id': self.address_id,
            'shop_id': self.shop_id,
            'well_known_uri': self.well_known_uri,
            'status': self.status,
            'xumm_url': f'https://xumm.app/sign/{self.well_known_uri}',
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
        
        return data


class CustomerAccount(Base):

    __tablename__ = 'customer_account'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer)
    company_name = Column(String(128))
    contact_name = Column(String(128))
    company_email = Column(String(128))
    contact_email = Column(String(128))
    phone = Column(String(64))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    notes = Column(String)
    status = Column(String(32))
    account_wallet_id = Column(Integer, ForeignKey('wallet.id'))
    account_wallet = relationship('Wallet', backref='account_wallet', foreign_keys=[account_wallet_id], cascade="all, delete")

    # # address as a foreign key to the address table
    shipping_address_id = Column(Integer, ForeignKey('address.id'))
    shipping_address = relationship('Address', backref='shipping_address', cascade="all, delete")
  
    sales_rep_name = Column(String(128))
    sales_rep_email = Column(String(128))
    sales_rep_phone = Column(String(64))
    sales_rep_notes = Column(String)

    def serialize(self):
        return {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'company_name': self.company_name,
            'contact_name': self.contact_name,
            'company_email': self.company_email,
            'contact_email': self.contact_email,
            'phone': self.phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'notes': self.notes,
            'status': self.status,
            'account_wallet_id': self.account_wallet_id,
            'account_wallet': self.account_wallet.serialize(),
            'shipping_address_id': self.shipping_address_id,
            'shipping_address': self.shipping_address.serialize() if self.shipping_address else None,
            'sales_rep_name': self.sales_rep_name,
            'sales_rep_email': self.sales_rep_email,
            'sales_rep_phone': self.sales_rep_phone,
            'sales_rep_notes': self.sales_rep_notes
        }


# class AccountAddress(Base):

#     __tablename__ = 'account_address'

#     id = Column(Integer, primary_key=True)
#     customer_account_id = Column(Integer, ForeignKey('customer_account.id'))
#     customer_account = relationship('CustomerAccount', backref='customer_account', cascade="all, delete")
#     address_id = Column(Integer, ForeignKey('address.id'))
#     address = relationship('Address', backref='address', cascade="all, delete")

#     def serialize(self):
#         return {
#             'id': self.id,
#             'customer_account_id': self.customer_account_id,
#             'customer_account': self.customer_account.serialize(),
#             'address_id': self.address_id,
#             'address': self.address.serialize()
#         }
    


class PaymentItem(Base):
    """
    a payment item is a xurl entity that is used to create a payment payload
    the verb is baked in to the xurl by the backend
    """
    __tablename__ = "payment_item"   

    id = Column(Integer, primary_key=True)

    fiat_i8n_currency = Column(String(3))
    fiat_i8n_price = Column(Float)
    wallet_id = Column(Integer, ForeignKey('wallet.id'))

    inventory_item_id = Column(Integer, ForeignKey('inventory_item.id'))
    inventory_item = relationship('InventoryItem', backref='inventory_item', cascade="all, delete")
    
    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    in_shop = Column(Integer)
    verb = Column(String(32))
    is_xurl_item = Column(Integer)

    # def __init__(self):
    #     self.created_at = dt.now()
    #     self.updated_at = dt.now()

    def __init__(self,
        fiat_i8n_currency=None,
        fiat_i8n_price=None,
        name=None,
        description=None,
        sku_id=None,
        wallet_id=None):
                
        self.fiat_i8n_currency = fiat_i8n_currency
        self.fiat_i8n_price = fiat_i8n_price
        # self.name = name
        # self.description = description
        # self.sku_id = sku_id
        self.wallet_id = wallet_id
        self.in_shop = 0
        self.verb = XurlVerbType.NOOP.lower()
        self.is_xurl_item = 0
        self.created_at = dt.now()
        self.updated_at = dt.now()

    def __repr__(self):
        return f"<PaymentItem(id={self.id})>"

    def to_dict(self):
        return self.serialize()
    
    def from_dict(self, data):
        for field in ['fiat_i8n_currency', 'fiat_i8n_price', 'in_shop', 'verb', 'is_xurl_item']:
            if field in data:
                setattr(self, field, data[field])

    def serialize(self):
        return {
            "id": self.id,
            "fiat_i8n_currency": self.fiat_i8n_currency,
            "fiat_i8n_price": self.fiat_i8n_price,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "inventory_item": self.inventory_item.serialize(),
        }

class InventoryItem(Base):
    __tablename__ = 'inventory_item'
    id = Column(Integer, primary_key=True, nullable=False)
    wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=False)

    name = Column(String(255))
    description = Column(String(1024))
    sku_id = Column(String(32))
      
    is_stocked_item = Column(Integer)
    in_stock_count = Column(Integer)
    on_backorder_count = Column(Integer)

    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    def __init__(self):
        self.created_at = dt.now()
        self.updated_at = dt.now()
    
    def to_dict(self):
        return self.serialize()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "sku_id": self.sku_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "images":[ImageSerializer(image=image).get_data() for image in self.images],
            "in_stock_count": self.in_stock_count,
            "on_backorder_count": self.on_backorder_count
        }

ORDER_STATUS = ['processed', 'saved', 'shipped']

# this is the order of the store, orders can have multiple items
class OrderInvoice(Base):
    __tablename__ = 'order_invoice'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime()) 
    updated_at = Column(DateTime()) 

    # which merchant is the seller
    wallet_id = Column(Integer, ForeignKey("wallet.id"))

    payment_status = Column(String(32))
    order_status = Column(Integer)
    tracking_number = Column(String)
    shipping_cost = Column(Float)
    is_shipped_item = Column(Integer)

    terms_period = Column(String)
    terms_qty = Column(Integer)
          
    customer_account_id = Column(Integer, ForeignKey('customer_account.id'), nullable=True)
    customer_account = relationship('CustomerAccount', backref='customer_account', cascade="none")

    items = relationship("OrderItem",
                    primaryjoin="and_(OrderInvoice.id==OrderItem.order_id)", viewonly=True)

    def __init__(self, wallet_id, payment_status, customer_id):
        self.created_at = dt.now()
        self.updated_at = dt.now()
        self.wallet_id = wallet_id
        self.payment_status = payment_status
        self.is_shipped_item = 0
        self.order_status = 0,
        self.customer_id = customer_id
        self.terms_period = 'DAYS'
        self.terms_qty = 30
    
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        items = []
        for item in self.items:
            iv = item.serialize()
            # del iv['description_n']
            items.append(iv)

        dto = {
            'id': self.id,
            'order_status': ORDER_STATUS[self.order_status],
            'tracking_number': self.tracking_number,
            'payment_status': self.payment_status,
            'customer_id': self.customer_account_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'items': items,
            'terms_qty': self.terms_qty,
            'terms_period': self.terms_period
        }

        if hasattr(self,'customer_account'):
            dto['customer_account'] = self.customer_account.serialize()

        if hasattr(self,'total_cost_fiat'):
            dto['total_cost_fiat'] = self.total_cost_fiat

        if hasattr(self, 'lines_summary'):
            dto['lines_summary'] = self.lines_summary

        return dto


class OrderItem(Base):
    __tablename__ = 'order_item'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime)
 
    order_id = Column(Integer, ForeignKey('order_invoice.id'), nullable=True)
    order = relationship('OrderInvoice', backref='order_item', cascade="all, delete")

    fiat_i8n_currency = Column(String(3))
    fiat_i8n_price = Column(Float)
    wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=False)

    inventory_item_id = Column(Integer, ForeignKey('inventory_item.id'), nullable=False)

    created_at = Column(DateTime, nullable=False, default=dt.utcnow)
    updated_at = Column(DateTime, onupdate=dt.utcnow)

    def __init__(self, quantity, order_id, inventory_item_id):
        self.quantity = quantity
        self.order_id = order_id
        self.inventory_item_id = inventory_item_id
        self.created_at = dt.now()
        self.updated_at = dt.now()

    def serialize(self):
        model_basic = {
            'id': self.id,
            'quantity': self.quantity,
            'order_id': self.order_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        # if hasattr(self, 'payment_item') and self.payment_item != None:
        #     model_basic['payment_item'] = self.payment_item.serialize()
        
        # if hasattr(self, 'amount_sats'):
        #     model_basic['amount_sats'] = self.amount_sats
        #     model_basic['fiat_i8n_currency'] = self.fiat_i8n_currency
        #     model_basic['fiat_amount'] = self.fiat_amount
        
        return model_basic

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

class InventoryItemImage(FileUpload):
    inventory_item_id = Column(Integer, ForeignKey('inventory_item.id'), nullable=True)
    inventory_item = relationship('InventoryItem', backref='images', cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'InventoryItemImage'
    }

