import os
from dotenv import dotenv_values

from api.schema import XurlSubjectType, XurlVerbType
config = {
    # load shared development variables
    **dotenv_values(os.getenv("APP_CONFIG")),
    **os.environ,  # override loaded values with environment variables
}

class ImageSerializer():
    def __init__(self, image):
        self.data = {
            'id': image.inventory_item_id,
            'data_url': image.file_path.replace('\\', '/')}
    def get_data(self):
        return self.data

class PaymentItemDetailsSerializer():
    def __init__(self, payment_item, shop_id, verb=XurlVerbType.NOOP):

        uri_base = f'{config["XURL_BASEURL"].replace("{shop_id}", shop_id)}'

        xumm_url=f'{config["XUMM_APP_DEEPLINK"]}?uri_base={uri_base}&uri=xurl://payload/{XurlSubjectType.payment_item}/{payment_item.id}/{payment_item.verb}'

        self.data = {
            'id': payment_item.id,
            'inventory_item': payment_item.inventory_item.serialize(),
            'fiat_i8n_price': payment_item.fiat_i8n_price,
            'fiat_i8n_currency': payment_item.fiat_i8n_currency,
            'in_shop': payment_item.in_shop == 1,
            'is_xurl_item': payment_item.is_xurl_item == 1,
            'created_at': str(payment_item.created_at),
            'updated_at': str(payment_item.updated_at),
            'verb': payment_item.verb,
        }
        self.data['xumm_url'] = xumm_url


    def serialize(self):
        return self.data


class PostalAddressSerializer():
    def __init__(self, postal_addess, verb=XurlVerbType.SHARE):

        uri_base = f'{config["XURL_BASEURL"].replace("{shop_id}", postal_addess.shop_id)}'

        xumm_url=f'{config["XUMM_APP_DEEPLINK"]}?uri_base={uri_base}&uri=xurl://payload/{XurlSubjectType.postal_address}/{postal_addess.id}/{verb}'

        self.data = {
            'id': postal_addess.id,
            'wallet_id': postal_addess.wallet_id,
            'address_id': postal_addess.address_id,
            'shop_id': postal_addess.shop_id,
            'well_known_uri': postal_addess.well_known_uri,
            'status': postal_addess.status,
            'created_at': str(postal_addess.created_at),
            'updated_at': str(postal_addess.updated_at)
        }
        
        self.data['xumm_url'] = xumm_url


    def serialize(self):
        return self.data



# =============
# Path: api/routes/xurl.py
# Compare this snippet from api/routes/xurl.py:
#

class XurlInventoryItemSerializer():
    def __init__(self, inventory_item):
        xurl=f'xurl://inventory/{inventory_item.id}'
        self.data = inventory_item.serialize()
        self.data['uri'] = xurl

    def serialize(self):
        return self.data

class XurlPaymentItemSerializer():
    def __init__(self, payment_item, shop_id):

        uri_base = f'{config["XURL_BASEURL"].replace("{shop_id}", shop_id)}'

        xurl=f'xurl://subject/{XurlSubjectType.payment_item}/{payment_item.id}/{payment_item.verb}'
        payload=f'xurl://payload/subject/{XurlSubjectType.payment_item}/{payment_item.id}/{payment_item.verb}'
        xumm_url=f'{config["XUMM_APP_DEEPLINK"]}?uri_base={uri_base}&uri=xurl://payload/{XurlSubjectType.payment_item}/{payment_item.id}/{payment_item.verb}'

        self.data = {
            'id': payment_item.id,
            'inventory_item': XurlInventoryItemSerializer(inventory_item=payment_item.inventory_item).serialize(),
            'fiat_i8n_price': payment_item.fiat_i8n_price,
            'fiat_i8n_currency': payment_item.fiat_i8n_currency,
            'created_at': str(payment_item.created_at),
            'updated_at': str(payment_item.updated_at),
            'verb': payment_item.verb,
            'uri': xurl,
            'payload': payload,
            'xumm_url': xumm_url
        }

        print(self.data)

    def serialize(self):
        return self.data

class XurlPaymentItemsSerializer():
    def __init__(self, payment_item_list, shop_id, verb=XurlVerbType.NOOP):
        self.data = [XurlPaymentItemSerializer(payment_item=payment_item, shop_id=shop_id).serialize() for payment_item in payment_item_list]

    def serialize(self):
        return self.data
