from flask import request
from flask_restful import Resource
from alembicM.db import db_session
from alembicM.models import User, Passenger, Airport, Flight, Order
from schemas import FlightSchema
from marshmallow.exceptions import ValidationError
from resp_error import errs, json_error

flight_schema = FlightSchema()


class FlightIdAPI(Resource):
    def get(self, flight_id):
        flight = Flight.query.get(flight_id)
        if not flight:
            return errs.not_found
        return flight_schema.dump(flight), 200

    def delete(self, flight_id):
        flight = Flight.query.get(flight_id)
        if not flight:
            return errs.not_found
        db_session.delete(flight)
        db_session.commit()
        return '', 204


class FlightAPI(Resource):
    def get(self):
        flights_list = Flight.query.all()
        return flight_schema.dump(flights_list, many=True), 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        flight = Flight.query.get(json_data.get("flight_id", None))
        if flight:
            return errs.exists
        arr_airport = Airport.query.get(json_data.get("arriving_airport_id", None))
        dep_airport = Airport.query.get(json_data.get("departing_airport_id", None))
        if not arr_airport or not dep_airport:
            return errs.bad_request
        try:
            data = flight_schema.load(json_data, session=db_session)
        except ValidationError as err:
            return json_error(err.messages, 400)

        db_session.add(data)
        db_session.commit()
        return json_data, 201

    def put(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        flight = Flight.query.get(json_data.get("flight_id", None))
        if not flight:
            return errs.not_found
        arr_airport = Airport.query.get(json_data.get("arriving_airport_id", None))
        dep_airport = Airport.query.get(json_data.get("departing_airport_id", None))
        if not arr_airport or not dep_airport:
            return errs.bad_request
        try:
            data = flight_schema.load(json_data, session=db_session)
        except ValidationError as err:
            return json_error(err.messages, 400)

        db_session.add(data)
        db_session.commit()
        return json_data, 200


class FlightByCityAPI(Resource):
    def get(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        if 'departing_city' not in json_data:
            return json_error('departing_city was not provided', 400)
        airports = Airport.query.filter_by(city=json_data['departing_city'])
        ids = [airport.airport_id for airport in airports]

        flights = Flight.query.filter(Flight.departing_airport_id.in_(ids))

        return flight_schema.dump(flights, many=True), 200


class FlightByDateAPI(Resource):
    def get(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        if 'datetime' not in json_data:
            return json_error('datetime was not provided', 400)
        flight = Flight.query.filter_by(flight_no=json_data['datetime']).first()
        if not flight:
            return errs.not_found
        return flight_schema.dump(flight), 200


class FlightByNameAPI(Resource):
    def get(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        if 'flight_no' not in json_data:
            return json_error('flight_no was not provided', 400)
        flight = Flight.query.filter_by(flight_no=json_data['flight_no']).first()
        if not flight:
            return errs.not_found
        return flight_schema.dump(flight), 200
