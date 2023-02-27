import os
from dotenv import dotenv_values
config = {
    # load shared development variables
    **dotenv_values(os.getenv("APP_CONFIG")),
    **os.environ,  # override loaded values with environment variables
}

class ImageSerializer():
    def __init__(self, image):
        self.data = {
            'id': image.payment_item_id,
            'data_url': image.file_path.replace('\\', '/')}
    def get_data(self):
        return self.data

class PaymentItemDetailsSerializer():
    def __init__(self, payment_item):

        # https://xumm.app/detect/xapp:sandbox.32849dc99872?TransactionType=Payment&LookupType=PaymentItem&LookupRef=1

        xurl=f'{config["XUMM_APP_DEEPLINK"]}?xurl=xurl://{config["XURL_DOMAIN"]}/v1/paymentitem/{payment_item.payment_item_id}/buynow'

        self.data = {
            'payment_item_id': payment_item.payment_item_id,
            'name': payment_item.name,
            'description': payment_item.description,
            'sku_id': payment_item.sku_id,
            'fiat_i8n_price': payment_item.fiat_i8n_price,
            'fiat_i8n_currency': payment_item.fiat_i8n_currency,
            'images': [ImageSerializer(image=image).get_data() for image in payment_item.images],
            'xurl': xurl
        }
    def serialize(self):
        return self.data
