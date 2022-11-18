from alembicM.models import User, Passenger, Airport, Flight, Order
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
    


class FlightSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        load_instance = True
        include_fk = True


class AirportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        load_instance = True
        include_fk = True


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True


class PassengerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Passenger
        load_instance = True
        include_fk = True
