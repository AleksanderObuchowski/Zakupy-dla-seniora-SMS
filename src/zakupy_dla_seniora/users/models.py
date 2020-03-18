from zakupy_dla_seniora import sql_db as db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from random import randint


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(35), unique=True, nullable=False)
    first_name = db.Column('first_name', db.String(35), nullable=False)
    last_name = db.Column('last_name', db.String(35), nullable=False)
    password_hash = db.Column('password_hash', db.String(128))
    create_date = db.Column('create_date', db.DateTime)
    phone = db.Column('phone', db.String(12), nullable=False, unique=True)
    verification_code = db.Column('verification_code', db.Integer)
    verified = db.Column('verified', db.Boolean, default=False)
    points = db.Column('points', db.Integer, default=0)

    def __init__(self, name, first_name, last_name, password, phone):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)
        self.phone = phone
        self.create_date = datetime.now(timezone.utc)
        self.verification_code = randint(1000, 9999)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
