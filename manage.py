import os

from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values

config = {
    **dotenv_values(os.getenv("APP_CONFIG",".env")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

engine = create_engine(
    config['DATABASE_URL'], connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


if __name__ == '__main__':
    pass