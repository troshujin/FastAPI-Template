from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config

# The Engine is a factory that can create new database connections for us,
# which also holds onto connections inside of a Connection Pool for fast reuse
engine = create_engine(
    f"postgresql://{Config.DBUSER}:{Config.DBPASSWORD}@{Config.SERVICE_HOST}/{Config.DB}"
)

# The purpose of sessionmaker is to provide a factory for Session objects with a fixed configuration
Session = sessionmaker(engine, future=True)


def get_db():
    """DB Session dependency for FastAPI"""
    session = Session()
    try:
        yield session
    finally:
        session.close()
