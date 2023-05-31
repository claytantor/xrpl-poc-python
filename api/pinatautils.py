import os, sys
import uuid
import json
from pinatapy import PinataPy
import requests
import traceback

# === logging
import logging

# from api.s3utils import get_image_from_s3
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

# === config
app_config = os.getenv("APP_CONFIG",f"{os.path.dirname(__file__)}/../env/local/testnet_app.env")
logger.debug(f"app_config: {app_config}")
from dotenv import dotenv_values
config = {
    **dotenv_values(app_config),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}


pinata = PinataPy(config['PINATA_API_KEY'], config['PINATA_SECRET_KEY'])




async def pinata_pin_dict(dict=None, options={}):
    if dict is None:
        return ValueError("dict is required")

    # === pinata pin json
    return pinata.pin_json_to_ipfs(json_to_pin=dict, options=options)


async def pinata_get_pin(hash=None):
    if hash is None:
        return ValueError("hash is required")

    try:

        # Make a GET request to the URL of the JSON file
        response = requests.get(f'{config["PINATA_GATEWAY"]}/{hash}')

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Load the JSON data from the response
        return response.json()


    except requests.exceptions.HTTPError as err:
        logger.error(err)

    except requests.exceptions.ConnectionError as err:
        logger.error(err)

    except requests.exceptions.Timeout as err:
        logger.error(err)

    except requests.exceptions.RequestException as err:
        logger.error(err)
