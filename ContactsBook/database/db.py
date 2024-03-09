from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.config import settings


# DATABASE_URL = settings.POSTGRESQL_URL

DATABASE_URL = settings.SQLITE_URL
engine = create_engine(DATABASE_URL, echo=False) 
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
