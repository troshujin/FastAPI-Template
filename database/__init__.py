from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config

engine = create_engine(
    f"postgresql://{Config.DBUSER}:{Config.DBPASSWORD}@{Config.SERVICE_HOST}/{Config.DB}"
)

Session = sessionmaker(engine, future=True)


def get_db():
    """DB Session dependency for FastAPI"""
    session = Session()
    try:
        yield session
    finally:
        session.close()
