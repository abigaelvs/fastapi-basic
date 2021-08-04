from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connecting to sqlite database
SQLALCHEMY_DATABASE_URL = "sqlite:///blog.db"

# create engine for sqlalchemy
# the connect args argument only needed for sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# database session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for creating database models
Base = declarative_base()