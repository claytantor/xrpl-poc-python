from http import HTTPStatus
import os

from fastapi import APIRouter
from fastapi import Depends, HTTPException, Request, Form
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from api.schema import Xurl, XurlCustomer, XurlInfoSchema, XurlSubject, XurlSubjectType, XurlType, XurlVerb, XurlVerbType, XurlVersion
from api.models import InventoryItem, PaymentItem, Wallet
from api.decorators import determine_xurl_wallet
from api.dao import CustomerAccountDao, PaymentItemDao, PostalAddressDao, get_db
from api.serializers import XurlInventoryItemSerializer, XurlPaymentItemSerializer, XurlPaymentItemsSerializer

from api.routes.base import make_create_account_payload, make_payment_item_payload

import logging
ulogger = logging.getLogger("uvicorn.error")

from dotenv import dotenv_values
config = {
    # load shared development variables
    **dotenv_values(os.getenv("APP_CONFIG")),
    **os.environ,  # override loaded values with environment variables
}

router = APIRouter()

@router.get("/xurl")
@determine_xurl_wallet
def xurl_base(request: Request, db: Session = Depends(get_db)):
    return {
        "version": "v1",
        "uris": {
            "xurl://info": "Information about this xurl server",
            "xurl://jwks": "keys for this xurl server in the jwks format",
            "xurl://verb": "A list of verbs supported by this xurl server",
            "xurl://verb/{verb}": "Information about a specific verb",
            "xurl://verb/subject/{subject}": "A list of verbs supported by a specific subject type",
            "xurl://verb/subject/{subject}/{subjectid}": "A list of verbs supported by a specific subject instance",
            "xurl://subject": "A list of subject types supported by this xurl server",
            "xurl://subject/{subject}": "A list all entities of a specific subject type",
            "xurl://subject/{subject}/{subjectid}": "Detailed information about a specific subject instance",
            "xurl://payload/{subject}/{subjectid}/{verb}": "Generate a payload for the given subject, subjectid, and verb",
        }
    }


@router.get("/xurl/info", response_model=XurlInfoSchema)
@determine_xurl_wallet
def xurl_info(request: Request,
    db: Session = Depends(get_db)):
    ulogger.info(f"==== xurl info: {request.url.scheme} {request.url.hostname} {request.url.port} {request.url.path} {request.url.query}")
    ulogger.info(f"==== headers: {request.headers} {'x-xurl-user' in request.headers}")

    xurl_customer = None

    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers: 
        ulogger.info(f"=== XURLUSER  x-xurl-user {request.headers['x-xurl-user']} shopid: {request.headers['x-xurl-shopid']}")

        # try to lookup the user wallet
        try:
            customer_account = CustomerAccountDao.fetch_by_customer_classic_address(db, request.headers['x-xurl-user'])
            ulogger.info(f"=== customer_account {customer_account.serialize()} {request.headers['x-xurl-user']}")

            verbs = []
            v_noop = XurlVerb(
                type=XurlVerbType.NOOP.lower(),
                description="No operation"
            )
            verbs.append(v_noop)

            v_carry = XurlVerb(
                type=XurlVerbType.CARRY.lower(),
                description="Carry a payload"
            )
            verbs.append(v_carry)

            # {request.url.scheme} {request.url.hostname} {request.url.port}
            well_known_domain = f"{request.headers['x-xurl-shopid']}{request.url.hostname}:{request.url.port}"

            # can we add the po

            xurl_customer = XurlCustomer(
                customer_id=customer_account.id if customer_account else None,
                classic_address=request.headers['x-xurl-user'] if customer_account else None, 
                supported_verbs=verbs,
                well_known_domain=well_known_domain,      
            )

        except Exception as e:
            ulogger.error(f"=== x-xurl-user error {e}")
        finally:
            ulogger.info(f"=== XURLUSER  x-xurl-user {request.headers['x-xurl-user']} shopid: {request.headers['x-xurl-shopid']} finally") 
    else:
        ulogger.info(f"=== XURLUSER no x-xurl-user")
        
    ulogger.info(f"=== XURLUSER HEY {request.headers['x-xurl-shopid']}")

    # {request.url.scheme} {request.url.hostname} {request.url.port}
    well_known_domain = f"{request.headers['x-xurl-shopid']}{request.url.hostname}:{request.url.port}"

    ulogger.info(f"=== XURLUSER well_known_domain {well_known_domain}")

    return XurlInfoSchema(
        version="v1",
        commit_sha=config['API_GIT_SHA'],
        api_branch=config['API_GIT_BRANCH'],
        endpoint=config['XURL_BASEURL'].replace('{shop_id}', request.headers['x-xurl-shopid']),
        shop_id=request.headers['x-xurl-shopid'],
        xurl_user=request.headers['x-xurl-user'] if customer_account else None,
        xurl_customer=xurl_customer,
        well_known_domain=well_known_domain, 
    )

@router.get("/xurl/jwks", response_model=XurlInfoSchema)
@determine_xurl_wallet
def xurl_jwks(request: Request,
    db: Session = Depends(get_db)):
    keys = {
        "keys": [
            {
                "kty": "RSA",
                "e": "AQAB",
                "use": "sig",
                "kid": "CXup",
                "n": "hrwD-lc-IwzwidCANmy4qsiZk11yp9kHykOuP0yOnwi36VomYTQVEzZXgh2sDJpGgAutdQudgwLoV8tVSsTG9SQHgJjH9Pd_9V4Ab6PANyZNG6DSeiq1QfiFlEP6Obt0JbRB3W7X2vkxOVaNoWrYskZodxU2V0ogeVL_LkcCGAyNu2jdx3j0DjJatNVk7ystNxb9RfHhJGgpiIkO5S3QiSIVhbBKaJHcZHPF1vq9g0JMGuUCI-OTSVg6XBkTLEGw1C_R73WD_oVEBfdXbXnLukoLHBS11p3OxU7f4rfxA_f_72_UwmWGJnsqS3iahbms3FkvqoL9x_Vj3GhuJSf97Q"
                }
            ]
    }

    return JSONResponse(status_code=HTTPStatus.OK, content=keys)



def _make_xurl_payload(
    xurl: Xurl,
    request: Request,
    db: Session = Depends(get_db)):

    """
    will return a xrp native payload suitable for signing this can also be injected 
    into a xumm payload via the txjson field
    """

    ulogger.info(f"==== query params: {request.query_params}")

    if xurl.subject_type == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {xurl.subject_id} {xurl.verb_type}")
        payment_item = db.query(PaymentItem).filter_by(id=int(xurl.subject_id)).first()
        # # get the wallet for this payment item
        wallet = db.query(Wallet).filter_by(id=payment_item.wallet_id).first()
        if wallet is None:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "payment item wallet not found"})
        
        qty=1
        if 'qty' in request.query_params:
            qty = int(request.query_params['qty'])
        
        return make_payment_item_payload(xurl=xurl, 
                                         payment_item=payment_item, 
                                         wallet=wallet)
    
    elif xurl.subject_type == XurlSubjectType.customer_account and xurl.verb_type.lower() == XurlVerbType.CREATEACCOUNT.lower():

        # get the wallet for this 
        shop_wallet = db.query(Wallet).filter_by(shop_id=request.headers['x-xurl-shopid']).first()
        if shop_wallet is None:
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "shop wallet not found"})

        ulogger.info(f"==== xurl customer_account: {xurl.subject_type}")

        new_customer_account = request.headers['x-xurl-user']
        if new_customer_account is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="x-xurl-user header required to create account")

        return make_create_account_payload(xurl=xurl, wallet=shop_wallet)

        
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
@determine_xurl_wallet
def xurl_gen_payload(
    subject:XurlSubjectType,
    subjectid:str,
    verb:XurlVerbType,
    request: Request,
    db: Session = Depends(get_db)):

    xurl_base_url = f"{config['XURL_BASEURL'].replace('{shop_id}', request.headers['x-xurl-shopid'])}"

    xurl = Xurl(
        xurl_type=XurlType.payload,
        base_url=xurl_base_url, 
        version=XurlVersion.v1,
        subject_type=subject,
        subject_id=subjectid,
        verb_type=verb,
        query_params=[])


    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers:
        ulogger.debug(f"=== x-xurl-user {request.headers['x-xurl-user']}")

        # try to lookup the user wallet
        customer_account = CustomerAccountDao.fetch_by_classic_address(db, request.headers['x-xurl-user'])


    if verb.lower() == XurlVerbType.NOOP.lower() and customer_account is None:
        """
        will return a xrp native payload suitable for signing this can also be injected 
        into a xumm payload via the txjson field
        """

        xurl_p = _make_xurl_payload(xurl=xurl, request=request, db=db)
        ulogger.info(f"==== xurl_p: {xurl_p}")

        return JSONResponse(status_code=HTTPStatus.OK, content=xurl_p)
    elif verb.lower() == XurlVerbType.CARRY.lower() and customer_account is not None:
        """
        will return a xrp native payload suitable for signing this can also be injected 
        into a xumm payload via the txjson field
        """
        xurl_p = _make_xurl_payload(xurl=xurl, request=request, db=db)
        ulogger.info(f"==== xurl_p: {xurl_p}")

        return JSONResponse(status_code=HTTPStatus.OK, content=xurl_p)
    
    elif verb.lower() == XurlVerbType.CREATEACCOUNT.lower() and customer_account is None:
        """
        will return a xrp native payload suitable for signing this can also be injected 
        into a xumm payload via the txjson field
        """
        xurl_p = _make_xurl_payload(xurl=xurl, request=request, db=db)
        ulogger.info(f"==== xurl_p: {xurl_p}")

        return JSONResponse(status_code=HTTPStatus.OK, content=xurl_p)
    else:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="cannot create payload due to verb rules, customer account not found or invalid")

@router.get("/xurl/subject", response_model=list[XurlSubject])
@determine_xurl_wallet
def xurl_get_subjects(
    request: Request,
    db: Session = Depends(get_db)):

    ulogger.info(f"==== xurl_get_subjects: {request.url.scheme} {request.url.hostname} {request.url.port} {request.url.path} {request.url.query}")

    """
    get a list of all subjects supported by this xurl api and the endpoints
    """
    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers:
        ulogger.info(f"=== x-xurl-user {request.headers['x-xurl-user']}")

        # try to lookup the user wallet
        customer_account = CustomerAccountDao.fetch_by_classic_address(db, request.headers['x-xurl-user'])

    supported_subjects = []
    supported_subjects.append(XurlSubject(type=XurlSubjectType.payment_item, uri=f"xurl://subject/{XurlSubjectType.payment_item}"))
    if customer_account is not None:
        supported_subjects.append(XurlSubject(type=XurlSubjectType.order_invoice, uri=f"xurl://subject/{XurlSubjectType.order_invoice}"))

        supported_subjects.append(XurlSubject(type=XurlSubjectType.postal_address, uri=f"xurl://subject/{XurlSubjectType.postal_address}"))

    else:
        supported_subjects.append(XurlSubject(type=XurlSubjectType.customer_account, uri=f"xurl://subject/{XurlSubjectType.customer_account}"))




    return supported_subjects

# @router.get("/xurl/verb/{subject}", response_model=list[XurlVerbType])
@router.get("/xurl/verb/{subject}", response_model=list[XurlVerb])
@determine_xurl_wallet
def xurl_get_verbs(
    subject:XurlSubjectType,
    request: Request,
    db: Session = Depends(get_db)):

    """
    get a list of all verbs supported by this xurl api and the endpoints
    """

    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers:
        ulogger.debug(f"=== x-xurl-user {request.headers['x-xurl-user']}")

        # try to lookup the user wallet
        customer_account = CustomerAccountDao.fetch_by_classic_address(db, request.headers['x-xurl-user'])

    supported_verbs = []
    supported_verbs.append(XurlVerb(type=XurlVerbType.NOOP.lower(), uri=f"/verb/{XurlVerbType.NOOP.lower()}"))
    
    if customer_account is not None and subject == XurlSubjectType.payment_item:
        supported_verbs.append(
            XurlVerb(type=XurlVerbType.CARRY.lower(), 
                     description="carry on sign",
                     uri=f"/verb/{XurlVerbType.CARRY.lower()}"))

    if customer_account is None and subject == XurlSubjectType.customer_account:
        supported_verbs.append(
            XurlVerb(type=XurlVerbType.CREATEACCOUNT.lower(), 
                    description="create a customer account",
                    uri=f"/verb/{XurlVerbType.CREATEACCOUNT.lower()}"))

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

    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers:
        ulogger.debug(f"=== x-xurl-user {request.headers['x-xurl-user']}")

        # try to lookup the user wallet
        customer_account = CustomerAccountDao.fetch_by_classic_address(db, request.headers['x-xurl-user'])   

    if subject == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {subject}")

        customer_verbs = [XurlVerbType.NOOP.lower(), XurlVerbType.CARRY.lower()]
        no_customer_verbs = [XurlVerbType.CARRY.lower()]

        if customer_account is not None:
            ulogger.info(f"==== xurl payment_item: {subject} customer_verbs {customer_verbs}")
            payment_items = PaymentItemDao.fetch_xurl_by_wallet_and_verbs(db, wallet_id=shop_wallet.id, verbs=customer_verbs)
        else:
            ulogger.info(f"==== xurl payment_item: {subject} no_customer_verbs {no_customer_verbs}")
            payment_items = PaymentItemDao.fetch_xurl_by_wallet_and_verbs(db, wallet_id=shop_wallet.id, verbs=no_customer_verbs)


        # payment_items = PaymentItemDao.fetch_xurls_by_wallet_id(db, wallet_id=shop_wallet.id)
        ulogger.info(f"==== serialized payment_items {payment_items}")
        return XurlPaymentItemsSerializer(payment_items, shop_wallet.shop_id).serialize()
    
    elif subject == XurlSubjectType.customer_account:
        if customer_account is not None:
            c_dict = [customer_account.serialize()]
            return c_dict
        else:
            return []
    elif subject == XurlSubjectType.postal_address:
    
        all_postal_addresses = []
        # get all the postal addresses for this customer
        for account in customer_account:
            postal_addresses = PostalAddressDao.fetch_by_wallet_id(db, wallet_id=account.account_wallet_id)
            ls_s = [p_a.serialize for p_a in postal_addresses]
            all_postal_addresses.extend(ls_s)
        
        # return the postal addresses
        return all_postal_addresses


    else:
        raise HTTPException(status_code=HTTPStatus.NOT_IMPLEMENTED, detail="subject not supported")


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

    ulogger.info(f"==== xurl subject: {subject} subjectid: {subjectid}")

    # get the wallet for this 
    shop_wallet = db.query(Wallet).filter_by(shop_id=request.headers['x-xurl-shopid']).first()
    if shop_wallet is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "shop wallet not found"})

    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers:
        ulogger.debug(f"=== x-xurl-user {request.headers['x-xurl-user']}")
        customer_account = CustomerAccountDao.fetch_by_classic_address(db, request.headers['x-xurl-user'])   



    if subject == XurlSubjectType.payment_item:
        ulogger.info(f"==== xurl payment_item: {subjectid}")
        # payment_item = db.query(PaymentItem).filter_by(id=int(subjectid)).first()

        # needs to be an item for this shop and is a xurl item
        # payment_item = PaymentItemDao.fetch_xurl_by_id_and_wallet_id_verbs(db, id=subjectid, wallet_id=shop_wallet.id)
        customer_verbs = [XurlVerbType.NOOP.lower(), XurlVerbType.CARRY.lower()]
        no_customer_verbs = [XurlVerbType.NOOP.lower()]

        if customer_account is not None:
            payment_item = PaymentItemDao.fetch_xurl_by_id_and_wallet_and_verbs(db, id=int(subjectid), wallet_id=shop_wallet.id, verbs=customer_verbs)
        else:
            payment_item = PaymentItemDao.fetch_xurl_by_id_and_wallet_and_verbs(db, id=int(subjectid), wallet_id=shop_wallet.id, verbs=no_customer_verbs)
        
        if payment_item is None:
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "payment item not found"})
        
        return XurlPaymentItemSerializer(payment_item, shop_id=shop_wallet.shop_id).serialize()
    elif subject == XurlSubjectType.customer_account:
        ulogger.info(f"==== xurl customer_account: {subjectid}")
        if customer_account is not None and customer_account.id == subjectid:
            return customer_account.serialize()
        else:
            # raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="account not found")
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "account not found"})
    else:
        # raise HTTPException(status_code=HTTPStatus.NOT_IMPLEMENTED, detail="subject not supported")
        return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "subject not supported"})

@router.get("/xurl/verb/{subject}/{subjectid}")
@determine_xurl_wallet
def xurl_get_subject_entities(
    subject:XurlSubjectType,
    subjectid:str,
    request: Request,
    db: Session = Depends(get_db)):

    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers:
        ulogger.debug(f"=== x-xurl-user {request.headers['x-xurl-user']}")
        customer_account = CustomerAccountDao.fetch_by_classic_address(db, request.headers['x-xurl-user'])       

    """
    will return a list of verbs supported by the given subject
    """
    if subject == XurlSubjectType.payment_item:
        supported_verbs = []
        supported_verbs.append(XurlVerb(type=XurlVerbType.NOOP.lower(), uri=f"xurl://verb/{XurlVerbType.NOOP.lower()}"))

        if customer_account is not None:
            supported_verbs.append(XurlVerb(type=XurlVerbType.CARRY.lower(), uri=f"xurl://verb/{XurlVerbType.CARRY.lower()}"))

        return supported_verbs
    elif subject == XurlSubjectType.customer_account:
        supported_verbs = []
        supported_verbs.append(XurlVerb(type=XurlVerbType.NOOP.lower(), uri=f"xurl://verb/{XurlVerbType.NOOP.lower()}"))
        if customer_account is None:
            supported_verbs.append(XurlVerb(type=XurlVerbType.CREATEACCOUNT.lower(), uri=f"xurl://verb/{XurlVerbType.CREATEACCOUNT.lower()}"))
            
        return supported_verbs

    else:
        return JSONResponse(status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": "invalid subject"})
    
    

@router.get("/xurl/verb/{verb}")
@determine_xurl_wallet
def xurl_get_subject_entities(
    verb:XurlVerbType,
    request: Request,
    db: Session = Depends(get_db)):

    # get the user from request header
    customer_account = None
    if 'x-xurl-user' in request.headers:
        ulogger.debug(f"=== x-xurl-user {request.headers['x-xurl-user']}")
        customer_account = CustomerAccountDao.fetch_by_classic_address(db, request.headers['x-xurl-user'])       

    """
    will return a list of verbs supported by the given subject
    """
    if verb.lower() == XurlVerbType.CARRY.lower() and customer_account is not None:
        return XurlVerb(
            type=XurlVerbType.CARRY.lower(), 
            description="buyer to carry merchandise on signing",
            uri=f"xurl://verb/{XurlVerbType.CARRY.lower()}")
    elif verb.lower() == XurlVerbType.NOOP.lower():
        return XurlVerb(
            type=XurlVerbType.NOOP.lower(), 
            description="no operation required by seller",
            uri=f"xurl://verb/{XurlVerbType.NOOP.lower()}")
    elif verb.lower() == XurlVerbType.CREATEACCOUNT.lower():
        return XurlVerb(
            type=XurlVerbType.CREATEACCOUNT.lower(), 
            description="create a new customer account for this shop",
            uri=f"xurl://verb/{XurlVerbType.CREATEACCOUNT.lower()}")
    else:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": "invalid subject"})


@router.get("/xurl/inventory/{id}")
@determine_xurl_wallet
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
