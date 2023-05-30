import os
import uuid
from sqlalchemy import create_engine, desc, and_, or_, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from api.models import Address, Base, CustomerAccount, InventoryItem, PaymentItem, PostalAddress, Wallet, XummPayload

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
        db_item.shop_id = str(uuid.uuid4()).replace('-', '')[:8]
        db_item.shop_description = d_v['classic_address']
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def fetch_by_id(db: Session, _id):
        return db.query(Wallet).filter(Wallet.id == _id).first()

    def fetch_by_classic_address(db: Session, classic_address: str):
        return db.query(Wallet).filter(Wallet.classic_address == classic_address).first()
    
    def fetch_by_shopid(db: Session, shop_id: str):
        return db.query(Wallet).filter(Wallet.shop_id == shop_id).first()
    
    

    
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


class CustomerAccountDao:

    @staticmethod
    def create(db: Session, customer_account: CustomerAccount):
        db.add(customer_account)
        db.commit()
        db.refresh(customer_account)
        return customer_account


    @staticmethod
    def fetch_by_id(db:Session, customer_account_id:int):
        return db.query(CustomerAccount).filter(CustomerAccount.id == customer_account_id).first()

    @staticmethod
    def fetch_by_account_wallet_id(db:Session, account_wallet_id:int):
        return db.query(CustomerAccount).filter(CustomerAccount.account_wallet_id == account_wallet_id).first()
    
    @staticmethod
    def fetch_by_wallet_id(db:Session, wallet_id:int):
        return db.query(CustomerAccount).filter(CustomerAccount.wallet_id == wallet_id).all()
    
    @staticmethod
    def fetch_by_classic_address(db:Session, classic_address:str):
        wallet = WalletDao.fetch_by_classic_address(db, classic_address)      
        if wallet:
            account = CustomerAccountDao.fetch_by_wallet_id(db, wallet.id)
            return account
        else:
            return None
    
    @staticmethod
    def fetch_by_customer_classic_address(db:Session, classic_address:str):
        wallet = WalletDao.fetch_by_classic_address(db, classic_address)    
        if wallet:
            account = CustomerAccountDao.fetch_by_account_wallet_id(db=db, account_wallet_id=wallet.id)
            return account
        else:
            return None

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
    def fetch_xurl_by_wallet_and_verbs(db:Session, wallet_id:int, verbs:list[str]):
        verbs = [verb.upper() for verb in verbs]
        logger.info(f"verbs:{verbs}")
        return db.query(PaymentItem).filter(and_(PaymentItem.wallet_id == wallet_id,
            PaymentItem.verb.in_(verbs),
            PaymentItem.is_xurl_item == 1)).all()

    @staticmethod
    def fetch_xurl_by_id_and_wallet_and_verbs(db:Session, id:int, wallet_id:int, verbs:list[str]):
        return db.query(PaymentItem).filter(and_(PaymentItem.wallet_id == wallet_id,
            PaymentItem.id == id, 
            PaymentItem.verb.in_(verbs),
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
        
class AddressDao:
    @staticmethod
    def fetch_by_id(db:Session, address_id:int):
        return db.query(Address).filter(Address.id == address_id).first()
    
    @staticmethod
    def fetch_by_wallet_id(db:Session, wallet_id:int):
        return db.query(Address).filter(Address.wallet_id == wallet_id).all()
    
    @staticmethod
    def create(db: Session, address: Address):
        db.add(address)
        db.commit()
        db.refresh(address)
        return address
    
    @staticmethod
    def update(db: Session, address: Address):
        db.merge(address)
        db.commit()
        return address
    
    @staticmethod
    def delete(db: Session, address: Address):
        db.delete(address)
        db.commit()
        return address

class PostalAddressDao:
    @staticmethod
    def fetch_by_id(db:Session, postal_address_id:int):
        return db.query(PostalAddressDao).filter(PostalAddress.id == postal_address_id).first()
    
    @staticmethod
    def fetch_by_wallet_id(db:Session, wallet_id:int):
        return db.query(PostalAddress).filter(PostalAddress.wallet_id == wallet_id).all()
    
    @staticmethod
    def create(db: Session, postal_address: PostalAddress):
        db.add(postal_address)
        db.commit()
        db.refresh(postal_address)
        return postal_address
    
    @staticmethod
    def update(db: Session, postal_address: PostalAddress):
        db.merge(postal_address)
        db.commit()
        return postal_address
    
    @staticmethod
    def delete(db: Session, postal_address: PostalAddress):
        db.delete(postal_address)
        db.commit()
        return postal_address
       


if __name__ == "__main__":
    logger.info("Attempting database connection")
    # db = SessionLocal()
    # print(db.query(Wallet).all())