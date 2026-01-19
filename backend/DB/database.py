from sqlalchemy import create_engine#create_engine — Database connection banane ke liye
from sqlalchemy.orm import sessionmaker#sessionmaker — Transaction handle karne ke liye
from sqlalchemy.ext.declarative import declarative_base#declarative_base — Python class <-> DB table mapping

from core.config import settings 

engine=create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)









































































































