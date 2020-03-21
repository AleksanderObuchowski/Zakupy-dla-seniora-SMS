from zakupy_dla_seniora import sql_db as db, login_manager
from datetime import datetime, timezone
from random import randint
from flask_login import UserMixin
from zakupy_dla_seniora.placings.models import Placings


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, nullable=False)
    display_name = db.Column('display_name', db.String(35), unique=True, nullable=False)
    create_date = db.Column('create_date', db.DateTime)
    phone = db.Column('phone', db.String(12), unique=True)
    code_sent = db.Column('code_sent', db.Boolean, default=False)
    verification_code = db.Column('verification_code', db.Integer)
    verified = db.Column('verified', db.Boolean, default=False)
    points = db.Column('points', db.Integer, default=0)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)

    placings = db.relationship('Placings', backref='user', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, display_name, email, password):
        self.display_name = display_name
        self.email = email
        self.password_hash = password

        self.create_date = datetime.now(timezone.utc)
        self.verification_code = randint(1000, 9999)

    def __repr__(self):
        return "<User(id='%s', display_name='%s', points='%s')>" % (self.id, self.display_name, self.points)

    def as_json(self):
        return {
            'id': self.id,
            'display_name': self.display_name,
            'points': self.points
        }

    def set_phone(self, phone):
        self.phone = phone

    def set_code_sent(self):
        self.code_sent = True

    def set_verified(self):
        self.verified = True

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def get_password_hash(self):
        return self.password_hash

    def save(self):
        db.session.add(self)
        db.session.commit()
