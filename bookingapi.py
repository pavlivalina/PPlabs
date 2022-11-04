from flask import request
from flask_restful import Resource
from alembicM.db import db_session
from alembicM.models import User, Passenger, Airport, Flight, Order
from schemas import OrderSchema
from marshmallow.exceptions import ValidationError
from resp_error import errs, json_error


order_schema = OrderSchema()


class OrderIdAPI(Resource):
    def get(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return errs.not_found
        return order_schema.dump(order), 200

    def delete(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return errs.not_found
        db_session.delete(order)
        db_session.commit()
        return '', 204


class OrderAPI(Resource):
    def get(self):
        orders_list = Order.query.all()
        return order_schema.dump(orders_list, many=True), 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        order = Order.query.get(json_data.get("order_id", None))
        if order:
            return errs.exists
        passenger = Passenger.query.get(json_data.get("passenger_id", None))
        flight = Flight.query.get(json_data.get("flight_id", None))
        if not passenger or not flight:
            return errs.bad_request
        try:
            data = order_schema.load(json_data, session=db_session)
        except ValidationError as err:
            return json_error(err.messages, 400)

        db_session.add(data)
        db_session.commit()
        return json_data, 201

    def put(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        order = Order.query.get(json_data.get("order_id", None))
        if not order:
            return errs.not_found
        passenger = Passenger.query.get(json_data.get("passenger_id", None))
        flight = Flight.query.get(json_data.get("flight_id", None))
        if not passenger or not flight:
            return errs.bad_request
        try:
            data = order_schema.load(json_data, session=db_session)
        except ValidationError as err:
            return json_error(err.messages, 400)

        db_session.add(data)
        db_session.commit()
        return json_data, 200


class OrderByDateAPI(Resource):
    def get(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        if 'order_done_datetime' not in json_data:
            return json_error('order_done_datetime was not provided', 400)
        orders = Order.query.filter_by(order_done_datetime=json_data['order_done_datetime'])

        return order_schema.dump(orders, many=True), 200
