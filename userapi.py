from flask import request, jsonify
from flask_restful import Resource
from alembicM.db import db_session
from alembicM.models import User, Passenger, Airport, Flight, Order
from schemas import UserSchema, PassengerSchema
from marshmallow.exceptions import ValidationError
from resp_error import errs, json_error
from sqlalchemy import exc
from main import bcrypt
from main import admin_required, flight_administrator_required, get_user
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from flask_jwt_extended import create_access_token
user_schema = UserSchema()
passenger_schema = PassengerSchema()



class UserIdAPI(Resource):
    @jwt_required()
    def get(self, username):
        claims = get_user()
        if claims.role != 'admin' and claims.role != 'flight_administrator' and claims.username != username:
            return json_error("Forbidden. Can`t get other user`s info.", 403)
        user = User.query.filter_by(username=username)[0]
        if not user:
            return errs.not_found
        data = user_schema.dump(user)
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        return data, 200

    @jwt_required()
    def delete(self, username):
        claims = get_user()
        if claims.role != 'admin' and claims.username != username:
            return json_error("Forbidden. Can`t delete other users.", 403)
        user = User.query.filter_by(username=username)[0]
        if not user:
            return errs.not_found
        db_session.delete(user)
        db_session.commit()
        return '', 204


class UserAPI(Resource):
    @flight_administrator_required()
    def get(self):
        users_list = User.query.all()
        data = user_schema.dump(users_list, many=True)
        for d in data:
            d['password'] = bcrypt.generate_password_hash(d['password']).decode('utf-8')
        return data, 200

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

        roles = ['admin', 'flight_administrator', 'passenger', None]
        if data.role not in roles:
            return json_error(f'Bad request. Invalid role. Must be one of these: {", ".join(roles[:-1])}', 400)

        if data.role != 'passenger':
            verify_jwt_in_request()
            claims = get_user()
            if claims.role != 'admin':
                return json_error("Forbidden. Only admins can assign roles", 403)

        db_session.add(data)
        db_session.commit()
        if 'password' in json_data:
            json_data['password'] = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')
        return json_data, 201

    @jwt_required()
    def put(self):
        json_data = request.get_json()
        if not json_data:
            return errs.bad_request
        user_id = json_data.get("user_id", None)
        claims = get_user()
        role = claims.role
        if claims.role != 'admin' and claims.user_id != json_data.get('user_id', None):
            return json_error("Forbidden. Can`t change other users info", 403)
        user = User.query.get(user_id)
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

        roles = ['admin', 'flight_administrator', 'passenger', None]
        if data.role not in roles:
            return json_error(f'Bad request. Invalid role. Must be one of these: {", ".join(roles[:-1])}', 400)

        if data.role != None:
            if role != 'admin' and role != data.role:
                return json_error("Forbidden. Only admins can assign roles", 403)

        db_session.add(data)
        db_session.commit()
        if 'password' in json_data:
            json_data['password'] = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')    
        return json_data, 200


class UserLoginAPI(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = User.query.filter_by(username=username)[0]
        if not user:
            return json_error("User not found", 404)
        if user.password != password:
            return json_error("Invalid password", 403)

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)


class UserPassengersAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_user()

        passengers = Passenger.query.filter_by(user_id=claims.user_id)

        return {'user':user_schema.dump(claims),'passengers':passenger_schema.dump(passengers, many=True)}, 200

