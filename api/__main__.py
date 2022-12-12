import uvicorn
import os
from dotenv import dotenv_values
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("APP START")
log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
logger.info("APP CONFIG PATH: " + os.getenv("APP_CONFIG"))


config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}




if __name__ == "__main__":
    uvicorn.run("api:app", port=5000, host="0.0.0.0", reload=True) 
