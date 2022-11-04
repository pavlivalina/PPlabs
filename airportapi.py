from flask import request
from flask_restful import Resource
from alembicM.db import db_session
from alembicM.models import User, Passenger, Airport, Flight, Order
from schemas import AirportSchema
from marshmallow.exceptions import ValidationError
from resp_error import errs, json_error

airport_schema = AirportSchema()


class AirportIdAPI(Resource):
    def get(self, airport_id):
        airport = Airport.query.get(airport_id)
        if not airport:
            return errs.not_found
        return airport_schema.dump(airport), 200


class AirportAPI(Resource):
    def get(self):
        airport_list = Airport.query.all()
        return airport_schema.dump(airport_list, many=True), 200
