from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:password1234@sma-db.cgugp201zgzj.eu-west-3.rds.amazonaws.com:3306/sites_db"
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:9906/seccom-cctv"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Session object are used to create a connection to the database and execute queries
session = Session(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
