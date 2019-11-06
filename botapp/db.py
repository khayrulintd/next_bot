from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#from config.py import SQLALCHEMY_DATABASE_URI
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:QWEewq123@localhost/blood_pressure"

#engine = create_engine(SQLALCHEMY_DATABASE_URI)
engine = create_engine("postgresql://postgres:QWEewq123@localhost/blood_pressure")
metadata = MetaData(bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
