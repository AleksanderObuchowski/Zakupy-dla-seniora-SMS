from zakupy_dla_seniora import sql_db as db
from datetime import datetime, timezone
from zakupy_dla_seniora.placings.models import Placings


class Messages(db.Model):
    __tablename__ = 'message'
    id = db.Column('id', db.Integer, primary_key=True)
    message_content = db.Column('message_content', db.String(1600), nullable=False)
    message_date = db.Column('message_date', db.DateTime)
    message_location = db.Column('message_location', db.String(200))
    message_location_lat = db.Column('message_location_lat', db.Float)  # latitude
    message_location_lon = db.Column('message_location_lon', db.Float)  # longitude

    message_precise_location = db.Column('message_precise_location', db.String(60))
    phone_number = db.Column('phone_number', db.String(12))
    message_status = db.Column('message_status', db.String(100))
    placings = db.relationship('Placings', backref='message', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, message_content, phone_number, message_location='unk', message_location_lat=0,
                 message_location_lon=0, message_status='Received'):
        self.message_content = message_content
        self.message_date = datetime.now(timezone.utc)
        self.message_location = message_location
        self.phone_number = phone_number
        self.message_status = message_status
        self.message_location_lat = message_location_lat
        self.message_location_lon = message_location_lon

    def prepare_board_view(self):
        return {
            'id': self.id,
            'message_content': self.message_content,
            'message_date': str(self.message_date),
            'message_location': self.message_location,
            'message_location_lat': self.message_location_lat,
            'message_location_lon': self.message_location_lon,
            'message_status': self.message_status,
        }

    def prepare_profile_view(self):
        return {
            'id': self.id,
            'message_content': self.message_content,
            'message_date': str(self.message_date),
            'message_location': self.message_location,
            'message_status': self.message_status,
            'message_precise_location': self.message_precise_location
        }

    @classmethod
    def get_by_phone(cls, phone):
        return cls.query.filter_by(phone_number=phone).order_by(cls.message_date.desc()).first()

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def __repr__(self):
        return f'<Message from {self.message_location}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
