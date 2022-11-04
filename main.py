from flask import Flask
from flask_restful import Api
from alembicM.db import db_session, init_db
from flightapi import FlightAPI, FlightByNameAPI, FlightIdAPI, FlightByCityAPI, FlightByDateAPI
from userapi import UserAPI, UserIdAPI
from bookingapi import OrderAPI, OrderIdAPI, OrderByDateAPI
from airportapi import AirportIdAPI, AirportAPI

app = Flask(__name__)
api = Api(app, prefix='/api/v1')
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


api.add_resource(FlightAPI, '/flight')
api.add_resource(FlightByNameAPI, '/flight/findByName')
api.add_resource(FlightIdAPI, '/flight/<int:flight_id>')
api.add_resource(FlightByCityAPI, '/flight/findByDepartingCity')
api.add_resource(FlightByDateAPI, '/flight/findByDate')

api.add_resource(UserAPI, '/user')
api.add_resource(UserIdAPI, '/user/<username>')

api.add_resource(OrderAPI, '/booking/order')
api.add_resource(OrderIdAPI, '/booking/order/<int:order_id>')
api.add_resource(OrderByDateAPI, '/booking/order/findByDate')

api.add_resource(AirportAPI, '/airport')
api.add_resource(AirportIdAPI, '/airport/<int:airport_id>')
