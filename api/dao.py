import os
from http.client import HTTPException
from fastapi import FastAPI
from sqlalchemy import create_engine, desc, and_, or_, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from api.models import Base, InventoryItem, PaymentItem, Wallet, XummPayload

import logging

from api.schema import WalletCreateSchema
logger = logging.getLogger("uvicorn.error") 

from dotenv import dotenv_values
config = {
    # load shared development variables
    **dotenv_values(os.getenv("APP_CONFIG")),
    **os.environ,  # override loaded values with environment variables
}

logger.info("Connecting to database: %s %s", config['DATABASE_URL'], os.path.dirname(__file__))

engine = create_engine(config['DATABASE_URL'],  echo=True)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class WalletDao:
    
    def create(db: Session, item: WalletCreateSchema):
        d_v = item.dict()
        logger.info("WalletDao.create: %s", d_v)
        db_item = Wallet(classic_address=d_v['classic_address'])
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def fetch_by_id(db: Session, _id):
        return db.query(Wallet).filter(Wallet.id == _id).first()

    def fetch_by_classic_address(db: Session, classic_address: str):
        return db.query(Wallet).filter(Wallet.classic_address == classic_address).first()
    
#  def fetch_by_name(db: Session,name):
#      return db.query(Item).filter(Item.name == name).first()
 
#  def fetch_all(db: Session, skip: int = 0, limit: int = 100):
#      return db.query(Item).offset(skip).limit(limit).all()
 
#  async def delete(db: Session,item_id):
#      db_item= db.query(Item).filter_by(id=item_id).first()
#      db.delete(db_item)
#      db.commit()
     
     
# #  async def update(db: Session,item_data):
#     updated_item = db.merge(item_data)
#     db.commit()
#     return updated_item

class XummPayloadDao:
        
    @staticmethod
    def fetch_by_id(db: Session, _id):
        return db.query(XummPayload).filter(XummPayload.id == _id).first()

    @staticmethod
    def fetch_by_wallet_id(db: Session, wallet_id: int):
        return db.query(XummPayload).filter(XummPayload.wallet_id == wallet_id) \
            .order_by(desc(XummPayload.created_at)).all()

    @staticmethod
    def fetch_by_payload_uuidv4(db: Session, payload_uuidv4: str):
        return db.query(XummPayload).filter_by(payload_uuidv4=payload_uuidv4).first()

    @staticmethod
    def fetch_payload_by_wallet_id(db:Session, wallet_id:int, payload_id:int):
        return db.query(XummPayload).filter(and_(XummPayload.wallet_id == wallet_id, 
            XummPayload.id == payload_id)).first()

    @staticmethod
    def fetch_by_wallet_payload_uuidv4(db:Session, wallet_id:int, payload_uuidv4:str):
        return db.query(XummPayload).filter(and_(XummPayload.wallet_id == wallet_id, 
            XummPayload.payload_uuidv4 == payload_uuidv4)).first()


    @staticmethod
    def get_page_by_wallet(db: Session, wallet_id:int, page:int=1, page_size:int=10): 
        return db.query(XummPayload).filter_by(wallet_id=str(wallet_id)) \
            .order_by(desc(XummPayload.created_at)).paginate(page=page,per_page=page_size)

    @staticmethod
    def create(db: Session, payload: XummPayload):
        db.add(payload)
        db.commit()
        db.refresh(payload)
        return payload

    @staticmethod
    def update(db: Session, payload: XummPayload):
        db.merge(payload)
        db.commit()
        return payload


class InventoryItemDao:
    
    @staticmethod
    def create(db: Session, inventory_item: InventoryItem):
        db.add(inventory_item)
        db.commit()
        db.refresh(inventory_item)
        return inventory_item


class PaymentItemDao:
    @staticmethod
    def fetch_by_id(db:Session, payment_item_id:int):
        return db.query(PaymentItem).filter(PaymentItem.id == payment_item_id).first()

    @staticmethod
    def fetch_all_by_wallet_id(db:Session, wallet_id:int):
        return db.query(PaymentItem).filter(PaymentItem.wallet_id == wallet_id).all()

    @staticmethod
    def fetch_single_by_wallet_id(db:Session, payment_item_id:int, wallet_id:int):
        return db.query(PaymentItem).filter(and_(PaymentItem.wallet_id == wallet_id, 
            PaymentItem.id == payment_item_id)).first()
    
    @staticmethod
    def fetch_xurls_by_wallet_id(db:Session, wallet_id:int):
        return db.query(PaymentItem).filter(and_(PaymentItem.wallet_id == wallet_id, 
            PaymentItem.is_xurl_item == 1)).all()
    

    @staticmethod
    def fetch_xurl_by_id_and_wallet_id(db:Session, id:int, wallet_id:int):
        return db.query(PaymentItem).filter(and_(PaymentItem.wallet_id == wallet_id,
            PaymentItem.id == id, 
            PaymentItem.is_xurl_item == 1)).first()
   

    @staticmethod
    def create(db: Session, payment_item: PaymentItem):
        db.add(payment_item)
        db.commit()
        db.refresh(payment_item)
        return payment_item

    @staticmethod
    def update(db: Session, payment_item: PaymentItem):
        db.merge(payment_item)
        db.commit()
        return payment_item

    @staticmethod
    def delete(db: Session, payment_item: PaymentItem):
        db.delete(payment_item)
        db.commit()
        return payment_item
        

if __name__ == "__main__":
    logger.info("Attempting database connection")
    # db = SessionLocal()
    # print(db.query(Wallet).all())