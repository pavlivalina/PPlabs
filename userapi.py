from flask import request
from flask_restful import Resource
from alembicM.db import db_session
from alembicM.models import User, Passenger, Airport, Flight, Order
from schemas import UserSchema
from marshmallow.exceptions import ValidationError
from resp_error import errs, json_error
from sqlalchemy import exc

user_schema = UserSchema()


class UserIdAPI(Resource):
    def get(self, username):
        user = User.query.get(username)
        if not user:
            return errs.not_found
        return user_schema.dump(user), 200

    def delete(self, username):
        user = User.query.get(username)
        if not user:
            return errs.not_found
        db_session.delete(user)
        db_session.commit()
        return '', 204


class UserAPI(Resource):
    def get(self):
        users_list = User.query.all()
        return user_schema.dump(users_list, many=True), 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        user = User.query.get(json_data.get("user_id", None))
        if user:
            return errs.exists
        try:
            data = user_schema.load(json_data, session=db_session)
        except ValidationError as err:
            return json_error(err.messages, 400)

        if User.query.filter_by(username=data.username).first():
            return json_error('Not unique username', 400)
        if User.query.filter_by(phone_number=data.phone_number).first():
            return json_error('Not unique phone number', 400)
        if User.query.filter_by(email=data.email).first():
            return json_error('Not unique email', 400)

        db_session.add(data)
        db_session.commit()

        return json_data, 201

    def put(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        user = User.query.get(json_data.get("user_id", None))
        if not user:
            return errs.not_found
        try:
            data = user_schema.load(json_data, session=db_session)
        except ValidationError as err:
            return json_error(err.messages, 400)
        username = User.query.filter_by(username=data.username).first()
        num = User.query.filter_by(phone_number=data.phone_number).first()
        email = User.query.filter_by(email=data.email).first()
        if username and username.user_id != data.user_id:
            return json_error('Not unique username', 400)
        if num and num.user_id != data.user_id:
            return json_error('Not unique phone number', 400)
        if email and email.user_id != data.user_id:
            return json_error('Not unique email', 400)

        db_session.add(data)
        db_session.commit()
        return json_data, 200
