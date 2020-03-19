from zakupy_dla_seniora import sql_db as db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from random import randint
import zakupy_dla_seniora.orders.models


class Messages(db.Model):
    __tablename__ = 'message'
    id = db.Column('id', db.Integer, primary_key=True)
    message_content = db.Column('message_content', db.String(164), unique=True, nullable=False)
    message_date = db.Column('message_date', db.DateTime)
    message_location  = db.Column('message_location',db.String(100))
    message_location_lat = db.Column('message_location_lat',db.String(30))
    message_location_lon = db.Column('message_location_lon',db.String(30))

    message_precise_location =  db.Column('message_precise_location',db.String(60))
    phone_number = db.Column('phone_number', db.String(12))
    message_status = db.Column('message_status',db.String(10))
    orders = db.relationship('Orders', backref = 'message', cascade = 'all, delete-orphan', lazy = 'dynamic')

    def __init__(self, message_content, message_location,message_location_lat, message_location_lon, phone_number):
        self.message_content = message_content
        self.message_date = datetime.now(timezone.utc)
        self.message_location = message_location
        self.phone_number = phone_number
        self.message_status = 'Received'
        self.message_location_lat = message_location_lat
        self.message_location_lon = message_location_lon

    def save(self):
        db.session.add(self)
        db.session.commit()
