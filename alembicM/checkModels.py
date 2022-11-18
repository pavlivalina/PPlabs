from models import User, Passenger, Airport, Flight, Order
from db import db_session

session = db_session()

user = User(user_id=1, admin=False, username="Davemag", firstname="Oleh", lastname="Lozovyi",
            email="abcd@im.a", phone_number="123456789", password="my_password")
user1 = User(user_id=2, admin=False, username="NazarcO", firstname="Nazar", lastname="Lomachinkiy",
             email="abc@im.a", phone_number="123476789", password="some_password")

passenger = Passenger(passenger_id=1, firstname="Oleh", lastname="Lozovyi", date_of_birth='2002-09-10',
                      passport_number="1234", user_id=1)
passenger1 = Passenger(passenger_id=2, firstname="Nazar", lastname="Lomachinkiy", date_of_birth='2003-12-12',
                       passport_number="1284", user_id=2)

airport = Airport(airport_id=1, aiport_name="Bandera Airport", city="Lviv", country="Ukraine")
airport1 = Airport(airport_id=2, aiport_name="Shuhevich Airport", city="Kyiv", country="Ukraine")

flight = Flight(flight_id=1, flight_no="2134", datetime='2022-09-10 00:00:01', cost_of_flight=12.50,
                num_of_seats=12, arriving_airport=airport, departing_airport=airport1)
flight1 = Flight(flight_id=2, flight_no="2234", datetime='2022-09-10 00:00:02', cost_of_flight=120.50,
                 num_of_seats=120, arriving_airport=airport1, departing_airport=airport)

order = Order(order_id=1, order_done_datetime='2022-09-07 00:00:01', status="in progress", flight_id=1, passenger_id=1)
order1 = Order(order_id=2, order_done_datetime='2022-09-07 00:00:02', status="in progress", flight_id=2, passenger_id=2)

session.add(user)
session.add(passenger)
session.add(airport)
session.add(flight)
session.add(order)
session.add(user1)
session.add(passenger1)
session.add(airport1)
session.add(flight1)
session.add(order1)
session.commit()
