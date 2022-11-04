from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DBURL = "postgresql://postgres:postgres@localhost:5432/flybooking"
engine = create_engine(DBURL)

SessionFactory = sessionmaker(bind=engine)
db_session = scoped_session(SessionFactory)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from .models import User, Passenger, Airport, Flight, Order
    Base.metadata.create_all(bind=engine)
