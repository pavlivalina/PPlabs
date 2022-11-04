from sqlalchemy import Column, Integer, String, Enum, orm, ForeignKey, DateTime, Date, Boolean, Float
from .db import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    admin = Column(Boolean, default=False, nullable=False)
    username = Column(String(45), nullable=False, unique=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    phone_number = Column(String(15), unique=True)


class Passenger(Base):
    __tablename__ = "passenger"
    passenger_id = Column(Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    passport_number = Column(String(10), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey(User.user_id))
    user = orm.relationship(User, backref="passenger")


class Airport(Base):  # bandera
    __tablename__ = "airport"

    airport_id = Column(Integer, primary_key=True)
    aiport_name = Column(String(45), nullable=False, unique=True)
    city = Column(String(45), nullable=False)
    country = Column(String(45), nullable=False)


class Flight(Base):  # chornovil
    __tablename__ = "flight"

    flight_id = Column(Integer, primary_key=True)
    flight_no = Column(String(45), nullable=False, unique=True)
    datetime = Column(DateTime, nullable=False)
    cost_of_flight = Column(Float, nullable=False)
    num_of_seats = Column(Integer, nullable=False)

    arriving_airport_id = Column(Integer, ForeignKey(Airport.airport_id))
    arriving_airport = orm.relationship(Airport, foreign_keys=[arriving_airport_id], backref="flight_from",
                                        lazy="joined")
    departing_airport_id = Column(Integer, ForeignKey(Airport.airport_id))
    departing_airport = orm.relationship(Airport, foreign_keys=[departing_airport_id], backref="flight_to",
                                         lazy="joined")


class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True)
    order_done_datetime = Column(DateTime, nullable=False)
    status = Column(String(45), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.flight_id))
    flight = orm.relationship(Flight, backref="order")
    passenger_id = Column(Integer, ForeignKey(Passenger.passenger_id))
    passenger = orm.relationship(Passenger, backref="order")
