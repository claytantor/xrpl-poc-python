
import io
from pydoc import describe
from typing import Union
import uuid
from http import HTTPStatus
import os
import requests
import json
import shortuuid 
import json
import base64
from datetime import datetime as dt, timedelta
import xumm
import asyncio
from PIL import Image

from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import JSONResponse, Response, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from api.schema import MessageSchema, ApiInfoSchema, OAuth2AuthSchema, OAuth2TokenSchema, PaymentItemSchema, PaymentRequestSchema, XurlSubject, XurlSubjectType, XurlVerb, XurlVerbType, WalletCreateSchema, WalletSchema, XrpCurrencyRateSchema, XummPayloadSchema, XurlVersion
from api.models import InventoryItem, InventoryItemImage, Message, ApiInfo, PaymentItem, Wallet, XrpCurrencyRate, XummPayload
from api.decorators import determine_xurl_wallet, verify_user_jwt_scopes
from api.jwtauth import make_signed_token, get_token_body
from api.dao import InventoryItemDao, PaymentItemDao, XummPayloadDao, get_db, WalletDao
from api.serializers import XurlInventoryItemSerializer, XurlPaymentItemSerializer, XurlPaymentItemsSerializer
from api.utils import parse_xurl
from api.xrpcli import get_account_info, get_rpc_network_from_wss, get_rpc_network_type, get_xrp_network_from_jwt, xrp_to_drops, get_xapp_tokeninfo, get_wss_network_type, get_rpc_network_from_jwt

from api.routes.base import make_payment_item_payload

import logging
ulogger = logging.getLogger("uvicorn.error")

from dotenv import dotenv_values
config = {
    # load shared development variables
    **dotenv_values(os.getenv("APP_CONFIG")),
    **os.environ,  # override loaded values with environment variables
}

router = APIRouter()

@router.get("/xurl/info", response_model=ApiInfoSchema)
@determine_xurl_wallet
def xurl_info(request: Request):
    ulogger.info(f"==== xurl info: {request.url.scheme} {request.url.hostname} {request.url.port} {request.url.path} {request.url.query}")
    ulogger.info(f"==== headers: {request.headers}")

    #endpoint_url = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}{request.url.path.replace('//','/').replace('/info', '')}"

    return ApiInfoSchema(
        version="v1",
        commit_sha=config['API_GIT_SHA'],
        api_branch=config['API_GIT_BRANCH'],
        endpoint=config['XURL_BASEURL'],
        shop_id=request.headers['x-xurl-shopid'],
    )


def _make_xurl_payload(version:XurlVersion,
    subject:XurlSubjectType,
    subjectid:int,
    verb:XurlVerbType,
    request: Request,
    db: Session = Depends(get_db)):

    """
    will return a xrp native payload suitable for signing this can also be injected 
    into a xumm payload via the txjson field
    """

    ulogger.info(f"==== query params: {request.query_params}")

    if subject == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {subjectid}")
        payment_item = db.query(PaymentItem).filter_by(id=int(subjectid)).first()
        # # get the wallet for this payment item
        wallet = db.query(Wallet).filter_by(id=payment_item.wallet_id).first()
        if wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "payment item wallet not found"})
        
        qty=1
        if 'qty' in request.query_params:
            qty = int(request.query_params['qty'])
        
        return make_payment_item_payload(payment_item=payment_item, wallet=wallet, verb=verb, qty=qty)
        
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="invalid xurl")


@router.post("/xurl/key")
def xurl_post_key(
    XurlClient: str,
    request: Request,
    db: Session = Depends(get_db)):

    """
    a client registers a key with the xurl endpoint. This can protected by the server and not exposed
    if the server doesnt want to allow anyone to register a key publically. The key can be used to 
    sign the xurl so the server can identify the caller and verify the xurl is valid
    """
    ulogger.info(f"==== xurl_post_key: {request}")

    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "ok"})


#            /xurl/payload/paymentitem/10/noop
@router.get("/xurl/payload/{subject}/{subjectid}/{verb}")
def xurl_gen_payload(
    subject:XurlSubjectType,
    subjectid:str,
    verb:XurlVerbType,
    request: Request,
    db: Session = Depends(get_db)):
    
    """
    will return a xrp native payload suitable for signing this can also be injected 
    into a xumm payload via the txjson field
    """
    xurl_p = _make_xurl_payload(version=XurlVersion.v1, subject=subject, subjectid=subjectid, verb=verb, request=request, db=db)
    ulogger.info(f"==== xurl_p: {xurl_p}")

    return JSONResponse(status_code=HTTPStatus.OK, content=xurl_p)

@router.get("/xurl/subject", response_model=list[XurlSubject])
def xurl_get_subjects(
    request: Request,
    db: Session = Depends(get_db)):

    """
    get a list of all subjects supported by this xurl api and the endpoints
    """

    supported_subjects = []
    supported_subjects.append(XurlSubject(type=XurlSubjectType.payment_item, uri=f"xurl://subject/{XurlSubjectType.payment_item}"))
    supported_subjects.append(XurlSubject(type=XurlSubjectType.order_invoice, uri=f"xurl://subject/{XurlSubjectType.order_invoice}"))


    return supported_subjects

@router.get("/xurl/verb", response_model=list[XurlVerbType])
def xurl_get_verbs(
    request: Request,
    db: Session = Depends(get_db)):

    """
    get a list of all verbs supported by this xurl api and the endpoints
    """
    supported_verbs = []
    supported_verbs.append(XurlVerb(type=XurlVerbType.carry_on_sign, endpoint=f"/verb/{XurlVerbType.carry_on_sign}"))
    supported_verbs.append(XurlVerb(type=XurlVerbType.no_op, endpoint=f"/verb/{XurlVerbType.no_op}"))

    return supported_verbs



@router.get("/xurl/subject/{subject}")
@determine_xurl_wallet
def xurl_get_subject_entities(
    subject:XurlSubjectType,
    request: Request,
    db: Session = Depends(get_db)):

    """
    will return a list of entities for the given subject,
    for example, if subject is payment_item, then this will 
    return a list of payment items. The verb is a parameter
    that can be used to filter the list of entities if needed
    otherwise it will return all entities for the given subject 
    with a noop (no operation) verb
    """

    # get the wallet for this 
    shop_wallet = db.query(Wallet).filter_by(shop_id=request.headers['x-xurl-shopid']).first()
    if shop_wallet is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "shop wallet not found"})

    if subject == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {subject}")
        payment_items = PaymentItemDao.fetch_xurls_by_wallet_id(db, wallet_id=shop_wallet.id)
        return XurlPaymentItemsSerializer(payment_items).serialize()


@router.get("/xurl/subject/{subject}/{subjectid}")
@determine_xurl_wallet
def xurl_get_subject_entities(
    subject:XurlSubjectType,
    subjectid:str,
    request: Request,
    db: Session = Depends(get_db)):

    """
    will return a list of entities for the given subject,
    for example, if subject is payment_item, then this will 
    return a list of payment items. The verb is a parameter
    that can be used to filter the list of entities if needed
    otherwise it will return all entities for the given subject 
    with a noop (no operation) verb
    """

    # get the wallet for this 
    shop_wallet = db.query(Wallet).filter_by(shop_id=request.headers['x-xurl-shopid']).first()
    if shop_wallet is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "shop wallet not found"})

    if subject == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {subjectid}")
        # payment_item = db.query(PaymentItem).filter_by(id=int(subjectid)).first()

        # needs to be an item for this shop and is a xurl item
        payment_item = PaymentItemDao.fetch_xurl_by_id_and_wallet_id(db, id=subjectid, wallet_id=shop_wallet.id)
        
        if payment_item is None:
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})
        
        return XurlPaymentItemSerializer(payment_item).serialize()

@router.get("/xurl/verb/{subject}/{subjectid}")
def xurl_get_subject_entities(
    subject:XurlSubjectType,
    subjectid:str,
    request: Request,
    db: Session = Depends(get_db)):

    pass
    """
    will return a list of verbs supported by the given subject
    """
    if subject == XurlSubjectType.payment_item:
        supported_verbs = []
        supported_verbs.append(XurlVerb(type=XurlVerbType.carry_on_sign, uri=f"xurl://verb/{XurlVerbType.carry_on_sign}"))
        supported_verbs.append(XurlVerb(type=XurlVerbType.no_op, uri=f"xurl://verb/{XurlVerbType.no_op}"))

        return supported_verbs
    
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "invalid subject"})

@router.get("/xurl/verb/{verb}")
def xurl_get_subject_entities(
    verb:XurlVerbType,
    request: Request,
    db: Session = Depends(get_db)):

    pass
    """
    will return a list of verbs supported by the given subject
    """
    if verb == XurlVerbType.carry_on_sign:
        return XurlVerb(
            type=XurlVerbType.carry_on_sign, 
            description="buyer to carry merchandise on signing",
            uri=f"xurl://verb/{XurlVerbType.carry_on_sign}")
    elif verb == XurlVerbType.no_op:
        return XurlVerb(
            type=XurlVerbType.no_op, 
            description="no operation required by seller",
            uri=f"xurl://verb/{XurlVerbType.no_op}")
    else:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "invalid subject"})


@router.get("/xurl/inventory/{id}")
def xurl_get_inventory(
    id: int,
    request: Request,
    db: Session = Depends(get_db)):

    """
    get inventory by id
    """
    ulogger.info(f"==== xurl_get_inventory: {id}")
    inventory = db.query(InventoryItem).filter_by(id=id).first()
    if inventory is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "inventory not found"})
    return XurlInventoryItemSerializer(inventory).serialize()
