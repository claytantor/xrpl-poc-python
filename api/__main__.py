import uvicorn
import os
from dotenv import dotenv_values

config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}


if __name__ == "__main__":
    uvicorn.run("api:app", port=5000, reload=True) 