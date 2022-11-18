from flask import Flask, jsonify
from flask_restful import Api
from alembicM.db import db_session, init_db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from resp_error import json_error

app = Flask(__name__)
bcrypt = Bcrypt(app)
api = Api(app, prefix='/api/v1')
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)
init_db()

from functools import wraps
from alembicM.models import User

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user = User.query.filter_by(username=claims['sub'])[0]
            if not user:
                return json_error("Authentication failed. User not found", 404)

            if user.role == 'admin':
                return fn(*args, **kwargs)
            return json_error("Must be an admin", 403)

        return decorator

    return wrapper
    
def flight_administrator_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user = User.query.filter_by(username=claims['sub'])[0]
            if not user:
                return json_error("Authentication failed. User not found", 404)

            if user.role == 'admin' or user.role == 'flight_administrator':
                return fn(*args, **kwargs)
            return json_error("Must be a flight administrator", 403)
        return decorator

    return wrapper

def get_user():
    return User.query.filter_by(username=get_jwt()['sub'])[0]

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


from flightapi import FlightAPI, FlightByNameAPI, FlightIdAPI, FlightByCityAPI, FlightByDateAPI
from userapi import UserAPI, UserIdAPI, UserLoginAPI, UserPassengersAPI
from bookingapi import OrderAPI, OrderIdAPI, OrderByDateAPI
from airportapi import AirportIdAPI, AirportAPI

api.add_resource(FlightAPI, '/flight')
api.add_resource(FlightByNameAPI, '/flight/findByName')
api.add_resource(FlightIdAPI, '/flight/<int:flight_id>')
api.add_resource(FlightByCityAPI, '/flight/findByDepartingCity')
api.add_resource(FlightByDateAPI, '/flight/findByDate')

api.add_resource(UserAPI, '/user')
api.add_resource(UserIdAPI, '/user/<username>')
api.add_resource(UserLoginAPI, '/login')
api.add_resource(UserPassengersAPI, '/passengers')

api.add_resource(OrderAPI, '/booking/order')
api.add_resource(OrderIdAPI, '/booking/order/<int:order_id>')
api.add_resource(OrderByDateAPI, '/booking/order/findByDate')

api.add_resource(AirportAPI, '/airport')
api.add_resource(AirportIdAPI, '/airport/<int:airport_id>')
