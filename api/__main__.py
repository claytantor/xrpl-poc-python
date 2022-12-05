import uvicorn
import os
from dotenv import dotenv_values
import logging

config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    # logger = logging.getLogger(__name__)
    # logger.info("APP START")
    # log_config = uvicorn.config.LOGGING_CONFIG
    # log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    # uvicorn.run(app, log_config=log_config)    

    # logger.info("BASIC message")
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
    uvicorn.run("api:app", port=5000, reload=True) 