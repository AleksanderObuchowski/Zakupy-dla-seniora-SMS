from zakupy_dla_seniora import sql_db as db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from random import randint
from zakupy_dla_seniora.placings.models import Placings


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, nullable=False)
    uid = db.Column('uid', db.String(255), unique=True, nullable=False)
    display_name = db.Column('display_name', db.String(35), unique=True, nullable=False)
    create_date = db.Column('create_date', db.DateTime)
    phone = db.Column('phone', db.String(12), unique=True)
    code_sent = db.Column('code_sent', db.Boolean, default=False)
    verification_code = db.Column('verification_code', db.Integer)
    verified = db.Column('verified', db.Boolean, default=False)
    points = db.Column('points', db.Integer, default=0)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)

    placings = db.relationship('Placings', backref='user', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, display_name, email, uid):
        self.display_name = display_name
        self.email = email
        self.uid = uid

        self.create_date = datetime.now(timezone.utc)
        self.verification_code = randint(1000, 9999)

    def set_phone(self, phone):
        self.phone = phone

    def set_code_sent(self):
        self.code_sent = True

    def set_verified(self):
        self.verified = True

    @classmethod
    def get_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).first()

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
