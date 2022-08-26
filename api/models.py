from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from api import db

class Wallet(db.Model):
    __tablename__ = "wallet"
    wallet_id = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.String)
    private_key = Column(String)
    public_key = Column(String)
    classic_address = Column(String)

    def __init__(self,
                 seed=None,
                 private_key=None,
                 public_key=None,
                 classic_address=None):
                 
        self.seed = seed
        self.private_key = private_key
        self.public_key = public_key
        self.classic_address = classic_address  
    
    def __repr__(self):
        return f"<Wallet(wallet_id={self.wallet_id})>"

    def serialize(self):
        return {
            "wallet_id": self.wallet_id,
            "public_key": self.public_key,
            "classic_address": self.classic_address,
        }


    @staticmethod
    def get_wallet_by_classic_address(classic_address):
        wallet = db.session.query(Wallet).filter_by(classic_address=classic_address).first()
        return wallet
    
