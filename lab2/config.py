import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:19401944@localhost/postgres')
Session = sessionmaker(bind=engine)
base = declarative_base()