from zakupy_dla_seniora import sql_db as db
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint, exc


class Orders(db.Model):
    __tablename__ = 'order'
    __table_args__ = (UniqueConstraint('id_user','id_message', name = 'unique_message_user'),)
    id = db.Column('id', db.Integer, primary_key=True)
    id_user = db.Column('id_user', db.Integer, db.ForeignKey('user.id'))
    id_message = db.Column('id_message', db.Integer, db.ForeignKey('message.id'))
    order_status = db.Column('order_status', db.String(40))
    order_date = db.Column('order_date', db.DateTime, default=datetime.utcnow)

    def __init__(self, id_user, id_message, order_status, order_date):
        self.id_user = id_user
        self.id_message = id_message
        self.order_status = order_status
        self.order_date = order_date

    def save(self):
        db.session.add(self)
        db.session.commit()
